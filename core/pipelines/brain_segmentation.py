"""
This is a pipeline performs brain segmentation using the winning network from mrbrains18 (https://doi.org/10.1007/978-3-030-11723-8_40).
"""
import os
import logging
from core.adapters.file_loader import read_input_path_as_np_array
from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.services.marching_cubes import generate_mesh
from core.adapters.glb_file import write_mesh_as_glb_with_colour
from core.services.np_image_manipulation import seperate_segmentation
from models.model_controller import get_seg_types
from core.client.viewer import view_mesh
from models.brain_segmentation.model import brain_model

this_plid = os.path.basename(__file__).replace(".py", "")


def run(
    input_directories: list, output_path: str, segment_type: list, open_viewer=True
):
    flair_input_path = input_directories[0]
    t1_input_path = input_directories[1]
    ir_input_path = input_directories[2]

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

    if open_viewer:
        meshes = convert_meshes_trimesh(meshes)
        segment_dict = get_seg_types(this_plid)
        mesh_names = [k for k, v in segment_dict.items() if v in segment_type]
        view_mesh(meshes=meshes, mesh_names=mesh_names, output_file=output_path)
    else:
        write_mesh_as_glb_with_colour(meshes, output_path)
    logging.info("Brain pipeline finished successfully")
