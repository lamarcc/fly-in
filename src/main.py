from engine import Simulation, PathfindingError
from parser import ParsingError
from map_chooser import MapMenu

if __name__ == "__main__":
    try:
        map = MapMenu()
        run = Simulation()
        print("\033[H\033[J")
        map_path = str(map.choose())
        run.parser.parse(map_path)
        run.init()
        run.run()
        print()
    except (KeyboardInterrupt, EOFError, ParsingError, PathfindingError) as e:
        print(e)
