# Full Slack bot script updated to include:
# - Dialog with order number input
# - Checkboxes for multiple issue types
# - Posts the submitted data as a message
# - Opens a thread on the message

updated_bot_code = """
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize your app with bot token and socket mode handler
app = App(token="xoxb-your-bot-token")

# Command to post "Contact Support" button
@app.command("/post-support-button")
def post_button(ack, say, command):
    ack()
    say(
        text="Need help with your telecom order?",
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*Need help with your telecom order?*"}
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "📞 Contact Support"},
                        "action_id": "open_support_form"
                    }
                ]
            }
        ]
    )

# Action to open modal when button is clicked
@app.action("open_support_form")
def open_form(ack, body, client):
    ack()
    trigger_id = body["trigger_id"]

    client.views_open(
        trigger_id=trigger_id,
        view={
            "type": "modal",
            "callback_id": "support_form_submission",
            "title": {"type": "plain_text", "text": "Contact Support"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "order_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "order_input"
                    },
                    "label": {"type": "plain_text", "text": "Order Number"}
                },
                {
                    "type": "input",
                    "block_id": "issue_block",
                    "element": {
                        "type": "checkboxes",
                        "action_id": "issue_select",
                        "options": [
                            {"text": {"type": "plain_text", "text": "SIM not received"}, "value": "sim"},
                            {"text": {"type": "plain_text", "text": "Wrong plan"}, "value": "plan"},
                            {"text": {"type": "plain_text", "text": "Activation delay"}, "value": "delay"},
                            {"text": {"type": "plain_text", "text": "Porting issue"}, "value": "port"},
                        ]
                    },
                    "label": {"type": "plain_text", "text": "Select the issues you're facing"}
                }
            ]
        }
    )

# Handle modal form submission
@app.view("support_form_submission")
def handle_form_submission(ack, body, client, view):
    ack()
    user = body["user"]["id"]
    order_number = view["state"]["values"]["order_block"]["order_input"]["value"]
    selected_options = view["state"]["values"]["issue_block"]["issue_select"]["selected_options"]
    issue_types = [opt["text"]["text"] for opt in selected_options]
    issue_text = "\\n• " + "\\n• ".join(issue_types)

    # Post message in the channel
    result = client.chat_postMessage(
        channel="#your-private-channel",  # Change this to your actual channel
        text=f":telephone_receiver: New support request from <@{user}>",
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Order Number:* `{order_number}`\\n*Issues Reported:*{issue_text}"}}
        ]
    )

    # Start a thread on the posted message
    client.chat_postMessage(
        channel=result["channel"],
        thread_ts=result["ts"],
        text="Thanks for reaching out! Our team will follow up with you here."
    )

if __name__ == "__main__":
    SocketModeHandler(app, "xapp-your-app-level-token").start()
"""

with open("/mnt/data/contact_support_threaded_bot.py", "w") as f:
    f.write(updated_bot_code)

"/mnt/data/contact_support_threaded_bot.py"
