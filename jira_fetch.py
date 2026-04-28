import requests
from datetime import datetime
import pytz

from config import JIRA_URL, HEADERS, PARAMS, TIMEZONE

# ==========================================
# TIMEZONE CONFIGURATION
# ==========================================

LOCAL_TZ = pytz.timezone(TIMEZONE)

# ==========================================
# CUSTOM FIELD CONFIGURATION
# Replace with your actual Jira field IDs
# ==========================================

CF_L2_ASSIGNEE = "customfield_13500"
CF_ACTUAL_UPDATED = "customfield_13700"
CF_CLASSIFICATION = "customfield_10800"
CF_AGING_DURATION = "customfield_14600"
CF_CHARGE_CODE = "customfield_13200"
CF_RESOLVED_SLA = "customfield_10300"

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_user(field):
    """
    Return Jira user's display name.
    """
    if not field:
        return None

    return field.get("displayName")


def get_value(field):
    """
    Return value from Jira custom field.
    Supports dictionary or direct values.
    """
    if isinstance(field, dict):
        return field.get("value") or field.get("name")

    return field


def get_issue_links(links):
    """
    Return linked issue keys.
    """
    if not links:
        return None

    linked_keys = []

    for link in links:
        if "outwardIssue" in link:
            linked_keys.append(link["outwardIssue"]["key"])
        elif "inwardIssue" in link:
            linked_keys.append(link["inwardIssue"]["key"])

    return ", ".join(linked_keys) if linked_keys else None


def get_resolved_time(field):
    """
    Return latest completed SLA cycle.
    """
    try:
        return field["completedCycles"][-1]["stopTime"]["friendly"]
    except Exception:
        return None


def format_datetime(dt_str):
    """
    Convert Jira UTC datetime to local timezone.
    """
    if not dt_str:
        return None

    try:
        dt = datetime.strptime(
            dt_str,
            "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        dt_local = dt.astimezone(LOCAL_TZ)

        return dt_local.strftime("%-m/%-d/%Y %H:%M")

    except Exception:
        return None


def clean_text(value):
    """
    Extract text before '('.

    Example:
    Tableau (CFGAFR-455092) -> Tableau
    """
    if not value:
        return None

    if isinstance(value, str):
        return value.split(" (")[0].strip()

    return value


# ==========================================
# CORE FUNCTION
# ==========================================

def fetch_issues():
    """
    Fetch Jira issues using pagination.
    """
    start_at = 0
    all_rows = []

    while True:
        PARAMS["startAt"] = start_at

        response = requests.get(
            JIRA_URL,
            headers=HEADERS,
            params=PARAMS
        )

        if response.status_code != 200:
            print("Error:", response.status_code)
            print(response.text)
            break

        data = response.json()
        issues = data.get("issues", [])

        if not issues:
            break

        print(
            f"Fetching {len(issues)} issues "
            f"(startAt={start_at})..."
        )

        for issue in issues:
            fields = issue["fields"]

            row = {
                "Issue Type":
                    fields.get("issuetype", {}).get("name"),

                "Key":
                    issue.get("key"),

                "Summary":
                    fields.get("summary"),

                "Created":
                    format_datetime(fields.get("created")),

                "Updated":
                    format_datetime(fields.get("updated")),

                "Actual Updated":
                    format_datetime(
                        get_value(
                            fields.get(CF_ACTUAL_UPDATED)
                        )
                    ),

                "Status":
                    fields.get("status", {}).get("name"),

                "Assignee":
                    get_user(fields.get("assignee")),

                "Reporter":
                    get_user(fields.get("reporter")),

                "L2 Assignee":
                    get_value(
                        fields.get(CF_L2_ASSIGNEE)
                    ),

                "Classification":
                    get_value(
                        fields.get(CF_CLASSIFICATION)
                    ),

                "Assignment Group":
                    get_value(
                        fields.get(CF_CLASSIFICATION)
                    ),

                "Category":
                    get_value(
                        fields.get(CF_CLASSIFICATION)
                    ),

                "Subcategory":
                    clean_text(
                        get_value(
                            fields.get(CF_CLASSIFICATION)
                        )
                    ),

                "Aging Duration (days)":
                    get_value(
                        fields.get(CF_AGING_DURATION)
                    ),

                "Charge Code":
                    clean_text(
                        get_value(
                            fields.get(CF_CHARGE_CODE)
                        )
                    ),

                "Charge Code Description":
                    clean_text(
                        get_value(
                            fields.get(CF_CHARGE_CODE)
                        )
                    ),

                "Charge Code Name":
                    get_value(
                        fields.get(CF_L2_ASSIGNEE)
                    ),

                "Charged Companies":
                    clean_text(
                        get_value(
                            fields.get(CF_CLASSIFICATION)
                        )
                    ),

                "Linked Issues":
                    get_issue_links(
                        fields.get("issuelinks")
                    ),

                "Resolved":
                    get_resolved_time(
                        fields.get(CF_RESOLVED_SLA)
                    )
            }

            all_rows.append(row)

        start_at += len(issues)

    return all_rows


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    rows = fetch_issues()

    print(f"\n✅ Total issues fetched: {len(rows)}")

    if rows:
        print("\nSample row:")
        print(rows[-1])