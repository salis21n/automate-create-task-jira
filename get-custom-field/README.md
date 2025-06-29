# Get Jira Custom Fields & Transitions Script

## Description
This Python script retrieves Jira custom field IDs and available transitions for an issue. It helps developers and administrators identify:
- Custom field IDs (e.g., Epic Link, Start Date)
- Transition IDs required for automating issue status changes

---

## Key Features
1. **Custom Field Discovery**  
   Lists all custom fields with:
   - Field ID (`customfield_xxxx`)
   - Field Name (e.g., "Epic Link")
   - Schema Type (e.g., "string", "option")

2. **Transition Analysis**  
   For a specified issue, shows available workflow transitions including:
   - Transition ID
   - Transition Name (e.g., "Resolve Issue")
   - Target Status (e.g., "Done")

---

## Prerequisites
1. **Environment Configuration**  
   - **Environment Variables**: Create a `.env` file in the script's directory with:
     ```env
     JIRA_EMAIL=your_jira_email@example.com
     JIRA_API_TOKEN=your_api_token_here
     ```
   - **Jira URL**: Update the `JIRA_URL` constant in `get-custom-field.py` to your Jira instance URL:
     ```python
     JIRA_URL = "https://your_jira_instance.atlassian.net"  # Replace with your Jira URL
     ```

2. **Python Dependencies**  
   Ensure `python-dotenv` and `requests` are installed.

---

## Usage

### 1. Retrieve Custom Fields
Run the script to get custom fields list:
```bash
python get-custom-field.py
```

Sample output format:
```
Daftar Custom Field ID beserta Nama dan Tipe:
---------------------------------------------------------------------------------------------------
ID                      | Nama Field                      | Tipe Skema                | Notes
---------------------------------------------------------------------------------------------------
customfield_10000       | Epic Link                       | string                    | (Epic reference)
customfield_10001       | Start Date                      | datetime                  | 
...
```

### 2. Check Transitions for Specific Issue
The script checks transitions for `SYS-50` by default. To check another issue:
1. Modify the `issue_to_check` variable in the script
2. Or create a command-line parameter (advanced usage)

---

## Docker Deployment

### Build Container
```bash
docker build -t jira-field-inspector -f Dockerfile .  # Ensure .env is removed before building for security
```

### Run Container
```bash
docker run --rm \
  -e JIRA_EMAIL="your-email@example.com" \
  -e JIRA_API_TOKEN="your_api_token" \
  jira-field-inspector
```
⚠️ **Security Note**: Remove the `.env` file before building the Docker image to avoid exposing credentials in the container.

⚠️ Ensure environment variables are passed correctly when running in Docker.

---

## Important Notes
- **API Permissions**: The Jira account needs "Browse Projects" and "Work Issues" permissions
- **Transition Example**: The script highlights transitions leading to "Done" status
- **Error Handling**: Outputs detailed API errors if authentication fails or endpoints aren't reachable

---

## Example Output
```text
--- Mendapatkan Custom Field IDs ---
Daftar Custom Field ID beserta Nama dan Tipe:
---------------------------------------------------------------------------------------------------
ID                      | Nama Field                      | Tipe Skema                | Notes
---------------------------------------------------------------------------------------------------
customfield_10000       | Epic Link                       | string                    | (Epic reference)
customfield_10001       | Start Date                      | datetime                  | 

--- Mendapatkan Informasi Transisi ---
Transisi yang tersedia untuk isu 'SYS-50':
----------------------------------------------------
ID Transisi      | Nama Transisi          | Status Tujuan    
----------------------------------------------------
1               | To Do                  | To Do            
41              | Done                   | Done             <<< Transition ID to Done
...
