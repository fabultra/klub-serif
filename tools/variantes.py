# -*- coding: utf-8 -*-
"""Variantes signature K.lub (v1.1).

1. g a un etage, par defaut : greffe de la panse/fût du q et du crochet
   descendant du j (pieces du dessin d'origine => qualite conservee).
   L'ancien g a deux etages reste accessible via ss01 (g.ss01).
2. Ligature k_period_l (« k.l ») cablee dans la fonctionnalite liga.

S'applique aux quatre styles, en place (fonts/ttf), puis regenere les WOFF2.
"""
import pathops
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables as ot
from fontTools.otlLib import builder as otb
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

FONTS = [
    "fonts/ttf/KlubSerifDisplay-Regular.ttf",
    "fonts/ttf/KlubSerifDisplay-Italic.ttf",
    "fonts/ttf/KlubSerifText-Regular.ttf",
    "fonts/ttf/KlubSerifText-Italic.ttf",
]


def glyph_path(glyphSet, name, transform=None):
    p = pathops.Path()
    pen = p.getPen(glyphSet=glyphSet)
    if transform:
        pen = TransformPen(pen, transform)
    glyphSet[name].draw(pen)
    return p


def rect_path(x0, y0, x1, y1):
    p = pathops.Path()
    pen = p.getPen()
    pen.moveTo((x0, y0))
    pen.lineTo((x1, y0))
    pen.lineTo((x1, y1))
    pen.lineTo((x0, y1))
    pen.closePath()
    return p


def crop(path, x0, y0, x1, y1):
    return pathops.op(path, rect_path(x0, y0, x1, y1),
                      pathops.PathOp.INTERSECTION)


def stem_center(path, y0, y1):
    """Centre horizontal du fût mesure dans la bande [y0, y1]."""
    band = crop(path, -2000, y0, 3000, y1)
    x0, _, x1, _ = band.bounds
    return (x0 + x1) / 2, (x1 - x0)


def to_ttglyph(path):
    pen = TTGlyphPen(None)
    path.draw(pen)
    return pen.glyph()


def build_single_story_g(font):
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    q = glyph_path(gs, "q")
    j = glyph_path(gs, "j")
    # bande de mesure commune aux deux fûts
    qc, qw = stem_center(crop(q, -2000, 40, 3000, 240) or q, 40, 240)
    # pour q : le fût est a droite ; la bande contient panse+fût, on isole
    # la partie droite avant de mesurer
    xq0, _, xq1, _ = q.bounds
    q_right = crop(q, xq1 - 260, 40, xq1 + 10, 240)
    qc, qw = ((q_right.bounds[0] + q_right.bounds[2]) / 2,
              q_right.bounds[2] - q_right.bounds[0])
    jc, jw = stem_center(j, 40, 240)
    dx = qc - jc
    corps = crop(q, xq0 - 50, -20, xq1 + 60, 2000)      # panse + fût
    queue = glyph_path(gs, "j", transform=(1, 0, 0, 1, dx, 0))
    queue = crop(queue, -2000, -2000, 3000, 240)         # crochet seul
    g_new = pathops.op(corps, queue, pathops.PathOp.UNION)
    g_new.simplify()
    aw, _ = hmtx["q"]
    lsb = int(round(g_new.bounds[0]))
    return to_ttglyph(g_new), (aw, lsb), abs(qw - jw)


def build_ligature(font, tighten_kp=55, tighten_pl=45):
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    k_aw = hmtx["k"][0]
    p_aw = hmtx["period"][0]
    l_aw = hmtx["l"][0]
    x_p = k_aw - tighten_kp
    x_l = x_p + p_aw - tighten_pl
    lig = glyph_path(gs, "k")
    for name, dx in (("period", x_p), ("l", x_l)):
        lig = pathops.op(lig, glyph_path(gs, name, transform=(1, 0, 0, 1, dx, 0)),
                         pathops.PathOp.UNION)
    lig.simplify()
    aw = x_l + l_aw
    lsb = int(round(lig.bounds[0]))
    return to_ttglyph(lig), (aw, lsb)


def add_glyphs(font, new_glyphs):
    """new_glyphs: dict name -> (ttglyph, (aw, lsb)). Ajoute a la fin."""
    glyf, hmtx = font["glyf"], font["hmtx"]
    order = font.getGlyphOrder()
    for name, (g, metrics) in new_glyphs.items():
        if name in order:
            raise ValueError(f"{name} existe deja")
        order.append(name)
    font.setGlyphOrder(list(order))
    for name, (g, metrics) in new_glyphs.items():
        glyf[name] = g
        hmtx[name] = metrics
    font["maxp"].numGlyphs = len(order)
    if hasattr(font["post"], "extraNames"):
        font["post"].extraNames = []          # regenere depuis glyphOrder


def _all_langsys(gsub):
    for sr in gsub.ScriptList.ScriptRecord:
        if sr.Script.DefaultLangSys is not None:
            yield sr.Script.DefaultLangSys
        for lsr in sr.Script.LangSysRecord:
            yield lsr.LangSys


def add_feature_lookup(gsub, tag, lookup_index):
    """Ajoute lookup_index a la feature `tag` (creee et referencee dans
    tous les LangSys si absente, en preservant l'ordre trie des tags)."""
    recs = gsub.FeatureList.FeatureRecord
    for rec in recs:
        if rec.FeatureTag == tag:
            rec.Feature.LookupListIndex.append(lookup_index)
            rec.Feature.LookupCount = len(rec.Feature.LookupListIndex)
            return
    rec = ot.FeatureRecord()
    rec.FeatureTag = tag
    rec.Feature = ot.Feature()
    rec.Feature.FeatureParams = None
    rec.Feature.LookupListIndex = [lookup_index]
    rec.Feature.LookupCount = 1
    old = list(recs)
    new = sorted(old + [rec], key=lambda r: r.FeatureTag)
    remap = {old.index(r): new.index(r) for r in old}
    gsub.FeatureList.FeatureRecord = new
    gsub.FeatureList.FeatureCount = len(new)
    new_idx = new.index(rec)
    for ls in _all_langsys(gsub):
        ls.FeatureIndex = [remap[i] for i in ls.FeatureIndex]
        if ls.ReqFeatureIndex != 0xFFFF:
            ls.ReqFeatureIndex = remap.get(ls.ReqFeatureIndex,
                                           ls.ReqFeatureIndex)
        ls.FeatureIndex.append(new_idx)
        ls.FeatureCount = len(ls.FeatureIndex)
    fv = getattr(gsub, "FeatureVariations", None)
    if fv:
        for fvr in fv.FeatureVariationRecord:
            for sub in fvr.FeatureTableSubstitution.SubstitutionRecord:
                sub.FeatureIndex = remap.get(sub.FeatureIndex,
                                             sub.FeatureIndex)


def add_gsub(font):
    gsub = font["GSUB"].table
    lookups = gsub.LookupList.Lookup
    lig_lookup = otb.buildLookup(
        [otb.buildLigatureSubstSubtable({("k", "period", "l"): "k_period_l"})])
    lookups.append(lig_lookup)
    add_feature_lookup(gsub, "liga", len(lookups) - 1)
    ss_lookup = otb.buildLookup(
        [otb.buildSingleSubstSubtable({"g": "g.ss01"})])
    lookups.append(ss_lookup)
    add_feature_lookup(gsub, "ss01", len(lookups) - 1)
    gsub.LookupList.LookupCount = len(lookups)


def bump_version(font):
    font["head"].fontRevision = 1.1
    name = font["name"]
    for rec in name.names:
        if rec.nameID == 5:
            name.setName("Version 1.100; variantes signature K.lub", 5,
                         rec.platformID, rec.platEncID, rec.langID)


def process(path):
    font = TTFont(path)
    glyf = font["glyf"]
    # conserver l'ancien g (deux etages) comme alternative ss01
    old_g = glyf["g"]
    old_metrics = font["hmtx"]["g"]
    g_new, g_metrics, stem_diff = build_single_story_g(font)
    lig, lig_metrics = build_ligature(font)
    add_glyphs(font, {"g.ss01": (old_g, old_metrics),
                      "k_period_l": (lig, lig_metrics)})
    glyf["g"] = g_new
    font["hmtx"]["g"] = g_metrics
    add_gsub(font)
    bump_version(font)
    font.save(path)
    w = TTFont(path)
    w.flavor = "woff2"
    w.save(path.replace("/ttf/", "/web/").replace(".ttf", ".woff2"))
    print(f"ok {path}  (delta fût q/j: {stem_diff:.0f} unites)")


if __name__ == "__main__":
    for p in FONTS:
        process(p)
