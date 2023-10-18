import time
import requests
import sett
import json

def obtener_mensaje_wpp(message):
    if 'type' not in message:
        text = 'mensaje no reconocido'
        return text
        
    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']

    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text == message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text == message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no reconocido'
    
    return text


def enviar_mensaje_wpp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type':'application/json',
                    'Authorization':'Bearer ' + whatsapp_token
                }
        response = requests.post(whatsapp_url,
                                  headers=headers, 
                                  data=data
                                )
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'errore al enviar mensaje', response.status_code

    except Exception as e:
        return e,403
    

def text_message(number, text):
    data = json.dumps(
                {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )

    return data


def buttonReply_message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply":{
                    "id":sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data


def listreplay_message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_btn_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps (
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        },
                    ]
                }
            }
        }
    )

    return data


def document_message(number, url, caption, filename):
    data = json.dumps (
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "url": url,
                "caption": caption,
                "filename": filename
            }
        }
    )

    return data


def sticker_message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data



def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "sticker":
        media_id == sett.stickers.get(media_name, None)
    elif media_type == "image":
        media_id = sett.images.get(media_name, None)
    elif media_type == "video":
        media_id == sett.videos.get(media_name, None)
    elif media_type == "audio":
        media_id == sett.audio.get(media_name, None)
    return media_id


def replyreactions_message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji,
            }
        }
    )
    return data



def replytext_message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": {"message_id": messageId},
            "type": "text",
            "reaction": {
                "body": text
            }
        }
    )

    return data


def marread_message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": messageId
        }
    )

    return data


def administrar_chatbot(text, number, messageId, name): 
    text = text.lower() #mensaje que sera enviado al usuario
    list = []

    if "hola" in text:
        body = "Hola! bienvenido a Hossaik, como te puedo ayudar hoy?"
        footer = "Equipo Hossaik"
        options = ["✅ Servicios ", "Agendar cita"]

        replyButtonData = buttonReply_message(number, options, body, footer, "sed1", messageId)
        replyReaction = replyreactions_message(number, messageId, "😎")

        list.append(replyReaction)
        list.append(replyButtonData)

    elif "Servicios" in text:
        body = "Tenemos varias areas de desarrollo a elegir, cuentanos. Cual de estos servicios te gustaria explorar?"
        footer = "Equipo Hossaik"
        options = ["Desarrollo web 👨‍💻 ", "Ciencia de datos 📉", "Venta de droga", "Inteligencia artificial 🤖"]

        listReplyData = listreplay_message(number, options, body, footer, "sed2", messageId)
        sticker = sticker_message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)
    elif "Desarrollo web" in text:
        body = "Maginifica opcion, cuando se trata de Desarrollo web en hossaik nos lo tomamos muy enserio, te gustaria recivir un pdf con detalles de nuestros desarrollos en Desarrollo web?"

        footer = "Equipo Hossaik"
        options = ["Si, enviame el PDF ✔", "No, gracias 🔴"]

        replyButtonData = buttonReply_message(number, options, body, footer, "sed3", messageId)

        list.append(replyButtonData)

    elif "Si, enviame el PDF" in text:
        
        sticker = sticker_message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_message(number, "Genial, por favor espere un momento.")

        enviar_mensaje_wpp(sticker)
        enviar_mensaje_wpp(textMessage)
        time.sleep(3)

        document = document_message(number, sett.document_url, "Listo 👍", "Desarrollo web PDF")
        enviar_mensaje_wpp(document)
        time.sleep(3)

        body = "Te gustaria programar una reunion con uno de nuestros especialistas para discutir estos servicios mas a fondo?"
        footer = "Equipo Hossaik"
        options = ["Por supuesto, agenda una reunion ✔", "No, gracias 🔴"]

        replyButtonData = buttonReply_message(number, options, body, footer, "sed4", messageId)

        list.append(replyButtonData)
        
    elif "Por supuesto, agenda una reunion" in text:
        body = "Estupendo, Por favor, selecciona una fecha y hora para la reunion:"
        footer = "Equipo Hossaik"
        options = ["📅 19 de Octubre, 10 AM","📅 19 de Octubre, 2 PM","📅 19 de Octubre, 4 PM", "📅 20 de Octubre, 10 AM",]

        listReply = listreplay_message(number, options, body, footer, "sed5", messageId)

        list.append(listReply)

    elif "19 de Octubre, 10 AM" in text:
        body = "Magnifico, has seleccionado la reunion para el 19 de octubre a las 10 AM. Te enviare un recordatorio un dia antes. Necesitas ayuda con algo mas hoy?"
        footer = "Equipo Hossaik"
        options = ["✅ Si, por favor", "❌ No, gracias."]

        buttonsReply = buttonReply_message(number, options, body, footer, "sed5", messageId)

        list.append(buttonsReply)

    elif "No, gracias" in text:
        textMessage = textMessage(number, "Perfecto, no dudes en contactarnos si tienes mas preguntas. Recuerda que tambien ofrecemos material gratuito para la comunidad, Hasta luego! 👋")

        list.append(textMessage)
    else:
        data = text_message(number, 'Lo siento, no entendi lo que jisite, Quieres que te ayude con alguna de estas opciones?')
        list.append(data)

    for item in list:
        enviar_mensaje_wpp(item)
