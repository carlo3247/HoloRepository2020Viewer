"""
This is a pipeline performs brain segmentation using the winning network from mrbrains18 (https://doi.org/10.1007/978-3-030-11723-8_40).
"""
import os

from core.adapters.nifti_file import read_nifti_as_np_array
from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import seperate_segmentation


from core.client.viewer import view_mesh

from models.brain_segmentation.model import brain_model
import logging

this_plid = os.path.basename(__file__).replace(".py", "")


def run(
    flair_input_directory: str,
    t1_input_directory: str,
    ir_input_directory: str,
    output_path: str,
    segment_type: list,
):
    logging.info("Starting brain pipeline")
    flair_array = read_nifti_as_np_array(flair_input_directory)
    t1_array = read_nifti_as_np_array(t1_input_directory)
    ir_array = read_nifti_as_np_array(ir_input_directory)
    segmented_array = brain_model.predict(flair_array, t1_array, ir_array)

    meshes = [
        generate_mesh(segment, 0)
        for segment in seperate_segmentation(
            segmented_array, unique_values=segment_type
        )
    ]

    meshes = convert_meshes_trimesh(meshes)
    view_mesh(meshes, output_path)
    logging.info("Brain pipeline finished successfully")
