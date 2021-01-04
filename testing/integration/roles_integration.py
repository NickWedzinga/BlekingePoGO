import traceback

import discord

from common import constants, tables
from utils.database_connector import execute_statement, create_select_query


async def call_roles_test(bot, ctx):
    try:
        await basic_roles_test(bot, ctx)
        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Roles[Basic test]: Give/Remove/Roles command invocation without error.")
    except Exception as e:
        traceback.print_exc()
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during roles integration-tests: {e}")
        raise ValueError(f"Error during roles integration-tests")


async def basic_roles_test(bot, ctx):
    register_command = bot.get_command("configure register_role")
    await ctx.invoke(register_command, "test_role")
    maybe_registered_role = execute_statement(create_select_query(
        table_name=tables.REGISTERED_ROLES,
        where_key="role_name",
        where_value=f"'test_role'"
    )).all(as_dict=True)
    assert(len(maybe_registered_role) == 1)

    test_role = discord.utils.get(ctx.guild.roles, name="test_role")
    assert(not any(role == test_role for role in ctx.author.roles))

    roles_command = bot.get_command("roles")
    await ctx.invoke(roles_command)

    give_command = bot.get_command("give")
    await ctx.invoke(give_command, "test_role")
    assert(any(role == test_role for role in ctx.author.roles))

    remove_command = bot.get_command("remove")
    await ctx.invoke(remove_command, "test_role")
    assert(not any(role == test_role for role in ctx.author.roles))

    remove_registered_command = bot.get_command("configure unregister_role")
    await ctx.invoke(remove_registered_command, "test_role")
    maybe_registered_role = execute_statement(create_select_query(
        table_name=tables.REGISTERED_ROLES,
        where_key="role_name",
        where_value=f"'test_role'"
    )).all(as_dict=True)
    assert (not maybe_registered_role)


async def run_tests(bot, ctx):
    await call_roles_test(bot, ctx)
