import argparse

import numpy as np

import globals as g
import plotter
from env_manager import EnvManager
from model import DQN
from replay_memory import ReplayMemory
from train import Trainer

# Parse command line arguments
parser = argparse.ArgumentParser(description="Train DeepQbert")
parser.add_argument(
    "--load-checkpoint",
    choices=["best", "latest", "none"],
    default="none",
    help="Load from checkpoint: best model, latest model, or none",
)
parser.add_argument(
    "--num-episodes",
    type=int,
    default=5,
    help="Number of episodes to train for",
)
parser.add_argument(
    "--checkpoint-freq",
    type=int,
    default=2,
    help="Save checkpoint every N episodes",
)
parser.add_argument(
    "--max-frames",
    type=int,
    default=None,
    help="Maximum number of frames to train for (default: no limit)",
)
parser.add_argument(
    "--env-name",
    type=str,
    default="ALE/Pong-v5",
    help="Environment name. Can be: ALE/Pong-v5, ALE/BeamRider-v5, ALE/Qbert-v5, ALE/Breakout-v5, ALE/Seaquest-v5, ALE/Pong-v5",
)
parser.add_argument(
    "--no-recording",
    action="store_true",
    help="Disable recording",
)
args = parser.parse_args()

# clean up the env name for the checkpoint directory
env_name = args.env_name.replace("/", "-")

envManager = EnvManager(args.env_name)

# Make the network
network = DQN(g.QUEUE_N_FRAMES, envManager.env.action_space.n).to(g.DEVICE)

if not args.no_recording:
    envManager.setup_recording(args.checkpoint_freq)

# Make the memory
memory = ReplayMemory(1000000)

# Create trainer instance
trainer = Trainer(
    env_manager=envManager,
    network=network,
    memory=memory,
    checkpoint_dir=f"checkpoints/{env_name}",
)

# Train the model
episodes_rewards = trainer.train(
    num_episodes=args.num_episodes,
    checkpoint_freq=args.checkpoint_freq,
    load_checkpoint_type=args.load_checkpoint,
    max_frames=args.max_frames,
)

plotter.plot_data(
    x=np.arange(len(episodes_rewards)),
    y=episodes_rewards,
    config=plotter.PlotConfig(
        title="Episode Rewards",
        xlabel="Episode",
        ylabel="Reward",
        running_avg=True,
        window_size=100,
        filepath=f"plots/{env_name}/rewards_{len(episodes_rewards)}.png",
    ),
)

# Close the environment
envManager.env.close()
