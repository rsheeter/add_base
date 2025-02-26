"""Adds a crude BASE table to a font.

Usage:

    python add_base.py my-font.ttf
"""

from fontTools import ttLib
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.ttFont import newTable
from pathlib import Path
import sys


# Shameless copy of https://github.com/fonttools/fonttools/blob/0d6b000c1ac9140d57a82bab5f14381f40bb88a7/Lib/fontTools/feaLib/builder.py#L731
def baseCoord(c):
    coord = otTables.BaseCoord()
    coord.Format = 1
    coord.Coordinate = c
    return coord


def addBase(font_file: Path):
    assert font_file.is_file(), font_file

    print("Adding BASE to", font_file)
    font = ttLib.TTFont(font_file)
    if "BASE" in font.keys():
        print("WARNING: BASE is already present and will be overwritten")

    scripts = (
        # Tag, ((min, max),...)
        ("dflt", ()),
        ("VIT ", ((-555, 2163),)),
    )

    # Shamelessly borrowed from https://github.com/fonttools/fonttools/blob/0d6b000c1ac9140d57a82bab5f14381f40bb88a7/Lib/fontTools/feaLib/builder.py#L737
    horzAxis = otTables.Axis()
    
    horzAxis.BaseScriptList = otTables.BaseScriptList()
    horzAxis.BaseScriptList.BaseScriptRecord = []
    horzAxis.BaseScriptList.BaseScriptCount = len(scripts)
    for (i, (tag, minmaxes)) in enumerate(scripts):
        record = otTables.BaseScriptRecord()
        record.BaseScriptTag = tag
        record.BaseScript = otTables.BaseScript()
        record.BaseScript.BaseValues = otTables.BaseValues()
        record.BaseScript.BaseValues.DefaultIndex = 0
        record.BaseScript.BaseValues.BaseCoord = []
        record.BaseScript.BaseValues.BaseCoordCount = len(minmaxes)
        record.BaseScript.BaseLangSysRecord = []

        for (minv, maxv) in minmaxes:
            minmax_record = otTables.MinMax()
            minmax_record.MinCoord = baseCoord(minv)
            minmax_record.MaxCoord = baseCoord(maxv)
            minmax_record.FeatMinMaxCount = 0
            if tag.lower() == "dflt":
                record.BaseScript.DefaultMinMax = minmax_record
            else:
                lang_record = otTables.BaseLangSysRecord()
                lang_record.BaseLangSysTag = tag
                lang_record.MinMax = minmax_record
                record.BaseScript.BaseLangSysRecord.append(lang_record)
        record.BaseScript.BaseLangSysCount = len(
            record.BaseScript.BaseLangSysRecord
        )
        horzAxis.BaseScriptList.BaseScriptRecord.append(record)

    base = newTable("BASE")
    base.table = otTables.BASE()
    base.table.Version = 0x00010000
    base.table.HorizAxis = horzAxis
    font["BASE"] = base

    print(horzAxis.BaseScriptList.BaseScriptRecord)

    print("Updating", font_file)
    font.save(font_file)


def main():
    for font_file in sys.argv[1:]:
        addBase(Path(font_file))

if __name__ == "__main__":
    main()