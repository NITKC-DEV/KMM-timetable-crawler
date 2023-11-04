import requests as req
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
import time

FETCH_SLEEP = 0
room = ["特別教室", "階段教室", "ネットワーク情報センター", "第1講義室", "第2講義室", "第3講義室", "第4講義室",
        "第5講義室", "第6講義室", "専攻科講義室A", "専攻科講義室B",
        "専攻科ゼミ室A", "共通ゼミ室A", "マルチメディア講義室A", "マルチメディア講義室B", "多目的室A,B(講義棟C)",
        "M製図室", "E実験室", "D実験室",
        "実習工場", "J計算機演習室", "J回路実験室", "コミュニティールームB", "コミュミニティルームD", "CAD室",
        "校内外フィールド", "C都市創造実験室・レクチャー室", "水理実験室",
        "図書館フリー閲覧室", "学友会研修室1", "学友会館研修室2/3", "学友会館研修室4", "物理実験室", "化学実験室",
        "ものづくり実習室"]
departmentName = [
    {
        "name": "機械工学科",
        "alphabet": 'M'
    },
    {
        "name": "電気電子工学科",
        "alphabet": 'E'
    },
    {
        "name": "電子制御工学科",
        "alphabet": 'D'
    },
    {
        "name": "情報工学科",
        "alphabet": 'J'
    },
    {
        "name": "環境都市工学科",
        "alphabet": 'C'
    }
]


def generation_progress_bar(num):
    result = "["
    done = int(30 * num)
    for count in range(done):
        result += "#"
    for count in range(30 - done):
        result += "-"
    result += "] "

    if done == 30:
        result += "done"
    else:
        result += str(num * 100 * 100 // 1 / 100) + "%"
    return result


def generation_select_menu(title, options):
    root = Tk()
    root.title(title)

    # Frame
    frame = ttk.Frame(root, padding=10)
    frame.grid()

    # Combobox
    v = StringVar()
    cb = ttk.Combobox(
        frame, textvariable=v,
        values=options, width=10)
    cb.set(options[len(options)-1])
    cb.bind(
        '<<ComboboxSelected>>',
        lambda e: print('v=%s' % v.get()))
    cb.grid(row=0, column=0)

    # Button
    button1 = ttk.Button(
        frame, text='OK',
        command=lambda: print('v=%s' % v.get()))
    button1.grid(row=0, column=1)
    root.mainloop()


print("------------------------------")
print("KMM-timetable-crawler v0.0.0\ndeveloped by kokastar")
print("------------------------------")

print("年度を指定してください", end=":")
year: str = input()

subjectElements = []
allSubjectSiz = 0
print("\nfetching syllabus department data...")
print(generation_progress_bar(0), end="")
for i in range(5):
    page = req.get("https://syllabus.kosen-k.go.jp/Pages/PublicSubjects?school_id=14&department_id=1" + str(
        i + 1) + "&year=" + year + "&lang=ja")
    soup = BeautifulSoup(page.text, "html.parser")
    mcc_show = soup.find_all(class_="mcc-show")
    subjectElements.append(mcc_show)
    allSubjectSiz += len(mcc_show)
    print("\r" + generation_progress_bar((i + 1) / 5), end="")
    time.sleep(FETCH_SLEEP)

subjectData = [[], [], [], [], []]
fetchedSubject = 0
print("\nfetching subjects data...")
print(generation_progress_bar(0), end="")
for i in range(5):
    #for j in range(len(subjectElements[i])):
    for j in range(1):
        try:
            url = "https://syllabus.kosen-k.go.jp" + subjectElements[i][j].attrs['href']
            page = req.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            tdData = soup.find_all("td")
            subjectName = soup.find("h1").string
            teachers = []
            for k in soup.find_all(id="Teachers"):
                teachers.append(k.string)
            subjectData[i].append({"subjectName": subjectName, "subjectId": str(i + 1) + tdData[10].string,
                                           "professor": teachers, "url": url, "room": ""})
        except KeyError:
            a = 0
            # subjectPageData.append()
        fetchedSubject += 1
        print("\r" + generation_progress_bar(fetchedSubject / allSubjectSiz), end="")
        time.sleep(FETCH_SLEEP)

for i in subjectData:
    grade = int(i[0]["subjectId"]) // 10
    department = int(i[0]["subjectId"]) % 10 - 1
    className = str(grade) + "年" + departmentName[department]["name"]
    option = room
    option.append(className)
    generation_select_menu(title=className + " " + i[0]["subjectName"], options=option)
