from ursina import *
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='cube', collider='box', scale=(12, 0.05, 12), texture='metal', texture_scale=(4,4))

editor_camera = EditorCamera(enabled=True, ignore_paused=True)

# block = Entity(model='assets/ground.obj', texture='assets/ground.png', scale=0.05)

# sun = DirectionalLight()
# sun.look_at(Vec3(1,-1,-1))
# Sky()

app.run()

