"""
This module contains functionality related to writing a mesh to disk as an GLB file.
"""
import logging
import numpy as np
import trimesh
from trimesh import repair
from trimesh.smoothing import filter_laplacian


def write_mesh_as_glb(meshes, output_obj_file_path: str, metadata={}) -> None:
    logging.info(
        "Writing mesh to glb file. Saving here: {}".format(output_obj_file_path)
    )
    scene = trimesh.Scene(metadata=metadata)
    for mesh in meshes:
        mesh2 = trimesh.Trimesh(vertices=mesh[0], faces=mesh[1], vertex_normals=mesh[2])
        filter_laplacian(mesh2, volume_constraint=False)
        repair.fix_inversion(mesh2)
        scene.add_geometry(mesh2)
    scene.export(output_obj_file_path)


def write_mesh_as_glb_with_colour(
    meshes, output_obj_file_path: str, colour=[], metadata={}
) -> None:
    logging.info(
        "Writing mesh to glb file. Saving here: {}".format(output_obj_file_path)
    )
    scene = trimesh.Scene(metadata=metadata)
    index = 0
    if len(colour) != len(meshes):
        colour = get_random_rgb_colours(len(meshes))
    for mesh in meshes:
        mesh2 = trimesh.Trimesh(
            vertices=mesh[0], faces=mesh[1], vertex_normals=mesh[2],
        )
        filter_laplacian(mesh2, volume_constraint=False)
        repair.fix_inversion(mesh2)
        mesh2.visual.material = trimesh.visual.material.SimpleMaterial(
            diffuse=np.asarray(colour[index])
        )
        scene.add_geometry(mesh2)
        index += 1
    scene.export(output_obj_file_path)


def get_random_rgb_colours(length, alpha=0.5):
    colour = np.random.rand(length, 3)
    alpha = np.ones((length, 1)) * alpha
    colour = (np.concatenate([colour, alpha], axis=1) * 255).astype(np.uint8)
    return colour
