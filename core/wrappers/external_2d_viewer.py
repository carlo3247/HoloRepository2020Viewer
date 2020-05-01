import os


def start(input_path):
    _, file_extension = os.path.splitext(input_path)
    # assuming an input directory contains a stack of DICOM images
    if file_extension == "":
        # take first file in directory and open it
        input_path = os.path.join(input_path, os.listdir(input_path)[0])
    os.startfile(input_path)
