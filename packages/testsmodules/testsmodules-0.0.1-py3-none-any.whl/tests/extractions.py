import os
import json
import re
from .paths import Paths
from PyPDF2 import *

class Extractions:
    def __init__(self) -> None:
        pass

    def save_into_json(self, fileName, data):
        try:
            if not os.path.exists(fileName):
                raise FileExistsError
            with open(fileName,'r+') as file:
                a = json.load(file)
                for d in data:
                    a.append(d)
                file.seek(0)
                json.dump(a, file, indent = 2)
        except json.decoder.JSONDecodeError:
            with open(fileName,'w') as file:
                json.dump(data, file, indent = 2)
        except FileExistsError:
            print("Cannot find this file!")

    def get_phrases(self, fileName, column = None):
        try:
            if not os.path.exists(fileName):
                raise FileNotFoundError
            availableExtensions = [".txt", ".csv", ".xlsx"]
            flag = False
            e = ""
            for extension in availableExtensions:
                le = -1 * len(extension)
                e = fileName[le:]
                if e == extension:
                    flag = True
                    break
            if not flag:
                raise NameError
            else:
                p = Paths()
                if e == ".txt":
                    return p.data_txt(fileName)
                elif e == ".csv":
                    return p.data_csv(fileName, column)
                elif e == ".xlsx":
                    return p.data_excel(fileName, column)
        except NameError:
            print("Cannot read this type of file!")
        except FileNotFoundError:
            print("Cannot find this file!")

    def extract(self, phrases, pdfFile):
        try:
            if pdfFile[-4:] != ".pdf":
                pdfFile += ".pdf"
            if not os.path.exists:
                raise FileNotFoundError
            result = []
            doc = PdfReader(pdfFile, strict=False)
            pages = len(doc.pages)
            for page in range(pages):
                text = doc.pages[page].extract_text()
                for phrase in phrases:
                    found_phrase_count = len(re.findall(phrase.lower(), text.lower()))
                    if found_phrase_count != 0:
                        if len(result) == 0:
                            result.append({"page":page, "phrases":[{"phrase" : phrase.lower(), "count" : found_phrase_count}]})
                        else:
                            if result[-1]["page"] == page:
                                result[-1]["phrases"].append({"phrase" : phrase.lower(), "count" : found_phrase_count})
                            else:
                                result.append({"page":page, "phrases":[{"phrase" : phrase.lower(), "count" : found_phrase_count}]})

            return result
        except FileNotFoundError:
            print("Cannot find this file!")

    def search_phrases_in_PDF(self, pdfFile : str, phrases: list):
        try:
            if not os.path.exists(pdfFile):
                raise FileNotFoundError
            result = []
            reader = PdfReader(pdfFile)
            for phrase in phrases:
                re = self.search_phrase(reader, phrase)
                if len(re) != 0:
                    result.append({
                        "phrase" : phrase,
                        "pages" : re
                    })
            return result
        except FileNotFoundError:
            print("Cannot find this file!")

    def search_phrase(self, reader : PdfReader, phrase : str):
        result = []
        for p in range(len(reader.pages)):
            
            page = reader.pages[p]
            parts = []
            def visitor_body(text, cm, tm, fontDict, fontSize):
                y = tm[5]
                if y > 50 and y < 720:
                    parts.append(text)
            page.extract_text(visitor_text=visitor_body)
            text_body = "".join(parts)

            re = self.search_phrase_in_page(text_body, phrase)
            if len(re) != 0:
                result.append({
                        "page" : p,
                        "lines" : re
                    })
        return result
    
    def search_phrase_in_page(self,text : str, phrase : str):
        words = re.split(" ", phrase)
        result = []
        lines = re.split("\n", text)
        
        for i, v in enumerate(lines):
            if v.replace(" ", "") == "":
                while True:
                    lines.pop(i)
                    if i == len(lines) or lines[i].replace(" ", "") != "":
                        break

        if len(words) == 1:
            for index, line in enumerate(lines):
                foundWord = len(re.findall(words[0], line))
                if foundWord != 0:
                    result.append(index)
        else:
            for i, v in enumerate(lines):
                lines[i] = re.split(" ", v)
            for i in range(len(lines)):
                for j in range(len(lines[i])):
                    if len(re.findall(words[0], lines[i][j])) != 0:
                        if i == len(lines)-1 and j > len(lines[i])-len(words):
                            pass
                        else:
                            currentWord = lines[i][j]
                            if currentWord.find(".") == len(currentWord)-1 or currentWord.find(".") == len(currentWord)-1:
                                pass
                            else:
                                currentWord = currentWord.replace(".", "")
                                currentWord = currentWord.replace(",", "")
                                if currentWord != words[0]:
                                    pass
                                else:
                                    currentLineIndex = i
                                    currentWordIndex = j
                                    getWords = []
                                    for c in range(len(words)):
                                        getWords.append(lines[currentLineIndex][currentWordIndex])
                                        currentWordIndex += 1
                                        if currentWordIndex >= len(lines[currentLineIndex]):
                                            currentLineIndex += 1
                                            currentWordIndex = 0
                                        if currentLineIndex >= len(lines):
                                            break
                                    if len(getWords) != len(words):
                                        pass
                                    else:
                                        if len(words) == 2:
                                            if getWords[-1].find(".") == 0 or getWords[-1].find(",") == 0:
                                                pass
                                            else:
                                                getWords[1] = getWords[1].replace(".", "")
                                                getWords[1] = getWords[1].replace(",", "")
                                                if getWords[1] == words[1]:
                                                    result.append(i)
                                        else:
                                            if getWords[-1].find(".") == 0 or getWords[-1].find(",") == 0:
                                                pass
                                            else:
                                                flag = True
                                                for midWordIndex in range(1, len(words)-1):
                                                    if getWords[midWordIndex].find(".") != -1 or getWords[midWordIndex].find(",") != -1:
                                                        flag = False
                                                        break
                                                    if getWords[midWordIndex] != words[midWordIndex]:
                                                        flag = False
                                                        break
                                                if flag:
                                                    lastWord = getWords[-1]
                                                    lastWord = lastWord.replace(".", "")
                                                    lastWord = lastWord.replace(",", "")
                                                    if lastWord == words[-1]:
                                                        result.append(i)
        return result