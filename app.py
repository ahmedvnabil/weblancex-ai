import logging
import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

logger = logging.getLogger(__name__)


def _notify_slack(name: str, email: str, message: str, budget: str) -> None:
    """Post a contact form submission to the configured Slack webhook.

    Raises requests.RequestException on failure so the caller can log and
    continue without breaking the user flow.
    """
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
    if not webhook_url:
        logger.warning("SLACK_WEBHOOK_URL not set — skipping Slack notification")
        return

    budget_label = budget if budget else "not specified"
    payload = {
        "text": (
            f":envelope: *New contact form submission*\n"
            f"*Name:* {name}\n"
            f"*Email:* {email}\n"
            f"*Budget:* {budget_label}\n"
            f"*Message:*\n{message}"
        )
    }
    response = requests.post(webhook_url, json=payload, timeout=5)
    response.raise_for_status()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    """HTMX partial — handles contact form submission, returns success fragment."""
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    budget = request.form.get("budget", "").strip()

    # Server-side validation
    if not name or not email or not message:
        return (
            render_template("partials/contact_error.html", error="Name, email, and message are required."),
            422,
        )

    logger.info("[contact] %s <%s> | budget=%s | msg=%.80s", name, email, budget, message)

    try:
        _notify_slack(name, email, message, budget)
    except Exception as exc:
        # Never break the user flow — just log and continue
        logger.error("[contact] Slack notification failed: %s", exc)

    return render_template(
        "partials/contact_success.html",
        name=name,
        email=email,
    )


@app.route("/partials/example", methods=["GET"])
def partial_example():
    """HTMX partial — returns an HTML fragment, not a full page."""
    from datetime import datetime, timezone

    return render_template("partials/example.html", now=datetime.now(timezone.utc).strftime("%H:%M:%S UTC"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
