import argparse
import pkg_resources
import sys
import ecmd.controller


def parse_args(command_line):
    parser = argparse.ArgumentParser(
        description="ecmd - elastichosts command line client")
    group_version = parser.add_mutually_exclusive_group()
    group_version.add_argument(
        "-V", "--version", action="version",
        version=pkg_resources.get_distribution("ecmd").version,
        help="display program version and exit")
    group_command = parser.add_mutually_exclusive_group()
    group_command.add_argument("command",
                        choices=["drives",], help="list drives")
    parser.set_defaults(func=commands)
    return parser.parse_args(command_line)


def commands(args):
    if args.commands == "drives":
        for k, v in controller.drives():
            print("{}: {}".format(k, " ".join(v)))


def main(argv=None):
    global controller
    argv = argv if argv else sys.argv[1:]
    controller = ecmd.controller.Controller()
    args = parse_args(argv)
    if 'func' in args:
        args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()
