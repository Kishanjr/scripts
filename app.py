
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Slack tokens
bot_token = os.getenv("SLACK_BOT_TOKEN")
app_token = os.getenv("SLACK_APP_TOKEN")

# Channel ID to listen to
TARGET_CHANNEL_ID = "C0123456789"  # Replace with your channel ID

# Initialize Slack app
app = App(token=bot_token)

# Event listener for messages
@app.event("message")
def handle_message_events(event, say):
    # Check if the message is from the target channel
    if event.get("channel") == TARGET_CHANNEL_ID:
        user = event.get("user")
        text = event.get("text")
        # Respond to the message
        say(f"Hello, <@{user}>! You said: {text}")

# Start the app with Socket Mode
if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
