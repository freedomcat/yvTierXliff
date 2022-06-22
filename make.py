import sys
import glob
from lxml import etree
import csv

folder = sys.argv[1]
xliff_files = glob.glob("./"+sys.argv[1]+"/*.xliff")
tree = etree.parse(xliff_files[0])
root = tree.getroot()
mynsmap = dict()
mynsmap['x'] = root.nsmap[None]


def get_text(trans_unit, id, element):
    xp = trans_unit + "[@id='" + id + "']/x:" + element + "/text()"
    return tree.xpath(xp, namespaces=mynsmap)


file_id = tree.xpath("//x:file/@id", namespaces=mynsmap)
rows = []
for fid in file_id:
    trans_unit = "//x:file[@id='"+fid+"']//x:trans-unit"
    trans_unit_id = trans_unit+"/@id"
    ids = tree.xpath(trans_unit_id, namespaces=mynsmap)
    for i in ids:
        source = get_text(trans_unit, i, "source")
        target = get_text(trans_unit, i, "target")
        rows.append([i, source[0], target[0]])


with open("./"+sys.argv[1]+"/xliff.csv", "w", newline="") as f:
    writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerows(rows)


