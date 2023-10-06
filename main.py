import requests as req
from bs4 import BeautifulSoup
import re


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
        result += str(num * 100) + "%"
    return result


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

subjectData = [{},{},{},{},{}]
fetchedSubject = 0
print("\nfetching subjects data...")
print(generation_progress_bar(0), end="")
for i in range(5):
    for j in range(len(subjectElements[i])):
        try:
            url = "https://syllabus.kosen-k.go.jp" + subjectElements[i][j].attrs['href']
            page = req.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            tdData = soup.find_all("td")
            subjectName = soup.find("h1").string
            teachers = []
            for k in soup.find_all(id="Teachers"):
                teachers.append(k.string)
            subjectData[i][subjectName] = {"subjectName": subjectName, "subject_id": str(i+1) + tdData[10].string, "professor": teachers, "url":url}
            print("a")
        except KeyError:
            print("error")
            #subjectPageData.append()
        fetchedSubject += 1
        print("\r" + generation_progress_bar(fetchedSubject / allSubjectSiz), end="")