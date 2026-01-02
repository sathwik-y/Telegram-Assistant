from context.store import get_chat_context
from classifier.intent import classify_message


def handle_update(event):
    if event["@type"] != "updateNewMessage":
        return

    msg = event["message"]
    if msg["content"]["@type"] != "messageText":
        return

    text = msg["content"]["text"]["text"]
    chat_id = msg["chat_id"]
    message_id = msg["id"]

    context = get_chat_context(chat_id, message_id)

    decision = classify_message(text, context)
    print(decision)
