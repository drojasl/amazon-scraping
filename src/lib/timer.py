from datetime import datetime

def print_now(message, start_time=None):
    now = datetime.now()
    print(f"{message} " + now.strftime("%Y-%m-%d %H:%M:%S"))

    if start_time:
        elapsed = now - start_time
        days = elapsed.days
        hours, remainder = divmod(elapsed.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        duration_str = f"{days}d {hours}h {minutes}m {seconds}s"
        print(f"Duration: {duration_str}")

    return now
