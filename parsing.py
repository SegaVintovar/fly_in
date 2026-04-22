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
        "nb_drones": 0,
        "hubs": [],
        "connections": []
    }
    for key, value in tmp_result.items():
        if "hub" in key:
            result["hubs"].append(value)
        # if "start" in key:
        #     result["start"] = value
        # if "end" in key:
        #     result["goal"] = value
        if key == "connection":
            result["connections"].append(value)
        if key == "nb_drones":
            try:
                result["nb_drones"] = int(value)
            except ValueError:
                raise "Parsing error: nb_drones value has to be int"
        