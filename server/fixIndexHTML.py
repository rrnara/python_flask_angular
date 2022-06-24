import os
import re
from pathlib import Path

currPath = Path(os.getcwd())
appPath = currPath.absolute().__str__()

# use this function to find all 'href' and 'src' urls in index.html
def find_all(html: str, sub: str):
    start = 0
    indexList = []
    while True:
        location = html.find(sub, start)
        # print(location)
        start = location + 1
        if location == -1: break
        indexList.append(location)
    return indexList

# this function adds a '?' in front off all href and src urls in index.html so that they are requested as args to root url
def fixIndexHTMLdoc():
    staticIndex = []
    offset = 0
    staticURLref = ["href=\"", "src=\""]
    with open(f"{appPath}/app/dist/app/index.html", "r") as main:
        indexHTML = main.read()
    # print(indexHTML)
    for staticRef in staticURLref:
        indexes = find_all(indexHTML, staticRef)  # find all static urls
        staticIndex += indexes
    staticIndex.pop(0)  # remove base reference
    # print(staticIndex)
    for index in staticIndex:
        sliced_str = indexHTML[index:index+15]
        re_search = re.search(r"(href|src)=\"http(s?)://", sliced_str)
        if re_search is not None or indexHTML[index + 5 + offset] == "?" or indexHTML[index + 6 + offset] == "?":
            pass
            # print(f"already done: {index}")
        else:
            # print(f"add ? here: {index}")
            if indexHTML.find(staticURLref[0], index) != -1:
                # fix href tags
                indexHTML = indexHTML[0:index + 6 + offset] + "?" + indexHTML[index + 6 + offset:]
                offset += 1
            else:
                # fix src tags
                indexHTML = indexHTML[0:index + 5 + offset] + "?" + indexHTML[index + 5 + offset:]
                offset += 1

    with open(f"{appPath}/app/dist/app/index.html", "w") as main:
        indexHTML = main.write(indexHTML)
