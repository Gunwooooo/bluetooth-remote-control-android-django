import json
import pandas as pd
import os
import shutil

DATA_DIR = "../data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")
DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")

IntroList_columns = (
        "id",           # 기업 고유번호
        "enterprise",   # 기업 이름
        "start",        # 채용 시작
        "end"           # 채용 끝
    )

Intro_columns = (
        "id",
        "index",
        "parent_id",
        "career",
        "number",
        "department",
        "title"
    )


def import_data(data_path=DATA_FILE):
    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path}` 가 존재하지 않습니다.")
        exit(1)

    print("-----------------------------------------------------------")
    print(data[1])
    print("-----------------------------------------------------------")
    introLists = []     # 기업 리스트
    intros = []         # 기업 리스트

    print("****************************************************************************")
    print(data[1].get("department")[0].get('question')[1])
    print("****************************************************************************")

    idx = 0
    for d in data:

        introLists.append(
            [
                d["index"],
                d["enterprise"],
                d["start"],
                d["end"]
            ]
        )
        index = d["index"]
        for dp in d["department"]:
            number = 1
            for q in dp['question']:
                intros.append(
                    [
                        idx,
                        dp['qid'],
                        index,
                        dp['career'],
                        number,
                        dp['name'],
                        q.get('question')
                    ]
                )
                idx+=1
                number+=1

    introList_frame = pd.DataFrame(data=introLists, columns=IntroList_columns)
    intro_frame = pd.DataFrame(data=intros, columns=Intro_columns)

    print(intro_frame)
    # print(introList_frame)

    return {"lists": introList_frame, "intros" : intro_frame}


def dump_dataframes(dataframes):
    pd.to_pickle(dataframes, DUMP_FILE)


def load_dataframes():
   
    return pd.read_pickle(DUMP_FILE)


def main():

    print("[*] Parsing data...")
    data = import_data()            # 이러면 빅데이터를 panda 형식으로 넣어서 그걸 data에 넣어줌
    print("[+] Done")

    print("[*] Dumping data...")
    dump_dataframes(data)
    print(data)
    print("[+] Done\n")

    data = load_dataframes()
    
    print(data)
    


if __name__ == "__main__":
    main()
