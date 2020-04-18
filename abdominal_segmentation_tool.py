import argparse
from argparse import RawTextHelpFormatter
from core.pipelines.pipelines_controller import (
    get_pipeline_description, load_pipeline_dynamically)
from models.model_controller import (get_seg_types,
                                     get_file_types,
                                     get_proc_seg_types)

plid = "abdominal_organs_segmentation"


def get_description():
    pipeline_description = get_pipeline_description(plid)
    model_file_types = get_file_types(plid)
    return pipeline_description +\
        "\nInput files must be of type " +\
        " or ".join(model_file_types) +\
        "\nDefault segmentaion: spleen & liver & stomach "


def add_parser_arguments(parser):
    model_seg_types = get_seg_types(plid)
    model_proc_seg_types = get_proc_seg_types(plid)
    parser.add_argument("input", metavar="i", type=str,
                        help="Specify the path to the directory containing the input scans")
    parser.add_argument("output", metavar="o", type=str,
                        help="Specify the path of a single output file in the form of a glb file")
    parser.add_argument("-type", metavar="t", type=int, nargs="*", default=[1, 5, 6], choices=range(0, len(model_seg_types)),
                        help="Specify the type of abdominal segmentation through an integer. Multiple integers can be supplied"
                        + "\n"+"Segmentation types include " + model_proc_seg_types)


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


if __name__ == "__main__":
    main()
