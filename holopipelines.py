import sys
from argparse import ArgumentParser
import brain_segmentation_tool


def main():
    parser = ArgumentParser(
        prog="HoloPipelinesCLI", description="TODO")
    subparsers = parser.add_subparsers(help="pipeline name")

    brain_parser = subparsers.add_parser(
        brain_segmentation_tool.plid,
        description=brain_segmentation_tool.get_description(),
        help="brain segmentation tool")
    brain_segmentation_tool.add_parser_arguments(brain_parser)

    args = parser.parse_args()

    try:
        plid = args.which
    except AttributeError:
        plid = None

    if plid == brain_segmentation_tool.plid:
        sys.exit(brain_segmentation_tool.run(args))
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
