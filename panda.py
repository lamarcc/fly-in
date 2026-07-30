from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from math import pi, sin, cos

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "assets", "heli.obj")

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        model = self.loader.loadModel(model_path)
        model.reparentTo(self.render)
        model.setPos(0, 0, 5)
        model.setScale(1)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 2.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = MyApp()
app.run()
