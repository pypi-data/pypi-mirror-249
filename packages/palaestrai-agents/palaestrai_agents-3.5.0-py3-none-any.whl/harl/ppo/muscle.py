from typing import List

import numpy as np
import torch

from harl.ppo.network import ActorNetwork, CriticNetwork
from palaestrai.agent import (
    BrainDumper,
    ActuatorInformation,
    SensorInformation,
)
from palaestrai.agent import Muscle, LOG
from palaestrai.types import Box


def output_scaling(actuators_available, actions):
    """Method to scale the output to the given actuator space.

    If the network output space changes, this method needs to be
    modified as well.
    """
    assert len(actions) == len(actuators_available)

    input_range = [-1, 1]

    for idx, action in enumerate(actions):
        assert isinstance(
            actuators_available[idx].action_space, Box
        ), f'{actuators_available[idx].action_space} must be "Box" type'
        value = np.interp(
            action,
            input_range,
            [
                actuators_available[idx].action_space.low[0],
                actuators_available[idx].action_space.high[0],
            ],
        )
        actuators_available[idx]([value])
    return actuators_available


class PPOMuscle(Muscle):
    def __init__(self, broker_uri, brain_uri, uid, brain_id):
        super().__init__(broker_uri, brain_uri, uid, brain_id, "")

        # Initialize the covariance matrix used to query the actor for actions
        self.cov_mat = None
        self.actor = None
        self.critic = None

    def setup(self):
        pass

    @torch.no_grad()
    def propose_actions(
        self,
        sensors: List[SensorInformation],
        actuators_available: List[ActuatorInformation],
    ):
        if self.cov_mat is None:
            cov_var = torch.full(size=(len(actuators_available),), fill_value=0.5)
            self.cov_mat = torch.diag(cov_var)

        input_values = [val() for val in sensors]
        obs = torch.tensor(
            np.array(
                input_values
            ),  # Erases "UserWarning: Creating a tensor from a list of numpy.ndarray is slow..."
            dtype=torch.float,
        ).to(self.actor.device)
        # Query the actor network for a mean action
        dist = self.actor(obs)
        value = self.critic(obs)
        action = dist.sample()

        probs = dist.log_prob(action).cpu().data.numpy().flatten()
        action = action.cpu().data.numpy().flatten()
        value = value.cpu().data.numpy().flatten()

        assert len(action) == len(actuators_available)

        # env_actions = output_scaling(actuators_available, action)
        additional_data = {"probs": probs, "vals": value}

        # return env_actions, action, input_values, additional_data
        return actuators_available, (action, additional_data)

    def update(self, update: dict):
        """Update weights of actor network."""

        if self.actor is None or self.critic is None and update is not None:
            self._init(**update)
        elif update is not None:
            self._update_weights(weights=update)

    def _init(self, in_dim, out_dim, weights):
        """Initialize the actor-network."""
        self.actor = ActorNetwork(
            state_dim=in_dim,
            action_dim=out_dim,
        )
        self.critic = CriticNetwork(
            state_dim=in_dim,
        )
        self._update_weights(weights=weights)

    def _update_weights(self, weights):
        self.actor.load_state_dict(weights["actor"])
        self.critic.load_state_dict(weights["critic"])

    def prepare_model(self):
        assert self._model_loaders, "Brain loaders are not set for preparing model"
        bio = BrainDumper.load_brain_dump(self._model_loaders, "ppo_actor")
        if bio is not None:
            try:
                self._load_model(bio)
            except Exception as e:
                LOG.exception(
                    "PPOMuscle(id=0x%x, uid=%s) encountered error while "
                    "loading model: %s ",
                    id(self),
                    str(self.uid),
                    e,
                )
                raise

    def _load_model(self, model):
        self._model = torch.load(model)
        self._model.eval()

    def __repr__(self):
        pass
