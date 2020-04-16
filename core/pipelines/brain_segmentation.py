"""
This is a pipeline performs brain segmentation using the winning network from mrbrains18 (https://doi.org/10.1007/978-3-030-11723-8_40).
"""
import os

from core.adapters.nifti_file import read_nifti_as_np_array
from core.adapters.glb_file import write_mesh_as_glb_with_colour
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import seperate_segmentation

from models.brain_segmentation.model import brain_model

this_plid = os.path.basename(__file__).replace(".py", "")


def run(flair_input_directory, t1_input_directory, ir_input_directory, output_path: str):

    flair_array = read_nifti_as_np_array(flair_input_directory)
    t1_array = read_nifti_as_np_array(t1_input_directory)
    ir_array = read_nifti_as_np_array(ir_input_directory)

    segmented_array = brain_model.predict(flair_array, t1_array, ir_array)

    # TODO for now just use two of the segments
    meshes = [generate_mesh(segment, 0) for segment in seperate_segmentation(
        segmented_array, unique_values=[1, 5])]

    # TODO do something for colours
    colours = [[0, 0.3, 1.0, 0.2], [1.0, 1.0, 0.0, 1.0]]
    write_mesh_as_glb_with_colour(meshes, output_path, colours)
