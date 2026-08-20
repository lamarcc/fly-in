from init import Simulation, Parse, Hub, Map, Connection

if __name__ == "__main__":
    try:
        run = Simulation()
        run.parse.parse("../maps/easy/01_linear_path.txt")
        run.init()
    except (KeyboardInterrupt, EOFError):
        print("Selem")
