import requests
from ms_graph_auth import get_graph_token

def fetch_graph_emails(user_id="me", max_messages=10):
    token = get_graph_token()
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/inbox/messages?$top={max_messages}&$filter=isRead eq false"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        messages = response.json().get("value", [])
        parsed = []
        for msg in messages:
            parsed.append({
                "id": msg["id"],
                "from": msg["from"]["emailAddress"]["address"],
                "subject": msg["subject"],
                "body": msg["body"]["content"],
                "contentType": msg["body"]["contentType"]
            })
        return parsed
    else:
        raise Exception(f"Graph API fetch failed: {response.status_code} - {response.text}")

def send_graph_email(to, subject, body, from_user="me"):
    token = get_graph_token()
    url = f"https://graph.microsoft.com/v1.0/users/{from_user}/sendMail"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [{"emailAddress": {"address": to}}]
        }
    }

    response = requests.post(url, headers=headers, json=message)
    if response.status_code != 202:
        raise Exception(f"Send failed: {response.status_code} - {response.text}")

def mark_email_as_read(message_id, user_id="me"):
    token = get_graph_token()
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"isRead": True}
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to mark email as read: {response.status_code} - {response.text}")