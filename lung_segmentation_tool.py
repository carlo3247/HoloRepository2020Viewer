import argparse
from argparse import RawTextHelpFormatter
from core.pipelines.pipelines_controller import (
    get_pipeline_description, load_pipeline_dynamically)
from models.model_controller import (get_seg_types,
                                     get_file_types, get_proc_seg_types)


plid = "lung_segmentation"

pipeline_description = get_pipeline_description(plid)

model_seg_types = get_seg_types(plid)
model_proc_seg_types = get_proc_seg_types(plid)
model_file_types = get_file_types(plid)


def get_description():
    return pipeline_description+"\n" +\
        "Input file must be of type " +\
        ", ".join(model_file_types) +\
        "\nDefault segmentaion: lung "


def add_parser_arguments(parser):
    parser.add_argument("input", metavar="i", type=str,
                        help="Specify the path to the directory containing the input scans")
    parser.add_argument("output", metavar="o", type=str,
                        help="Specify the path of a single output file in the form of a glb file")
    parser.add_argument("-type", metavar="t", type=int, default=1, choices=range(0, len(model_seg_types)),
                        help="Specify the type of lung segmentation through an integer"+"\n"+"Segmentation types include " + model_proc_seg_types)
    parser.set_defaults(which=plid)


def run(args):
    input_dir = args.input
    output_path = args.output
    segment_type = args.type

    pipeline_module = load_pipeline_dynamically(plid)
    pipeline_module.run(input_dir, output_path, segment_type)


def main():
    parser = argparse.ArgumentParser(
        description=get_description(), formatter_class=RawTextHelpFormatter)
    add_parser_arguments(parser)

    args = parser.parse_args()
    run(args)
