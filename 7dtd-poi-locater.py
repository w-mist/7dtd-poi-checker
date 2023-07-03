import sys
import math
import xml.etree.ElementTree as ET

# Exclude Lot_Rural_Filler from result or not.
b_exclude_lot=True

def append_loc(f_master, f_prefabs_xml, i_loc_current_x, i_loc_current_y):
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
        if s_deconame in set_master:
            if b_exclude_lot and 'lot_' in s_deconame:
                continue
            s_decopos = elem.get('position')
            li = s_decopos.split(',')
            i_c += 1
            f_distance_x = int(li[0]) - int(i_loc_current_x) if int(li[0]) > int(i_loc_current_x) else int(i_loc_current_x) - int(li[0])
            f_distance_y = int(li[2]) - int(i_loc_current_y) if int(li[2]) > int(i_loc_current_y) else int(i_loc_current_y) - int(li[2])
            f_distance = round(math.sqrt(f_distance_x * f_distance_x + f_distance_y * f_distance_y))
            print(f"{s_deconame}\t{li[0]}\t{li[1]}\t{li[2]}\t{f_distance}")
    print(f"found: {i_c} POIs")
    print(f"current_pos: E/W {i_loc_current_x} N/S {i_loc_current_y}")
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
    i_loc_current_x = sys.argv[3]
    i_loc_current_y = sys.argv[4]

    append_loc(f_master, f_prefabs_xml, i_loc_current_x, i_loc_current_y)

if __name__ == '__main__':
    main()
