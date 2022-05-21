# gettor-bot

If you encounter permission issues while running `debug.py`, run:

```sh
usermod -a -G signald $(whoami)
```

If you encounter

```
ImportError: cannot import name 'Bot' from 'semaphore'
```

while installing requirements, do build semaphore manually instead

```sh
cd path/to/cloned/semaphore
pip install wheel
make build
make install
cd -
pip install -r requirements.txt
```
