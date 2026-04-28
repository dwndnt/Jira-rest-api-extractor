# ==========================================
# Jira Extractor Configuration Sample
# Copy this file as config.py
# ==========================================

# ==========================================
# JIRA API CONFIGURATION
# ==========================================

# Jira API Base URL
JIRA_URL = "https://jira.yourcompany.com/rest/api/2/search"

# Personal Access Token
JIRA_TOKEN = "your_personal_access_token"

# ==========================================
# AUTHENTICATION HEADER
# ==========================================

HEADERS = {
    "Authorization": f"Bearer {JIRA_TOKEN}",
    "Accept": "application/json"
}

# ==========================================
# FIELD CONFIGURATION
# Replace custom field IDs with your Jira IDs
# ==========================================

FIELDS = [
    # Standard Fields
    "issuetype",
    "created",
    "summary",
    "assignee",
    "status",
    "updated",
    "reporter",
    "issuelinks",

    # Custom Fields
    "customfield_13500",   # L2 Assignee
    "customfield_13700",   # Actual Updated
    "customfield_10800",   # Classification
    "customfield_14600",   # Aging Duration
    "customfield_13200",   # Charge Code
    "customfield_10300"    # Resolved SLA
]

# ==========================================
# JQL QUERY
# ==========================================

JQL = """
project = ABC
ORDER BY created DESC
"""

# ==========================================
# REQUEST PARAMETERS
# ==========================================

PARAMS = {
    "jql": JQL,
    "maxResults": 500,
    "fields": ",".join(FIELDS)
}

# ==========================================
# LOCAL TIMEZONE
# ==========================================

TIMEZONE = "Asia/Jakarta"