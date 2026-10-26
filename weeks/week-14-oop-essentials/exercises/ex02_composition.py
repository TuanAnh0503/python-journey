"""Exercise 02: compose Bot with a strategy."""

from collections.abc import Callable

Strategy = Callable[[dict[str, int]], str]


class Bot:
    """Choose actions by delegating to a replaceable strategy."""

    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy

    def choose_action(self, state: dict[str, int]) -> str:
        return self.strategy(state)


def move_toward_goal(state: dict[str, int]) -> str:
    """Move one step toward a goal at either end of the course."""
    position = state["position"]
    goal = state["goal"]

    if position < goal:
        return "right"
    if position > goal:
        return "left"
    return "wait"


def defensive(state: dict[str, int]) -> str:
    """Wait when the opponent is nearby; otherwise move toward the goal."""
    opponent = state.get("opponent_position")
    if opponent is not None and abs(opponent - state["position"]) <= 1:
        return "wait"
    return move_toward_goal(state)


def balanced(state: dict[str, int]) -> str:
    """Use a straightforward movement toward the goal."""
    return move_toward_goal(state)


def aggressive(state: dict[str, int]) -> str:
    """Move toward the goal without pausing for a nearby opponent."""
    return move_toward_goal(state)


if __name__ == "__main__":
    state = {"position": 1, "opponent_position": 4, "goal": 4}
    for strategy in (defensive, balanced, aggressive):
        print(Bot(strategy).choose_action(state))

    reverse_state = {"position": 3, "opponent_position": 4, "goal": 0}
    for strategy in (defensive, balanced, aggressive):
        print(Bot(strategy).choose_action(reverse_state))
