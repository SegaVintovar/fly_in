import sys
from parsing import Parsing
from fly_in import Map

def main() -> None:
    # print("starts")
    if len(sys.argv) == 2:
        parser = Parsing()
        # try:
        with open(sys.argv[1], "r") as f:
            config_data = f.read()
            data_4_map = parser.parsing(config_data)
        # except Exception as e:
        #     print(str(e), file=sys.stderr)
        # else:
            hubs = parser.parse_hubs(data_4_map["hubs"])
        connections = Parsing.parse_connections(data_4_map["connections"])
        # my_map = Map(data_4_map["nb_drones"])            
    else:
        print("The program is missing congiguration file", file=sys.stderr)
    # create a fleet and a map
    # hubs = Parsing.parse_hubs(data_4_map["hubs"])
    # connections = Parsing.parse_connections(data_4_map["connections"])
    # my_map = Map(data_4_map["nb_drones"])
    

if __name__ == "__main__":
    main()
