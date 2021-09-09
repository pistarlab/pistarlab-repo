
from pistarlab.utils.env_helpers import get_environment_data, get_env_spec_data
import logging
from pistarlab import ctx
from pistarlab.meta import RL_MULTIPLAYER_ENV, RL_SINGLEPLAYER_ENV

from pistarlab.extension_tools import load_extension_meta
EXT_META = load_extension_meta(__name__)
EXTENSION_ID = EXT_META["id"]
EXTENSION_VERSION =  EXT_META["version"]


def get_env_specs():
    spec_list = []

    spec = get_env_spec_data(
        displayed_name="Unity: 3d ball",
        spec_displayed_name="3d ball",
        spec_id='unity_3dball',
        env_type=RL_MULTIPLAYER_ENV,
        env_kwargs={'game_name':"3dball"},
        entry_point="pistarlab_unity_envs.wrapper:Unity3DEnv",
        default_render_mode='rgb_array',
        default_wrappers=[])
    spec_list.append(spec)

    return spec_list


def manifest():
    environment = get_environment_data(
        environment_id="unity_envs",
        displayed_name="Unity Envs",
        categories=[],
        collection="Unity Envs",
        env_specs = get_env_specs() )
    return {'environments':[environment]}


def install():
    ctx.install_extension_from_manifest(EXTENSION_ID, EXTENSION_VERSION)
    return True


def load():
    return True


def uninstall():
    ctx.disable_extension_by_id(EXTENSION_ID)
    return True
