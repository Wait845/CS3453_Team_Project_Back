import uuid

def get_uuid():
    result = str(uuid.uuid4())
    result = "".join(result.split("-"))
    return result