# Jira Batch Task Creator

## Getting Started

## Add your files

```
cd existing_repo
git remote add origin https://github.com/salis21n/automate-create-task-jira.git
git branch -M main
git push -uf origin main
```

---

# Jira Batch Task Creator Documentation

## Description

This Python script creates Jira tasks in bulk based on data from a CSV file. Features include:

- Reads task data from CSV files.
- Dynamically retrieves "Task" issue types for each project.
- Automatically fetches custom field IDs (e.g., Epic Link).
- Retrieves user `accountId` from email with fallback capability.
- Creates tasks with proper payloads including Atlassian Document Format (ADF) descriptions.
- Populates start date (via custom field) and due date.
- Automatically transitions tasks to "Done" status using provided transition ID.

---

## Prerequisites

1. **CSV File Requirements**
   The CSV must contain these minimum columns:
   - `project-key` (e.g., SYS)
   - `title-task` (task title)
   - `desc-task` (task description)
   - `due-date` (due date in `YYYY-MM-DD` format)
   - `epic-code` (epic code if applicable, can be empty)
   - `assign` (assignee's email)

2. **Configuration**
   Update the script's configuration variables to match your Jira instance:
   ```python
   JIRA_URL = "https://your_url_jira.atlassian.net"  # Your Jira URL
   EMAIL = "your_jira_email_here"  # Your Jira login email
   API_TOKEN = "your_jira_api_token_here"  # Your Jira API token
   FALLBACK_ACCOUNT_ID = "your_jira_account_id_here"
   START_DATE_CUSTOM_FIELD = "customfield_xxxxx"  # ID for Start Date custom field
   TRANSITION_ID_DONE = "xxx"  # Transition ID to "Done" status
   ```

---

## Script Workflow

- Groups tasks by `due-date` to process batches per date.
- Each task is created with populated fields: summary, description, assignee, due date, start date, and epic link (if provided).
- Falls back to `FALLBACK_ACCOUNT_ID` if email lookup fails.
- Automatically transitions tasks to "Done" using Jira's API after creation.

---

## Docker Deployment

### Dockerfile

Create a `Dockerfile` with:
```Dockerfile
FROM python:alpine

WORKDIR /jira

COPY . .

RUN pip install pandas requests openpyxl

CMD ["sh", "-c", "python your_script_name.py data.csv"]
```

> **Note:** Replace `your_script_name.py` with your actual Python script filename.

---

### Running the Docker Container

1. **Build the Docker image:**
```sh
docker build -t jira-batch-task-creator .
```

2. **Run the container with CSV file mounted from host:**
```sh
docker run --rm -v /path/to/csv/folder:/app jira-batch-task-creator
```
Replace `/path/to/csv/folder` with your actual CSV file directory path.

---

## Direct Execution (Without Docker)

```bash
python your_script_name.py
```
The script will automatically read `data.csv` from the current directory.

---

## Important Notes

- Ensure your API token has sufficient permissions in Jira.
- Verify email assignments exist in Jira and are accessible via API.
- The `TRANSITION_ID_DONE` must match your project's workflow "Done" transition.
- CSV formatting and column consistency are critical for successful execution.
