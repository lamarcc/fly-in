from init import Simulation, Parse, Hub, Map, Connection

if __name__ == "__main__":
    Parse.parse("../maps/easy/01_linear_path.txt")
    simulation = Simulation()
    simulation.init_hubs(Parse.hubs)
    for hub in simulation.map.hubs:
        print(hub.name)
        print(hub.x_pos)
        print(hub.y_pos)
        print(hub.metadata)
        print()
    simulation.init_connections(Parse.connection)
    for connection in simulation.map.connections:
        print(connection.hub_a)
        print(connection.hub_b)
        print(connection.max_link_capacity)
        print()
