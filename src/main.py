from init import Simulation, Parse, Hub, Map, Connection, ParsingError

if __name__ == "__main__":
    try:
        run = Simulation()
        # run.parse.parse("../maps/easy/01_linear_path.txt")
        run.parse.parse("../maps/easy/map")
        run.init()
        run.run()
    except (KeyboardInterrupt, EOFError, ParsingError):
        print("Selem")
