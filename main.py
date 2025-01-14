import websocket
import json
import rel

from messages import app_id, subscribe_message


def on_message(ws, _msg):
    msg = json.loads(_msg)

    if msg["result"]:
        if msg["result"]["success"]:
            for success in msg["result"]["success"]:

                if success["__type"] == "AUTH":
                    ws.send(json.dumps(subscribe_message))

                if success["__type"] == "STREAM":

                    # ML Data coming from (web) model server:
                    if success["stream_name"] == "ml":
                        models = success["models"]
                        for model in models:
                            predicts = model["predicts"]
                            for predict in predicts:
                                value = predict["value"]
                                if value == "CONCENTRATION":
                                    print(predict)
                                    # pass

                    # EEG data coming from (local) desktop app:
                    if success["stream_name"] == "eeg":
                        channels_data = success["channels_data"]
                        railing = success["railing"]
                        # Uncomment the following lines to see the data
                        # print(channels_data)
                        # print(railing)
                        # pass

        if msg["result"]["failure"]:
            for failure in msg["result"]["failure"]:
                print(failure)


def on_error(ws, error):
    print("ERROR", error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        f"ws://0.0.0.0:8080?app_id={app_id}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever(
        dispatcher=rel, reconnect=5
    )  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
