class ParsingError(Exception):
    def __init__(self, message: str):
        super.__init__(message)


def parsing(input: str) -> dict:
    lines = input.split("\n")
    tmp_result: dict = {}
    i = 0
    for row in lines:
        if row == "" or row.startswith("#"):
            continue
        else:
            entry = row.split(": ")
            if i == 0 and entry[0] != "nb_drones":
                raise ParsingError(
                    "First line has to be nb_drones: <positive int>")                
            tmp_result[entry[0]] = entry[1]
            i += 1
    result = {
        "start": None,
        "goal": None,
        "hubs": None,
        "connections": None
    }
    for key, value in tmp_result.items():
        if "start" in key:
            result["start"] = value
        if "end" in key:
            