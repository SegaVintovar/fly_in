from pydantic import BaseModel, Field
from fly_in import Hub, Drone, Connection


class ParsingError(Exception):
    def __init__(self, message: str):
        super.__init__(message)


class Parsing(BaseModel):
    @staticmethod
    def parsing(input: str) -> dict:
        '''
        Returns dict with keys "nb_drones", "hubs", "connections"
        '''
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
                tmp_result[f"{i}" + entry[0]] = entry[1]
                i += 1
        print(tmp_result)
        print()
        result = {
            "nb_drones": 0,
            "hubs": [],
            "connections": []
        }
        for key, value in tmp_result.items():
            if "hub" in key:
                result["hubs"].append(value)
            if "connection" in key:
                result["connections"].append(value)
            if "nb_drones" in key:
                try:
                    result["nb_drones"] = int(value)
                except ValueError:
                    raise "Parsing error: nb_drones value has to be int"
        print(result["hubs"])
        print()
        return result

    @staticmethod
    def parse_hubs(data: list[str]) -> list:
        result: list[Hub] = []
        for entry in data:
            id = entry.split(" ")[0]
            positon = (entry.split(" ")[1], entry.split(" ")[2])

        return result

    @staticmethod
    def parse_connections(data: list[str]) -> list:
        ...
