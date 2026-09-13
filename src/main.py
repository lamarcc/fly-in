if __name__ == "__main__":
    try:
        from engine import Simulation, PathfindingError
        from parser import ParsingError, SimulationStop, MapFileError
        from map_chooser import MapMenu, EmptyMapFolder
        import os
        map = MapMenu()
        run = Simulation()
        os.system("clear")
        map_path = str(map.choose())
        run.parser.parse(map_path)
        if not run.parser.start_hub or not run.parser.end_hub:
            print(MapFileError.msg("Map file not conform"))
            exit(0)
        run.init()
        run.run()
    except KeyboardInterrupt:
        print(SimulationStop(), end="")
    except ImportError as importerr:
        print(importerr)
    except EmptyMapFolder as emptyerr:
        print(emptyerr)
    except (EOFError, ParsingError, PathfindingError) as e:
        print(e)
