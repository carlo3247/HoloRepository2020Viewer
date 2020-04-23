import os
import logging
import numpy as np
from core.adapters.nifti_file import read_nifti_as_np_array
from core.adapters.dicom_file import (
    read_dicom_as_np_ndarray_and_normalise,
    read_dicom_pixels_as_np_ndarray,
)


def read_input_path_as_np_array(input_path: str, normalise: bool = True) -> np.ndarray:
    logging.info("Determining file type")
    file_extension = get_file_extension(input_path)
    # assuming gunzip compressed file is compressed nifti .nii.gz
    if file_extension == ".nii" or file_extension == ".gz":
        return read_nifti_as_np_array(input_path, normalise=normalise)
    # assuming an input directory contains a stack of DICOM images
    elif file_extension == "":
        if normalise:
            return read_dicom_as_np_ndarray_and_normalise(input_path)
        else:
            return read_dicom_pixels_as_np_ndarray(input_path)
    else:
        raise Exception(
            "Can not determine input path. Please specify a folder containing DICOM images or a NIfTI image."
        )


def get_file_extension(input_path: str) -> str:
    _, file_extension = os.path.splitext(input_path)
    return file_extension
