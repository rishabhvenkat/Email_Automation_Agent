import openai
from config import OPENAI_API_KEY
from data_fetchers.google_sheets import search_sheet_for_entity

openai.api_key = OPENAI_API_KEY

def extract_entity_with_openai(text):
    prompt = f"""
You are an assistant that helps extract shipping entity IDs from emails. These IDs can be:
- Container ID (e.g., ABC123, XYZ789)
- Vessel name with number (e.g., MAERSK 148)

Extract the most relevant ID from the following message:
{text}

Return just the ID. If no ID is found, return: NONE
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message["content"].strip()
    return None if result.upper() == "NONE" else result

def generate_reply_with_openai(row):
    prompt = f"""
You are a helpful shipping assistant. Here is the shipping detail:

{row}

Write a friendly and informative email reply to a customer based on this data.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].strip()

def classify_query_domain(text):
    prompt = f"""
You are an AI classifier that reads customer emails and assigns them to one of the following domains:

- Track and Trace
- Vessel Schedule
- Customs
- Invoice
- Other

Here is the email content:
{text}

Only return one of the domain labels from the list above. If unsure, return: Other
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    domain = response.choices[0].message["content"].strip()
    return domain if domain in ["Track and Trace", "Vessel Schedule", "Customs", "Invoice", "Other"] else "Other"