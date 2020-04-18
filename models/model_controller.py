"""
This module contains helper functions to show infos about pipelines
and load them dynamically.
"""
import json


def get_models_dict() -> dict:
    """
    :return: dict of available pipelines representing "pipelines.json"
    """
    with open("./models/models.json", "r") as models_file:
        return json.load(models_file)


def get_models_ids_list() -> list:
    """
    :return: list of the ids of available pipelines according to "pipelines.json"
    """
    return list(get_models_dict().keys())


def get_model_dict(modelname: str) -> dict:
    """
    :param modelname: Name of the model as written in models.json
    :return: dict containing the dictionairy for the specified model
    try:
        return get_models_dict()[modelname]
    except:
        raise Exception("Could not find {} in model.json".format(modelname))
    """


def get_seg_types(modelname: str) -> dict:
    return get_models_dict()[modelname]["segmentation_dict"]


def get_proc_seg_types(modelname: str) -> dict:
    seg_types = get_seg_types(modelname)
    return ", ".join(
        "\n* {!s} = {!r}".format(key, val) for (key, val) in seg_types.items()
    )


def get_file_types(modelname: str) -> dict:
    return get_models_dict()[modelname]["filetypes"]


def get_req_modalities(modelname: str) -> dict:
    return get_models_dict()[modelname]["required_modalities"]
