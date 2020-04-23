import argparse
from argparse import RawTextHelpFormatter
import logging

from core.pipelines.pipelines_controller import (
    get_pipeline_description,
    load_pipeline_dynamically,
)
from models.model_controller import (
    get_seg_types,
    get_file_types,
    get_req_modalities,
    get_proc_seg_types,
)

import logging
from sys_logger import configureLogger

plid = "glb_importer"


def get_description():
    pipeline_description = get_pipeline_description(plid)
    model_file_types = get_file_types(plid)
    model_req_mods = get_req_modalities(plid)

    return (
        pipeline_description
        + "\n3 input scans (modalities) required of types "
        + ", ".join(model_req_mods)
        + "\nInput files must be of type "
        + " or ".join(model_file_types)
        + "\nDefault segmentaion: cortical_gray_matter "
    )


def add_parser_arguments(parser):
    parser.add_argument(
        "input_file",
        metavar="input_file",
        type=str,
        help="Specify the path to the directory containing the T2-FLAIR input scans",
    )
    parser.set_defaults(which=plid)


def run(args):
    logger = logging.getLogger(__name__) 
    logger.info("INITIALIZE PIPELINE")
    input_file = args.input_file
    logger.info("LOADING_MODEL")
    pipeline_module = load_pipeline_dynamically(plid)
    pipeline_module.run(
        input_file
    )
    logger.info("COMPLETION")


def main():
    description = get_description()
    parser = argparse.ArgumentParser(
        description=description, formatter_class=RawTextHelpFormatter
    )
    add_parser_arguments(parser)

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
