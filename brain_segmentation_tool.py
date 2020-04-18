import argparse
from argparse import RawTextHelpFormatter

from core.pipelines.pipelines_controller import (
    get_pipeline_description, load_pipeline_dynamically)
from models.model_controller import (
    get_seg_types,
    get_file_types,
    get_req_modalities,
    get_proc_seg_types
)

plid = "brain_segmentation"


def get_description():
    pipeline_description = get_pipeline_description(plid)
    model_file_types = get_file_types(plid)
    model_req_mods = get_req_modalities(plid)

    return pipeline_description +\
        "\n3 input scans (modalities) required of types " +\
        ", ".join(model_req_mods) +\
        "\nInput files must be of type " +\
        " or ".join(model_file_types) +\
        "\nDefault segmentaion: cortical_gray_matter "


def add_parser_arguments(parser):
    model_seg_types = get_seg_types(plid)
    model_proc_seg_types = get_proc_seg_types(plid)

    parser.add_argument("flair_input", metavar="flair_input", type=str,
                        help="Specify the path to the directory containing the T2-FLAIR input scans")
    parser.add_argument("t1_input", metavar="t1_input", type=str,
                        help="Specify the path to the directory containing the T1 input scans")
    parser.add_argument("ir_input", metavar="t1_inversion_recovery_input", type=str,
                        help="Specify the path to the directory containing the T1-IR input scans")
    parser.add_argument("output", metavar="output", type=str,
                        help="Specify the path of a single output file in the form of a glb file")
    parser.add_argument("-t", "--type", metavar="t", type=int, nargs="*", default=[1], choices=range(0, len(model_seg_types)),
                        help="Specify the type of brain segmentation through an integer. Multiple integers can be supplied"+"\n"+"Segmentation types include " + model_proc_seg_types)
    parser.set_defaults(which=plid)


def run(args):
    flair_input_directory = args.flair_input
    t1_input_directory = args.t1_input
    ir_input_directory = args.ir_input
    output_path = args.output
    segment_type = args.type

    pipeline_module = load_pipeline_dynamically(plid)
    pipeline_module.run(flair_input_directory, t1_input_directory,
                        ir_input_directory, output_path, segment_type)


def main():
    description = get_description()
    parser = argparse.ArgumentParser(
        description=description, formatter_class=RawTextHelpFormatter)
    add_parser_arguments(parser)

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
