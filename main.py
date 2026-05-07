import sys
from parsing import Parsing
from fly_in import Map, Hub
from game_ui import GameUI

def main() -> None:
    # print("starts")
    if len(sys.argv) == 2:
        parser = Parsing()
        # try:
        with open(sys.argv[1], "r") as f:
            config_data = f.read()
            # print("Config data: ", config_data)
            print("start part")
            data_4_map = parser.parsing(config_data)
            # print(data_4_map)
            for hub in data_4_map["hubs"]:
                hub.validate_input()
                hub.validate_meta()
            my_map = Map(**data_4_map)
            # for hub in my_map.hubs:
            #     print(hub.id, hub.position, hub.type)
            # for connection in my_map.connections:
            #     connection.setup(my_map.hubs)
                # print(connection.linked_members)
            my_map.prepare_4_start()
        # except Exception as e:
        #     print(str(e))
        #     exit(1)
        # else:
        graph = my_map.make_graph()

        # here is te code to check graph
        # for key, item in graph.items():
        #     print(key.id, end=": ")
        #     for i in item:
        #         print(i.id, end=", ")
        #     print()
        # for hub in my_map.hubs:
        #     print(hub.id, hub.zone)
        # for path in my_map.all_pathes:
        #     hubs, cost = path

        #     print(cost, end=": ")
        #     for h in hubs:
        #         print(h.id, end=", ")
        #     print()
        
        # cheapest_cost = 0
        cheapest_path, cost = min(my_map.all_pathes, key=lambda x: x[1])
        print("Cost: ", cost)
        for h in cheapest_path:
            print(h.id)
        ui = GameUI(my_map)
        ui.run()


        # print(my_map.nb_drones)
        # my_map.make_move()
        # print()
        # my_map.make_move()
        
            # my_map.make_move()
            # print()
            # my_map.make_move()
            # print()
            # my_map.make_move()
      



            

        # except Exception as e:
        #     print(str(e), file=sys.stderr)
        # else:
        #     hubs = parser.parse_hubs(data_4_map["hubs"])
        # connections = Parsing.parse_connections(data_4_map["connections"])
        # my_map = Map(data_4_map["nb_drones"])            
    else:
        print("The program is missing congiguration file", file=sys.stderr)
    # create a fleet and a map
    # hubs = Parsing.parse_hubs(data_4_map["hubs"])
    # connections = Parsing.parse_connections(data_4_map["connections"])
    # my_map = Map(data_4_map["nb_drones"])
    

if __name__ == "__main__":
    main()
