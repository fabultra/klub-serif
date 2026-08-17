# -*- coding: utf-8 -*-
"""Derive la famille Klub Serif depuis DM Serif (OFL).

Obligations OFL respectees : les mentions de copyright et la licence
(name IDs 0, 13, 14) sont conservees telles quelles ; seuls les noms de
famille/style changent. Le nom reserve 'Source' n'est pas utilise.
"""
from fontTools.ttLib import TTFont
import os

JOBS = [
    ("base/DMSerifDisplay-Regular.ttf", "Klub Serif Display", "Regular"),
    ("base/DMSerifDisplay-Italic.ttf",  "Klub Serif Display", "Italic"),
    ("base/DMSerifText-Regular.ttf",    "Klub Serif Text",    "Regular"),
    ("base/DMSerifText-Italic.ttf",     "Klub Serif Text",    "Italic"),
]

os.makedirs("out", exist_ok=True)

for path, fam, style in JOBS:
    f = TTFont(path)
    name = f["name"]
    ps = fam.replace(" ", "") + "-" + style
    full = f"{fam} {style}"
    old_version = name.getDebugName(5) or "Version 1.000"
    for rec in list(name.names):
        nid = rec.nameID
        if nid in (0, 13, 14):        # copyright + licence : intacts
            continue
        if nid == 1:
            name.setName(fam, 1, rec.platformID, rec.platEncID, rec.langID)
        elif nid == 2:
            name.setName(style, 2, rec.platformID, rec.platEncID, rec.langID)
        elif nid == 3:
            name.setName(f"{full}; adaptation K.lub", 3,
                         rec.platformID, rec.platEncID, rec.langID)
        elif nid == 4:
            name.setName(full, 4, rec.platformID, rec.platEncID, rec.langID)
        elif nid == 6:
            name.setName(ps, 6, rec.platformID, rec.platEncID, rec.langID)
        elif nid in (16,):
            name.setName(fam, 16, rec.platformID, rec.platEncID, rec.langID)
        elif nid in (17,):
            name.setName(style, 17, rec.platformID, rec.platEncID, rec.langID)
    # note de derivation (description)
    for pid, eid, lid in {(r.platformID, r.platEncID, r.langID)
                          for r in name.names if r.nameID == 1}:
        name.setName(
            "Adaptation K.lub de DM Serif (SIL OFL 1.1), "
            "derivee de Source Serif.", 10, pid, eid, lid)
    out_ttf = f"out/{ps}.ttf"
    f.save(out_ttf)
    f2 = TTFont(out_ttf)
    f2.flavor = "woff2"
    f2.save(f"out/{ps}.woff2")
    print("ok", out_ttf, "| famille:", fam, "| style:", style,
          "|", old_version.strip())
