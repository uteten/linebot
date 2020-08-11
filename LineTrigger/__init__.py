
import azure.functions as func

import logging
import os
import io
import re
from ..shared_function import DeepL, AzureVision
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (ImageMessage, MessageEvent,
                            TextMessage, TextSendMessage)

# LINE設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


def iterable_to_stream(iterable, buffer_size=io.DEFAULT_BUFFER_SIZE):
    class IterStream(io.RawIOBase):
        def __init__(self):
            self.leftover = None

        def readable(self):
            return True

        def readinto(self, b):
            try:
                ll = len(b)  # We're supposed to return at most this much
                chunk = self.leftover or next(iterable)
                output, self.leftover = chunk[:ll], chunk[ll:]
                b[:len(output)] = output
                return len(output)
            except StopIteration:
                return 0    # indicate EOF
    return io.BufferedReader(IterStream(), buffer_size=buffer_size)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('----------- triger start11 ---------------')
    signature = ""
    if 'X-Line-Signature' in req.headers:
        signature = req.headers['X-Line-Signature']
    body = req.get_body().decode()
    logging.info(["body::",body])
    logging.info(["signature::",signature])

    try:
        handler.handle(body, signature)
        return func.HttpResponse("ok", status_code=200)
    except InvalidSignatureError:
        logging.info("in error")
        return func.HttpResponse("damepox2")


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    logging.info("in text handler")
    logging.info(["en_text::", event.message.text])
    reply=""
    for en_text in event.message.text.split(". "):
        if not re.match(r'(\.|\?)$', en_text):
            en_text+= "."
        jp_text = DeepL.DeepL().translateText(en_text)
        logging.info(["jp_text::", jp_text])
        reply+= "E: " + en_text + "\nJ: " + jp_text + "\n"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    logging.info("in image handler")
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    stream = iterable_to_stream(message_content.iter_content())
    en_text_all = AzureVision.AzureVision().image2text(stream)
    reply=""
    for en_text in en_text_all.split(". "):
        if not re.match(r'(\.|\?)$', en_text):
            en_text+= "."
        
        logging.info(["en_text::", en_text])
        jp_text = DeepL.DeepL().translateText(en_text.replace("\n", " "))
        reply+= "E: " + en_text + "\nJ: " + jp_text + "\n"
        
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))

