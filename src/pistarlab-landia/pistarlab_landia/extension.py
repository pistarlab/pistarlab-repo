
from pistarlab.utils.env_helpers import get_environment_data, get_env_spec_data
import logging
from pistarlab import ctx
from pistarlab.meta import RL_MULTIPLAYER_ENV, RL_SINGLEPLAYER_ENV

EXTENSION_ID = "pistarlab-landia"
EXTENSION_VERSION = "0.0.1"


def get_env_specs():
    spec_list = []
    spec = get_env_spec_data(
        displayed_name="Landia: Capture the Flag",
        spec_displayed_name="Capture the Flag",
        description="Two teams (red/blue) try to capture each other flag.",
        spec_id='landia_ctf',
        env_type=RL_MULTIPLAYER_ENV,
        env_kwargs={
            "remote_client": False,
            "tick_rate": 0,
            "hostname": "localhost",
            "resolution": (42, 42),
            "port": 10001,
            "agent_map": {
                "1": {
                    "team_name": "red"
                },
                "2": {
                    "team_name": "red"
                },
                "3": {
                    "team_name": "blue"
                },
                "4": {
                    "team_name": "blue"
                }
            },
            "content_overrides": {
                'active_controllers': ["ctf"],
                "controllers": {
                    "ctf": {
                        "class": "CTFController",
                        "config": {
                            "min_team_size": 0
                        }
                    }},

                "maps": {
                    "main": {"static_layers": ['ctf_map_1.txt']}
                }

            }},
        entry_point="landia.env:LandiaEnv",
        default_render_mode='rgb_array',
        default_wrappers=[])
    spec_list.append(spec)

    spec = get_env_spec_data(
        displayed_name="Landia: Forage",
        spec_displayed_name="Forage",
        spec_id='landia_forage',
        env_type=RL_MULTIPLAYER_ENV,
        env_kwargs={
            "remote_client": False,
            "tick_rate": 0,
            "hostname": "localhost",
            "resolution": (42, 42),
            "port": 10001,
            "content_overrides": {
                'active_controllers': ["pspawn", "foodcollect", "objcollision"],
                "maps": {
                    "main": {"static_layers": ['map_9x9_vwall.txt']}
                }

            }},
        entry_point="landia.env:LandiaEnv",
        default_render_mode='rgb_array',
        default_wrappers=[])
    spec_list.append(spec)

    spec = get_env_spec_data(
        displayed_name="Landia: Infection",
        spec_displayed_name="Infection",
        spec_id='landia_infection',
        env_type=RL_MULTIPLAYER_ENV,
        env_kwargs={
            "remote_client": False,
            "tick_rate": 0,
            "hostname": "localhost",
            "resolution": (42, 42),
            "port": 10001,
            "content_overrides": {
                'active_controllers': ["pspawn", "objcollision", "infect1"],
                "maps": {
                    "main": {"static_layers": ['map_9x9_vwall.txt']}
                }}
        },

        entry_point="landia.env:LandiaEnv",
        default_render_mode='rgb_array',
        default_wrappers=[])
    spec_list.append(spec)

    spec = get_env_spec_data(
        displayed_name="Landia: Tag",
        spec_displayed_name="Tag",
        spec_id='landia_tag',
        env_type=RL_MULTIPLAYER_ENV,
        env_kwargs={
            "remote_client": False,
            "tick_rate": 0,
            "hostname": "localhost",
            "resolution": (42, 42),
            "port": 10001,
            "content_overrides": {
                'active_controllers': ["pspawn", "objcollision", "tag1"],
                "maps": {
                    "main": {"static_layers": ['map_8x8_empty.txt']}
                }
            }},
        entry_point="landia.env:LandiaEnv",
        default_render_mode='rgb_array',
        default_wrappers=[])
    spec_list.append(spec)

    return spec_list


def manifest():
    environment = get_environment_data(
        environment_id="landia",
        displayed_name="Landia",
        categories=[],
        collection="piSTAR Lab",
        env_specs=get_env_specs())
    return {'environments': [environment]}


def install():
    ctx.install_extension_from_manifest(EXTENSION_ID, EXTENSION_VERSION)
    return True


def load():
    return True


def uninstall():
    ctx.disable_extension_by_id(EXTENSION_ID)
    return True
