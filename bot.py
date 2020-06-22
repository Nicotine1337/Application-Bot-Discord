import discord
from discord.ext import commands
import asyncio
import requests

TOKEN = 'NzIyMTM0OTg0ODM5OTIxNzI1.XueqoQ.2sPu_R6TKXCmn-9B69q2D-DcAO0'
bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    print('Online as %s' % (bot.user.name))

STICKIES = {}
OBJS = {}
APP_IDS = []
@bot.event
async def on_message(message):
    global APP_IDS
    global STICKIES
    global OBJS

    if message.author == bot.user: return

    if message.channel.id in STICKIES.keys():
        await bot.delete_message(OBJS[message.channel.id])
        await bot.send_message(message.channel, STICKIES[message.channel.id])

    if message.content.startswith('-sticky'):
        if message.author.id == '604047460402462726':
            args = message.content.split(' ')
            content = ' '.join(args[1:-1])
            msg = '''
            ⚠️***__Sticky Message, Read Before Typing!__***⚠️\n%s
            ''' % (content)
            chan = args[-1]
            chan = bot.get_channel(chan)
            m1 = await bot.send_message(chan, msg)
            STICKIES[args[-1]] = msg
            OBJS[args[-1]] = m1

    if message.content.lower().startswith('-apply'):
        emojis = ['👮', '🚒', '🗺️']
        embed = discord.Embed(color=0x05B8CC, description='CLRP Application')
        embed.add_field(name='Law Enforcement Officer', value='👮', inline=False)
        embed.add_field(name='Fire Department', value='🚒', inline=False)
        embed.add_field(name='Dispatch', value='🗺️', inline=False)
        msg = await bot.send_message(message.channel, embed=embed)
        for x in emojis:
            await bot.add_reaction(msg, x)
        APP_IDS.append(msg.id)

    myList = ['722135310842069014']
    if message.channel.id in myList:
        await bot.add_reaction(message, '👍')
        await bot.add_reaction(message, '👎')
        
PENDING_APPS = {}
@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user: return

    if reaction.message.id in PENDING_APPS.keys():
        if reaction.emoji == '✅':
            if PENDING_APPS[reaction.message.id].split('|')[-1] == 'leo':            
                for role in reaction.message.server.roles:
                    if role.id == '722135434830020758':
                        user_to_give = reaction.message.server.get_member(PENDING_APPS[reaction.message.id].split('|')[0])
                        await bot.add_roles(user_to_give, role)
                        await bot.send_message(user_to_give, 'You have been accepted as a LEO!')
                        break
            elif PENDING_APPS[reaction.message.id].split('|')[-1] == 'fire department':
                for role in reaction.message.server.roles:
                    if role.id == '722135616204308543':
                        user_to_give = reaction.message.server.get_member(PENDING_APPS[reaction.message.id].split('|')[0])
                        await bot.add_roles(user_to_give, role)
                        await bot.send_message(user_to_give, 'You have been accepted as a Fire Fighter!')
                        break
            elif PENDING_APPS[reaction.message.id].split('|')[-1] == 'dispatch':
                for role in reaction.message.server.roles:
                    if role.id == '722135585174716426':
                        user_to_give = reaction.message.server.get_member(PENDING_APPS[reaction.message.id].split('|')[0])
                        await bot.add_roles(user_to_give, role)
                        await bot.send_message(user_to_give, 'You have been accepted as a Dispatcher!')
                        break
        else:
            msg = 'Your %s application has been declined, better luck next time!' % (PENDING_APPS[reaction.message.id].split('|')[-1])
            user_to_give = reaction.message.server.get_member(PENDING_APPS[reaction.message.id].split('|')[0])
            await bot.send_message(user_to_give, msg)

    if reaction.message.id in APP_IDS:
        if reaction.emoji == '👮':
            try:
                description = '1) What is your email?\n\n2) Birth Date?\n\n3) Why do you wanna be leo?\n\n4) Do you have any experience as leo? If not N/A'
                description += '\n\n5) (Scenario) You get a call from dispatch saying there was a silent alarm at a store. When you get there you find out that the door is tied with 2 socks what do you do next?'
                description += '\n\n6) (Scenario) You pulled someone over for going 65 in a 35. When you walked up to the window you find he is very hot and scared and is moving his hands around a lot what do you do next?'
                description += '\n\n7) What are your best traits in your opinion?\n\n8) What can you bring to our department?'
                embed = discord.Embed(color=0x05B8CC, title='Application for Law Enforcement Officer', description=description)
                try:
                    msg = await bot.send_message(user, embed=embed)
                except:
                    await bot.send_message(reaction.message.channel, 'Please turn on direct messages to apply, {}.'.format(user.mention))
                    return

                resp = await bot.wait_for_message(author=user)
                app = resp.content
                channel = bot.get_channel('722136708484694218')
                embed = discord.Embed(color=0x05B8CC, title='LEO Application from %s#%s' % (user.name, user.discriminator), description=app)
                send_app = await bot.send_message(channel, embed=embed)
                await bot.add_reaction(send_app, '✅')
                await bot.add_reaction(send_app, '❌')
                PENDING_APPS[send_app.id] = user.id + '|' + 'leo'
            except:
                pass

        elif reaction.emoji == '🚒':
            try:
                description = '1) What is your email?\n\n2) Birth Date?\n\n3) Do you have any experience in any emergency services positions IRL?\n\n'
                description += '4) Do you have any previous experience in the fire department?\n\n5) Tell us a bit about yourself.\n\n6) What can you bring to this department?'
                embed = discord.Embed(color=0xFF0000, title='Application for Fire Department', description=description)
                await bot.send_message(user, embed=embed)

                resp = await bot.wait_for_message(author=user)
                app = resp.content
                channel = bot.get_channel('722136688603824138')
                embed = discord.Embed(color=0x05B8CC, title='Fire Department Application from %s#%s' % (user.name, user.discriminator), description=app)
                send_app = await bot.send_message(channel, embed=embed)
                await bot.add_reaction(send_app, '✅')
                await bot.add_reaction(send_app, '❌')
                PENDING_APPS[send_app.id] = user.id + '|' + 'fire department'         
            except:
                await bot.send_message(reaction.message.channel, 'Please turn on direct messages to apply, {}.'.format(user.mention))

        elif reaction.emoji == '🗺️':
            try:
                description = '1) What is your email?\n\n2) Birth Date?\n\n3) Do you have IRL experience in any emergency services department?\n\n'
                description += '4) Do you have any experience in the communications division?\n\n'
                description += '5) Why do you want to be a dispatch operator?\n\n6) Tell us about yourself.\n\n7) What can you bring to this department?'
                embed = discord.Embed(color=0x05B8CC, title='Application for Dispatch', description=description)
                await bot.send_message(user, embed=embed)

                resp = await bot.wait_for_message(author=user)
                app = resp.content
                channel = bot.get_channel('722136662964043827')
                embed = discord.Embed(color=0x05B8CC, title='Dispatch Application from %s#%s' % (user.name, user.discriminator), description=app)
                send_app = await bot.send_message(channel, embed=embed)
                await bot.add_reaction(send_app, '✅')
                await bot.add_reaction(send_app, '❌')
                PENDING_APPS[send_app.id] = user.id + '|' + 'dispatch'

            except:
                await bot.send_message(reaction.message.channel, 'Please turn on direct messages to apply, {}.'.format(user.mention))

bot.run(TOKEN, bot=True)