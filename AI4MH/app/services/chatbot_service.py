def get_response(text):
    text = text.lower()

    if "sad" in text or "alone" in text:
        return "You are not alone. I'm here with you."

    elif "help" in text:
        return "It's okay to ask for help. You can talk to someone you trust."

    elif "happy" in text:
        return "That's great to hear. Keep going!"

    else:
        return "I'm here to listen. Tell me more."