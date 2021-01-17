# Coded by t.me/Fusuf #
# Please ask before kang #
# 2020 @AsenaUserBot #

from userbot.events import register
from requests import get, post
from os import remove
from telethon.tl.functions.users import GetFullUserRequest
from time import time

@register(outgoing=True, pattern=r"^.phub ?(.*)")
async def tweet(event):
    if not event.is_reply:
        return await event.edit('**Lütfen bir mesaja yanıt verin!**')
    
    if not event.text:
        return await event.edit('**Lütfen bir mesaja yanıt verin!**')

    await event.edit("`Dıtdıtdun (PornHub Intro)...`")
    reply = await event.get_reply_message()
    foto = await event.client.download_profile_photo(reply.from_id)
    if foto == None:
        return await event.edit("`Bu kişinin profil fotoğrafı yüklemek için yardıma ihtiyacı var!`")
    kullanici = await event.client(
        GetFullUserRequest(
            reply.from_id
        )
    )
    url = post(f'https://uguu.se/upload.php', files={'files[]': (f'{time()}.jpg', open(foto, 'rb'))}).json()
    print(url)
    if kullanici.user.username:
        json = get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={url['files'][0]['url']}&text={reply.message}&username={kullanici.user.username}").json()
    else:
        json = get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={url['files'][0]['url']}&text={reply.message}&username={kullanici.user.first_name}").json()

    await event.client.send_file(event.chat_id, json["message"], caption="[🔥](https://t.me/AsenaUserBot)", reply_to=reply)
    await event.delete()
    remove(foto)
