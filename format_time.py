import datetime


def format_time(seconds):
    time_obj = datetime.datetime.utcfromtimestamp(seconds)
    formatted_time = time_obj.strftime("%H:%M:%S").lstrip("0").lstrip(":")
    if not formatted_time:
        formatted_time = "0"
    return formatted_time