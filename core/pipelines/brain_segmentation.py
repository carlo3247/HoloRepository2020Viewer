"""
This is a pipeline performs brain segmentation using the winning network from mrbrains18 (https://doi.org/10.1007/978-3-030-11723-8_40).
"""
import os

from core.adapters.file_loader import read_input_path_as_np_array
from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import seperate_segmentation


from core.client.viewer import view_mesh

from models.brain_segmentation.model import brain_model
import logging

this_plid = os.path.basename(__file__).replace(".py", "")


def run(
    input_directories: list, output_path: str, segment_type: list,
):
    flair_input_directory = input_directories[0]
    t1_input_directory = input_directories[1]
    ir_input_directory = input_directories[2]

    logging.info("Starting brain pipeline")
    flair_array = read_input_path_as_np_array(flair_input_path)
    t1_array = read_input_path_as_np_array(t1_input_path)
    ir_array = read_input_path_as_np_array(ir_input_path)
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
