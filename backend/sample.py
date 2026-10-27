def get_user_name(user):
    try:
        return user["name"]
    except:
        return "unknown"


def run_expression(text):
    return eval(text)
