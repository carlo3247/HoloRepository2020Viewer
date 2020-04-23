import numpy as np
import math

import trimesh
from trimesh import visual
from trimesh import repair,smoothing
from vtkplotter import Text2D, show

import logging





def convert_meshes_trimesh(
        meshes
):
    trimesh_objects = []
    index = 0
    for mesh in meshes:
        mesh2 = trimesh.Trimesh(vertices=mesh[0],
                                faces=mesh[1],
                                vertex_normals=mesh[2],
                               )
        smoothing.filter_laplacian(mesh2)
        trimesh_objects.append(mesh2)
        index += 1
    return trimesh_objects