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

            if issue_type == "sim_not_received":
                say(f"Thanks! We've noted your delivery address:\n*{text}*.\nOur logistics team will verify the shipment for order #{order_number}.", thread_ts=thread_ts)

            elif issue_type == "wrong_plan":
                say(f"Thanks! You expected plan:\n*{text}*.\nWe will check if it matches the activated plan on order #{order_number}.", thread_ts=thread_ts)

            elif issue_type == "activation_delay":
                say(f"Noted! Your order was placed on *{text}*.\nWe'll verify the expected activation time for order #{order_number}.", thread_ts=thread_ts)

            elif issue_type == "porting_issue":
                say(f"Thanks! We'll check porting status from *{text}* for order #{order_number}.", thread_ts=thread_ts)

            elif issue_type == "other":
                say(f"Got it. Our team will review this issue:\n*{text}*\nfor order #{order_number}.", thread_ts=thread_ts)

            else:
                say(f"Thanks! We've noted your message:\n*{text}*.\nWe'll follow up on order #{order_number}.", thread_ts=thread_ts)

            # End conversation
            del user_state[user_id]
        else:
            say("Please provide your order number (e.g., order #12345) to get started.", thread_ts=thread_ts)
    else:
        say("Please provide your order number (e.g., order #12345) to begin.", thread_ts=thread_ts)
