from enum import Enum
from collections import deque
from typing import Set

global COUNT

class Zone(Enum):
    RESTRICTED = 2
    BLOCKED = 1000
    NORMAL = 1
    PRIORITY = 1


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
        self.zone: str | None = "NORMAL"
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
        self.type = self.input[0]
        tmp = self.input[1].split()
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


class Connection():
    def __init__(self, connection: tuple[str, str], meta: str | None = None):
        self.connection = sorted(connection)
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

    def validate_connections(self) -> None:
        normalized = sorted([member.connection for member in self.connections])
        print(normalized)
        to_compare = set()
        for n in normalized:
            to_compare.add(str(n))
        if len(normalized) != len(to_compare):
            raise Exception("Invalid connections: duplicates found")

    def find_connection(self, hub1: Hub, hub2: Hub) -> Connection:
        for con in self.connections:
            linked_m = con.linked_members
            if linked_m == (hub1, hub2).sort():
                return con

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

        # here Exception could happen. use try block here or on top of this method 
        # current version also do not work
        self.validate_connections()

        # make pathfinding here?
        # self.find_valid_path()
        # make path finding and ranking of the hubs
        for hub in self.hubs:
            print(hub.id, hub.max_drones, hub.path, [h.id for h in hub.neighbour_hubs])
        
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

            while hubs_with_drones:
                hub = hubs_with_drones.pop()
                # here 
                # print(hub.id)
                to_visit = [
                    h for h in hub.neighbour_hubs
                    if len(h.drones) < h.max_drones
                    and h.zone in ["NORMAL", "PRIORITY"]
                    # and len(h.neighbour_hubs) > 1
                    ]
                second_option = [
                    h for h in hub.neighbour_hubs
                    if len(h.drones) < h.max_drones
                    and h.zone == "RESTRICTED"
                ]
                i = 0
                # check link cap here

                while to_visit and hub.drones:
                    next_hub = to_visit.pop()
                    # if self.end_hub in next_hub.neighbour_hubs:
                    # here goes link cap check
                    # if self.find_connection(hub, next_hub) <= i:
                    #     to_visit.remove(next_hub)
                    #     break
                    if len(next_hub.neighbour_hubs) < 2 and next_hub.id != "goal":
                        continue
                    drone = hub.drones.pop()
                    if next_hub not in drone.visited_hubs:
                        drone.visited_hubs.add(next_hub)
                    else:
                        tmp = next_hub
                        next_hub = to_visit.pop()
                        to_visit.append(tmp)
                    drone.position = next_hub.position
                    next_hub.drones.append(drone)
                    drone.visited_hubs.add(hub)
                    i += 1
                    print(
                        drone.id,
                        " flew to the ",
                        next_hub.id,
                        end=", ")
                    if next_hub.max_drones > len(next_hub.drones):
                        to_visit.append(next_hub)
                    else:
                        break

        hubs_with_drones: list[Hub] = []
        for hub in self.hubs:
            if len(hub.drones) > 0 and hub.id != "goal":
                hubs_with_drones.append(hub)
                # print(hub.id)
        # print(len(hubs_with_drones))
        # sort these hubs by the rank
        if len(hubs_with_drones) > 0:
            # print("before move to next")
            move_to_next(hubs_with_drones)
        else:
            print("All drones has arrived to the goal")
            exit(0)
        print()


    def make_graph(self):
        return {hub: hub.neighbour_hubs for hub in self.hubs}

    def find_valid_path(self) -> None:
        # use BFS to find all possible ways to the finish and use them for
        # self.make_move()
        q = deque()
        start = self.start_hub
        visited = {start}
        start.visited = True
        q.append(start)
        path = []
        while q:
            current = q.popleft()
            # s = list(current.neighbour_hubs).sort(key=lambda x: x.max_drones, reverse=True)
            s = sorted(list(current.neighbour_hubs), key=lambda x: x.max_drones, reverse=True)
            # print(s)
            for hub in s:
                # here i need to check for the max cap of hub, their zones and link_cap
                if not hub.visited:
                    hub.visited = True
                    visited.add(hub)
                    if hub.id == "goal":
                        hub.path = True
                        q = False
                        break
                    # print("Goes to the queue", hub.id, hub.position, end=", ")
                    q.append(hub)
        print([h.id for h in visited])
        