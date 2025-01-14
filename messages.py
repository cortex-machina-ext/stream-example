app_id = "stream-example-app"

subscribe_message = {
    "method": "SUBSCRIBE_STREAMS",
    "params": {
        "streams": [
            "eeg",
            "ml",
        ],
        "app_id": app_id,
    },
}
