import logging
from pistarlab import ctx

EXTENSION_ID = "pistarlab-envs-gym-minigrid"
EXTENSION_VERSION = "0.0.1.dev0"

from pistarlab.utils.gym_importer import get_environments_from_gym_registry

def manifest():
    import gym_minigrid
    envs = get_environments_from_gym_registry(
        entry_point_prefix=f"gym_minigrid.envs",
        max_count = 300,
        default_wrappers=[{'entry_point':"gym_minigrid.wrappers:ImgObsWrapper",'kwargs':{}}],
        force_environment_id="minigrid",
        collection="MiniGrid",
        force_environment_displayed_name="MiniGrid")
    return {'environments': envs}

def install():
    ctx.install_extension_from_manifest(EXTENSION_ID,EXTENSION_VERSION)
    return True

def load():
    import gym_minigrid
    return True

def uninstall():
    logging.info("Uninstalling {}".format(EXTENSION_ID))
    ctx.disable_extension_by_id(EXTENSION_ID)
    return True