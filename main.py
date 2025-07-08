from fastapi import FastAPI, BackgroundTasks
from ms_graph_client import fetch_graph_emails, send_graph_email, mark_email_as_read
from ai_agent import extract_entity_with_openai, generate_reply_with_openai, classify_query_domain
from data_fetchers.google_sheets import search_sheet_for_entity
from config import HUMAN_AGENT_EMAIL

app = FastAPI()

config_store = {
    "listen": "",
    "forward": HUMAN_AGENT_EMAIL,
    "allowed_domains": ["Track and Trace", "Vessel Schedule"]
}

automation_stats = {"automated": 0, "forwarded": 0}
query_breakdown = {}

@app.post("/process-emails")
def process_emails(background_tasks: BackgroundTasks):
    background_tasks.add_task(_handle_emails)
    return {"status": "processing"}

@app.post("/config")
def update_config(config: dict):
    config_store["listen"] = config.get("listen", "")
    config_store["forward"] = config.get("forward", HUMAN_AGENT_EMAIL)
    config_store["allowed_domains"] = config.get("allowed_domains", ["Track and Trace", "Vessel Schedule"])
    return {"status": "success"}

@app.get("/dashboard")
def get_dashboard():
    return {
        "totals": automation_stats,
        "query_breakdown": query_breakdown,
        "allowed_domains": config_store["allowed_domains"]
    }

def _handle_emails():
    emails = fetch_graph_emails()

    for mail in emails:
        text = mail["body"]
        domain = classify_query_domain(text)

        if domain not in config_store["allowed_domains"]:
            send_graph_email(config_store["forward"], f"FWD: {mail['subject']}", mail["body"])
            automation_stats["forwarded"] += 1
            query_breakdown[domain] = query_breakdown.get(domain, 0) + 1
            mark_email_as_read(mail["id"])
            continue

        entity_id = extract_entity_with_openai(text)

        if entity_id:
            row = search_sheet_for_entity(entity_id)
            if row:
                reply = generate_reply_with_openai(row)
                send_graph_email(mail["from"], "Re: " + mail["subject"], reply)

                automation_stats["automated"] += 1
                query_breakdown[domain] = query_breakdown.get(domain, 0) + 1

                mark_email_as_read(mail["id"])
                continue

        send_graph_email(config_store["forward"], f"FWD: {mail['subject']}", mail["body"])
        automation_stats["forwarded"] += 1
        query_breakdown[domain] = query_breakdown.get(domain, 0) + 1
        mark_email_as_read(mail["id"])