from ubot import ldr

CAT_URL = 'http://api.thecatapi.com/v1/images/search'
DOG_URL = 'http://api.thedogapi.com/v1/images/search'
SHIBE_URL = 'http://shibe.online/api/shibes'
BIRD_URL = 'http://shibe.online/api/birds'
CAT_API_KEY = 'e5a56813-be40-481c-9c8a-a6585c37c1fe'
DOG_API_KEY = '105555df-5c50-40fe-bd59-d15a17ce1c2e'
CAT_HEADERS = {"x-api-key": CAT_API_KEY}
DOG_HEADERS = {"x-api-key": DOG_API_KEY}
IMGPARAM = {"mime_types": "jpg,png"}
GIFPARAM = {"mime_types": "gif"}
MIMGPARAM = {"mime_types": "jpg,png", "limit": 6}


async def neko_atsume(params):
    async with ldr.aioclient.get(CAT_URL, params=params, headers=CAT_HEADERS) as response:
        if response.status == 200:
            neko = await response.json()
        else:
            neko = response.status

    return neko


async def inu_atsume(params):
    async with ldr.aioclient.get(DOG_URL, params=params, headers=DOG_HEADERS) as response:
        if response.status == 200:
            inu = await response.json()
        else:
            inu = response.status

    return inu


async def shibe_inu_atsume():
    async with ldr.aioclient.get(SHIBE_URL, params=None, headers=None) as response:
        if response.status == 200:
            shibe_inu = await response.json()
        else:
            shibe_inu = response.status

    return shibe_inu


async def tori_atsume():
    async with ldr.aioclient.get(BIRD_URL, params=None, headers=None) as response:
        if response.status == 200:
            tori = await response.json()
        else:
            tori = response.status

    return tori


@ldr.add("shibe", help="Fetches an image of a shibe.")
async def shibe(event):
    shibe_inu = await shibe_inu_atsume()

    if isinstance(shibe_inu, int):
        await event.reply(f"There was an error finding the shibes! :( -> {shibe_inu}")
        return

    await event.reply(file=shibe_inu[0])


@ldr.add("bird", help="Fetches an image of a bird.")
async def bird(event):
    tori = await tori_atsume()

    if isinstance(tori, int):
        await event.reply(f"There was an error finding the birdies! :( -> {tori}")
        return

    await event.reply(file=tori[0])


@ldr.add_list(["cat", "pussy"], pattern_extra="(gif|)(f|)", help="Fetches an image of a cat.")
async def cat(event):
    neko = await neko_atsume(GIFPARAM if event.other_args[0] else IMGPARAM)

    if isinstance(neko, int):
        await event.reply(f"There was an error finding the cats! :( -> {neko}")
        return

    await event.reply(file=neko[0]["url"], force_document=bool(event.other_args[1]))


@ldr.add_list(["dog", "bitch"], pattern_extra="(gif|)(f|)", help="Fetches an image of a dog.")
async def dog(event):
    inu = await inu_atsume(GIFPARAM if event.other_args[0] else IMGPARAM)

    if isinstance(inu, int):
        await event.reply(f"There was an error finding the dogs! :( -> {inu}")
        return

    await event.reply(file=inu[0]["url"], force_document=bool(event.other_args[1]))


@ldr.add_inline_photo("cat", default="cat")
async def cat_inline(_):
    return [neko["url"] for neko in await neko_atsume(MIMGPARAM)]


@ldr.add_inline_photo("dog", default="dog")
async def dog_inline(_):
    return [inu["url"] for inu in await inu_atsume(MIMGPARAM)]
