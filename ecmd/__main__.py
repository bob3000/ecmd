import argparse
import os
import pkg_resources
import sys
import ecmd.controller


def parse_args(command_line):
    parser = argparse.ArgumentParser(
        description="ecmd - elastichosts command line client")
    parser.add_argument(
        "-V", "--version", action="version",
        version=pkg_resources.get_distribution("ecmd").version,
        help="display program version and exit")
    parser.add_argument("command",
                        choices=["drives"], help="list drives")
    parser.set_defaults(func=commands)
    return parser.parse_args(command_line)


def commands(args):
    try:
        if args.command == "drives":
            for k, v in controller.drive_server_mapping().items():
                print("{}: {}".format(k, " ".join(v)))
    except RuntimeError as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)


def main(argv=None):
    global controller
    argv = argv if argv else sys.argv[1:]
    credentials = sorted(["EHUUID", "EHSECRET", "EHBASEURL"])
    env = sorted(dict(os.environ).keys())
    if set(credentials) & set(env) != set(credentials):
        print("Error:", "the environment variables {} are not set"
              "".format(" ".join(credentials)), file=sys.stderr)
        sys.exit(1)
    controller = ecmd.controller.Controller(os.environ.get("EHUUID"),
                                            os.environ.get("EHSECRET"),
                                            os.environ.get("EHBASEURL"))
    args = parse_args(argv)
    if 'func' in args:
            args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()
