from enum import Enum
from collections import deque
from typing import Set


class Zone(Enum):
    restricted = 2
    blocked = 1000
    normal = 1
    priority = 1


class Drone():
    def __init__(self, id: str, location: tuple[int, int]):
        self.id = id
        self.location = location
        self.visited_hubs = set()
        self.on_the_way = False


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
        self.neighbour_hubs: Set = set()
        self.type: str
        self.meta: str | None = None
        self.path = False
        self.visited = False

    class HubValidationError(Exception):
        def __init__(self, message: str):
            super.__init__(message)

    def validate_input(self) -> None:
        # print(self.input)
        self.type = self.input[0]
        tmp = self.input[1].split()
        print(tmp)
        if len(tmp) == 3:
            self.id, x, y = tmp
        elif len(tmp) >= 4:
            self.id, x, y = tmp[0], tmp[1], tmp[2]
            self.meta = " ".join(tmp[3:])
        else:
            raise ValueError(f"{tmp} is incorrect")
        try:
            self.position = (int(x), int(y))
        except Exception as e:
            raise str(e) + ": position values have to be int"
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
    def __init__(self, connection: tuple[str, str], meta: str | None = None):
        self.connection = connection
        self.linked_members: tuple[Hub | None, Hub | None] = (None, None)
        self.link_cap = 1
        self.meta = meta

    def setup(self, hubs: list[Hub]) -> None:
        # print(self.linked_members)
        one_hub: Hub
        two_hub: Hub
        for hub in hubs:
            if hub.id == self.connection[1]:
                one_hub = hub
            if hub.id == self.connection[0]:
                two_hub = hub
        try:
            self.linked_members = (one_hub, two_hub)
        except Exception as e:
            print(str(e))
            exit(1)
        if self.meta:
            tmp = self.meta.strip("[]")
            tmp = tmp.split("=")
            if len(tmp) > 1 and tmp[0] == "max_link_capacity":
                try:
                    self.link_cap = int(tmp[1])
                except ValueError as e:
                    raise str(e)
            else:
                raise ValueError(f"Provided meta is incorrect: {self.meta}")


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
        # self.visited = False
        # self.rank = as closer to the finish, as higher rank

    # to check !!!
    def validate_connections(self) -> None:
        normalized = sorted([member for member in self.connections])
        if len(normalized) != len(set(normalized)):
            raise Exception("Invalid connections: duplicates found")

    def prepare_4_start(self) -> None:
        for connection in self.connections:
            connection.setup(self.hubs)

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

        # make pathfinding here?
        # print("Path finding here")
        # self.find_valid_path()

        # print()
        # print("<hub: neighbours>")
        # for hub in self.hubs:
        #     print(hub.id, end=": ")
        #     for n in hub.neighbour_hubs:
        #         print(n.id, end=", ")
        #     print()
        # print()
        
    # def __prepare__()
    
    # we need to validate the hubs and connections

    def make_move(self) -> None:
        # loop through hubs starting from the end
            # loop through drons at the hub and check if they can go further
                # if yes
        def move_to_next(hubs_with_drones: list[Hub]):
            # I need to use start from the hubs that are
            # the nearest to the goal
            # sort hubs by their rank - rank has to represent
            # how close they are to the finish
            # sorted by rank and rank is distance from the goal multipliyed by in path(1 or 0)
            for hub in hubs_with_drones:
                # here 
                to_visit = [
                    h for h in hub.neighbour_hubs
                    if len(h.drones) < h.max_drones
                    and hub.path
                    ]
                while len(to_visit) > 0 and len(hub.drones) > 0:
                    next_hub = to_visit.pop()
                    drone = hub.drones.pop()
                    drone.on_the_way = True
                    drone.position = next_hub.position
                    next_hub.drones.append(drone)
                    drone.visited_hubs.add(hub)
                    print(
                        drone.id,
                        " flew to the ",
                        next_hub.id,
                        end=", ")
                    if next_hub.max_drones > len(next_hub.drones):
                        to_visit.append(next_hub)
                    else:
                        break
                hubs_with_drones.remove(hub)
                    
        hubs_with_drones: list[Hub] = []
        for hub in self.hubs:
            if len(hub.drones) > 0 and hub.id != "goal":
                hubs_with_drones.append(hub)
        l = len(hubs_with_drones)
        # print("before move to next")
        move_to_next(hubs_with_drones)

        # How to pick a hub that is closer to the goal?
        # try to go from goal to start?
        # algo?


    def make_graph(self):
        return {hub: hub.neighbour_hubs for hub in self.hubs}

    def find_valid_path(self) -> None:
        # use BFS to find all possible ways to the finish and use them for
        # self.make_move()
        q = deque()
        start = self.start_hub
        visited = [start]
        start.visited = True
        q.append(start)
        path = []
        while q:
            current = q.popleft()
            print("Current", current.id, end=" ")
            for hub in current.neighbour_hubs:
                # here i need to check for the max cap of hub, their zones and link_cap
                if not hub.visited:
                    hub.visited = True
                    visited.append(hub)
                    if hub.id == "goal":
                        hub.path = True
                        q = False
                        break
                    # print("Goes to the queue", hub.id, hub.position, end=", ")
                    q.append(hub)
            # print()
        # print("queue: ", list(q))
        # print(visited)
        # for h in visited:
        #     print(h.id, end=", ")
        