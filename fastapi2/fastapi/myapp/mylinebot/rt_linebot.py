from fastapi import APIRouter, Request, HTTPException
from fastapi.logger import logger
import copy


## import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, FlexSendMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage,
    CarouselTemplate,CarouselColumn,URITemplateAction,TemplateSendMessage
)
from aiolinebot import AioLineBotApi

from imgdetect import mydetect as dt

# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = AioLineBotApi('XF20+5ncWc3EI2Nn3OlnsmE4wddpa/DPMlIXexXwyuiUydsDGF6fz97laNfB0qmXBwZfVjDVS0w9mBD6OUzBLUIElxrZEO0FdQJO7e/y8O6zjv7PQSrWJKF67GlXeLnb7IaqfwGMjFeb4ledGL+wDwdB04t89/1O/w1cDnyilFU=')
# your linebot message API - Channel secret
handler = WebhookHandler('cb8b888eb01153fab0e05c4b65f62f6b')

from .utils import *
print(f'images path:{ipath}')
icnt = imgCounter(ipath)

router = APIRouter()

@router.post("/")
async def linebot01(request: Request):
    # get X-Line-Signature header value
    signature = dict(request.headers)['x-line-signature']

    # get request body as text
    body = await request.body()
    body = body.decode("utf-8")
    logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=404, detail="Item not found")
    return 'OK'


tmpl_tbl = {"type":"bubble","body":{"type":"box","layout":"vertical","contents": []}}
tmpl_row = {"type":"box","layout":"horizontal","contents":[]}
tmpl_col = {"type":"box","layout":"vertical","contents":[]}
tmpl_itm = {"type":"box","layout":"vertical","contents":[]}
tmpl_txt = {"type":"text","flex":0,"wrap":True,"margin":"2px", "text": ""}

def mk_item(text, flex=None):
    oText = tmpl_txt.copy()
    oText['text'] = text
    oItem = copy.deepcopy(tmpl_itm)
    oItem['contents'] = [oText]
    if flex:
        oItem['flex'] = flex
    return oItem

def mk_items(tmpl, ilist, flex=None):
    oItms = copy.deepcopy(tmpl)
    if flex:
        oItms['contents'] = [ mk_item(i, flex=flex[k]) for k,i in enumerate(ilist) ]
    else:
        oItms['contents'] = [ mk_item(i) for i in ilist ]
    return oItms

def mk_group(tmpl, ilist, flex=None):
    oGrp = copy.deepcopy(tmpl)
    oGrp['contents'] = ilist
    if flex:
        oGrp['flex'] = flex
    return oGrp


# handle linebot message
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event): # ???????????????????????????
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='????????????'))
    image_content = line_bot_api.get_message_content(event.message.id)
    image_path = icnt.getName(3, image_content.content_type)

    with open(image_path, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)
    retList = dt.aiPredict(image_path)

    oTbl = copy.deepcopy(tmpl_tbl)
    for row in retList:
        item1 = mk_item(row[0], flex=1)
        item2 = mk_group(tmpl_col, [
            mk_items(tmpl_row, row[1:4], [4,4,3]), 
            mk_items(tmpl_row, row[4:7], [4,4,3])], flex=4)
        oTbl['body']['contents'].append(mk_group(tmpl_row, [item1, item2]))

    line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text='????????????', contents=oTbl) )
    return

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    #button 1
    text = event.message.text
    if text == "???????????????":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="???????????????????????????")
            )
    #button 2
    elif text == "????????????":
        reply_cols = [
        CarouselColumn(
            thumbnail_image_url='https://tokyo-kitchen.icook.network/uploads/recipe/cover/231185/6054dd528fc38777.jpg',
            title='???????????????????????????',
            text='???????????????',
            actions=[
                URITemplateAction(label='?????????????????? ???????????????????????????', uri='https://icook.tw/recipes/231185'),
                URITemplateAction(label='?????????????????????????????????????????????', uri='https://icook.tw/recipes/252050'),
                URITemplateAction(label='??????????????????????????????', uri='https://icook.tw/recipes/226424')
            ]),
        CarouselColumn(
            thumbnail_image_url='https://tokyo-kitchen.icook.network/uploads/recipe/cover/97426/eff6b0db072efdf7.jpg',
            title='???????????????????????????',
            text='???????????????',
            actions=[
                URITemplateAction(label='?????????????????????????????????', uri='https://icook.tw/recipes/97426'),
                URITemplateAction(label='??????????????????????????????', uri='https://icook.tw/recipes/133527'),
                URITemplateAction(label='?????????????????????', uri='https://icook.tw/recipes/83221')
            ]),
        CarouselColumn(
            thumbnail_image_url='https://tokyo-kitchen.icook.network/uploads/recipe/cover/215588/afa1dd2d3737ddcd.jpg',
            title='???????????????????????????',
            text='???????????????',
            actions=[
                URITemplateAction(label='?????????????????????', uri='https://icook.tw/recipes/215588'),
                URITemplateAction(label='???????????????~????????????', uri='https://icook.tw/recipes/124418'),
                URITemplateAction(label='???????????????', uri='https://icook.tw/recipes/113707')
            ])
        ]

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="food_recommend",
                template=CarouselTemplate(columns=reply_cols)
            )
        )
