import asyncio
import json
import random
import time
from collections import namedtuple
from functools import partial
from typing import Optional

import discord
from discord import ActivityType
from discord.ext import commands

Giveaway = namedtuple("Giveaway", ["channel", "duration", "count", "item_name"])

with open("config.json") as file:
    info = json.load(file)
    token = info["token"]
    prefix = info["prefix"]
    status = info["status"]
    icon_url = info["icon_url"]
    emoji = info["emoji"]

client = commands.Bot(
    command_prefix=prefix, help_command=None, intents=discord.Intents.all()
)


def _check_context_matches(ctx_a, ctx_b):
    return ctx_a.author == ctx_b.author and ctx_a.channel == ctx_b.channel


async def ask_question(ctx, question: str) -> Optional[str]:
    await ctx.send(question)

    try:
        message = await client.wait_for(
            "message", timeout=30.0, check=partial(_check_context_matches, ctx)
        )
    except asyncio.TimeoutError:
        await ctx.send(
            "You didn't answer in time.  Please try again and be sure to send your answer within 30 seconds of the question."
        )
        return
    return message.content


async def gather_arguments(ctx) -> Optional[Giveaway]:
    giveaway_answers = [
        await ask_question(ctx, question)
        for question in [
            "Which channel will I host the giveaway in?",
            "How long should the giveaway run for (in seconds)?",
            "How many things should I giveaway?",
            "What things should I giveaway?",
        ]
    ]
    channel_id, duration, giveaway_count, giveaway_item = giveaway_answers

    try:
        channel_id = int(channel_id[2:-1])
    except:
        await ctx.send(
            f"You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}"
        )
        return

    return Giveaway(
        duration=int(duration),
        channel=client.get_channel(channel_id),
        count=giveaway_count,
        item_name=giveaway_item,
    )


async def start_giveaway(ctx, args: Giveaway) -> int:
    give = discord.Embed(color=0x2ECC71)
    give.set_author(
        name=f"{args.count} {args.item_name.upper()} GIVEAWAY TIME!",
        icon_url=icon_url,
    )
    give.add_field(
        name=f"{args.count} {args.item_name} Giveaway!",
        value=f"React with {emoji} to enter!\n Ends in {round(args.duration / 60, 2)} minutes!",
        inline=False,
    )
    give.set_footer(text=f"Hosted By {ctx.author.name}")
    my_message = await args.channel.send("@everyone", embed=give)

    await my_message.add_reaction(emoji)

    return my_message.id


async def end_giveaway(message_id: int, args: Giveaway) -> None:
    giveaway_message = await args.channel.fetch_message(message_id)

    users = await giveaway_message.reactions[0].users().flatten()
    users = list(filter(lambda x: not x.bot, users))

    num_winners = min(int(args.count), len(users))

    if not num_winners:
        return

    winners = random.sample(users, num_winners)
    winners = list(dict.fromkeys(winners))

    winning_announcement = discord.Embed(color=0xFF2424)
    winning_announcement.set_author(
        name=f"{args.item_name.upper()} GIVEAWAY HAS ENDED!", icon_url=icon_url
    )
    winner_names = ",".join([winner.mention for winner in winners])
    winning_announcement.add_field(
        name=f"{args.item_name} giveaway",
        value=f"🥳 **Winner**: {winner_names}\n 🎫 **Number of Entrants**: {len(users)}",
        inline=False,
    )

    winning_announcement.set_footer(
        text="Thanks for entering! We will bring the winner into a private channel! WE WILL NOT DM YOU."
    )
    await args.channel.send(embed=winning_announcement)


@client.event
async def on_ready():
    print("[Connected]")
    activity = discord.Game(name=status, type=ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.command()
@commands.has_permissions(manage_channels=True)
async def giveaway(ctx):

    args = await gather_arguments(ctx)
    if not args:
        return

    await ctx.send(
        f"The {args.item_name} giveaway will begin shortly.\nPlease direct your attention to {args.channel.mention}, this giveaway will end in {args.duration} seconds."
    )

    message_id = await start_giveaway(ctx, args)
    await asyncio.sleep(args.duration)
    await end_giveaway(message_id, args)


@client.event
async def on_command_error(ctx, error):
    return


if __name__ == "__main__":
    client.run(token)
