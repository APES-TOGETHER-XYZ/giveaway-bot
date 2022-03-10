import discord
import json
from discord.ext import commands
import datetime
import time
import random
import asyncio

# These are annoying but fix things
time.sleep(0.5)

with open("config.json") as file:
    info = json.load(file)
    token = info["token"]
    prefix = info["prefix"]
    status = info["status"]
    icon_url = info["icon_url"]

time.sleep(0.5)

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
# We don't want the help command
client.remove_command("help")

time.sleep(0.5)


@client.event
async def on_ready():
    print("[Connected]")
    activity = discord.Game(name=status, type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.command()
@commands.has_permissions(manage_channels=True)
async def giveaway(ctx):
    giveaway_questions = [
        "Which channel will I host the giveaway in?",
        "How long should the giveaway run for (in seconds)?",
        "How many things should I giveaway?",
        "What things should I giveaway?",
    ]
    giveaway_answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for question in giveaway_questions:
        await ctx.send(question)
        try:
            message = await client.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(
                "You didn't answer in time.  Please try again and be sure to send your answer within 30 seconds of the question."
            )
            return
        else:
            giveaway_answers.append(message.content)

    try:
        c_id = int(giveaway_answers[0][2:-1])
    except:
        await ctx.send(
            f"You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}"
        )
        return

    channel = client.get_channel(c_id)
    time = int(giveaway_answers[1])

    await ctx.send(
        f"The {giveaway_answers[3]} giveaway will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} seconds."
    )

    give = discord.Embed(color=0x2ECC71)
    give.set_author(
        name=f"{giveaway_answers[2]} {giveaway_answers[3].upper()} GIVEAWAY TIME!",
        icon_url=icon_url,
    )
    give.add_field(
        name=f"{giveaway_answers[2]} {giveaway_answers[3]} Giveaway!",
        value=f"React with 🐒 to enter!\n Ends in {round(time/60, 2)} minutes!",
        inline=False,
    )
    give.set_footer(text=f"Hosted By {ctx.author.name}")
    my_message = await channel.send("@everyone", embed=give)

    await my_message.add_reaction("🐒")
    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    users = await new_message.reactions[0].users().flatten()
    _num_winners = int(giveaway_answers[2])
    if len(users) < _num_winners:
        _num_winners = len(users)
    if _num_winners == 0:
        return
    winners = random.sample(users, _num_winners)
    winners = list(dict.fromkeys(winners))

    winning_announcement = discord.Embed(color=0xFF2424)
    winning_announcement.set_author(
        name=f"{giveaway_answers[3].upper()} GIVEAWAY HAS ENDED!", icon_url=icon_url
    )
    winner_names = ",".join([winner.mention for winner in winners])
    winning_announcement.add_field(
        name=f"{giveaway_answers[3]} giveaway",
        value=f"🥳 **Winner**: {winner_names}\n 🎫 **Number of Entrants**: {len(users)}",
        inline=False,
    )

    winning_announcement.set_footer(
        text="Thanks for entering! We will bring the winner into a private channel! WE WILL NOT DM YOU."
    )
    await channel.send(embed=winning_announcement)


@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"{ctx} {error}")


time.sleep(0.5)


client.run(token)
