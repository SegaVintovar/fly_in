import sys
from parsing import Parsing
from fly_in import Map, Hub

def main() -> None:
    # print("starts")
    if len(sys.argv) == 2:
        parser = Parsing()
        # try:
        with open(sys.argv[1], "r") as f:
            config_data = f.read()
            data_4_map = parser.parsing(config_data)
            for hub in data_4_map["hubs"]:
                hub.validate_input()
                hub.validate_meta()
            my_map = Map(**data_4_map)
            # for hub in my_map.hubs:
            #     print(hub.id, hub.position, hub.type)
            for connection in my_map.connections:
                connection.setup(my_map.hubs)
                # print(connection.linked_members)
            my_map.prepare_4_start()
            my_map.make_move()
            

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
