import unreal

actors = unreal.EditorLevelLibrary.get_all_level_actors()
counts = {}
for a in actors:
    label = a.get_actor_label()
    for key, prefix in {
        'buildings': 'CampusBuilding_', 'roads': 'Road_', 'paths': 'Path_',
        'plazas': 'Plaza_', 'bridges': 'BridgeMarker_', 'ravine': 'RavineBuffer_'
    }.items():
        if label.startswith(prefix):
            counts[key] = counts.get(key, 0) + 1
for key in ('buildings','roads','paths','plazas','bridges','ravine'):
    unreal.log('NATURAL_VALIDATE_%s=%d' % (key.upper(), counts.get(key, 0)))
unreal.log('NATURAL_VALIDATE_ACTORS=%d' % len(actors))
