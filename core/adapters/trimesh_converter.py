import logging
import trimesh
from trimesh.smoothing import filter_laplacian
import numpy as np


def convert_meshes_trimesh(meshes):
    logging.info("Converting meshes to trimesh.")
    trimesh_objects = []
    index = 0
    for mesh in meshes:
        tmp_mesh = trimesh.Trimesh(
            vertices=mesh[0],
            faces=mesh[1],
            vertex_normals=mesh[2],
            vertex_colors=get_random_rgb_colours()
            + [0.5],  # set alpha to 0.5 for all colours
        )
        filter_laplacian(tmp_mesh, volume_constraint=False)
        trimesh_objects.append(tmp_mesh)
        index += 1
    return trimesh_objects


def get_random_rgb_colours():
    return list(np.random.rand(3))
