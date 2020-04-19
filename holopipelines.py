import sys
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import brain_segmentation_tool
import kidney_segmentation_tool
import bone_segmentation_tool
import lung_segmentation_tool
import abdominal_segmentation_tool


def main():
    parser = ArgumentParser(
        prog="HoloPipelinesCLI",
        description="""
        This is a command line tool to use the local versions of the HoloPipelines.
        Please select on of the pipelines and the required arguments to create a hologram.
        Run "HoloPipelinesCLI pipeline_name -h" for more information on a specific pipeline.
        """,
    )
    subparsers = parser.add_subparsers(help="pipeline_name")

    brain_parser = subparsers.add_parser(
        brain_segmentation_tool.plid,
        description=brain_segmentation_tool.get_description(),
        help="brain segmentation tool",
        formatter_class=RawTextHelpFormatter
    )
    brain_segmentation_tool.add_parser_arguments(brain_parser)

    kidney_parser = subparsers.add_parser(
        kidney_segmentation_tool.plid,
        description=kidney_segmentation_tool.get_description(),
        help="kidney segmentation tool",
        formatter_class=RawTextHelpFormatter
    )
    kidney_segmentation_tool.add_parser_arguments(kidney_parser)

    bone_parser = subparsers.add_parser(
        bone_segmentation_tool.plid,
        description=bone_segmentation_tool.get_description(),
        help="bone segmentation tool",
        formatter_class=RawTextHelpFormatter
    )
    bone_segmentation_tool.add_parser_arguments(bone_parser)

    lung_parser = subparsers.add_parser(
        lung_segmentation_tool.plid,
        description=lung_segmentation_tool.get_description(),
        help="lung segmentation tool",
        formatter_class=RawTextHelpFormatter
    )
    lung_segmentation_tool.add_parser_arguments(lung_parser)

    abdominal_parser = subparsers.add_parser(
        abdominal_segmentation_tool.plid,
        description=abdominal_segmentation_tool.get_description(),
        help="abdominal segmentation tool",
        formatter_class=RawTextHelpFormatter
    )
    abdominal_segmentation_tool.add_parser_arguments(abdominal_parser)

    args = parser.parse_args()

    try:
        plid = args.which
    except AttributeError:
        plid = None

    if plid == brain_segmentation_tool.plid:
        sys.exit(brain_segmentation_tool.run(args))
    elif plid == kidney_segmentation_tool.plid:
        sys.exit(kidney_segmentation_tool.run(args))
    elif plid == bone_segmentation_tool.plid:
        sys.exit(bone_segmentation_tool.run(args))
    elif plid == lung_segmentation_tool.plid:
        sys.exit(lung_segmentation_tool.run(args))
    elif plid == abdominal_segmentation_tool.plid:
        sys.exit(abdominal_segmentation_tool.run(args))
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
