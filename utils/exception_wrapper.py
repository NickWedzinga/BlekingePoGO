import traceback

import common


def _formatted_error_log(source: str = "unspecified", error_message:str = None):
    """
    Returns a formatted error log containing the function that raised the Exception
    as well as the stacktrace.
    """
    return f"""-------------------------------------------------------------------------------------------
    **Error[{source}]:**
    Additional info: {error_message}\n
    {traceback.format_exc()}-------------------------------------------------------------------------------------------
    """


def catch_with_print(function_to_try, source: str = "unspecified"):
    try:
        function_to_try
    except:
        print(_formatted_error_log(source))


async def catch_with_pm(bot, function_to_try, source: str = "unspecified", error_message: str = None):
    try:
        function_to_try
    except:
        await pm_dev_error(bot, source=source, error_message=error_message)


async def pm_dev_error(bot, error_message: str = None, source="unspecified"):
    for dev in common.DEVELOPERS:
        user = bot.get_user(dev)
        await user.send(_formatted_error_log(source=source, error_message=error_message))
