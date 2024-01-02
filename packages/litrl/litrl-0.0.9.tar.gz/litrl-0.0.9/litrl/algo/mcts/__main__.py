# from loguru import logger  # TODO
# from .agent import MCTSAgent
# from .mcts_config import MCTSConfig, MCTSConfigBuilder
# from litrl.env.typing import ConnectFourObs
# from typing import cast

# if __name__ == "__main__":
#     import argparse
#     from time import sleep
#     from litrl.algo.mcts.typing import MctsEnv
#     from litrl import make

#     parser = argparse.ArgumentParser()
#     parser.add_argument("--n-simulations", default=500, type=int)
#     parser.add_argument("--wait-time", default=1, type=int)
#     parser.add_argument(
#         "--prompt-action",
#         default=True,
#         action=argparse.BooleanOptionalAction,
#     )
#     args = parser.parse_args()

#     cfg = MCTSConfigBuilder().vanilla()
#     agent = MCTSAgent(cfg, prompt_action=args.prompt_action)
#     opponent = MCTSAgent(cfg, prompt_action=args.prompt_action)
#     env = cast(MctsEnv, make("ConnectFour-v3"))
#     env.reset(seed=123)
#     obs, reward, terminated, truncated, info = env.last()
#     terminated, truncated = False, False
#     while not (terminated or truncated):
#         sleep(args.wait_time)
#         action = agent.get_action(env)
#         env.step(action)
#         obs, reward, terminated, truncated, info = env.last()
#     logger.info(f"Game over, final reward is {reward}")
