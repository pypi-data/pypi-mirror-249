import dash
from dash import Input, Output, callback, callback_context, dcc, html
from loguru import logger
from PIL import Image

from litrl.common.agent import Agent
from litrl.wrappers.static_opponent_wrapper import StaticOpponentWrapper

OpponentId = str

HUMAN_TURN = "Human's turn to play"
BOT_TURN = "Bot's turn to play"
GAME_OVER = "Game over"
PLAYER_COLORS = {"player_0": "red", "player_1": "black"}


def get_server(
    env: StaticOpponentWrapper,
    n_actions: int,
    opponents: dict[OpponentId, Agent],
):
    app = dash.Dash(__name__)

    @callback(
        [
            Output(component_id="image", component_property="src"),
            Output(component_id="turn", component_property="children"),
            Output(component_id="player-color", component_property="children"),
            Output(component_id="player-description-div", component_property="hidden"),
            Output(component_id="winner-div", component_property="hidden"),
            Output(component_id="winner-name", component_property="children"),
        ],
        [
            Input(component_id=f"action-{action}", component_property="n_clicks")
            for action in range(n_actions)
        ]
        + [Input(component_id="reset_button", component_property="n_clicks")],
        prevent_initial_call=True,
    )
    def render_env(*args, **kwargs):
        logger.info("Button was clicked")
        trigger = callback_context.triggered[0]
        button_id = trigger["prop_id"].split(".")[0]
        if button_id == "reset_button":
            env.reset()
            turn = HUMAN_TURN
            description_hidden = False
            winner_div_hidden = True
            winner_name = ""
        else:
            action = int(button_id.replace("action-", ""))
            _, reward, terminated, truncated, _ = env.step(action)
            if terminated or truncated:
                turn = GAME_OVER
                description_hidden = True
                winner_div_hidden = False
                winner_name = "human" if reward == 1 else "bot"
            else:
                turn = HUMAN_TURN
                description_hidden = False
                winner_div_hidden = True
                winner_name = ""
        image = Image.fromarray(env.render())
        player_color = PLAYER_COLORS[env.unwrapped.agent_selection]
        return [
            image,
            turn,
            player_color,
            description_hidden,
            winner_div_hidden,
            winner_name,
        ]

    @app.callback(
        Output("opponent-name", "children"),
        Input(component_id="opponent-dropdown", component_property="value"),
    )
    def update_opponent(opponent_id: OpponentId) -> Output:
        env.get_wrapper_attr("set_opponent")(opponents[opponent_id])
        return str(env.get_wrapper_attr("opponent"))

    logger.info("Rendering connect four page")
    logger.info(f"n_actions is {n_actions}")
    pil_image = Image.fromarray(env.render())

    header_component = html.H1(
        children=[
            html.Span("Playing "),
            html.Span(f"{env.metadata['name']}", id="game-name"),
            html.Span(" against "),
            html.Span(id="opponent-name"),
        ],
        style={"display": "inline-block"},
    )
    opponent_names = list(opponents.keys())
    game_state_component = html.H2(
        html.Div(
            children=[
                html.Span(HUMAN_TURN, id="turn"),
                html.Div(
                    [
                        html.Span(" playing as "),
                        html.Span(
                            PLAYER_COLORS[env.unwrapped.agent_selection],
                            id="player-color",
                        ),
                    ],
                    id="player-description-div",
                ),
                html.Div(
                    [
                        html.Span(" player "),
                        html.Span("human", id="winner-name"),
                        html.Span(" won!"),
                    ],
                    id="winner-div",
                    hidden=True,
                ),
            ],
            style={"display": "inline-block"},
        ),
    )
    opponent_dropdown = dcc.Dropdown(
        opponent_names,
        opponent_names[0],
        id="opponent-dropdown",
    )
    game_image = html.Img(id="image", src=pil_image, width=500, height=500)
    action_buttons = html.Div(
        [
            html.Button(f"Action {action}", id=f"action-{action}")
            for action in range(n_actions)
        ],
    )
    reset_button = html.Button("Reset", id="reset_button")
    app.layout = html.Div(
        [
            header_component,
            opponent_dropdown,
            game_state_component,
            game_image,
            action_buttons,
            reset_button,
        ],
    )
    return app


if __name__ == "__main__":
    import argparse

    from litrl import make_multiagent
    from litrl.algo.mcts.agent import MCTSAgent
    from litrl.algo.mcts.mcts import MCTSConfig
    from litrl.algo.sac.agent import OnnxSacDeterministicAgent
    from litrl.env.visualisation import get_server

    parser = argparse.ArgumentParser()
    parser.add_argument("--simulations", type=int, default=500)
    args = parser.parse_args()

    opponents = {
        "MCTS": MCTSAgent(
            cfg=MCTSConfig(
                simulations=args.simulations,
                rollout_agent=OnnxSacDeterministicAgent(),
            ),
        ),
        "SAC": OnnxSacDeterministicAgent(),
    }
    env = make_multiagent(
        id="ConnectFour-v3",
        opponent=opponents["MCTS"],
        render_mode="rgb_array",
    )
    env.reset(seed=123)
    app = get_server(env=env, n_actions=7, opponents=opponents)
    app.run(debug=True)
