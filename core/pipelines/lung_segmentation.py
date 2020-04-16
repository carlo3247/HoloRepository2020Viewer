"""
This pipeline performs automatic segmentation of lungs. It uses an existing algorithmic
implementation for the actual segmentation.

Algorithm: https://github.com/wanwanbeen/ct_lung_segmentation
Paper: Discriminative Localization in CNNs for Weakly-Supervised Segmentation of Pulmonary Nodules
Xinyang Feng, Jie Yang, Andrew F. Laine, Elsa D. Angelini
"""

import os
import sys

from core.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise

from core.adapters.nifti_file import (
    convert_dicom_np_ndarray_to_nifti_image,
    read_nifti_as_np_array,
    write_np_array_as_nifti_image,
)
from core.adapters.glb_file import write_mesh_as_glb
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import downscale_and_conditionally_crop
from core.tasks.shared.dispatch_output import dispatch_output
from core.tasks.shared.receive_input import fetch_and_unzip
from core.third_party.lung_and_airway_segmentation import perform_lung_segmentation
from jobs.jobs_io import (
    get_input_directory_path_for_job,
    get_logger_for_job,
    get_result_file_path_for_job,
    get_temp_file_path_for_job,
)
from jobs.jobs_state import JobState, update_job_state

this_plid = os.path.basename(__file__).replace(".py", "")

# For this pipeline, take into account anything > 0 from the generated segmentation
hu_threshold = 0


def run(input_dir: str, output_path: str) -> None:

    image_data_np_ndarray = read_dicom_as_np_ndarray_and_normalise(
        input_dir)

    nifti_image = convert_dicom_np_ndarray_to_nifti_image(
        image_data_np_ndarray)

    downscaled_image = downscale_and_conditionally_crop(nifti_image.dataobj)

    write_np_array_as_nifti_image(downscaled_image, nifti_output_file_path)

    generated_segmented_lung_nifti_path = perform_lung_segmentation(
        nifti_output_file_path, output_nifti_directory_path
    )

    nifti_image_as_np_array = read_nifti_as_np_array(
        generated_segmented_lung_nifti_path, normalise=True
    )

    meshes = [generate_mesh(nifti_image_as_np_array, hu_threshold)]
    write_mesh_as_glb(meshes, output_path)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
