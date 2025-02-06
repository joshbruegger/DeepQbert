import argparse

# import globals as g
import train_refactor

# from env_manager import EnvManager
# from model import DQN
# from replay_memory import ReplayMemory
# from train import Trainer

# Parse command line arguments
parser = argparse.ArgumentParser(description="Train DeepQbert")
parser.add_argument(
    "--load-checkpoint",
    choices=["best", "latest", "none"],
    default="none",
    help="Load from checkpoint: best model, latest model, or none",
)
parser.add_argument(
    "--num-frames",
    type=int,
    default=10000000,
    help="Number of frames to train for",
)
parser.add_argument(
    "--lr",
    type=float,
    default=1e-4,
    help="Learning rate",
)
parser.add_argument(
    "--num-envs",
    type=int,
    default=1,
    help="Number of environments to train on",
)
parser.add_argument(
    "--memory-size",
    type=int,
    default=1000000,
    help="the replay memory size",
)
parser.add_argument(
    "--gamma",
    type=float,
    default=0.99,
    help="the discount factor gamma",
)
parser.add_argument(
    "--batch-size",
    type=int,
    default=32,
    help="the batch size of sample from the reply memory",
)
parser.add_argument(
    "--eps-start",
    type=float,
    default=1,
    help="the starting epsilon",
)
parser.add_argument(
    "--eps-end",
    type=float,
    default=0.1,
    help="the ending epsilon",
)
parser.add_argument(
    "--eps-decay",
    type=int,
    default=1000000,
    help="the last frame of the epsilon decay",
)
parser.add_argument(
    "--warmup-frames",
    type=int,
    default=8000,
    help="the number of frames to warm up for",
)
parser.add_argument(
    "--save-interval",
    type=int,
    default=1000,
    help="Save checkpoint every N episodes",
)
parser.add_argument(
    "--log-interval",
    type=int,
    default=100,
    help="Log interval",
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
    "--record",
    action="store_true",
    default=False,
    help="Record videos",
)
parser.add_argument(
    "--output-dir",
    type=str,
    default="output",
    help="Output directory",
)
args = parser.parse_args()

# # clean up the env name for the checkpoint directory
# env_name = args.env_name.replace("/", "-")

# envManager = EnvManager(args.env_name)

# Make the network
# network = DQN(g.MEMORY_SIZE, envManager.env.action_space.n).to(g.DEVICE)

train_refactor.train(
    num_frames=args.num_frames,
    env_name=args.env_name,
    num_envs=args.num_envs,
    record=args.record,
    checkpoint_type=args.load_checkpoint,
    log_interval=args.log_interval,
    save_interval=args.save_interval,
    warmup_frames=args.warmup_frames,
    max_frames=args.max_frames,
    batch_size=args.batch_size,
    lr=args.lr,
    gamma=args.gamma,
    output_dir=args.output_dir,
    eps_start=args.eps_start,
    eps_end=args.eps_end,
    eps_decay=args.eps_decay,
    memory_size=args.memory_size,
)


# if not args.no_recording:
#     envManager.setup_recording(args.checkpoint_freq)

# # Make the memory
# memory = ReplayMemory(1000000)

# # Create trainer instance
# trainer = Trainer(
#     env_manager=envManager,
#     network=network,
#     memory=memory,
#     output_dir=args.output_dir,
# )

# # Train the model
# episodes_rewards = trainer.train(
#     num_episodes=args.num_episodes,
#     checkpoint_freq=args.checkpoint_freq,
#     load_checkpoint_type=args.load_checkpoint,
#     max_frames=args.max_frames,
# )

# # Close the environment
# envManager.env.close()
