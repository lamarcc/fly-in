class Map():
    def __init__(self):
        self.nb_drone = 0
        self.start_hub = 0
        self.end_hub = 0
        self.zone = {}
        self.connection = {}

class Drone():
    def __init__(self, id):
        self.id = 0
        self.position: tuple = ()
        self.finished = False

    @classmethod
    def new_drone(cls):
         super.__init__()

class Zone():

class Connection():
