#!/usr/bin/env python3

"""Visualize strace output
"""
# pylint: disable=fixme

import os
import re
from ast import literal_eval
from collections.abc import (  # Iterator,
    AsyncIterable,
    Iterator,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import ClassVar, Protocol, Type, TypeVar

PPID = r"\d+"
PTIME = r"\d{10}\.\d{6}"
PFNAME = r"([a-z0-9_]+|\?+)"
PHEX = r"0x[0-9a-f]+"
PCOMMENT = r"\/\*\s(.*)\s\*\/"
PRESULT = rf"(\?|-?\d+|{PHEX})( [A-Z_]+)?( \(.*\))?( {PCOMMENT})?"
PPATH = r".*"
PFLAGS = r"[A-Z_\|]+"
PCONST = r"([A-Z_]+|\d+)"
PPERMISSION = r"0[0-7]{3}|000"
PANYTHING = r".*"

# All functions ttrace can somehow make use of
IMPLEMENTED_COMMANDS = set("execve openat vfork clone clone3 exit_group exited write".split())

# All function names I've stumbled upon so far
ALL_COMMANDS = set(
    "exited "
    "execve openat vfork clone clone3 exit_group "
    "getrusage fstatfs dup getegid rt_sigaction rmdir close rt_sigprocmask "
    "getrandom pipe2 write getcwd lseek munmap getppid unlinkat clock_nanosleep "
    "mprotect getpid readlink getpgrp setresuid sched_getaffinity fcntl umask "
    "gettid wait4 getuid rt_sigreturn sysinfo getdents64 sigaltstack "
    "geteuid chmod set_tid_address setresgid brk uname access "
    "fsetxattr mkdir pread64 set_robust_list rseq faccessat2 ioctl getgid "
    "renameat2 newfstatat tgkill mmap statx unlink splice prlimit64 dup2 "
    "getgroups kill arch_prctl read statfs rename chdir symlinkat fadvise64 "
    "futex socket connect readlinkat getpeername bind close_range epoll_create1 "
    "fchdir poll lstat clock_getres socketpair renameat recvmmsg sched_yield fchownat "
    "fgetxattr epoll_ctl accept4 eventfd2 timerfd_settime restart_syscall getsockname "
    "recvmsg dup3 stat epoll_create prctl ftruncate writev sendmmsg setuid mremap "
    "getsockopt fchown setitimer rt_sigtimedwait pselect6 fchmod fstat utimensat sendto "
    "alarm setsid capget setsockopt sendmsg shutdown symlink madvise timerfd_create "
    "epoll_wait fchmodat fallocate listen recvfrom times capset".split()
)


@dataclass
class StraceType:
    """A full strace logline, consisting of the PID, a unix timestamp (us),
    the syscall command name, the (unparsed) arguments and its result
    >>> parse(StraceType, "727862 1676908243.245515 foo(-1) = 42 (the answer) /* to everything */")
    strace<pid=727862, t=1676908243.245515, cmd=foo, res_nr=42, comment='to everything'>
    >>> parse(StraceType, "500918 1677690227.029671 +++ exited with 23 +++")
    strace<pid=500918, t=1677690227.029671, cmd=exited, res_nr=23, comment=None>
    """

    pid: int
    timestamp: str
    fname: str
    args: str
    result: str
    result_nr: int | None
    PATTERN: ClassVar[str] = (
        rf"^({PPID})\s+({PTIME})\s("
        rf"(({PFNAME})\(({PANYTHING})\)\s=\s({PRESULT}))"
        rf"|(\+\+\+ (exited) with (-?\d+) \+\+\+)"
        rf")$"
    )

    def __init__(self, args: tuple[str, ...]) -> None:
        self.pid = int(args[0])
        assert self.pid
        self.timestamp = args[1]
        self.fname = args[4] or args[14]
        assert self.fname
        self.args = args[6]
        self.result = args[7] or args[13]
        assert self.result
        result_nr_str = args[8] or args[15]
        assert result_nr_str is not None
        self.result_nr = (
            None
            if result_nr_str == "?"
            else int(result_nr_str, 16)
            if result_nr_str.startswith("0x")
            else int(result_nr_str)
        )
        self.comment = args[12]

    def __repr__(self) -> str:
        return (
            f"strace<pid={self.pid}"
            f", t={self.timestamp}"
            f", cmd={self.fname}"
            f", res_nr={self.result_nr}"
            f", comment={self.comment!r}>"
        )


@dataclass
class UnfinishedType:
    """Recognizes an `unfinished` strace element and stores PID (there is only
    one continuation per PID) and the part of the line needed to stitch it
    together later.
    >>> parse(UnfinishedType, "727862 1676908243.245515 wait4(-1,  <unfinished ...>")
    unfinished<pid=727862>
    >>> parse(UnfinishedType, "160833 1677921270.753070 ???( <unfinished ...>")
    unfinished<pid=160833>
    """

    line: str
    pid: int

    PATTERN: ClassVar[
        str
    ] = rf"^(({PPID})\s+{PTIME}\s{PFNAME}\({PANYTHING})\s<unfinished\s\.\.\.>{PANYTHING}$"

    def __init__(self, args: tuple[str, ...]) -> None:
        self.line = args[0]
        self.pid = int(args[1])

    def __repr__(self) -> str:
        return f"unfinished<pid={self.pid}>"


@dataclass
class ResumedType:
    """Recognizes a `resumed` strace element and stores PID and the part of the
    line needed to stitch it to the previous `unfinished` element.
    >>> parse(ResumedType, "727862 1676908243.255635 <... wait4 resumed>blabla) = 727863")
    resumed<pid=727862>
    """

    pid: int
    line: str
    PATTERN: ClassVar[str] = rf"^({PPID})\s+{PTIME}\s<\.\.\. {PFNAME} resumed>({PANYTHING})$"

    def __init__(self, args: tuple[str, ...]) -> None:
        self.pid = int(args[0])
        self.line = args[2]

    def __repr__(self) -> str:
        return f"resumed<pid={self.pid}>"


@dataclass
class ExecveType:
    """Content of an execve() call, including the path to the executable,
    the actual command with its arguments and the environment variables
    used for this command
    >>> parse(ExecveType, '"/bin/foo", ["foo", "-v"], ["FOO=bar"]')
    execve<exe='/bin/foo', cmd=['foo -v']>
    """

    executable: str
    command: str
    environment: str
    PATTERN: ClassVar[str] = rf'^"({PPATH})", \[({PANYTHING})\], \[({PANYTHING})\]$'

    def __init__(self, args: tuple[str, ...]) -> None:
        self.executable = args[0]
        self.command = literal_eval(args[1])
        self.environment = args[2]

    def __repr__(self) -> str:
        return f"execve<exe={self.executable!r}, cmd=[{' '.join(self.command)!r}]>"


@dataclass
class OpenatType:
    """Content of an openat() call, including the path to the opened file and
    the flags being used
    >>> parse(OpenatType, 'AT_FDCWD, "/usr/bin/print", O_RDONLY|O_CLOEXEC')
    openat<path='/usr/bin/print'>
    """

    position: str
    path: str
    flags: str
    PATTERN: ClassVar[str] = rf'^([A-Z_]+|\d+),\s"({PANYTHING})", ({PFLAGS})(, ({PPERMISSION}))?$'

    def __init__(self, args: tuple[str, ...]) -> None:
        self.position = args[0]
        self.path = args[1]
        self.flags = args[2]

    def __repr__(self) -> str:
        return f"openat<path={self.path!r}>"


@dataclass
class WriteType:
    """Content of a write() call,
    >>> parse(OpenatType, 'AT_FDCWD, "/usr/bin/print", O_RDONLY|O_CLOEXEC')
    openat<path='/usr/bin/print'>
    """

    filep: int
    string: str
    length: int
    PATTERN: ClassVar[str] = rf'^(\d+),\s"({PANYTHING})"(\.\.\.)?,\s(\d+)$'

    def __init__(self, args: tuple[str, ...]) -> None:
        self.filep = int(args[0])
        self.string = args[1]
        self.length = int(args[3])

    def __repr__(self) -> str:
        return f"write<fp={self.filep}, string={self.string!r}>"


@dataclass
class VforkType:
    """Content of an vfork() call
    >>> parse(VforkType, '')
    vfork<>
    """

    PATTERN: ClassVar[str] = r"^$"

    def __init__(self, _args: tuple[str, ...]) -> None:
        ...

    def __repr__(self) -> str:
        return "vfork<>"


@dataclass
class CloneType:
    """Content of an clone() call
    >>> parse(CloneType, 'child_stack=NULL, flags=SIGCHLD, child_tidptr=0x123')
    clone<child_stack='NULL', flags=['SIGCHLD'], child_tidptr='0x123'>
    """

    child_stack: str
    flags: Sequence[str]
    child_tidptr: str

    PATTERN: ClassVar[str] = (
        rf"^child_stack=(.*), flags=({PFLAGS})" rf"(, child_tidptr=(.*))?" rf"(, tls=({PHEX}))?$"
    )

    def __init__(self, args: tuple[str, ...]) -> None:
        self.child_stack = args[0]
        self.flags = args[1].split("|")
        self.child_tidptr = args[3]

    def __repr__(self) -> str:
        return (
            f"clone<child_stack={self.child_stack!r}"
            f", flags={self.flags!r}, child_tidptr={self.child_tidptr!r}>"
        )


@dataclass
class Clone3Type:
    """Content of an clone3() call
    >>> parse(Clone3Type, '{flags=FOO, exit_signal=SIGCHLD, stack=0x123, stack_size=0x90}, 88')
    clone3<flags=['FOO'], parent_tid_comment=None>
    >>> parse(Clone3Type,
    ...     '{flags=FOO|BAR, child_tid=0x123, parent_tid=0x345'
    ...     ', exit_signal=0, stack=0x234, stack_size=0x54, tls=0x2345}'
    ...     ' => {parent_tid=[1869 /* 1803473 in strace\\'s PID NS */]}, 88')
    clone3<flags=['FOO', 'BAR'], parent_tid_comment="1803473 in strace's PID NS">
    """

    flags: Sequence[str]
    parent_tid_comment: str
    PATTERN: ClassVar[str] = (
        rf"^\{{flags=({PFLAGS})(, child_tid={PHEX})?(, parent_tid={PHEX})?"
        rf"(, exit_signal={PCONST})?, stack={PHEX}, stack_size={PHEX}(, tls={PHEX})?\}}"
        rf"( => \{{parent_tid=\[(\d+)( {PCOMMENT})?\]\}})?, \d+$"
    )

    def __init__(self, args: tuple[str, ...]) -> None:
        self.flags = args[0].split("|")
        self.parent_tid_comment = args[9]

    def __repr__(self) -> str:
        return f"clone3<flags={self.flags}, parent_tid_comment={self.parent_tid_comment!r}>"


class ParsableBase(Protocol):  # pylint: disable=too-few-public-methods
    """Needed only to be able to access PATTERN inside parse(), see
    https://stackoverflow.com/questions/75507292"""

    PATTERN: ClassVar[str]

    def __init__(self, args: tuple[str, ...]) -> None:
        ...


Parsable = TypeVar("Parsable", bound=ParsableBase)


def maybe_parse(result_type: Type[Parsable], src: str | StraceType) -> Parsable | None:
    """Returns an element of given class from parsed line
    >>> maybe_parse(StraceType, '012345 1234567890.123456 abc(a, b, c) = 1')
    strace<pid=12345, t=1234567890.123456, cmd=abc, res_nr=1, comment=None>
    """
    if not (match := re.match(result_type.PATTERN, src if isinstance(src, str) else src.args)):
        return None
    return result_type(match.groups())


def parse(result_type: Type[Parsable], src: str | StraceType) -> Parsable:
    """Wrapper for maybe_parse() which raises on non-matching input"""
    if not (result := maybe_parse(result_type, src)):
        raise RuntimeError(
            f"Could not parse a {result_type.__name__}"
            f" from {src if isinstance(src, str) else src.args!r} with pattern"
            f" {result_type.PATTERN}"
        )
    return result


async def sanatized_strace_lines(  # pylint: disable=too-many-statements
    in_stream: AsyncIterable[str],
) -> AsyncIterable[tuple[int, str, StraceType]]:
    """Returns fully usable strace entries"""
    # pylint: disable=too-many-branches

    resume_state: MutableMapping[int, UnfinishedType] = {}
    pid_gen = {"clone", "clone3", "vfork"}
    line_stack_open: MutableSequence[tuple[str, StraceType]] = []
    line_stack: MutableSequence[tuple[str, StraceType]] = []
    line_nr = 0
    raw_line_nr = 0

    try:
        async for line in in_stream:
            # we don't have enumerate() here
            raw_line_nr += 1

            if strace := maybe_parse(StraceType, line):
                if "<unfinished ...>" in line or " resumed>" in line:
                    print(line)
                    print(StraceType.PATTERN)
                    raise SystemExit(1)

                if strace.fname == "exited" and strace.pid in resume_state:
                    del resume_state[strace.pid]

                if resume_state:
                    (line_stack_open if strace.fname in pid_gen else line_stack).append(
                        (line.rstrip(), strace)
                    )
                else:
                    yield line_nr, line.rstrip(), strace
                    line_nr += 1

                continue

            if unfinished := maybe_parse(UnfinishedType, line):
                line_nr += 1
                assert unfinished.pid not in resume_state
                resume_state[unfinished.pid] = unfinished
                # print("++++++UNFINISHED++++++", len(resume_state), raw_line_nr, line_nr)
                continue

            if resumed := maybe_parse(ResumedType, line):
                if resumed.pid not in resume_state:
                    raise RuntimeError(
                        f"'resumed' without corresponding 'unfinished' found: {line}"
                    )
                continued_line = resume_state[resumed.pid].line + resumed.line
                del resume_state[resumed.pid]
                # print("++++++RESUME++++++", len(resume_state), raw_line_nr, line_nr)

                continued_strace = parse(StraceType, continued_line)

                assert (
                    "<unfinished ...>" not in continued_line or continued_strace.result_nr is None
                )

                (line_stack_open if continued_strace.fname in pid_gen else line_stack).append(
                    (continued_line.rstrip(), continued_strace)
                )

                if not resume_state:
                    for element in sorted(line_stack_open, key=lambda e: e[1].timestamp):
                        yield line_nr, *element
                        line_nr += 1
                    line_stack_open.clear()
                    for element in line_stack:
                        yield line_nr, *element
                        line_nr += 1
                    line_stack.clear()
                    assert line_nr == raw_line_nr
                continue

            line_nr += 1
            if "+++ killed" in line:
                # print(line)
                continue
            if "--- SIGCHLD " in line:
                # print(line)
                continue

            if "--- SIGSEGV " in line:
                continue

            if "--- SIGTERM " in line:
                # print(line)
                continue

            if "--- SIGUSR2 " in line:
                # print(line)
                continue

            if "--- SIGURG " in line:
                # print(line)
                continue

            print(line)

            if any(s in line for s in ("+++ killed ", " --- ")):
                # TODO: we want to track this, too
                # line_nr += 1
                continue

            # Should raise
            parse(StraceType, line)

    finally:
        assert not resume_state


async def exctract_process_info(
    sane_strace_stream: AsyncIterable[tuple[int, str, StraceType]],
) -> AsyncIterable[tuple[int, str, StraceType, Sequence[int]]]:
    """This generator function takes sanatized (i.e. ordered and stitched together) strace
    lines and handles only the process relevant stuff, i.e. forking/cloning and execve instructions
    """

    # maps PIDs to their parents
    pid_path: MutableMapping[int, tuple[int, Sequence[int]]] = {}

    async for line_nr, line, strace in sane_strace_stream:

        if strace.result_nr is None:
            # sometimes we get an '?' instead of a result which always seems to be result
            # of an unfinished fork due to process termination
            # once we trace process termination we should assert the associated pid to be gone
            if strace.fname not in {
                "vfork",
                "clone",
                "clone3",
                "futex",
                "exit",
                "exit_group",
                "pselect6",
                "epoll_wait",
            }:
                print(f"found a {strace.fname}() call not returning a valid value:")
                print(line)
            continue

        if len(pid_path) == 0:
            # this is the first call. make sure we register the PID even though we have no
            # fork type yet
            assert strace.fname == "execve"
            pid_path[strace.pid] = 0, [strace.pid]

        if strace.pid not in pid_path:
            print(f">>> {line_nr}: {line}")
            # print(colored(f"{strace}", "yellow_bold"))
            assert strace.pid in pid_path, f"{strace.pid} not in `pid_path`"

        if strace.fname not in ALL_COMMANDS:
            print(f"fname not yet considered: '{strace.fname}'")

        if strace.fname not in IMPLEMENTED_COMMANDS:
            # skip stuff we can't use anyway
            continue

        if strace.fname in {"vfork", "clone", "clone3"}:
            new_pid = int(strace.comment.split()[0]) if strace.comment else strace.result_nr
            if new_pid > 0:
                assert new_pid not in pid_path, f"{line_nr}: {line} => {new_pid=}"
                pid_path[new_pid] = len(pid_path), list(chain(pid_path[strace.pid][1], [new_pid]))

        yield line_nr, line, strace, pid_path[strace.pid][1]


@contextmanager
def strace_output_path(path: Path | None = None) -> Iterator[Path]:
    """Wraps optional creation of named pipe and sanatizes @path argument"""
    result = path or Path("myfifo")
    result.unlink(missing_ok=True)
    try:
        if path is None:
            os.mkfifo(result, 0o600)
        yield result
    finally:
        if path is None:
            os.unlink(result)
