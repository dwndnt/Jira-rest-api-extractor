# Jira Issue Extractor

**Python Utility for Jira REST API Data Retrieval**

---

## Overview

Jira Issue Extractor is a Python-based utility designed to retrieve issue data from Jira using the Jira REST API.

This script is intended for reporting, analytics, operational monitoring, and historical ticket extraction. It supports both standard Jira fields and custom fields, with built-in pagination and data transformation.

### Primary Use Cases

* Operational reporting
* SLA monitoring
* Ticket aging analysis
* Dashboard data source preparation
* Support team performance reporting
* Historical issue export

---

## Key Features

### Jira API Integration

Connects directly to Jira Search API:

```text
/rest/api/2/search
```

Supports:

* Bearer Token Authentication
* JQL Filtering
* Selective Field Retrieval

---

### Pagination Handling

Jira limits the number of records per request.
This script automatically loops through all available records using:

```text
startAt
maxResults
```

---

### Standard Field Extraction

The script retrieves common Jira fields such as:

* Issue Type
* Issue Key
* Summary
* Status
* Assignee
* Reporter
* Created Date
* Updated Date

---

### Custom Field Extraction

Supports extraction of custom fields such as:

* L2 Assignee
* Actual Updated
* Classification
* Assignment Group
* Aging Duration
* Charge Code
* Resolved SLA

> Replace placeholder custom field IDs with actual IDs from your Jira instance.

---

### Datetime Conversion

Jira stores timestamps in UTC.

This script converts them into:

```text
Asia/Jakarta (WIB)
```

Example:

```text
2026-04-20T08:15:00.000+0000
→ 4/20/2026 15:15
```

---

### Data Cleansing

Some Jira values may contain combined text such as:

```text
Tableau (CFGAFR-455092)
```

The script extracts only the readable business value:

```text
Tableau
```

---

## Technical Stack

| Component           | Technology    |
| ------------------- | ------------- |
| Language            | Python 3.x    |
| HTTP Request        | requests      |
| Datetime Handling   | datetime      |
| Timezone Conversion | pytz          |
| Data Source         | Jira REST API |

---

## Project Structure

```text
jira-extractor/
│── jira_fetch.py
│── README.md
```

---

## Configuration

Update the following values inside the script before execution:

```python
JIRA_URL
HEADERS
FIELDS
PARAMS["jql"]
```

---

## Authentication

Use Personal Access Token:

```python
HEADERS = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Accept": "application/json"
}
```

---

## How to Run

```bash
python jira_fetch.py
```

---

## Sample Output

```text
Fetching 500 issues (startAt=0)...
Fetching 500 issues (startAt=500)...

Total issues fetched: 1000
```

---

# Jira REST API v2 vs v3

## Overview

Jira provides multiple REST API versions.
The two most commonly used versions are:

* REST API v2
* REST API v3

---

## Comparison Summary

| Category                  | API v2                    | API v3                    |
| ------------------------- | ------------------------- | ------------------------- |
| Endpoint                  | `/rest/api/2/`            | `/rest/api/3/`            |
| Stability                 | Mature and widely adopted | Latest version            |
| Jira Cloud                | Supported                 | Recommended               |
| Jira Server / Data Center | Commonly used             | Depends on version        |
| User Model                | Legacy username model     | accountId model           |
| Rich Text Support         | Basic / legacy            | Atlassian Document Format |
| Future Enhancements       | Limited                   | Active development        |

---

## User Identity Changes

### API v2 Response Example

```json
{
  "name": "john.doe",
  "displayName": "John Doe"
}
```

### API v3 Response Example

```json
{
  "accountId": "712020:abcd1234",
  "displayName": "John Doe"
}
```

### Important Note

For Jira Cloud, the following legacy identifiers are deprecated:

* username
* userKey

API v3 uses:

```text
accountId
```

---

## Description / Comment Field Format

### API v2

Typically simpler text representation.

### API v3

Uses Atlassian Document Format (ADF):

```json
{
  "type": "doc",
  "version": 1,
  "content": []
}
```

This requires additional parsing logic for descriptions and comments.

---

## Why This Project Uses API v2

This project currently uses:

```text
/rest/api/2/search
```

Because it offers:

* Strong compatibility with enterprise Jira environments
* Better support for Jira Server / Data Center
* Simpler response structure
* Stable integration for reporting purposes
* Lower migration complexity

---

## When to Use API v3

Consider API v3 when:

* Using Jira Cloud
* Building new integrations
* Requiring latest Atlassian enhancements
* Needing modern identity mapping
* Accessing newer metadata capabilities

---

## Migration Considerations (v2 → v3)

Potential updates required:

* Change endpoint path
* Update user field mapping
* Adjust description/comment parser
* Validate custom field structures
* Review authentication method

---

## Security Best Practice

Avoid hardcoding tokens inside source code.

Recommended approach:

```python
import os

TOKEN = os.getenv("JIRA_TOKEN")
```

---

## Future Enhancements

Planned improvements may include:

* CSV export
* Excel export
* Incremental load by date
* Logging framework
* Config file support
* Retry mechanism
* API v3 version
* Power BI integration

---

## Disclaimer

Custom field IDs vary between Jira environments.

Examples:

```text
customfield_135##
customfield_137##
```

Replace them with actual field IDs from your Jira instance.

---

