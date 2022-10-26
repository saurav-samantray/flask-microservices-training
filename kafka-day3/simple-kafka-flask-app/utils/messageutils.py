import randominfo as ri


def generate_message() -> dict:
    return {
        'first_name': ri.get_first_name(),
        'last_name': ri.get_last_name()
    }