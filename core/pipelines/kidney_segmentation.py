"""
This pipeline performs automatic kidney segmentation on abdominal CT with a 3d UNet.
It leverages a pre-trained network built with MISCNN and running in a separate container.
"""

import os
import logging

from core.adapters.nifti_file import (
    read_nifti_as_np_array,
    read_nifti_image,
    write_nifti_image,
)
from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.client.viewer import view_mesh
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import seperate_segmentation
from core.adapters.glb_file import write_mesh_as_glb_with_colour
from models.kidney_segmentation.model import kidney_model

this_plid = os.path.basename(__file__).replace(".py", "")


def run(input_directory: str, output_path: str, segment_type: list) -> None:
    logger = logging.getLogger("kidney_segmentation_tool")
    logger.info("READING_INPUT")
    # TODO for now take in nifti image
    nifti_image = read_nifti_image(input_directory)

    initial_nifti_output_file_path = kidney_model.get_input_path()
    write_nifti_image(nifti_image, initial_nifti_output_file_path)
    logger.info("SEGMENTATION")
    segmented_nifti_output_file_path = kidney_model.predict()

    segmented_array = read_nifti_as_np_array(
        segmented_nifti_output_file_path, normalise=False
    )

    meshes = [
        generate_mesh(segment, 0)
        for segment in seperate_segmentation(
            segmented_array, unique_values=segment_type
        )
    ]

    meshes = convert_meshes_trimesh(meshes)
    view_mesh(meshes,output_path)

    kidney_model.cleanup()
