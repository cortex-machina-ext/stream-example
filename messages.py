app_id = "grapher-app"  # do not change this

subscribe_message = {
    "method": "SUBSCRIBE_STREAMS",
    "params": {"streams": ["ml", "eeg"], "app_id": app_id},
}
