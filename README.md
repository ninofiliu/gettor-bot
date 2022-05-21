# gettor-bot

## Installation

1. Install [signald](https://signald.org/)
2. Start the signald daemon
3. Register or link a phone number to signald
4. Clone this repo, setup the python virtual environment, and install deps
   ```sh
   git clone git@github.com:ninofiliu/gettor-bot
   cd gettor-bot
   python -m venv .env
   source .env/bin/activate
   pip install -r requirements.txt
   ```

If you encounter

```
ImportError: cannot import name 'Bot' from 'semaphore'
```

while installing requirements, build [semaphore](https://github.com/lwesterhof/semaphore) manually instead

```sh
cd path/to/cloned/semaphore
pip install wheel
make build
make install
cd path/to/cloned/gettor-bot
pip install -r requirements.txt
```

# Getting started

Inside the virtual env, run the main script with the phone number you're using with signald

```sh
python ./main.py +330123456789
```

If you encounter permission issues while doing this, add yourself to the signald group and restart your computer:

```sh
usermod -a -G signald $(whoami)
```
