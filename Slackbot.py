from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import re

# Setup app with your bot tokens
app = App(token="xoxb-your-bot-token")
user_state = {}

# Static response dictionary
RESPONSES = {
    "sim_not_received": "Can you please confirm your delivery address?",
    "wrong_plan": "Please share the plan you were expecting.",
    "activation_delay": "When did you place the order? We'll check the timeline.",
    "porting_issue": "Please tell us your current carrier.",
    "other": "Please describe the issue you're facing.",
}

# Step 1: Detect order number and ask for issue type
@app.message(re.compile(r"order\s*#(\d+)", re.IGNORECASE))
def handle_order_message(message, say, context):
    order_number = context['matches'][0]
    user_id = message['user']
    thread_ts = message.get('ts')

    user_state[user_id] = {
        "order_number": order_number,
        "step": "issue_selection",
        "thread_ts": thread_ts
    }

    say(
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": f"What issue are you facing with order *#{order_number}*?"}},
            {
                "type": "actions",
                "elements": [
                    {"type": "button", "text": {"type": "plain_text", "text": "SIM not received"}, "value": "sim_not_received"},
                    {"type": "button", "text": {"type": "plain_text", "text": "Wrong plan"}, "value": "wrong_plan"},
                    {"type": "button", "text": {"type": "plain_text", "text": "Activation delay"}, "value": "activation_delay"},
                    {"type": "button", "text": {"type": "plain_text", "text": "Porting issue"}, "value": "porting_issue"},
                    {"type": "button", "text": {"type": "plain_text", "text": "Other"}, "value": "other"}
                ]
            }
        ],
        text="Please choose your issue.",
        thread_ts=thread_ts
    )

# Step 2: Handle button click and ask follow-up
@app.action(re.compile(r".+"))
def handle_button_click(ack, body, say):
    ack()
    user_id = body['user']['id']
    issue_type = body['actions'][0]['value']
    thread_ts = body['message'].get('thread_ts') or body['message']['ts']

    if user_id in user_state:
        user_state[user_id].update({
            "issue_type": issue_type,
            "step": "awaiting_followup",
            "thread_ts": thread_ts
        })

        followup_question = RESPONSES.get(issue_type, "Please explain the issue.")
        say(followup_question, thread_ts=thread_ts)

# Step 3: Handle user reply to follow-up question
@app.message("")
def handle_followup_message(message, say):
    user_id = message['user']
    text = message['text']
    thread_ts = message.get('thread_ts') or message['ts']

    if user_id in user_state:
        state = user_state[user_id]
        if state.get("step") == "awaiting_followup":
            order_number = state.get("order_number")
            issue_type = state.get("issue_type")

            say(
                f"Thank you! We've recorded your issue: *{issue_type.replace('_', ' ').title()}*\nYour message: *{text}*\nOur team will follow up on order #{order_number}.",
                thread_ts=state["thread_ts"]
            )

            del user_state[user_id]
        else:
            say("Please provide your order number (e.g., order #12345) to get started.", thread_ts=thread_ts)
    else:
        say("Please provide your order number (e.g., order #12345) to begin.", thread_ts=thread_ts)

if __name__ == "__main__":
    SocketModeHandler(app, "xapp-your-app-level-token").start()
