"""
This pipeline performs automatic segmentation of bones from CT scans.
It implements a basic Hounsfield unit thresholding.
"""

import os
import sys
import logging

import numpy as np
from core.adapters.file_loader import read_input_path_as_np_array
from core.adapters.file_loader import get_metadata
from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.services.marching_cubes import generate_mesh
from core.adapters.glb_file import write_mesh_as_glb_with_colour
from core.client.viewer import view_mesh
from models.model_controller import get_seg_types
from core.services.np_image_manipulation import downscale_and_conditionally_crop

this_plid = os.path.basename(__file__).replace(".py", "")
bone_hu_threshold = 300


def run(
    input_path: str, output_path: str, segment_type: list, open_viewer=True
) -> None:
    logging.info("Starting bone pipeline")
    dicom_image: np.ndarray = read_input_path_as_np_array(input_path)
    metadata = get_metadata(input_path)
    downscaled_image = downscale_and_conditionally_crop(dicom_image)
    meshes = [generate_mesh(downscaled_image, bone_hu_threshold)]
    if open_viewer:
        meshes = convert_meshes_trimesh(meshes)
        segment_dict = get_seg_types(this_plid)
        mesh_names = [k for k, v in segment_dict.items() if v in segment_type]
        view_mesh(
            meshes=meshes,
            mesh_names=mesh_names,
            output_file=output_path,
            patient_data=metadata,
        )
    else:
        write_mesh_as_glb_with_colour(meshes, output_path)
    logging.info("Bone pipeline finished successfully")
