import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()
# ========= CONFIGURASI ==============
JIRA_URL = os.getenv('JIRA_URL')  # URL Jira Anda
EMAIL = os.getenv('EMAIL')  # Email login Jira Anda
API_TOKEN = os.getenv('API_TOKEN')  # API Token Jira Anda
FALLBACK_ACCOUNT_ID = os.getenv('FALLBACK_ACCOUNT_ID')
START_DATE_CUSTOM_FIELD = os.getenv('START_DATE_CUSTOM_FIELD')  # Ganti dengan ID custom field Start Date
TRANSITION_ID_DONE = os.getenv('TRANSITION_ID_DONE')  # Ganti dengan ID transisi ke Done

# Validate required environment variables
for var_name, var_value in [
    ('JIRA_URL', JIRA_URL),
    ('EMAIL', EMAIL),
    ('API_TOKEN', API_TOKEN),
    ('FALLBACK_ACCOUNT_ID', FALLBACK_ACCOUNT_ID),
    ('START_DATE_CUSTOM_FIELD', START_DATE_CUSTOM_FIELD),
    ('TRANSITION_ID_DONE', TRANSITION_ID_DONE)
]:
    if not var_value:
        raise ValueError(f"Missing required environment variable: {var_name}")

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_issue_types(project_key):
    url = f"{JIRA_URL}/rest/api/3/issue/createmeta?projectKeys={project_key}"
    response = requests.get(url, auth=auth, headers=headers)
    if response.status_code == 200:
        projects = response.json().get("projects", [])
        for project in projects:
            if project.get("key") == project_key:
                return project.get("issuetypes", [])
    print(f"Failed fetching issuetypes for project {project_key}: {response.status_code} {response.text}")
    return []

def get_custom_field_id(field_name):
    url = f"{JIRA_URL}/rest/api/3/field"
    response = requests.get(url, auth=auth, headers=headers)
    if response.status_code == 200:
        fields = response.json()
        for f in fields:
            if f['name'].lower() == field_name.lower():
                return f['id']
    print(f"Failed to get custom field {field_name}: {response.status_code} - {response.text}")
    return None

def get_account_id(email):
    url = f"{JIRA_URL}/rest/api/3/user/search?query={email}"
    response = requests.get(url, auth=auth, headers=headers)
    if response.status_code == 200:
        users = response.json()
        if users:
            return users[0].get("accountId")
    print(f"Failed find accountId for email: {email} - {response.status_code} - {response.text}")
    return None

def transition_issue_to_done(issue_key):
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/transitions"
    payload = {
        "transition": {
            "id": TRANSITION_ID_DONE
        }
    }
    response = requests.post(url, json=payload, auth=auth, headers=headers)
    if response.status_code == 204:
        print(f"Transition to Done sukses untuk issue {issue_key}")
    else:
        print(f"Transition to Done gagal untuk issue {issue_key}: {response.status_code} - {response.text}")

def create_jira_task(task_data, epic_link_field_id, issuetype_id):
    project_key = task_data['project-key']
    summary = task_data['title-task']
    description = task_data['desc-task']
    duedate = str(task_data['due-date'])
    epic_code = task_data['epic-code']
    assignee_email = task_data['assign']

    # Ambil assignee accountId dari email
    assignee_account_id = get_account_id(assignee_email)
    if not assignee_account_id:
        # fallback accountId
        assignee_account_id = FALLBACK_ACCOUNT_ID

    # Siapkan payload dengan ADF description
    fields_payload = {
        "project": {"key": project_key},
        "summary": summary,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": description,
                            "type": "text"
                        }
                    ]
                }
            ]
        },
        "issuetype": {"id": issuetype_id},
        "duedate": duedate,
        START_DATE_CUSTOM_FIELD: duedate  # set start date = due date
    }
    # Set assignee jika valid
    if assignee_account_id:
        fields_payload['assignee'] = {"accountId": assignee_account_id}

    if epic_link_field_id and epic_code:
        fields_payload[epic_link_field_id] = epic_code

    payload = {
        "fields": fields_payload
    }

    print(f"Payload untuk task '{summary}':")
    print(payload)

    url = f"{JIRA_URL}/rest/api/3/issue"
    response = requests.post(url, json=payload, auth=auth, headers=headers)
    if response.status_code == 201:
        issue_key = response.json()['key']
        print(f"Berhasil membuat task '{summary}': {issue_key}")

        # Coba transition ke Done
        transition_issue_to_done(issue_key)
    else:
        print(f"Gagal membuat task '{summary}': {response.status_code} - {response.text}")

def main(csv_path):
    # Load CSV
    df = pd.read_csv(csv_path)

    # Ambil issuetype id 'Task' per project, cache biar efisien
    issuetype_cache = {}

    # Ambil custom field id Epic Link
    epic_link_field_id = get_custom_field_id("Epic Link")

    # Kelompokkan task berdasarkan due date
    df_grouped = df.groupby('due-date')

    for due_date, group_df in df_grouped:
        print(f"\n=== Membuat batch tugas untuk due date {due_date} ===")

        for idx, row in group_df.iterrows():
            project_key = row['project-key']
            if project_key not in issuetype_cache:
                issuetypes = get_issue_types(project_key)
                task_issuetype_id = None
                for it in issuetypes:
                    if it['name'].lower() == 'task':
                        task_issuetype_id = it['id']
                        break
                if not task_issuetype_id:
                    print(f"Issue type 'Task' tidak ditemukan di project {project_key}, lewati task ke-{idx+1}")
                    continue
                issuetype_cache[project_key] = task_issuetype_id
            else:
                task_issuetype_id = issuetype_cache[project_key]

            print(f"Membuat task ke-{idx+1}...")
            create_jira_task(row, epic_link_field_id, task_issuetype_id)

if __name__ == '__main__':
    input_file = "data.csv"
    main(input_file)
