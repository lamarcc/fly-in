from engine import Simulation, PathfindingError
from parser import ParsingError

if __name__ == "__main__":
    try:
        run = Simulation()
        # run.parse.parse("../maps/easy/01_linear_path.txt")
        run.parser.parse("../maps/easy/map")
        run.init()
        run.run()
    except (KeyboardInterrupt, EOFError, ParsingError, PathfindingError) as e:
        print(e)
