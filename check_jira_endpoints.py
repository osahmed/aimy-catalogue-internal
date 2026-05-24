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

auth_str = f"{email}:{token}"
headers = {
    'Authorization': f'Basic {base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")}',
    'Accept': 'application/json'
}

def check_endpoint(path):
    url = f"https://{site}{path}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"Endpoint {path}: SUCCESS!")
            if isinstance(data, list):
                print(f"  Returned list of size {len(data)}")
                if len(data) > 0:
                    print("  First item:", data[0])
            else:
                print(f"  Keys returned: {list(data.keys())}")
    except Exception as e:
        print(f"Endpoint {path}: FAILED - {e}")

print("=== Checking Jira endpoints ===")
check_endpoint("/rest/api/3/project")
check_endpoint("/rest/api/2/project")
check_endpoint("/rest/api/3/myself")
