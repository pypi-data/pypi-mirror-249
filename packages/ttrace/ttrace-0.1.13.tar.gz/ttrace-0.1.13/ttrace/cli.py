#!/usr/bin/env python3

"""Visualize strace output
"""
import asyncio
import re
import signal
import sys
from argparse import ArgumentParser, Namespace
from asyncio import StreamReader
from asyncio.subprocess import PIPE
from collections.abc import (  # MutableMapping,; MutableSequence,
    AsyncIterable,
    MutableMapping,
    Sequence,
)
from pathlib import Path
from typing import Any, NoReturn, TextIO

import aiofiles

from ttrace.utils.treestuff import attributed_tree, colored, get_node, insert

from .core import (
    Clone3Type,
    CloneType,
    ExecveType,
    OpenatType,
    StraceType,
    VforkType,
    WriteType,
    exctract_process_info,
    parse,
    sanatized_strace_lines,
    strace_output_path,
)


def parse_args(args: Sequence[str] | None = None) -> tuple[Namespace, Sequence[str]]:
    """Returns parsed arguments until the first
    >>> parse_args(["-v", "--grep", "abc", "foo", "-v", "bar"])
    (Namespace(verbose=True, no_color=False, record=None, grep='abc'), ['foo', '-v', 'bar'])
    """

    class MyArgumentParser(ArgumentParser):
        """Argument parser which not exits on error but raises an exception"""

        def error(self, message: str) -> NoReturn:
            """Just raises an error we can catch"""
            raise RuntimeError(message)

    parser = MyArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--no-color", "-n", action="store_true")
    parser.add_argument("--record", "-r", type=Path)
    parser.add_argument("--grep", "-g", type=str)

    all_args = args or sys.argv[1:]
    for split_at in (i for i, e in reversed(list(enumerate(all_args))) if not e.startswith("-")):
        try:
            return parser.parse_args(all_args[:split_at]), all_args[split_at:]
        except RuntimeError as exc:
            if any(not e.startswith("-") for e in all_args[:split_at]):
                continue
            parser.print_help(sys.stderr)
            print(exc, file=sys.stderr)
            raise SystemExit(-1) from exc

    parser.print_help(sys.stderr)
    print("No command provided", file=sys.stderr)
    raise SystemExit(-1)


def print_strace(line_nr: int, strace: StraceType) -> None:
    """Write out a nice colored pre-formatted strace line"""
    print(
        colored(
            f"{line_nr}" f"|{strace.pid}" f"|{strace.fname}  " f"|{strace.result_nr}"
            # f"|{strace.command}"
            "|",
            {
                "vfork": "blue_bold",
                "clone": "blue_bold",
                "clone3": "blue_bold",
                "execve": "green_bold",
            }[strace.fname],
        )
    )


async def process_strace(  # pylint: disable=too-many-branches
    in_stream: AsyncIterable[tuple[int, str, StraceType, Sequence[int]]], args: Namespace
) -> None:
    """Crawls through pre-digested strace data and handles operations readily associated
    to processes"""

    ptree: MutableMapping[str | int, Any] = {}

    try:
        async for line_nr, line, strace, pid_path in in_stream:
            if args.grep and re.findall(args.grep, line):
                print(line)

            # print(line_nr, strace, pid_path)

            if strace.fname in {"vfork", "clone", "clone3"}:
                if args.verbose:
                    print_strace(
                        line_nr,
                        parse(  # type: ignore[type-var, arg-type]
                            {
                                "vfork": VforkType,
                                "clone": CloneType,
                                "clone3": Clone3Type,
                            }[strace.fname],
                            strace.args,
                        ),
                    )
                insert(
                    ptree,
                    path=pid_path,
                    name=strace.result_nr,
                    attrs={
                        "tags": [strace.fname],
                    },
                )
            elif strace.fname == "exited":
                # print(strace.result_nr)
                get_node(ptree, pid_path).setdefault("__attrs__", {})["color"] = (
                    "blue" if strace.result_nr == 0 else "red"
                )

            elif strace.fname == "execve":
                assert strace.result_nr is not None

                if strace.result_nr >= 0:
                    execve = parse(ExecveType, strace.args)
                    assert execve
                    # if args.verbose:
                    #    print_strace(line_nr, strace)
                    if line_nr == 0:
                        insert(
                            ptree,
                            path=[],
                            name=strace.pid,
                            display_name=execve.command[0],
                            attrs={
                                "tags": [strace.fname],
                            },
                        )
                attrs = get_node(ptree, pid_path).setdefault("__attrs__", {})
                tags = attrs.setdefault("tags", [])
                attrs["color"] = "blue" if strace.result_nr == 0 else "red"
                cmd = (
                    " ".join(execve.command)
                    if isinstance(execve.command, (list, tuple))
                    else str(execve.command)
                )[:70].replace("\n", "\\n")
                if cmd not in tags:
                    tags.append(cmd)

            elif strace.fname == "openat":
                openat = parse(OpenatType, strace.args)
                assert openat
                if (
                    # args.verbose
                    # and
                    openat.path not in {".", "/proc/filesystems", "/dev/null"}
                    and ".so" not in openat.path
                    and not any(openat.path.endswith(s) for s in (".h", ".c", ".o", ".a", ".s"))
                    and not strace.result.startswith("-1")
                ):
                    print(
                        colored(
                            f"{line_nr}|{strace.pid}|openat |{strace.result}| {openat.path}",
                            "blue_bold",
                        )
                    )
                    insert(
                        ptree,
                        path=pid_path,
                        name=f"[{strace.result}] {openat.path}",
                        display_name="xxx",
                        attrs={
                            "color": "cyan_bold" if (strace.result_nr or 0) >= 0 else "red",
                        },
                    )
            elif strace.fname == "write":
                if (write := parse(WriteType, strace.args)).filep in {1, 2}:
                    string = write.string[:168].strip(" \n").replace("\n", "\\n")
                    insert(
                        ptree,
                        path=pid_path,
                        name=f"'{string}'",
                        display_name="xxx",
                        attrs={
                            "color": "yellow_bold" if write.filep == 2 else "white_bold",
                        },
                    )
    finally:
        print(attributed_tree(ptree))


async def process_strace_file(filename: Path, args: Namespace) -> None:
    """For testability: provides content of a file to process_strace()"""
    async with aiofiles.open(filename) as afp:
        await process_strace(
            exctract_process_info(
                sanatized_strace_lines(afp),
            ),
            args,
        )


async def buffer_stream(stream: StreamReader, out_file: TextIO) -> None:
    """Records a given stream to a buffer line by line along with the source"""
    while line := (await stream.readline()).decode():
        out_file.write(line)


async def main_invoke(cmd: Sequence[str], args: Namespace) -> None:
    """Runs a program using strace"""
    with strace_output_path(args.record) as output_file_path:
        full_cmd = (
            "strace",
            "--trace=fork,vfork,clone,clone3,execve,openat,write",
            "--decode-pids=pidns",
            "--timestamps=unix,us",
            "--follow-forks",
            "--columns=0",
            "--abbrev=none",
            "-s",
            "65536",
            "-o",
            f"{output_file_path}",
            *cmd,
        )

        if args.verbose:
            print(" ".join(full_cmd))

        process = await asyncio.create_subprocess_exec(*full_cmd, stdout=PIPE, stderr=PIPE)

        assert process.stdout and process.stderr
        signal.signal(signal.SIGINT, lambda _sig, _frame: 0)

        await asyncio.gather(
            *(
                awaitable
                for awaitable in (
                    buffer_stream(process.stdout, sys.stdout),
                    buffer_stream(process.stderr, sys.stderr),
                    None if args.record else process_strace_file(output_file_path, args),
                    process.wait(),
                )
                if awaitable
            )
        )
        raise SystemExit(process.returncode)


def main() -> int:
    """Main entrypoint"""
    args, command = parse_args()

    if command[0].endswith(".log"):
        asyncio.run(process_strace_file(Path(command[0]), args))
    else:
        asyncio.run(main_invoke(command, args))
    return 0


if __name__ == "__main__":
    main()
