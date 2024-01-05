"""
Brain for the PPO implementation in palaestrai.
"""

import io
import socket
from pathlib import Path
from typing import Sequence, List, Union, Optional, Any

import numpy as np
import torch as T

from harl.ppo.network import (
    PPOMemory,
    ActorNetwork,
    CriticNetwork,
)
from palaestrai.agent import (
    Brain,
    BrainDumper,
    Objective,
    SensorInformation,
    ActuatorInformation,
    LOG,
)
from palaestrai.core.protocol import MuscleUpdateResponse
from palaestrai.util.exception import NoneInputError


class PPOBrain(Brain):
    """
    Parameters
    ----------
    sensors : List[SensorInformation]
        List of sensor information.
    actuators : List[ActuatorInformation]
        List of actuator information.
    objective : Objective
        The agent's objective function.
    seed : int
        Seed for random number generators.
    timesteps_per_batch : int = 4
        Number of timesteps per batch.
    max_timesteps_per_episode : int = 96
        Maximum amount of timesteps per episode.
    n_updates_per_iteration : int = 50
        The number of updates per learning iteration.
    actor_lr : float = 3e-4
        The actor's learning rate.
    critic_lr : float = 1e-3
        The critic's learning rate.
    adam_eps : float = 1e-5
        The adam optimiser's epsilon parameter.

    fc_dims: Sequence[int] = (256, 256)
        Dimensions (amount of fully connected neurons) of the hidden layers
        in the agent's actor and critic networks.

    gamma : float = 0.99
        Factor by which to discount the worth of later rewards.
    clip : float = 0.2
        Epsilon value of the clipping function.
    gae_lambda : float = 0.95
        Lambda of the general advantage estimation.
    action_std_init : float = 0.6
        Initial standard deviation of the actions.
    action_std_decay_rate : float = 0.05
        Rate by which the action's standard deviation should decay.
    min_action_std : float = 0.1
        Minimum value of the action's standard deviation.
    action_std_decay_freq : int = 2.5e5
        Frequency of the decay (every x steps).
    """

    def __init__(
        self,
        muscle_updates_listen_uri_or_socket: Union[str, socket.socket],
        sensors: List[SensorInformation],
        actuators: List[ActuatorInformation],
        objective: Objective,
        seed: int,
        timesteps_per_batch: int = 4,
        max_timesteps_per_episode: int = 96,
        n_updates_per_iteration: int = 50,
        actor_lr: float = 3e-4,  # CleanRL: 2.5e-4
        critic_lr: float = 1e-3,  # CleanRL: 2.5e-4
        adam_eps: float = 1e-5,
        fc_dims: Sequence[int] = (256, 256),
        gamma: float = 0.99,
        clip: float = 0.2,
        gae_lambda: float = 0.95,
        action_std_init: float = 0.6,  # STD = Standard Deviation
        action_std_decay_rate: float = 0.05,
        min_action_std: float = 0.1,
        action_std_decay_freq: int = 2.5e5,
        **params,
    ):
        super().__init__()

        self._muscle_updates_listen_uri_or_socket = muscle_updates_listen_uri_or_socket
        self._sensors = sensors
        self._actuators = actuators
        self._objective = objective
        self._seed = seed

        T.manual_seed(self.seed)

        self.timesteps_per_batch = timesteps_per_batch
        self.max_timesteps_per_episode = max_timesteps_per_episode
        self.n_updates_per_iteration = n_updates_per_iteration
        self.actor_lr = actor_lr
        self.critic_lr = critic_lr
        self.adam_eps = adam_eps

        self.fc_dims = fc_dims

        self.gamma = gamma
        self.clip = clip
        self.gae_lambda = gae_lambda

        self.action_std_init = action_std_init
        self.action_std_decay_rate = action_std_decay_rate
        self.min_action_std = min_action_std
        self.action_std_decay_freq = action_std_decay_freq

        self.sen_dim = len(self._sensors)
        self.act_dim = len(self._actuators)

        self.actor = ActorNetwork(
            self.sen_dim,
            self.act_dim,
            self.actor_lr,
            self.adam_eps,
            self.fc_dims,
            action_std_init=self.action_std_init,
        )
        self.critic = CriticNetwork(
            self.sen_dim,
            self.critic_lr,
            self.adam_eps,
            self.fc_dims,
        )

        self.step = 0
        self.action_std = self.action_std_init

        self._memory = PPOMemory(self.timesteps_per_batch)

        self.init_muscle = False
        self.t = 0

    def _remember(self, state, action, probs, vals, reward, done):
        self._memory.store_memory(state, action, probs, vals, reward, done)

    def thinking(self, muscle_id, data_from_muscle: Any) -> Any:
        assert self.actor is not None
        assert self.critic is not None

        if not self.init_muscle:
            self.init_muscle = True
            return self._get_init_dict()

        if data_from_muscle is None:  # Okay, happens during initialization
            LOG.error(
                "Brain(id=0x%x) has received a none value",
                id(self),
            )
            raise NoneInputError
        assert isinstance(data_from_muscle, tuple)
        assert len(data_from_muscle) == 2

        self._remember(
            state=data_from_muscle[0],
            action=data_from_muscle[1][0],
            probs=data_from_muscle[1][1]["probs"],
            vals=data_from_muscle[1][1]["vals"],
            reward=self.memory.tail(1).objective.item(),
            done=self.memory.tail(1).dones.item(),
        )

        self.step += 1
        if self.step % self.max_timesteps_per_episode == 0:
            response = self._learn()
        else:
            response = None

        if self.step % self.action_std_decay_freq == 0:
            self.decay_action_std()
        return response

    def _learn(self):
        for update in range(self.n_updates_per_iteration):
            (
                state_arr,
                action_arr,
                old_prob_arr,
                values,
                reward_arr,
                dones_arr,
                batches,
            ) = self._memory.generate_batches()

            advantage = np.zeros(len(reward_arr), dtype=np.float32)
            self.learning_rate_annealing(update)

            for t in range(len(reward_arr) - 1):
                discount = 1
                a_t = 0
                for k in range(t, len(reward_arr) - 1):
                    a_t += discount * (
                        reward_arr[k]
                        + self.gamma * values[k + 1] * (1 - int(dones_arr[k]))
                        - values[k]
                    )
                    discount *= self.gamma * self.gae_lambda
                advantage[t] = a_t
            advantage = T.tensor(advantage).to(self.actor.device)

            values = T.tensor(values).to(self.actor.device)
            for batch in batches:
                states = T.tensor(state_arr[batch], dtype=T.float).to(self.actor.device)
                old_probs = T.tensor(old_prob_arr[batch]).to(self.actor.device)
                actions = T.tensor(action_arr[batch]).to(self.actor.device)

                critic_value = self.critic(states)
                critic_value = T.squeeze(critic_value)

                dist = self.actor(states)
                new_probs = dist.log_prob(actions)
                prob_ratio = new_probs.exp() / old_probs.exp()
                weighted_probs = advantage[batch] * prob_ratio
                weighted_clipped_probs = (
                    T.clamp(prob_ratio, 1 - self.clip, 1 + self.clip) * advantage[batch]
                )
                actor_loss = -T.min(weighted_probs, weighted_clipped_probs).mean()

                returns = advantage[batch] + values[batch]
                critic_loss = (returns - critic_value) ** 2
                critic_loss = 0.5 * critic_loss.mean()

                # Could add Entropy Bonus below, but no evidence of performance improvement
                total_loss = actor_loss + critic_loss
                self.actor.optimizer.zero_grad()
                self.critic.optimizer.zero_grad()
                total_loss.backward()
                self.actor.optimizer.step()
                self.critic.optimizer.step()

        self._memory.clear_memory()
        return {
            "actor": self._get_actor_params(),
            "critic": self._get_critic_params(),
            "var": self.actor.action_var,
        }

    def load(self):
        actor_dump = BrainDumper.load_brain_dump(self._dumpers, "ppo_critic")
        actor_target_dump = BrainDumper.load_brain_dump(self._dumpers, "ppo_actor")
        critic_dump = BrainDumper.load_brain_dump(self._dumpers, "ppo_critic")
        critic_target_dump = BrainDumper.load_brain_dump(self._dumpers, "ppo_critic")
        if any(
            [
                x is None
                for x in [
                    actor_dump,
                    actor_target_dump,
                    critic_dump,
                    critic_target_dump,
                ]
            ]
        ):
            return  # Don't apply "None"s
        self.actor = T.load(actor_dump)
        self.critic = T.load(critic_dump)

    def store(self):
        bio = io.BytesIO()

        T.save(self.actor, bio)
        BrainDumper.store_brain_dump(bio, self._dumpers, "ppo_actor")

        bio.seek(0)
        bio.truncate(0)
        T.save(self.critic, bio),
        BrainDumper.store_brain_dump(bio, self._dumpers, "ppo_critic")

    def _get_init_dict(self):
        """Special dict for the initialisation of the muscle."""
        return {
            "weights": {
                "actor": self._get_actor_params(),
                "critic": self._get_critic_params(),
            },
            "in_dim": len(self.sensors),
            "out_dim": len(self.actuators),
        }

    def _get_actor_params(self):
        return dict(self.actor.named_parameters())

    def _get_critic_params(self):
        return dict(self.critic.named_parameters())

    def decay_action_std(self):
        self.action_std = round(self.action_std - self.action_std_decay_rate, 4)
        if self.action_std <= self.min_action_std:
            self.action_std = self.min_action_std
        self.actor.set_action_std(self.action_std)

    def learning_rate_annealing(self, update):
        """Anneals the learning rate
        update: The current update iteration
        """
        frac = 1.0 - (update - 1.0) / self.n_updates_per_iteration
        actor_lrnow = frac * self.actor_lr
        critic_lrnow = frac * self.critic_lr
        self.actor.optimizer.param_groups[0]["lr"] = actor_lrnow
        self.critic.optimizer.param_groups[0]["lr"] = critic_lrnow
