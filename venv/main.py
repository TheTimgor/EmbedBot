import json
import discord
import asyncio

startup = True
client = discord.Client()

with open('config.json', 'r') as read_file:
    global config
    config = json.load(read_file)

with open('embeds.json') as f:
    embeds = json.load(f)

class commands:
    @staticmethod
    async def test(params, channel):
        if params:
            await channel.send('hello, {}!'.format(params[1]))
        else:
            await channel.send('hello, world!')
    @staticmethod
    async def support(params, channel):
        for embed_data in embeds:
            fields = embed_data['fields']
            title = embed_data['title']
            image_url = embed_data['image url']
            embed = discord.Embed()
            embed.title = title
            embed.set_image(url=image_url)
            for field_name in fields.keys():
                field_text = fields[field_name]
                embed.add_field(name=field_name,value=field_text,inline=False)
            await channel.send(embed=embed)

    @staticmethod
    async def delay(params, channel):
        if len(params) >= 2:
            delay = 3500 / (int(params[0])/int(params[1]))
            await channel.send('Delay should be at least {}ms'.format(int(delay)))


@client.event
async def on_message(message):
    if message.content.startswith(config['trigger']):
        content = message.content.replace(config['trigger'], '', 1).split(' ')
        command = content[0]
        params = []
        if len(content) > 1:
            params = content[1:]

        await getattr(commands, command)(params, message.channel)


@client.event
async def on_ready():
    global startup
    if startup:
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        print(discord.__version__)

client.run(config['token'])
