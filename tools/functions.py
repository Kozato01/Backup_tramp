import datetime

def gerar_protocolo():
    agora = datetime.datetime.now()
    protocolo = agora.strftime("%Y%m%d%H%M%S")
    return protocolo 


def format_response_for_dialogflow(texts, session_info='', target_flow='', target_page=''):
    messages = []
    for text in texts:
        messages.append(
            {
                "text": {
                    "text": [text],
                    "redactedText": [text]
                },
                "responseType": "HANDLER_PROMPT",
                "source": "VIRTUAL_AGENT"
            }
        )
    response_data = {
        "fulfillment_response": {
            "messages": messages
        }
    }
    if session_info:
        response_data["sessionInfo"] = session_info
    if target_flow:
        response_data["targetFlow"] = target_flow
    if target_page:
        response_data["targetPage"] = target_page
    return response_data