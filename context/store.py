from telegram.runtime import tdlib_client


def get_chat_context(chat_id, from_message_id, limit=10):
    tdlib_client.send({
        "@type": "getChatHistory",
        "chat_id": chat_id,
        "from_message_id": from_message_id,
        "limit": 50
    })

    messages = []
    while len(messages) < limit:
        event = tdlib_client.receive()
        if event and "messages" in event:
            for m in event["messages"]:
                if m["content"]["@type"] == "messageText":
                    messages.append(m["content"]["text"]["text"])
                if len(messages) == limit:
                    break

    return list(reversed(messages))
