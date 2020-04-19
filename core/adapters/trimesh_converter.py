import logging
import trimesh


def convert_meshes_trimesh(meshes):
    logging.info("Converting meshes to trimesh.")
    trimesh_objects = []
    index = 0
    for mesh in meshes:
        mesh2 = trimesh.Trimesh(
            vertices=mesh[0], faces=mesh[1], vertex_normals=mesh[2],
        )

        trimesh_objects.append(mesh2)
        index += 1
    return trimesh_objects
