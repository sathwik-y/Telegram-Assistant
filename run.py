from telegram.tdlib_client import TDLibClient
from telegram.listener import handle_update

def main():
    client = TDLibClient()
    print("Telegram listener started. Proceeding to auth")
    client.login()
    while True:
        event = client.receive()
        if event:
            handle_update(event)

if __name__ == "__main__":
    main()
