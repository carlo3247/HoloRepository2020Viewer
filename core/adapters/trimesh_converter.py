import logging
import trimesh
import numpy as np


def convert_meshes_trimesh(meshes):
    logging.info("Converting meshes to trimesh.")
    trimesh_objects = []
    index = 0
    for mesh in meshes:
        mesh2 = trimesh.Trimesh(
            vertices=mesh[0],
            faces=mesh[1],
            vertex_normals=mesh[2],
            vertex_colors=get_random_rgb_colours()
            + [0.5],  # set alpha to 0.5 for all colours
        )
        trimesh_objects.append(mesh2)
        index += 1
    return trimesh_objects


def get_random_rgb_colours():
    return list(np.random.rand(3))
