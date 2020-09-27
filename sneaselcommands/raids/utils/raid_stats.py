from datetime import datetime

import discord

import common
from utils.database_connector import execute_statement, create_insert_query, create_update_query


def insert_into_stats(ctx, reporter_name: str, reporter_id: int, channel_id: int, pokemon: str, gym: str, hatch_time: str):
    """Inserts a new entry into the stats table for reported raids"""
    team = _find_team(ctx, reporter_id)
    execute_statement(create_insert_query(
        table_name=common.STATS_REPORTED_RAIDS,
        keys="(reporter_name, reporter_id, channel_id, pokemon, gym, hatch_time, team, date)",
        values=f"('{reporter_name}', {reporter_id}, {channel_id}, '{pokemon}', '{gym}', '{hatch_time}', '{team}', '{datetime.today().date()}')"
    ))


def update_pokemon_in_stats(channel_id: int, column: str, new_value: str):
    """Updates the reported Pokémon in the stats for reported raids table"""
    try:
        execute_statement(create_update_query(
            table_name=common.STATS_REPORTED_RAIDS,
            column=column,
            new_value=new_value,
            where_key="channel_id",
            where_value=channel_id
        ))
    except:
        return


def _find_team(ctx, reporter_id: int) -> str:
    """Finds Valor/Mystic/Instinct from a reporter's roles"""
    member = discord.utils.get(ctx.guild.members, id=reporter_id)

    valor = discord.utils.get(ctx.guild.roles, name="valor")
    if valor is not None and valor in member.roles:
        return "valor"

    mystic = discord.utils.get(ctx.guild.roles, name="mystic")
    if mystic is not None and mystic in member.roles:
        return "mystic"

    instinct = discord.utils.get(ctx.guild.roles, name="instinct")
    if instinct is not None and instinct in member.roles:
        return "instinct"

    return "harmony"
