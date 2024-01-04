# ttrace - strace as a tree

Uses `strace` to trace a program call and displays what's going on in a human
friendly manner.


![Current screenshot](screenshot.png "Current screenshot")

[Project page](https://projects.om-office.de/frans/ttrace)


## Installation and Usage

Install `ttrace` via pip:
```
[<python executable> -m] pip install [-U] ttrace
```

A new executable is then provided which can be used instead of `strace`:
```
ttrace [<ARGS>] <CMD>
```
Note that you would'nt provide `strace` arguments since `ttrace` provides them
automatically.

Alternatively you can clone and use the current development tree, see below.


## Intended interface

The following commands and outputs reflect the current development plan:

```sh
ttrace <CMD|LOGFILE>
```
Prints annotated, pre-formatted and filtered output next to the process' original
`stdout` and `stderr`.

```sh
ttrace --attach <PID|NAME>
```
Attaches to the given process and displays all but `stdout` and `stderr` of the
process of course.

```sh
<CMD> | ttrace [<OTHER-ARGS>]
```
Same as with `attach` but using pipe semantics (limited due to the mixing of
`stderr` and `strace` output.


```sh
ttrace --grep <PATTERN> <CMD>
```
Applies pattern to the original `strace` output and only outputs the matching
content.

```sh
ttrace --tree <CMD>
```
Populates and displays a tree while the program is running.

```sh
ttrace --hybrid <CMD>
```
Not sure yet - plan is to have `ncurses` based split views for optionally any
of the following elements:

* tree output
* combined `stdout` and `stderr`
* alternatively split `stdout` and `stderr`
* strace console
* console with only warning character (whatever that means)

```sh
ttrace --timing <CMD>
```

### ToDo for v1.0

* trace process termination
* output growing process tree
* report / visualize abnormal process termination
* report / visualize file access
* optionally turn PIDs into PID counters for comparability
* optionally print timestamp, pid, line number
* no color
* logging


### Other ideas

* trace changes environment
* trace docker image usage
* highlight failed processes


## Development & Contribution

```
pip3 install -U poetry pre-commit
git clone --recurse-submodules https://projects.om-office.de/frans/ttrace.git
cd ttrace
pre-commit install
# if you need a specific version of Python inside your dev environment
poetry env use ~/.pyenv/versions/3.10.4/bin/python3
poetry install
```


## License

See `License.md`


## Read

* [The Difference Between fork(), vfork(), exec() and clone()](https://www.baeldung.com/linux/fork-vfork-exec-clone)
* [HN: The Magic of strace](https://news.ycombinator.com/item?id=7155799)
* [The Magic of strace (archive.org)](https://web.archive.org/web/20160116001752/http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/)

