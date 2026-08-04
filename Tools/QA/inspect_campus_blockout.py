import unreal

world = unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/L_Campus_Blockout')
actors = unreal.EditorLevelLibrary.get_all_level_actors()
labels = [a.get_actor_label() for a in actors]
terrain = [x for x in labels if x.startswith('Terrain_')]
bridges = [x for x in labels if x.startswith('Puente_')]
result = [
    'map_loaded=' + str(world is not None),
    'actor_count=' + str(len(actors)),
    'terrain_tiles=' + str(len(terrain)),
    'bridges=' + str(len(bridges)),
    'ravine=' + str('Quebrada_Cauce' in labels),
    'east_west_road=' + str('Camino_Principal_EO' in labels),
    'north_south_road=' + str('Camino_Principal_NS' in labels),
    'player_start=' + str('PlayerStart_Campus_Blockout' in labels),
]
with open(r'C:\Users\jeffa\Desktop\Proyecto\Proyecto-Memory\UnrealProject\Saved\QA\PlayerV0.1\campus-blockout-result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))
