import logging
from pistarlab import ctx

from pistarlab.extension_tools import load_extension_meta
EXT_META = load_extension_meta(__name__)
EXTENSION_ID = EXT_META["id"]
EXTENSION_VERSION =  EXT_META["version"]

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