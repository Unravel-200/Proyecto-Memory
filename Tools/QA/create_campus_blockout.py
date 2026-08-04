import math
import unreal

MAP = '/Game/Maps/L_Campus_Blockout'
CUBE = unreal.load_object(None, '/Engine/BasicShapes/Cube.Cube')

if CUBE is None:
    raise RuntimeError('No se encontró /Engine/BasicShapes/Cube.Cube')

unreal.EditorLevelLibrary.new_level(MAP)

def cube(name, location, dimensions, rotation=(0.0, 0.0, 0.0)):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        unreal.Rotator(*rotation))
    actor.set_actor_label(name)
    actor.static_mesh_component.set_static_mesh(CUBE)
    actor.set_actor_scale3d(unreal.Vector(dimensions[0] / 100.0, dimensions[1] / 100.0, dimensions[2] / 100.0))
    actor.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
    return actor

# Campus base: 700 x 850 m, assembled as 50 m tiles. Heights deliberately vary
# to leave a readable graybox relief before final Landscape sculpting.
tile = 5000.0
half_x, half_y = 7, 8
for ix in range(-half_x, half_x):
    for iy in range(-half_y, half_y + 1):
        x = (ix + 0.5) * tile
        y = iy * tile
        hill_a = max(0.0, 1.0 - math.hypot(ix + 3.0, iy - 2.0) / 6.5)
        hill_b = max(0.0, 1.0 - math.hypot(ix - 4.0, iy + 4.0) / 6.0)
        height = 600.0 + 900.0 * hill_a + 650.0 * hill_b
        if abs(ix) <= 1:
            height -= 900.0
        cube('Terrain_%02d_%02d' % (ix, iy), (x, iy * tile, height - 250.0), (tile, tile, 500.0))

# Deep ravine channel running north/south, with three crossings.
cube('Quebrada_Cauce', (0.0, 0.0, -650.0), (9000.0, 5000.0, 300.0))
for y in (-30000.0, 0.0, 30000.0):
    cube('Puente_Graybox_%d' % int(y), (0.0, y, 250.0), (10500.0, 3500.0, 400.0))

# Main graybox circulation strips, wide enough for the player.
cube('Camino_Principal_EO', (0.0, 0.0, 1550.0), (65000.0, 5000.0, 120.0))
cube('Camino_Principal_NS', (0.0, 0.0, 1550.0), (5000.0, 80000.0, 120.0))

start = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.PlayerStart, unreal.Vector(-25000.0, -30000.0, 1900.0), unreal.Rotator(0.0, 90.0, 0.0))
start.set_actor_label('PlayerStart_Campus_Blockout')

unreal.EditorLevelLibrary.save_current_level()
unreal.log('PM_CAMPUS_BLOCKOUT_CREATED ' + MAP)
