# CDP Screenshot Test / Client

This is Python client using [CDP (Chrome DevTools Protocol)](https://chromedevtools.github.io/devtools-protocol/) to create a screenshot from an existing Chromium instances.

Set it up in a [Python virtual environment](https://docs.python.org/3/library/venv.html):

```console
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
```

Run the client:

```console
python cdp-screenshot.py https://<NAME>.<METRO>.kraft.host
```
