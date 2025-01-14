# WebSocket Data Processing Application

This README explains the functionality and usage of the provided Python script, which processes data streams from Cortex Machina PRO local WebSocket server. The application handles both model (ML) predictions and EEG (Electroencephalography) data streams.

## Prerequisites

Before using this script, ensure the following requirements are met:

### Dependencies
- **Python 3.12**
- Required Python libraries:
  - `websocket-client`
  - `rel`

Install dependencies using pip, pip3 or pipenv

eg:

```bash
pip install websocket-client rel
```

### Additional Setup
The example imports two variables, `app_id` and `subscribe_message`, from a module named `messages`.
For your app:
- `app_id` must be a valid and unique application identifier.
- `subscribe_message` is a properly formatted message for subscribing to desired streams (eeg, ml or eeg and ml).

## How the Script Works

### 1. Establishing WebSocket Connection
The script connects to a WebSocket server using `websocket.WebSocketApp`. The server URL includes the `app_id` as a query parameter.

```python
ws = websocket.WebSocketApp(
    f"ws://0.0.0.0:8080?app_id={app_id}",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)
```

### 2. Callback Functions
The script defines the following callback functions for WebSocket events:

#### `on_open(ws)`
- Triggered when the connection is successfully opened.
- Logs the connection status to the console.

#### `on_message(ws, _msg)`
- Processes incoming WebSocket messages.
- The `_msg` parameter is parsed from JSON and handled based on its content.

#### `on_error(ws, error)`
- Handles errors during the WebSocket connection.
- Logs the error details to the console.

#### `on_close(ws, close_status_code, close_msg)`
- Invoked when the WebSocket connection is closed.
- Logs the closure event to the console.

### 3. Handling Incoming Messages
Incoming messages are JSON-encoded and processed by `on_message(ws, _msg)`. The logic includes:

#### Successful Responses
- **Authentication (`__type`: `AUTH`)**:
  - Sends the subscription message to the WebSocket server when handshake is done.
- **Streams (`__type`: `STREAM`)**:
  - Handles ML and EEG data streams based on the `stream_name` field:

##### ML Data (`stream_name: ml`):
- Iterates through models and predictions.
- Filters predictions where `value == "CONCENTRATION"` and logs concentration data.

##### EEG Data (`stream_name: eeg`):
- Logs `channels_data` and/or `railing` data to the console.

#### Failure Responses
- Logs failure messages to the console.

### 4. Running the Application
The WebSocket connection is started with automatic reconnection and clean termination on keyboard interrupt:

```python
ws.run_forever(
    dispatcher=rel, reconnect=5
)  # Reconnects after 5 seconds if disconnected unexpectedly.
rel.signal(2, rel.abort)  # Allows keyboard interrupt handling.
rel.dispatch()
```

## Usage
1. Ensure the WebSocket server is running and accessible at `ws://0.0.0.0:8080` by launching Cortex Machina PRO at first.
2. Modify the `app_id` and `subscribe_message` in the `messages` module as needed.
3. Run the script:

```bash
python main.py
```

4. Monitor the console output for processed data and connection events.

## Example Output
Sample console output may include:
```plaintext
Opened connection
{'value': 'CONCENTRATION', 'other_data': '...'}
{'channel1': [0.1, 0.2, 0.3], 'channel2': [0.4, 0.5, 0.6]}
### closed ###
```

## Notes
- Ensure proper error handling and validation for production usage.
- Adapt the message processing logic to suit specific data formats or requirements.
