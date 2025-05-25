import socketio
import argparse
import uuid
import threading
import time

# Setup arguments
parser = argparse.ArgumentParser()
parser.add_argument('--key', required=True, help='Tidio project public key')
parser.add_argument('--visitor_id', required=True, help='Visitor ID')
parser.add_argument('--url', default="http://localhost:8000", help='Tidio project URL (default: http://localhost:8000)')
args = parser.parse_args()

sio = socketio.Client()
connect_event = threading.Event()

@sio.event
def connect():
    print("[+] Connected to Tidio WebSocket")
    sio.emit("visitorRegister", {
        "id": args.visitor_id,
        "originalVisitorId": args.visitor_id,
        "project_public_key": args.key,
        "visitorId": args.visitor_id,
        "url": args.url
    })

@sio.event
def disconnect():
    print("[-] Disconnected from Tidio")


@sio.on('*')
def catch_all(event, *args):
    if event != "connected":
        print(f"[📩 Incoming] {event}: {args}")


@sio.on("operatorIsTyping")
def handle_typing(data):
    print("[🖊️ Operator is typing...]")


@sio.on("newMessage")
def handle_new_message(data):
    try:
        sender_type = data.get("data", {}).get("type")
        message_content = data.get("data", {}).get("message", {}).get("message", "")
        if sender_type == "operator":
            print(f"[🧑‍💼 Operator] {message_content}")
        else:
            print(f"[📨 New Message] {message_content}")
    except Exception as e:
        print(f"[⚠️ Error parsing newMessage] {e}")
        print(f"[📨 Raw message data]: {data}")


def send_messages():
    while True:
        try:
            msg = input("> ")
        except EOFError:
            break
        if not msg.strip():
            continue
        message_id = str(uuid.uuid4())
        sio.emit("visitorNewMessage", {
            "message": msg,
            "messageId": message_id,
            "visitorId": args.visitor_id,
            "projectPublicKey": args.key,
            "url": args.url
        })

def try_connect():
    try:
        sio.connect('https://socket.tidio.co', transports=['websocket'])
        connect_event.set()
    except Exception as e:
        print(f"[❌ Connection error] {e}")


def main():
    print("[*] Connecting to Tidio...")

    thread = threading.Thread(target=try_connect)
    thread.start()
    if not connect_event.wait(timeout=10):  # wait 10 seconds for connection
        print("[❌ Connection timed out after 10 seconds]")
        return

    threading.Thread(target=send_messages, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Exiting and disconnecting...")
        sio.disconnect()

if __name__ == "__main__":
    main()
