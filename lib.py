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
from typing import Dict, List

help_text = """
I did not undestand your message.

Please text me one of:

- help: sends this current help message
- get_bridge: sends one bridge info
"""


def respond(
    text: str, username: str, bridges: List[str], briges_by_username: Dict[str, str]
) -> str:
    if text == "help":
        return help_text
    if text == "get_bridge":
        if len(bridges) == 0:
            return "No bridges available"
        if not username in briges_by_username:
            bridge = choice(bridges)
            briges_by_username[username] = bridge
        return briges_by_username[username]
    else:
        return help_text
