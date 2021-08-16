import logging
from pistarlab.utils.env_helpers import get_environment_data, get_env_spec_data
EXTENSION_ID = "pistarlab-multigrid"
EXTENSION_VERSION = "0.0.1-dev"

def manifest():
    import gym_multigrid
    from pistarlab.utils.gym_importer import    get_environments_from_gym_registry 
    envs = get_environments_from_gym_registry(
        entry_point_prefix="gym_multigrid.envs",
        overwrite=False,
        max_count = 300,
        default_wrappers=[
            {'entry_point':"gym_minigrid.wrappers:ImgObsWrapper",'kwargs':{}}
        ],
        force_environment_id="multigrid",
        force_environment_displayed_name="MultiGrid")

    return {'environments':envs}

def install():
    
    # Original: https://github.com/ArnaudFickinger/gym-multigrid
    logging.info("Installing")

    

    return True

def load():
    import gym_multigrid
    logging.info("Importing gym_minigrid")
    return True

def uninstall():
    logging.info("Uninstalling minigrid")
    from pistarlab.dbmodels import EnvSpec
    from pistarlab import ctx
    ctx.disable_extension_by_id(EXTENSION_ID)

    return True