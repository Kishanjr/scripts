from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize your app with your bot token (xoxb-...) and Socket Mode app token (xapp-...)
app = App(token="xoxb-your-bot-token")

# 1. Slash Command Handler: /support
# When a user types /support, the bot posts a message with a button.
@app.command("/support")
def handle_support_command(ack, say):
    # Acknowledge the command
    ack()
    # Post a message with a button in the channel where the command was used.
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
                        "action_id": "open_support_form"  # This ID is used to trigger the modal
                    }
                ]
            }
        ]
    )

# 2. Action Handler: Button Click ("open_support_form")
# This handler opens a modal form when the button is clicked.
@app.action("open_support_form")
def handle_open_support_form(ack, body, client):
    # Always acknowledge an action within 3 seconds.
    ack()
    trigger_id = body["trigger_id"]

    # Open the modal with our form.
    client.views_open(
        trigger_id=trigger_id,
        view={
            "type": "modal",
            "callback_id": "support_form_submission",  # Identifier for submission handling
            "title": {"type": "plain_text", "text": "Contact Support"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                # Order Number Input
                {
                    "type": "input",
                    "block_id": "order_block",
                    "label": {"type": "plain_text", "text": "Order Number"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "order_input"
                    }
                },
                # Issue Types Checkboxes
                {
                    "type": "input",
                    "block_id": "issue_block",
                    "label": {"type": "plain_text", "text": "Select the issues you're facing"},
                    "element": {
                        "type": "checkboxes",
                        "action_id": "issue_select",
                        "options": [
                            {
                                "text": {"type": "plain_text", "text": "SIM not received"},
                                "value": "sim_not_received"
                            },
                            {
                                "text": {"type": "plain_text", "text": "Wrong plan"},
                                "value": "wrong_plan"
                            },
                            {
                                "text": {"type": "plain_text", "text": "Activation delay"},
                                "value": "activation_delay"
                            },
                            {
                                "text": {"type": "plain_text", "text": "Porting issue"},
                                "value": "porting_issue"
                            }
                        ]
                    }
                }
            ]
        }
    )

# 3. View Submission Handler: Process the Modal's Data
@app.view("support_form_submission")
def handle_support_form_submission(ack, body, client, view):
    # Acknowledge the view submission
    ack()

    # Extract submitted values from the modal
    user_id = body["user"]["id"]
    order_number = view["state"]["values"]["order_block"]["order_input"]["value"]
    selected_options = view["state"]["values"]["issue_block"]["issue_select"]["selected_options"]
    # Create a simple bullet list of issues
    issues_list = "\n• " + "\n• ".join([option["text"]["text"] for option in selected_options])

    # Post a message in the channel with the submitted information.
    # Replace "C12345678" with your actual channel ID (best for private channels)
    post_response = client.chat_postMessage(
        channel="C12345678",
        text=f":telephone_receiver: New support request from <@{user_id}>",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Order Number:* `{order_number}`\n*Issues Reported:*{issues_list}"
                }
            }
        ]
    )

    # Start a thread on the posted message for further conversation.
    client.chat_postMessage(
        channel=post_response["channel"],
        thread_ts=post_response["ts"],
        text="Thanks for reaching out! Our team will follow up with you here."
    )

# 4. Start your app using Socket Mode
if __name__ == "__main__":
    # Replace "xapp-your-app-level-token" with your actual Socket Mode token.
    handler = SocketModeHandler(app, "xapp-your-app-level-token")
    handler.start()
