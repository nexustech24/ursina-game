from ursina import *
from random import uniform
from ursina.prefabs.first_person_controller import FirstPersonController

# Create the game application
app = Ursina()

# Sky, player, and ground setup
Sky()
player = FirstPersonController(y=2, origin_y=-.5)
ground = Entity(model='plane', scale=(100, 1, 100), color=color.lime, texture="white_cube",
                texture_scale=(100, 100), collider='box')

# Walls for the scene
wall_1 = Entity(model="cube", collider="box", position=(-8, 0, 0), scale=(8, 5, 1), rotation=(0, 0, 0),
                texture="brick", texture_scale=(5, 5), color=color.rgb(255, 128, 0))
wall_2 = duplicate(wall_1, z=5)
wall_3 = duplicate(wall_1, z=10)
wall_4 = Entity(model="cube", collider="box", position=(-15, 0, 10), scale=(1, 5, 20), rotation=(0, 0, 0),
                texture="brick", texture_scale=(5, 5), color=color.rgb(255, 128, 0))

# Lighting setup for GoldSrc-like feel
light = PointLight(parent=player, position=(0, 2, 0), color=color.white, intensity=1.5)
ambient_light = AmbientLight(color=color.gray)

# ViewModel (gun)
viewmodel = Entity(
    model="assets/M1.obj",
    texture="assets/M1.png",
    parent=camera.ui,
    scale=.1,
    position=(.5, -.3),  # Adjust up-down and left-right
    rotation=(1, 169, 10)  # Adjust rotation
)

gun = Entity(model="assets/gun.obj", parent=camera.ui, scale=.08, color=color.gold, position=(.3, -.2),
             rotation=(-5, -10, -10))

# Footstep sound setup
footstep_sound = Audio("assets/sounds/footstep-loop.mp3", loop=True, autoplay=False)

# Fire sound effect
fire_sound = Audio("assets/sounds/cackling.wav", loop=True, autoplay=True)

# Fire particle system behind the long wall
fire_particles = ParticleSystem(
    parent=scene,
    position=(-13, 0.5, 10),  # Position behind the long wall
    texture="assets/particles/fire.png",  # Fire texture
    color=color.rgb(255, 165, 0),  # Fire color (orange)
    size=0.1,
    lifetime=2,
    speed=uniform(0.1, 0.5),
    loops=False,  # Don't loop particles forever, let them dissipate
    count=100,  # Number of particles
    emit_rate=10,  # Rate of emitting particles
    scale=(1, 1, 1)  # Scale of particles
)

# Variable to track player's previous position
previous_position = None

# Handle inputs
def input(key):
    if key == "left mouse down":
        # Play gunshot sound
        Audio("assets/sounds/pl_gun3.wav")

        # Perform the gun "recoil" animation
        gun.y += 0.1
        invoke(setattr, gun, 'y', gun.y - 0.1, delay=0.1)

        # Muzzle flash
        Animation("assets/particles/explosion.png", parent=camera.ui, scale=.15, position=(.19, -.03), loop=False)

# Updating the HUD and syncing players
def update():
    global previous_position

    # Initialize previous_position if it's the first frame
    if previous_position is None:
        previous_position = player.position

    # Check if the player moved a significant distance
    if distance(player.position, previous_position) > 0.05:  # Adjust threshold if needed
        if not footstep_sound.playing:
            footstep_sound.play()
    else:
        if footstep_sound.playing:
            footstep_sound.stop()

    # Update the previous position for the next frame
    previous_position = player.position

app.run()
