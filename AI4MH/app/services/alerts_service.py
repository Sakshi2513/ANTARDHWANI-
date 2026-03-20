def trigger_alert(level, text):
    if level == "High":
        print(f"ALERT: High risk detected -> {text}")