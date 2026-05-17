# from enum import Enum
from drone import Drone
# from collections import deque
from typing import Set  # TYPE_CHECKING
import sys
# class Zone(Enum):
#     RESTRICTED = 2
#     BLOCKED = 1000
#     NORMAL = 1
#     PRIORITY = 1


class HubValidationError(Exception):
    """
    Execption to separate general exceptions from Hub validation errors
    """
    def __init__(self, message: str):
        self.message = message


class Hub():
    """
    Represent a map hub with capacity, zone, color, and neighbor links.

    A hub is parsed from one hub definition line and then validated in two
    stages: core fields with validate_input and optional metadata with
    validate_meta.
    """
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
        self.rank = 0
        self.waiting_drones: list[tuple[Drone, Hub]] = []

    def validate_input(self) -> None:
        self.type = self.input[0]
        tmp = self.input[1].split()
        if len(tmp) == 3:
            self.id, x, y = tmp
        elif len(tmp) >= 4:
            self.id, x, y = tmp[0], tmp[1], tmp[2]
            self.meta = " ".join(tmp[3:])
        else:
            print(f"{tmp} is incorrect", file=sys.stderr)
            sys.exit(1)
        try:
            self.position = (int(x), int(y))
        except Exception as e:
            print(str(e), ": position values have to be int",
                  file=sys.stderr)
            sys.exit(1)

    def validate_meta(self) -> None:
        if self.meta:
            if not self.meta.startswith("[") or not self.meta.endswith("]"):
                print(f"{self.meta} is missing [ or ] brckets",
                      file=sys.stderr)
                exit(1)
            self.meta = self.meta.strip("[]")
            tmp = self.meta.split(" ")
            try:
                for entry in tmp:
                    kw = entry.split("=")
                    if len(kw) != 2:
                        raise HubValidationError(
                            f"{entry} in {tmp} is invalid")
                    else:
                        key, value = kw
                    if key == "max_drones":
                        # it has to be positive number
                        try:
                            tmp = int(value)
                            if tmp < 0:
                                raise HubValidationError(
                                    "max_drones has to be positive int"
                                )
                            else:
                                self.max_drones = tmp
                        except ValueError as e:
                            print(str(e), file=sys.stderr)
                            exit(1)
                        except HubValidationError as e:
                            print(str(e), file=sys.stderr)
                            exit(1)
                    elif key == "color":
                        c = value.strip().upper()
                        if c in [
                                "BLACK", "RED",
                                "GREEN", "YELLOW",
                                "BLUE", "MAGENTA",
                                "CYAN", "WHITE",
                                "PURPLE", "BROWN",
                                'ORANGE', "MAROON",
                                "GOLD", "DARKRED",
                                "VIOLET", "CRIMSON",
                                "LIME", "RAINBOW"
                                ]:
                            self.color = c
                        else:
                            raise HubValidationError(
                                f"Unknown color {value}"
                            )
                    elif key == "zone":
                        z = value.upper()
                        if z in [
                                "NORMAL", "BLOCKED", "PRIORITY", "RESTRICTED"]:
                            self.zone = value.upper()
                        else:
                            raise HubValidationError(
                                "Invalid zone"
                            )
                    else:
                        raise HubValidationError(
                            f"{self.id} recieved invalid metadata{entry}")
            except HubValidationError as e:
                print(str(e))
                exit(1)
            except Exception as e:
                print(str(e))
                exit(1)


class Connection():
    def __init__(self, connection: tuple[str, str], meta: str | None = None):
        self.connection = sorted(connection)
        self.linked_members: tuple[Hub | None, Hub | None] = (None, None)
        self.link_cap = 1
        self.meta = meta

    def setup(self, hubs: list[Hub]) -> None:
        # print(self.linked_members)
        one_hub: Hub | None = None
        two_hub: Hub | None = None
        # what if there is no hub?
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
                    if self.link_cap < 0:
                        raise ValueError("max_link_cap has to be positive int")
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
        self.all_pathes: list[tuple[list[Hub], int]]

    def validate_connections(self) -> None:
        normalized = sorted([member.connection for member in self.connections])
        # print(normalized)
        to_compare = set()
        for n in normalized:
            to_compare.add(str(n))
        if len(normalized) != len(to_compare):
            raise Exception("Invalid connections: duplicates found")

    def find_connection(self, hub1: Hub, hub2: Hub) -> Connection:
        # print("find connection")
        to_find = sorted((hub1.id, hub2.id), reverse=True)
        for con in self.connections:

            linked_m = sorted(con.connection, reverse=True)
            # print(linked_m, con.linked_members)

            # print([m for m in linked_m], len(linked_m), " and ",
            #       [l for l in to_find], len(to_find))
            if linked_m == to_find:
                return con

    # only cheapest path taken into account
    def rank_hubs(self) -> None:
        _, min_cost = min(self.all_pathes, key=lambda x: x[1])
        cheapest_pathes = []
        for path, cost in self.all_pathes:
            if cost == min_cost:
                cheapest_pathes.append(path)
        for path in cheapest_pathes:
            i = 0
            for h in path:
                h.rank = 100 // cost + i
                i += 1

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

        if self.start_hub.max_drones > self.end_hub.max_drones:
            print(
                "Drones cannot do this trip because of the",
                f"{self.end_hub.id} capacity",
                file=sys.stderr
                )
            exit(1)

        i = 0

        while i < self.nb_drones and i < self.start_hub.max_drones:
            self.start_hub.drones.append(
                Drone(f"D{i + 1}", self.start_hub.position))
            i += 1

        if self.nb_drones > self.start_hub.max_drones:
            print("Because of insufficient start_ hub capacity,",
                  "not all the drones were deployed")

        # here Exception could happen.
        # use try block here or on top of this method
        self.validate_connections()

        # make pathfinding here?
        self.find_valid_path()
        if len(self.all_pathes) == 0:
            raise Exception("There is no path from start to goal")

        self.rank_hubs()
        # make path finding and ranking of the hubs
        # for hub in self.hubs:
        #     print(hub.id, hub.max_drones, hub.path,
        #           [h.id for h in hub.neighbour_hubs])
        print("end of preparation")

    def make_move(self) -> bool:
        # loop through hubs starting from the end
        # loop through drons at the hub and check if they can go further
        # if yes
        def move_to_next(hubs_with_drones: list[Hub]):
            # I need to use start from the hubs that are
            # the nearest to the goal
            # sort hubs by their rank - rank has to represent
            # how close they are to the finish

            # there should be two different scenarios
            # if current hub has waiting drones
            #       move them and then check to_visit
            # then do standart stuff:
            #       which is

            while hubs_with_drones:
                hub = hubs_with_drones.pop()

                i = 0

                # to_visit = [
                #     h for h in hub.neighbour_hubs
                #     if len(h.drones) < h.max_drones
                #     and h.zone in ["NORMAL", "PRIORITY", "RESTRICTED"]
                #     and h.rank > 0
                #     ]
                to_visit = [h for h in hub.neighbour_hubs if h.rank > hub.rank
                            and h.max_drones > (
                                len(h.drones) + len(h.waiting_drones))]

                # to_visit.sort(key=lambda x: x.rank)
                # to_visit = [h for h in to_visit if hub.rank < h.rank]
                # firstly moving waiting drones
                while hub.waiting_drones:
                    drone, next_hub = hub.waiting_drones.pop()
                    if (
                        i < self.find_connection(hub, next_hub).link_cap
                        and i < (next_hub.max_drones -
                                 (len(next_hub.drones) +
                                  len(next_hub.waiting_drones)))
                                  ):
                        drone.move_to(hub, next_hub)
                        i += 1

                # when pushing all the drones further
                # thing is that to_visit is sorted by rank, so we are always
                # pushing the Hub that is closes to the Finish
                # that is why it empties the spot for next drone
                # that sits in the HUb behind
                while hub.drones and to_visit:

                    if len(to_visit) > 0:
                        next_hub = to_visit.pop()

                        # amount of drones that can fly to the next hub
                        # based on the minimum value between link cap
                        # and avaliable spots in the next hub
                        i = min([
                                self.find_connection(hub, next_hub).link_cap,
                                next_hub.max_drones - len(next_hub.drones)
                                ])
                        drones: list[Drone] = []
                        if next_hub.zone == "RESTRICTED":
                            # print("we are in restricted")
                            if hub.waiting_drones:
                                drones.append(hub.waiting_drones.pop()[0])
                            # or take drone from waiting list
                            # or put drone there and go to the next hub
                            else:
                                d = hub.drones.pop()
                                # stays in connection
                                # self.find_connection(hub, next_hub)
                                print(f"{d.id} stays in {hub.id}", end=", ")
                                hub.waiting_drones.append(
                                    (d, next_hub))
                        else:
                            while i:
                                drones.append(hub.drones.pop())
                                i -= 1

                        for drone in drones:
                            if next_hub not in drone.visited_hubs:
                                drone.visited_hubs.add(next_hub)
                            else:
                                tmp = next_hub
                                next_hub = to_visit.pop()
                                to_visit.append(tmp)

                            drone.move_to(hub, next_hub)
                            i += 1

                        if next_hub.max_drones > (len(next_hub.drones) +
                                                  len(next_hub.waiting_drones)
                                                  ):
                            to_visit.append(next_hub)
                        else:
                            break
                    else:
                        break

        hubs_with_drones: list[Hub] = []
        for hub in self.hubs:
            if ((len(hub.drones) > 0 or len(hub.waiting_drones) > 0)
                    and "goal" not in hub.id):
                hubs_with_drones.append(hub)

        hubs_with_drones = sorted(
            hubs_with_drones, key=lambda x: x.rank)
        if len(hubs_with_drones) > 0:
            move_to_next(hubs_with_drones)
            return True
        else:
            print("All drones has arrived to the goal")
            return False

    def make_graph(self):
        return {hub: hub.neighbour_hubs for hub in self.hubs}

    def find_valid_path(self) -> None:
        all_pathes = []
        # stack elment is a tuple with current hub,
        # path(list of hubs that led me here)
        # cost and set of visited hubs
        start = self.start_hub
        stack = [(start, [start], 0, {start})]

        while stack:
            current, path, cost, visited = stack.pop()
            if current is self.end_hub:
                all_pathes.append((path, cost))
                continue

            for n in current.neighbour_hubs:
                if n.zone == "BLOCKED":
                    continue
                if n in visited:
                    continue

                step_cost = 2 if n.zone == "RESTRICTED" else 1
                new_path = path + [n]
                new_visted = visited | {n}
                stack.append((
                    n,
                    new_path,
                    cost + step_cost,
                    new_visted
                ))

        self.all_pathes = all_pathes
