import datetime

import schedule


def _validate_datetime(at_time: str):
    try:
        return datetime.datetime.strptime(at_time, "%H:%M:%S")
    except Exception as e:
        if at_time == "0":
            return at_time
        else:
            raise ValueError(f"Time to run {at_time} should be either in HH:MM:SS or 0")


def _get_weekday(weekday):
    return {
        "monday": schedule.every().monday,
        "tuesday": schedule.every().tuesday,
        "wednesday": schedule.every().wednesday,
        "thursday": schedule.every().thursday,
        "friday": schedule.every().friday,
        "saturday": schedule.every().saturday,
        "sunday": schedule.every().sunday,
    }.get(weekday.lower())


def schedule_new_hourly_task(task, tag, **kwargs):
    schedule.every().hour.do(task, **kwargs).tag(tag)


def schedule_new_daily_task(task, tag, **kwargs):
    schedule.every().day.at(kwargs.get("at_time")).do(task, **kwargs).tag(tag)


def schedule_new_weekly_task(bot, task, weekday: str, at_time: str, tag: str, **kwargs):
    """Schedules previously scheduled events that don't need new new information messaging"""
    scheduled_day = _get_weekday(weekday)
    scheduled_day.at(at_time).do(task, bot, **kwargs).tag(tag)


async def schedule_new_weekly_task_command(bot, ctx, task, source: str, weekday: str, at_time: str, tag: str, **kwargs):
    if _validate_datetime(at_time) == "0":
        task(bot, **kwargs)
        await ctx.send(f"Time for schedule {source} set to execute immediately.")
    else:
        scheduled_day = _get_weekday(weekday)
        scheduled_day.at(at_time).do(task, bot, **kwargs).tag(tag)
        await ctx.send(f"Scheduled {source} every {weekday} at {at_time}.")
