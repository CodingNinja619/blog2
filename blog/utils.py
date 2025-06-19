import uuid
def get_filename(filename, request):
    return uuid.uuid4()

def truncate_string(string : str, symbols : int = 30):
    if len(string) <= symbols:
        return string
    else:
        return string[:symbols] + "..."