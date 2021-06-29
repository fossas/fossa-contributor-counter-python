# fossa-contributor-counter-python

This script counts active contributors in GitHub.
1. Queries the [FOSSA projects API](https://app.swaggerhub.com/apis-docs/FOSSA1/App) and aggregates the URLs of all the projects that you organization has integrated
2. Queries the [GitHub repositories API](https://docs.github.com/en/rest/reference/repos#list-repository-contributors) and aggregates the data for an accurate contributor count

### Running the script

1. `python -m venv .venv` (make sure to use Python 3 so you may have to run `python3 -m venv .venv` instead)
2. `source ./.venv/bin/activate`
3. `pip install -r requirements.txt`
4. Modify `count-contributors.py` with your secrets
