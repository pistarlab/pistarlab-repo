from pistarlab.task import AgentTask
from pistarlab.session_env import RLMultiSessionEnv, RLSingleSessionEnv
from pistarlab.session_config import RLSessionConfig
from stable_baselines3 import A2C, DDPG, DQN, HER, TD3, PPO, SAC
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.base_class import BaseAlgorithm

from pistarlab.agent import Agent
from pistarlab.task_runner import AgentTaskRunner
from pistarlab.meta import *

import time
import inspect
import logging
from pistarlab import ctx

import threading


class AgentCallback(BaseCallback):

    def __init__(self, env, agent, task, verbose=0):
        super().__init__(verbose)
        self.env = env
        self.agent:StableBaselineAgent=agent
        self.step_time = time.time()
        self.running = True
        self.last_check = 0
        self.check_freq_secs = 5
        self.task = task

        self.checkpoint_freq_secs = 20
        self.last_checkpoint = 0

        # Those variables will be accessible in the callback
        # (they are defined in the base class)
        # The RL model
        # self.model = None  # type: BaseRLModel
        # An alias for self.model.get_env(), the environment used for training
        # self.training_env = None  # type: Union[gym.Env, VecEnv, None]
        # Number of time the callback was called
        # self.n_calls = 0  # type: int
        # self.num_timesteps = 0  # type: int
        # local and global variables
        # self.locals = None  # type: Dict[str, Any]
        # self.globals = None  # type: Dict[str, Any]
        # The logger object, used to report things in the terminal
        # self.logger = None  # type: logger.Logger
        # # Sometimes, for event callback, it is useful
        # # to have access to the parent object
        # self.parent = None  # type: Optional[BaseCallback]

    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """
        pass

    def _on_rollout_start(self) -> None:
        """
        A rollout is the collection of environment interaction
        using the current policy.
        This event is triggered before collecting new samples.
        """
        pass

    def _on_step(self) -> bool:

        # Check for abort
        if time.time() - self.last_check > self.check_freq_secs:
            if self.task.get_status() != STATE_RUNNING:
                self.running = False
            self.last_check = time.time()

        if time.time() - self.last_checkpoint > self.checkpoint_freq_secs:
            self.agent.save_model(self.model,meta={})
            self.last_checkpoint = time.time()

        if self.running:
            self.running = not self.env.is_complete()

        if not self.running:
            ctx.get_logger().info("No longer running")

        return self.running

    def _on_rollout_end(self) -> None:
        """
        This event is triggered before updating the policy.
        """
        pass

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        pass


AGENT_REG = {
    "A2C": {'class': A2C, 'algo_type_ids':['A2C'],'default_policy': "MlpPolicy", "params": {}},
    "DDPG": {'class': DDPG, 'algo_type_ids':['DDPG'],'default_policy': "MlpPolicy", "params": {}},
    "DQN": {'class': DQN, 'algo_type_ids':['DQN'],'default_policy': "MlpPolicy", "params": {}},
    "HER": {'class': HER, 'algo_type_ids':['HER'],'default_policy': "MlpPolicy", "params": {}},
    "PPO": {'class': PPO, 'algo_type_ids':['PPO'],'default_policy': "MlpPolicy", "params": {}},
    "TD3": {'class': TD3, 'algo_type_ids':['TD3'],'default_policy': "MlpPolicy", "params": {}},
    "SAC": {'class': SAC, 'algo_type_ids':['SAC'],'default_policy': "MlpPolicy", "params": {}},
}

excluded_params = {'env', 'self', 'policy_kwargs', 'policy',
                   'full_tensorboard_log', 'tensorboard_log', '_init_setup_model', 'verbose'}


class SBEnvWrapper(RLSingleSessionEnv):

    def __init__(self,*args,**kwargs):
        self.reward_range = [0,2]

        super().__init__(*args,**kwargs)

import os
import pickle
import json
from pistarlab.utils.misc import get_timestamp_with_proc_info


class StableBaselineAgent(Agent):

    def load_model(self,cls, env, **kwargs):
        checkpoint = self.get_last_checkpoint()
        if checkpoint is None:
            return None
        else:
            path = os.path.join(self.get_checkpoint_path(checkpoint['id']),"model.zip")
            ctx.get_logger().info(f"Loading model from {path}")
            return cls.load(path, env, **kwargs)

    def save_model(self, model, meta):
        checkpoint_id = get_timestamp_with_proc_info()
        save_path = self.get_checkpoint_path(checkpoint_id)
        file_path = os.path.join(save_path,"model.zip")
        ctx.get_logger().info(f"Saving model to {file_path}")
        model.save(file_path)
        self.update_last_checkpoint(checkpoint_id,save_path,meta)


class StableBaselineAgentTaskRunner(AgentTaskRunner):



    def run(self):

        task = self.get_task()
        agent:StableBaselineAgent = task.get_agent()

        task_id = task.get_id()
        task_config = task.get_config()

        # checkpoint_freq = task_config['checkpoint_freq']
        # status_check_freq_secs = task_config['status_check_freq_secs']
        env_spec_id = task_config['env_spec_id']
        env_kwargs = task_config['env_kwargs']
        use_remote_client = task_config.get('use_remote_client', False)

        session_config = task_config['session_config']
        agent_run_config = agent.get_config(task_config['agent_run_config'])

        env = SBEnvWrapper(
            env_spec_id=env_spec_id,
            env_kwargs=env_kwargs,
            config=RLSessionConfig(**session_config),
            agent_id=agent.get_id(),
            agent_run_config=agent_run_config,
            task_id=task_id,
            use_remote_client=use_remote_client,
            timeout_abort_check_callback=lambda: task.get_status() != STATE_RUNNING)

        agent_cls_name = agent_run_config['agent_cls_name']
        policy = agent_run_config['policy']
        policy_kwargs = agent_run_config['policy_kwargs']
        model_args = agent_run_config['model_args']

        modelcls = AGENT_REG[agent_cls_name]['class']
        tensorboard_log=ctx.get_store().get_path_from_key((AGENT_ENTITY, agent.get_id(), 'tensorboard'))
        model: BaseAlgorithm = agent.load_model(modelcls, env,tensorboard_log=tensorboard_log)
        if model is None:
            model: BaseAlgorithm = modelcls(
                policy=policy,
                env=env,
                tensorboard_log= tensorboard_log,
                verbose=1,
                policy_kwargs=policy_kwargs,
                **model_args)

        callback = AgentCallback(
            env=env,
            agent=agent,
            task=task,
            verbose=1)

        total_timesteps = env.config.max_steps
        if not total_timesteps:
            total_timesteps = 10000000  # TODO: make absolute max configurable

        learn_results = model.learn(
            total_timesteps=total_timesteps, callback=callback)

        agent.save_model(model,meta={})

        self.get_logger().info("Learning complete {}".format(learn_results))
        env.close()
        exit_state = STATE_COMPLETED

        return {}, exit_state
