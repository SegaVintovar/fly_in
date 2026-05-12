from fly_in import Hub


class Drone():
    def __init__(self, id: str, location: tuple[int, int]):
        self.id = id
        self.location = location
        self.visited_hubs = set()
        self.on_the_way = False
        
    
    def move_to(self, current_hub: Hub, next_hub: Hub) -> None:
        self.location = next_hub.position
        next_hub.drones.append(self)
        self.visited_hubs.add(current_hub)
        i += 1
        print(
            self.id,
            "->",
            next_hub.id,
            end=", ")