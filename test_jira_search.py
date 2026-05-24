import os
import urllib.request
import urllib.parse
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

# Test 1: GET /rest/api/2/search
def test_get_v2():
    jql = f'project = {project}'
    encoded_jql = urllib.parse.quote(jql)
    url = f"https://{site}/rest/api/2/search?jql={encoded_jql}&maxResults=5"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("GET v2 search: SUCCESS! Found", data.get('total'), "issues.")
            return True
    except Exception as e:
        print("GET v2 search: FAILED -", str(e))
        return False

# Test 2: POST /rest/api/3/search
def test_post_v3():
    url = f"https://{site}/rest/api/3/search"
    payload = {
        "jql": f"project = {project}",
        "maxResults": 5,
        "fields": ["summary", "status", "issuetype"]
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("POST v3 search: SUCCESS! Found", data.get('total'), "issues.")
            return True
    except Exception as e:
        print("POST v3 search: FAILED -", str(e))
        return False

# Test 3: POST /rest/api/2/search
def test_post_v2():
    url = f"https://{site}/rest/api/2/search"
    payload = {
        "jql": f"project = {project}",
        "maxResults": 5,
        "fields": ["summary", "status", "issuetype"]
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("POST v2 search: SUCCESS! Found", data.get('total'), "issues.")
            return True
    except Exception as e:
        print("POST v2 search: FAILED -", str(e))
        return False

print("=== Running Jira Search Endpoint Tests ===")
test_get_v2()
print("-" * 40)
test_post_v3()
print("-" * 40)
test_post_v2()
