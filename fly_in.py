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
        self.drones: list[Drone] = []
        self.color: str | None = None
        self.zone: str | None = None
        self.position: tuple[int, int] = (0, 0)
        self.neighbour_hubs: set[Hub] = set()
        self.type: str
        self.meta: str | None = None
    
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
        self.linked_members: tuple[Hub | None, Hub | None] = (None, None)

    def setup(self, hubs: list[Hub]) -> None:
        # print(self.linked_members)
        one_hub: Hub
        two_hub: Hub
        for hub in hubs:
            if hub.id == self.connection[1]:
                one_hub = hub
            if hub.id == self.connection[0]:
                two_hub = hub
        self.linked_members = (one_hub, two_hub)


class Map():
    def __init__(
            self, nb_drones: int, hubs: list[Hub],
            connections: list[Connection]):
        self.nb_drones = nb_drones
        self.hubs = hubs
        self.connections = connections
        self.drones: list[Drone] = []
        self.start_hub: Hub
        self.end_hub: Hub
        # self.rank = as closer to the finish, as higher rank

    # to check !!!
    def validate_connections(self) -> None:
        normalized = sorted([member for member in self.connections])
        if len(normalized) != len(set(normalized)):
            raise Exception("Invalid connections: duplicates found")

    def prepare_4_start(self) -> None:

        for c in self.connections:
            a, b = c.linked_members
            a.neighbour_hubs.add(b)
            b.neighbour_hubs.add(a)

        for hub in self.hubs:
            if "start" in hub.id:
                self.start_hub = hub
            if "end" in hub.id or "goal" in hub.id:
                self.end_hub = hub

        i = 0

        while i < self.nb_drones:
            self.start_hub.drones.append(
                Drone(f"D{i + 1}", self.start_hub.position))
            i += 1
        
        for hub in self.hubs:
            print(hub.id, "\n")
            for n in hub.neighbour_hubs:
                print(n.id)
        
    # def __prepare__()
    
    # we need to validate the hubs and connections

    def make_move(self) -> None:
        # loop through hubs starting from the end
            # loop through drons at the hub and check if they can go further
                # if yes
        def move_to_next(hub_with_drones: list[Hub]):
            # I need to use start from the hubs that are
            # the nearest to the goal
            # sort hubs by their rank - rank has to represent
            # how close they are to the finish

            for hub in hubs_with_drones:
                for drone in hub.drones:
                    # here i need to choose neighbours
                    # that are closer to the goal

                    hub.neighbour_hubs
                    next_hub = None
                    drones_can_be_moved = 0
                    for nh in hub.neighbour_hubs:
                        if nh.max_drones > drones_can_be_moved:
                            drones_can_be_moved = nh.max_drones
                            next_hub = nh
                    while len(next_hub.drones) < next_hub.max_drones:
                        next_hub.drones.append(hub.drones.pop(0))
                        print(drone.id, " flew to the ", next_hub.id)


        hubs_with_drones: list[Hub] = []
        for hub in self.hubs:
            if len(hub.drones) > 0:
                hubs_with_drones.append(hub)
        move_to_next(hubs_with_drones)
        # How to pick a hub that is closer to the goal?
        # try to go from goal to start?
        # algo?


    def find_valid_path(self) -> None:
        # use BFS to find all possible ways to the finish and use them for
        # self.make_move()
        ...
