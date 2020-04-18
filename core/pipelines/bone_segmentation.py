"""
This pipeline performs automatic segmentation of bones from CT scans.
It implements a basic Hounsfield unit thresholding.
"""

import os
import sys

import numpy as np
from core.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise
from core.adapters.glb_file import write_mesh_as_glb
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import downscale_and_conditionally_crop

this_plid = os.path.basename(__file__).replace(".py", "")
bone_hu_threshold = 300


def run(input_dir: str, output_path: str) -> None:

    dicom_image: np.ndarray = read_dicom_as_np_ndarray_and_normalise(input_dir)

    downscaled_image = downscale_and_conditionally_crop(dicom_image)

    meshes = [generate_mesh(downscaled_image, bone_hu_threshold)]

    write_mesh_as_glb(meshes, output_path)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
