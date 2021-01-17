import asyncio
import re
import os
import base64
import telethon
from telethon.tl.types import (MessageMediaPhoto)
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot import bot, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY

@register(outgoing=True, pattern=r'^.hz(:? |$)(.*)?')
async def hazz(hazmat):
    await hazmat.edit("`Bir saniye...`")
    level = hazmat.pattern_match.group(2)
    if hazmat.fwd_from:
        return
    if not hazmat.reply_to_msg_id:
        await hazmat.edit("`WoWoWo Boş bir şeyi dönüştürmemi beklemiyorsun değil mi!`")
        return
    reply_message = await hazmat.get_reply_message()
    if not reply_message.media:
        await hazmat.edit("`Lütfen medya yanıtla (Animasyonlu Sticker olmaz!)...`")
        return
    if reply_message.sender.bot:
        await hazmat.edit("`Lütfen medya yanıtla ( Animasyonlu Sticker olmaz! )`")
        return
    chat = "@hazmat_suit_bot"
    await hazmat.edit("```Lütfen biraz bekle..```")
    message_id_to_reply = hazmat.message.reply_to_msg_id
    msg_reply = None
    async with hazmat.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/hazmat {level}"
                msg_reply = await conv.send_message(
                    m,
                    reply_to=msg.id)
                r = await conv.get_response()
            elif reply_message.gif:
                m = "/hazmat"
                msg_reply = await conv.send_message(
                    m,
                    reply_to=msg.id)
                r = await conv.get_response()
            response = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await hazmat.reply("`Şu botun engelini aç:` @hazmat_suit_bot`...`")
            return
        if response.text.startswith("I can't"):
            await hazmat.edit("`Bu GIF'i dönüştüremedim!`")
            await hazmat.client.delete_messages(
                conv.chat_id,
                [msg.id, response.id, r.id, msg_reply.id])
            return
        else:
            downloaded_file_name = await hazmat.client.download_media(
                response.media,
                TEMP_DOWNLOAD_DIRECTORY
            )
            await hazmat.client.send_file(
                hazmat.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply
            )
            """ - her şey bittikten sonra chati siler - """
            if msg_reply is not None:
                await hazmat.client.delete_messages(
                    conv.chat_id,
                    [msg.id, msg_reply.id, r.id, response.id])
            else:
                await hazmat.client.delete_messages(conv.chat_id,
                                                    [msg.id, response.id])
    await hazmat.delete()
    return os.remove(downloaded_file_name)

    CMD_HELP.update({
    "hazmat":
    "`.hz` or `.hz` [flip, x2, rotate (yön), background (sayı), black]"
    "\nUsage: Yanıtladığınız fotoğraf / çıkartmayı düzenler."
})
