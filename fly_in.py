class Drone():
    def __init__(self, location: tuple[int, int]):
        self.location = location
        self.visited_hubs = []


class Hub():
    def __init__(self,
                 id: str,
                 position: tuple[int, int],
                 
                 ):
        self.id = id
        self.capacity: int = 1
        self.color: str | None = None
        self.zone: str | None = None
        self.position = position
        self.next_hubs: list = []


class Connection():
    def __init__(self, connection: tuple[Hub, Hub]):
        self.connection = connection


class Map():
    def __init__(self, nb_drons: int):
        self.nb_drons = nb_drons
        self.drones = []
        self.map = []
    
    def make_move(self) -> None:
        # loop through hubs starting from the end
            # loop through drons at the hub and check if they can go further
                # if yes
        ...

    def find_valid_path(self) -> None:
        # use BFS to find all possible ways to the finish and use them for
        # self.make_move()
        ...
