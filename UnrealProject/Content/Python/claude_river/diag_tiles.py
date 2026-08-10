# -*- coding: utf-8 -*-
"""Vuelca la rejilla real de LandscapeStreamingProxy: nombre, centro y bounds
de cada tile, para saber que hay -o no hay- en cada casilla del landscape."""

import unreal

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
tiles = []
for a in eas.get_all_level_actors():
    if "LandscapeStreamingProxy" not in a.get_class().get_name():
        continue
    loc = a.get_actor_location()
    bnd = a.get_actor_bounds(False)
    c, ext = bnd[0], bnd[1]
    tiles.append((a.get_actor_label(), loc.x / 100.0, loc.y / 100.0,
                 (c.x - ext.x) / 100.0, (c.y - ext.y) / 100.0,
                 (c.x + ext.x) / 100.0, (c.y + ext.y) / 100.0))

tiles.sort(key=lambda t: (t[2], t[1]))
print("%d tiles" % len(tiles))
for n, x, y, x0, y0, x1, y1 in tiles:
    print("%-28s loc=(%7.1f,%7.1f)  bbox=(%7.1f,%7.1f)..(%7.1f,%7.1f)"
          % (n, x, y, x0, y0, x1, y1))

xs = sorted(set(round(t[1]) for t in tiles))
ys = sorted(set(round(t[2]) for t in tiles))
print("\nX de tiles:", xs)
print("Y de tiles:", ys)
