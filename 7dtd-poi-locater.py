import sys
import math
import xml.etree.ElementTree as ET

# Include only Lot_Rural_Filler_06(Wrong Harvester) in result or not.
# By default, exclude ALL Lot_.* .
b_include_lot_06=True

def output_loc(s_deconame: str, s_decopos: list, i_loc_cur_x: int, i_loc_cur_y: int):
    li = s_decopos.split(',')
    f_distance_x = int(li[0]) - int(i_loc_cur_x) \
        if int(li[0]) > int(i_loc_cur_x) else int(i_loc_cur_x) - int(li[0])
    f_distance_y = int(li[2]) - int(i_loc_cur_y) \
        if int(li[2]) > int(i_loc_cur_y) else int(i_loc_cur_y) - int(li[2])
    f_distance = round(math.sqrt(f_distance_x * f_distance_x + f_distance_y * f_distance_y))
    print(f"{s_deconame}\t{li[0]}\t{li[1]}\t{li[2]}\t{f_distance}")

def select_poi(f_master, f_prefabs_xml, i_loc_cur_x, i_loc_cur_y):
    with open(f_master, 'r') as file:
        set_master = set(file.read().splitlines())
    xml_tree = ET.parse(f_prefabs_xml)
    root = xml_tree.getroot()
    l_deco = root.findall('.//decoration')
    i_c = 0
    # header
    print("POI_NAME\tE(+)/W(-)\tElev\tN(+)/S(-)\tDistance")
    for elem in l_deco:
        s_deconame = elem.get('name')
        s_decopos = elem.get('position')
        if b_include_lot_06:
            if s_deconame == 'lot_rural_filler_06':
                output_loc(s_deconame, s_decopos, i_loc_cur_x, i_loc_cur_y)
                i_c += 1
            if not 'lot_' in s_deconame and s_deconame in set_master:
                output_loc(s_deconame, s_decopos, i_loc_cur_x, i_loc_cur_y)
                i_c += 1
        else:
            if not 'lot_' in s_deconame and s_deconame in set_master:
                output_loc(s_deconame, s_decopos, i_loc_cur_x, i_loc_cur_y)
                i_c += 1
    print(f"found: {i_c} POIs")
    print(f"current_pos: E/W {i_loc_cur_x} N/S {i_loc_cur_y}")
    return 0

def main():
    if len(sys.argv) != 5:
        print("検索するPOIを定義したテキストファイル, 検索対象のprefabs.xml, 現在地(E/W), 現在地(N/S)の4引数を指定してください.")
        print("* ファイルA:master.txt (input:" + sys.argv[1])
        print("* ファイルB:%AppData%\\Roaming\\7DaysToDie\\SavesLocal\\...\\World\\prefabs.xml (input was " + sys.argv[2])
        print("* input was " + sys.argv[3])
        print("* input was " + sys.argv[4])
        return -1

    f_master = sys.argv[1]
    f_prefabs_xml = sys.argv[2]
    i_loc_cur_x = sys.argv[3]
    i_loc_cur_y = sys.argv[4]
    select_poi(f_master, f_prefabs_xml, i_loc_cur_x, i_loc_cur_y)

if __name__ == '__main__':
    main()
