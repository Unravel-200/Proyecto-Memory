import unreal

MAP = '/Game/Maps/L_Campus_Blockout'
unreal.EditorLevelLibrary.load_level(MAP)

for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    label = actor.get_actor_label()
    if label.startswith('Terrain_'):
        parts = label.split('_')
        try:
            ix = int(parts[1])
        except (ValueError, IndexError):
            ix = 99
        if abs(ix) <= 1:
            unreal.EditorLevelLibrary.destroy_actor(actor)
    elif label.startswith(('Relief_', 'Quebrada_', 'Puente_', 'Camino_')):
        unreal.EditorLevelLibrary.destroy_actor(actor)

CUBE = unreal.load_object(None, '/Engine/BasicShapes/Cube.Cube')

def cube(name, location, dimensions, rotation=(0.0, 0.0, 0.0)):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, unreal.Vector(*location), unreal.Rotator(*rotation))
    actor.set_actor_label(name)
    actor.static_mesh_component.set_static_mesh(CUBE)
    actor.set_actor_scale3d(unreal.Vector(dimensions[0] / 100.0, dimensions[1] / 100.0, dimensions[2] / 100.0))
    actor.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
    return actor

# Deep, open ravine with two sloped banks. The river follows the campus Y axis.
cube('Quebrada_Cauce', (0.0, 0.0, -850.0), (6500.0, 80000.0, 300.0))
cube('Relief_Talud_Oeste', (-6500.0, 0.0, 700.0), (9000.0, 80000.0, 700.0), (10.0, 0.0, 0.0))
cube('Relief_Talud_Este', (6500.0, 0.0, 700.0), (9000.0, 80000.0, 700.0), (-10.0, 0.0, 0.0))

# Three visible crossings over the ravine.
for y in (-30000.0, 0.0, 30000.0):
    cube('Puente_Graybox_%d' % int(y), (0.0, y, 850.0), (11000.0, 3500.0, 450.0))

# Main circulation remains above terrain and crosses the ravine at the center.
cube('Camino_Principal_EO', (0.0, 0.0, 1900.0), (65000.0, 5000.0, 120.0))
cube('Camino_Principal_NS', (0.0, 0.0, 1900.0), (5000.0, 80000.0, 120.0))

# Large stepped hills at the campus edges. The tiers make the silhouette obvious
# in the editor before the final Landscape sculpt pass.
for prefix, x, y in (('Noroeste', -24000.0, 27000.0), ('Sureste', 24000.0, -27000.0), ('Noreste', 25000.0, 30000.0)):
    cube('Relief_%s_Base' % prefix, (x, y, 2200.0), (18000.0, 18000.0, 1000.0))
    cube('Relief_%s_Medio' % prefix, (x, y, 3100.0), (12000.0, 12000.0, 800.0))
    cube('Relief_%s_Cima' % prefix, (x, y, 3850.0), (6500.0, 6500.0, 700.0))

unreal.EditorLevelLibrary.save_current_level()
