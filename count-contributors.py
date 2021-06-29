import requests
import json

# Add secrets here
fossa_server_url = "https://app.fossa.com/" # Enter "https://app.fossa.com/" if using FOSSA SaaS
fossa_api_key = ""
fossa_org_id = "1" # Enter "1" if using FOSSA on-prem
gh_username = ""
gh_token = "" # Retrieve from https://github.com/settings/tokens (or equivalent link if using GitHub Enterprise)
gh_api_repos_url = "https://api.github.com/repos/" # Enter "https://api.github.com/repos/" if using github.com (SaaS)

# Make API request to the FOSSA projects API to aggregate all projects with a valid GitHub URL
fossa_projects_url = fossa_server_url + "api/projects" + "?organizationId=" + fossa_org_id

payload={}
headers = {
    'Authorization': "Bearer " + fossa_api_key
}

response = requests.request("GET", fossa_projects_url, headers=headers, data=payload)
projects = json.loads(response.text)
project_urls = []

for project in projects:
    # Omit project URLs that are null or empty strings
    if project['url'] != None and project['url'] != '':
        project_url = project['url'].split('/')
        project_url = project_url[-2] + "/" + project_url[-1]
        project_urls.append(project_url)

with open("fossa-project-urls.json", "w") as write_file:
    json.dump(project_urls, write_file)

# Make API request to the GitHub repositories API for contributor data associated with each valid GitHub URL
gh_session = requests.Session()
gh_session.auth = (gh_username, gh_token)

gh_contributors = []

for project_url in project_urls:
    response = gh_session.get(gh_api_repos_url + project_url + "/contributors")
    if response.status_code == 200:
        contributors = json.loads(response.text)
        for contributor in contributors:
            gh_contributors.append(contributor['login'])

gh_contributors = list(set(gh_contributors)) # Dedupe contributors
# print(gh_contributors)
# print(len(gh_contributors))

with open("fossa-contributors.json", "w") as write_file:
    json.dump(gh_contributors, write_file)

with open("fossa-contributor-count.json", "w") as write_file:
    json.dump(len(gh_contributors), write_file)
