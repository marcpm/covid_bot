from pushover import push_to_ios
from pushtelegram import push_to_telegram

def _compose_message(query):
    _sign = "Up" if query["daily_deaths_delta"] > 0 else "Down"
    message = "*{}*:\n Deaths Today: {} _({} {:.2f}%)_".format(query["date"], int(query["daily_deaths"]), _sign, query["daily_deaths_delta"])
    return message

def push(message, image_path, target="ios"):
    if target.lower() == "ios":
        push_to_ios(message, image_path)

    elif target.lower() == "telegram":
        push_to_telegram(message, image_path)
        
    else:  
        raise TypeError ("Communication target not implemented.")

