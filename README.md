# Session Grabber

![logo](./assets/logo.png)

Test app to create a client session through a login performed in the background
using Pyppeteer and making subsequent calls to an API with it.

## Setup

These are recommended steps, if you don't like them that's ok.

```shell
pyenv install 3.8.7
pyenv virtualenv yoink
pyenv activate yoink
pip install -r requirements.txt
```

## Running

For development purposes there's some extra debug things.

```shell
HEADLESS=false LOG_LEVEL=debug make
```

There will be a site available at http://localhost:8000.

## Contributing

```shell
pip install -r requirements-dev.txt
```

You should have `pre-commit` installed, there are hooks that will format and
update requirements files when committing changes.
