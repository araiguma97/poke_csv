import csv
import re
import jaconv
import time

# CSVの読み込み
def read_csv(csv_file_name) :
    csv_file = open(csv_file_name, 'r', encoding='utf8')
    reader = csv.reader(csv_file)
    list = [row for row in reader]
    return list

# ポケモン一覧（グローバル変数）
poke_list = read_csv('poke.csv')

# ポケモンリストから名前で名前を検索
def search_name_by_name(name) :
    for row in poke_list :
        if name == row[0] :
            return row
    return None

# ポケモンリストから名前で種族値を検索
def search_race_by_name(name) :
    ret_list = []
    for row in poke_list :
        if name in row[0] :
            ret_list.append(row[0])
    return ret_list

# リストの表示
def show_list(list) :
    cnt = 0             # 表示番号
    print("Num\tName\t\tHP\tAttack\tBlock\tContact\tDefence\tSpeed")    # 見出し
    for row in list :
        if row != [] :  # 行が削除されていなければ、行を表示
            print(cnt, end='\t')
            for column in row :
                print(column, end='\t')
            print()
        cnt += 1

def main() :
    my_poke_list = read_csv('my_poke.csv')    # 自分のパーティ

    visible_list = []  # 表示リスト；表示番号、名前、種族値が格納される

    # 自分のパーティを表示リスト追加
    for my_poke in my_poke_list :
        try :  
            visible_list.append(search_name_by_name(my_poke[0]))
        except: 
            print("Add failed.")

    print("Poke Viewer v0.1")
    while(1) :
        print("\r(VIEWER) ", end="")
        command = input("")
        # 削除コマンド
        if re.match(r'r\s+(\w*(\s*\w)*)\s*', command) != None :
            no_list = re.split(r'\s+', re.sub(r'r\s+(\w*(\s*\w)*)\s*', r'\1', command))
            for no in no_list :
                try :
                    if visible_list[int(no)] == [] :
                        print("No num " + no)
                    else :
                        visible_list[int(no)] = []
                except :
                    print("Error: Remove Failed: " + no)
        # 追加モード
        elif command == "a" :
            while(1) :
                input_name = jaconv.hira2kata(input("\rEnter name: "))
                ret_list = search_race_by_name(input_name)
                if input_name == "" :
                    break
                elif len(ret_list) < 1 :
                    print("Not found: " + input_name)
                elif len(ret_list) == 1:
                    visible_list.append(search_name_by_name(ret_list[0]))
                    print("Added: " + ret_list[0])
                else : 
                    for i, ret in enumerate(ret_list) :
                        print(str(i) + ": " + ret, end='\t')
                        if (i+1) % 4 == 0 :
                            print()
                    print()
                    input_num = input("Enter num: ")
                    try :
                        visible_list.append(search_name_by_name(ret_list[int(input_num)]))
                        print("Added: " + ret_list[int(input_num)])
                    except: 
                        print("Error: Invalid Num")
        elif command == "i" :   # 表示コマンド
            show_list(visible_list)    
        elif command == "q" :   # 終了コマンド
            print("Good bye.")
            time.sleep(1)
            break
        elif command != "" :
            print("Error: Invalid command")

main()
