"""
This pipeline performs automatic segmentation of bones from CT scans.
It implements a basic Hounsfield unit thresholding.
"""

import os
import sys
import logging

import numpy as np
from core.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise

from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.services.marching_cubes import generate_mesh
from core.client.viewer import view_mesh

from core.services.np_image_manipulation import downscale_and_conditionally_crop

this_plid = os.path.basename(__file__).replace(".py", "")
bone_hu_threshold = 300


def run(input_dir: str, output_path: str) -> None:
    logging.info("Reading input from {}".format(input_dir))
    dicom_image: np.ndarray = read_dicom_as_np_ndarray_and_normalise(input_dir)
    downscaled_image = downscale_and_conditionally_crop(dicom_image)
    meshes = [generate_mesh(downscaled_image, bone_hu_threshold)]
    meshes = convert_meshes_trimesh(meshes)
    view_mesh(meshes, output_path)
