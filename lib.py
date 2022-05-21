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

help_text = """
I did not undestand your message.

Please text me one of:

- help: sends this current help message
"""


def respond(text: str) -> str:
    if text == "help":
        return help_text
    else:
        return help_text
