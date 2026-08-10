# -*- coding: utf-8 -*-
"""Guarda L_Campus_Natural."""
import unreal

ok = unreal.EditorLoadingAndSavingUtils.save_dirty_packages(
    save_map_packages=True, save_content_packages=True)
print("guardado: %s" % ok)
