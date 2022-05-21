"""
Library part of gettor-bot

It should *not* depend on "services": semaphore, libsignal, redis etc
Instead, use this lib inside files like main.py that use services
This way, this lib
- is pure-python, pure-logic
- works everywhere
- can be easily reused to create bots for other platforms than Signal
- and can be properly unit tested

(* ^ ω ^)
"""

from random import choice
from typing import Callable, List, Union

help_text = """
I did not undestand your message.

Please text me one of:

- help: sends this current help message
- get_bridge: sends one bridge info
"""


def respond(
    text: str,
    username: str,
    bridges: List[str],
    get_bridge: Callable[[str], Union[str, None]],
    set_bridge: Callable[[str, str], None],
) -> str:
    if text == "help":
        return help_text
    if text == "get_bridge":
        if len(bridges) == 0:
            return "No bridges available"
        maybe_bridge = get_bridge(username)
        if maybe_bridge is None:
            new_bridge = choice(bridges)
            set_bridge(username, new_bridge)
            return new_bridge
        else:
            return maybe_bridge
    else:
        return help_text
