from enum import Enum


class Zone(Enum):
    restricted = 2
    blocked = 1000
    normal = 1
    priority = 1


class Drone():
    def __init__(self, id: str, location: tuple[int, int]):
        self.id = id
        self.location = location
        self.visited_hubs = []


class Hub():
    def __init__(self, input: str
                 ):
        self.input = input
        self.id: str | None = None
        self.max_drones: int = 1
        self.color: str | None = None
        self.zone: str | None = None
        self.position: tuple[int, int] = (0, 0)
        self.neighbour_hubs: list = []
        self.type: str
        self.meta: str | None = None
        # self.validate_input()
    
    class HubValidationError(Exception):
        def __init__(self, message: str):
            super.__init__(message)

    def validate_input(self) -> None:
        # print(self.input)
        self.type = self.input[0]
        tmp = self.input[1].split(" ")
        if len(tmp) == 3:
            self.id, x, y = tmp
        elif len(tmp) == 4:
            self.id, x, y, self.meta = tmp
        else:
            raise ValueError(f"{self.input} is incorrect")
        try:
            self.position = (int(x), int(y))
        except Exception as e:
            raise str(e)
        # return self.id + f"{self.position}" + self.meta
    
    def validate_meta(self) -> None:
        if self.meta:
            self.meta = self.meta.strip("[]")
            tmp = self.meta.split(" ")
            for entry in tmp:
                key, value = entry.split("=")
                if key == "max_drones":
                    self.max_drones = int(value)
                elif key == "color":
                    self.color = value
                elif key == "zone":
                    self.zone = value.upper()
                else:
                    raise self.HubValidationError(
                        f"{self.id} recieved invalid metadata{entry}")
            # return (f"max drones: {self.max_drones}, " +
            #         f"color: {self.color}, zone: {self.zone}")


class Connection():
    def __init__(self, connection: tuple[str, str]):
        self.connection = connection
        self.linked_members: tuple[Hub, Hub] | None = None

    def setup(self, hubs: list[Hub]) -> None:
        for hub in hubs:
            if hub.id == self.connection[0]:
                self.linked_members[0] = hub
            if hub.id == self.connection[1]:
                self.linked_members = hub


class Map():
    def __init__(
            self, nb_drones: int, hubs: list[Hub],
            connections: list[Connection]):
        self.nb_drones = nb_drones
        self.hubs = hubs
        self.connections = connections
    
    # to check !!!
    def validate_connections(self) -> None:
        normalized = sorted([member for member in self.connections])
        if len(normalized) != len(set(normalized)):
            raise Exception("Invalid connections: duplicates found")
        
    # def __prepare__()
    
    # we need to validate the hubs and connections

    def make_move(self) -> None:
        # loop through hubs starting from the end
            # loop through drons at the hub and check if they can go further
                # if yes
        ...

    def find_valid_path(self) -> None:
        # use BFS to find all possible ways to the finish and use them for
        # self.make_move()
        ...
