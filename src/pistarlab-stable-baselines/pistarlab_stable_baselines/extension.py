import logging
from pistarlab.dbmodels import *
import logging
from .agent import AGENT_REG
import inspect
from pistarlab.utils.param_helpers import create_params_from_dict

from pistarlab.utils.agent_helpers import get_agent_spec_dict,get_agent_spec_interface_dict

EXTENSION_ID = "pistarlab-stable-baselines"
EXTENSION_VERSION = "0.0.1-dev"

def get_agent_specs():
    spec_list = []
    for policy_name, data in AGENT_REG.items():
        logging.info("LOADING")
        logging.info(policy_name)
        cls = data['class']
        cls_name = cls.__name__
        # Extract Params
        # sig = inspect.signature(clss.__init__)
        # for name in sig.parameters:
        #     if name in excluded_params:
        #         continue
        #     param = sig.parameters[name]
        #     model_args[name] = "NO_DEFAULT" if param.default == inspect._empty else param.default


        doc = inspect.getdoc(cls)
        agent_spec = get_agent_spec_dict(
            spec_id='stable_baselines_{}'.format(cls_name),
            entry_point = 'pistarlab_stable_baselines.agent:StableBaselineAgent',
            runner_entry_point = 'pistarlab_stable_baselines.agent:StableBaselineAgentTaskRunner',
            config={
                'model_args': {},
                'policy': data['default_policy'],
                'policy_kwargs':{},
                'agent_cls_name': cls_name
            },
            components=None,
            interfaces={'run':get_agent_spec_interface_dict()},
            params=data.get("params"),
            disabled=False,
            displayed_name="{} - Stable Baselines".format(policy_name),
            version="0.0.1-dev",
            description='StableBaseline\n\nhttps://stable-baselines3.readthedocs.io/\n\n{}'.format(
                doc))

        spec_list.append(agent_spec)
    return spec_list




def install():
    logging.info("Installing: {}".format(EXTENSION_ID))
    from pistarlab import ctx
    for spec in get_agent_specs():
        ctx.register_agent_spec(**spec, extension_id=EXTENSION_ID, extension_version=EXTENSION_VERSION)

    return True


def load():
    return True

def uninstall():
    from pistarlab import ctx
    ctx.disable_extension_by_id(EXTENSION_ID)
    return True