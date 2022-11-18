# Github Insights

Github insights only allows free users to see data from the last couple of days. This script stores the data over a longer period to a local sqlite database

## Installation

Install the packages into a local Pipenv environment with:

```
pipenv install
```

You can then run `pipenv shell` to launch a shell with the correct python libraries installed.

## Configuration

The script reads its configuration from environment variables. This can either be set in the shell with `export`, or written to a `.env` file:

```
GITHUB_ACCESS_TOKEN=<generate an access token that has push access to the repo>
GITHUB_REPO=<for example 'codders/github-insights', or whatever your target repo is>
```

## Usage

From your pipenv shell, simply run:

```
python repo_data.py
```

to fetch the latest data and save it to disk
