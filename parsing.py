# from pydantic import BaseModel, Field
from fly_in import Hub, Drone, Connection
import sys


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
            row = row.strip()
            if row == "" or row.startswith("#"):
                continue
            else:
                entry = row.split(": ")
                if i == 0 and entry[0] != "nb_drones":
                    print("First line has to be nb_drones: <positive int>",
                          file=sys.stderr)
                    sys.exit(1)
                # tmp_result[f"{i} " + entry[0]] = entry[1]
                tmp_result[i] = (entry[0], entry[1])
                i += 1
        # print(tmp_result)
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
                # print(value)
                result["connections"].append(value)
                continue
            if "nb_drones" in key:
                try:
                    tmp = int(value)
                    if tmp > 0:
                        result["nb_drones"] = tmp
                    else:
                        raise ValueError("There has to be more then zero drones")
                except ValueError as e:
                    print(str(e))
                    exit(1)

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
        # print(data)
        for entry in data:
            tmp = entry.split()
            name = tmp[0]
            if len(tmp) > 1:
                result.append(Connection(
                    (tmp[0].split("-")[0], tmp[0].split("-")[1]), tmp[1]))
            elif len(tmp) == 1:
                result.append(Connection(
                    (tmp[0].split("-")[0], tmp[0].split("-")[1]), None))
            else:
                raise ValueError(f"Connection entry is invalid: {entry}")
        return result
