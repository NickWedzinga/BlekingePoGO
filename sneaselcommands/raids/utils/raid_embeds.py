from datetime import datetime, timedelta

from utils.channel_wrapper import find_first_embed_in_channel
from utils.time_wrapper import valid_time_hhmm, format_as_hhmm


async def update_time_in_embed(**kwargs):
    """Finds the embed to update and edits it"""
    embed_message = await find_first_embed_in_channel(kwargs.get("bot"), kwargs.get("channel"), "Raid/_edit_embed")
    if embed_message is None:
        return
    else:
        embed = embed_message.embeds[0]
        if "Hatch" in embed.description:
            old_split_embed = embed.description.split("Hatch time: ")
        else:
            old_split_embed = embed.description.split("Despawn time: ")
        old_description = old_split_embed[0]
        database_at_time = valid_time_hhmm(kwargs.get("at_time"))

        # if new time is in future, description -> Hatch time
        if database_at_time.time() > (datetime.now() + timedelta(minutes=1)).time():
            updated_hatch_time = format_as_hhmm(database_at_time)
            embed.description = f"{old_description}Hatch time: {updated_hatch_time}"
        # if new time is in past or now, description -> Despawn time
        else:
            despawn_time = format_as_hhmm(database_at_time + timedelta(minutes=45))
            embed.description = f"{old_description}Despawn time: {despawn_time}"

    await embed_message.edit(embed=embed)
    return embed
