# Python 3 library and CLI for [SporeStack](https://sporestack.com) [.onion](http://spore64i5sofqlfz5gq2ju4msgzojjwifls7rok2cti624zyq3fcelad.onion)

[Changelog](CHANGELOG.md)

## Requirements

* Python 3.7-3.11 (or maybe newer)

## Installation

* `pip install sporestack` (Run `pip install 'sporestack[cli]'` if you wish to use the CLI features and not just the Python library.)
* Recommended: Create a virtual environment, first, and use it inside there.
* Something else to consider: Installing [rich](https://github.com/Textualize/rich) (`pip install rich`) in the same virtual environment will make `--help`-style output prettier.

## Running without installing

* Make sure `pipx` is installed.
* `pipx run 'sporestack[cli]'`
* Make sure you're on the latest stable version comparing `sporestack version` with git tags in this repository, or releases on [PyPI](https://pypi.org/project/sporestack/).

## Usage

* `sporestack token create --dollars 20 --currency xmr  # Can use btc as well.`
* `sporestack token list`
* `sporestack token info`
* `sporestack server launch --hostname SomeHostname --operating-system debian-11 --days 1  # Will use ~/.ssh/id_rsa.pub as your SSH key, by default`
(You may also want to consider passing `--region` to have a non-random region. This will use the "primary" token by default, which is the default when you run `sporestack token create`.)
* `sporestack server stop --hostname SomeHostname`
* `sporestack server stop --machine-id ss_m_...  # Or use --machine-id to be more pedantic.`
* `sporestack server start --hostname SomeHostname`
* `sporestack server autorenew-enable --hostname SomeHostname`
* `sporestack server autorenew-disable --hostname SomeHostname`
* `sporestack server list`
* `sporestack server delete --hostname SomeHostname`
* `sporestack server remove --hostname SomeHostname # If expired`

## Notes

* If you want to communicate with SporeStack APIs using Tor, set this environment variable: `SPORESTACK_USE_TOR_ENDPOINT=1`

## Developing

* `pipenv install --deploy --dev`
* `pipenv run make test` (If you don't have `make`, use `almake`)
* `pipenv run make format` to format files and apply ruff fixes.

## Licence

[Unlicense/Public domain](LICENSE.txt)
