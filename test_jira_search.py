import os
import urllib.request
import json
import base64

def load_dotenv():
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        env_vars[parts[0]] = parts[1].strip()
    return env_vars

env = load_dotenv()
site = env.get('ATLASSIAN_SITE')
email = env.get('ATLASSIAN_EMAIL')
token = env.get('ATLASSIAN_API_TOKEN')
project = env.get('JIRA_PROJECT_KEY', 'AIMY')

auth_str = f"{email}:{token}"
headers = {
    'Authorization': f'Basic {base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def test_post_v3_enhanced_search():
    url = f"https://{site}/rest/api/3/search/jql"
    payload = {
        "jql": f"project = {project}",
        "maxResults": 5,
        "fields": ["summary", "status", "issuetype"],
        "fieldsByKeys": True
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            issue_count = len(data.get("issues", []))
            print(f"POST v3 enhanced search: SUCCESS! Returned {issue_count} issues.")
            print("  nextPageToken present:", bool(data.get("nextPageToken")))
            print("  isLast:", data.get("isLast"))
            return True
    except Exception as e:
        print("POST v3 enhanced search: FAILED -", str(e))
        return False

print("=== Running Jira Search Endpoint Tests ===")
test_post_v3_enhanced_search()
