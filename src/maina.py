from engine import Simulation, PathfindingError
from parser import ParsingError
import map_chooser

if __name__ == "__main__":
    try:
        chooser = map_chooser.MapMenu()
        chooser.choose()
        # print("\033[H\033[J", end="")
        # run = Simulation()
        # ## trouver la lib pour avoir le choix dans le terminal a l' exedcution
        # run.parser.parse("../maps/easy/map")
        # run.init()
        # run.run()
    except (KeyboardInterrupt, EOFError, ParsingError, PathfindingError) as e:
        print(e)
