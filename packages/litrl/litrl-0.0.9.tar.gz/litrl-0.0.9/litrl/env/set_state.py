from collections import Counter

from litrl.env.connect_four import Board, ConnectFour, flatten_board


def set_state(env: ConnectFour, board: Board) -> None:
    flat_board = flatten_board(board)
    env.unwrapped.board = flat_board

    # set the correct player turn
    counter = Counter(flat_board)
    if counter[1] > counter[2]:
        while env.unwrapped.agent_selection != "player_1":
            env.unwrapped.agent_selection = env.unwrapped._agent_selector.next()


if __name__ == "__main__":
    from litrl.env.connect_four import ConnectFour

    env = ConnectFour(render_mode="human")
    env.reset(seed=123)
    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 2, 0, 0],
    ]
    set_state(env, board)
    terminated, truncated = False, False
    while not (terminated or truncated):
        env.render()
        action = int(input("Enter action: "))
        env.step(action)
        _, reward, terminated, truncated, _ = env.last()
