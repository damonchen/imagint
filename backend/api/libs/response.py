def make_response(data=None, status="ok", message=""):
    return {"status": status, "message": message, "data": data}
