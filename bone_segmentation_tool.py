import argparse
from core.pipelines.pipelines_controller import (
    get_pipeline_description,
    load_pipeline_dynamically,
)
import logging

from sys_logger import configureLogger

plid = "bone_segmentation"


def get_description():
    return get_pipeline_description(plid)


def add_parser_arguments(parser):
    parser.add_argument(
        "input",
        metavar="i",
        type=str,
        help="Specify the path to the directory containing the scans in the form of DICOM",
    )
    parser.add_argument(
        "output",
        metavar="o",
        type=str,
        help="Specify the path of a single output file in the form of a glb file",
    )
    parser.add_argument(
        "-l",
        "--log",
        action='store_true',
        help="Set flag to turn on logging output",
    )
    parser.set_defaults(which=plid)


def run(args):
    logger = logging.getLogger(__name__) 
    logger.info("INITIALIZE PIPELINE")
    input_dir = args.input
    output_path = args.output
    logger.info("LOADING_MODEL")
    pipeline_module = load_pipeline_dynamically(plid)
    pipeline_module.run(input_dir, output_path)
    logger.info("COMPLETION")


def main():
    parser = argparse.ArgumentParser(description=get_description())
    add_parser_arguments(parser)
    args = parser.parse_args()
    logger = configureLogger(__name__,args.log)
    run(args)


if __name__ == "__main__":
    main()
