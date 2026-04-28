# from pydantic import BaseModel, Field
from fly_in import Hub, Drone, Connection


class ParsingError(Exception):
    def __init__(self, message: str):
        super.__init__(message)


# BaseModel ?
class Parsing():
    # @staticmethod
    def parsing(self, input: str) -> dict:
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
                # tmp_result[f"{i} " + entry[0]] = entry[1]
                tmp_result[i] = (entry[0], entry[1])
                i += 1
        result = {
            "nb_drones": 0,
            "hubs": [],
            "connections": []
        }
        for key, value in tmp_result.values():
            if "hub" in key:
                result["hubs"].append((key, value))
                continue
            if "connection" in key:
                result["connections"].append(value)
                continue
            if "nb_drones" in key:
                try:
                    result["nb_drones"] = int(value)
                except ValueError:
                    raise "Parsing error: nb_drones value has to be int"

        tmp = result
        result["hubs"] = self.parse_hubs(tmp["hubs"])
        result["connections"] = self.parse_connections(tmp["connections"])

        return result

    def meta_parser(meta_data_str: str) -> dict:
        ...

    def parse_hubs(self, data: list[str]) -> list:
        result: list[Hub] = []
        for entry in data:
            result.append(Hub((entry)))

        return result

    def parse_connections(self, data: list[tuple[str, str]]) -> list:
        result: list[Connection] = []
        for entry in data:
            # print(entry)
            result.append(Connection(
                (entry.split("-")[0], entry.split("-")[1])))
        return result
