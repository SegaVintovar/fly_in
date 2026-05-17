from typing import TYPE_CHECKING
from color import Color

if TYPE_CHECKING:
    from fly_in import Hub


class Drone():
    def __init__(self, id: str, location: tuple[int, int]):
        self.id = id
        self.location = location
        self.visited_hubs = set()
        self.on_the_way = False

    def move_to(self, current_hub: "Hub", next_hub: "Hub") -> None:
        self.location = next_hub.position
        next_hub.drones.append(self)
        self.visited_hubs.add(current_hub)
        # there exception is comming
        c = getattr(Color, next_hub.color.upper())
        # i += 1
        print(
            self.id,
            "->",
            c,
            next_hub.id,
            Color.Style.RESET_ALL,
            end=", ")
