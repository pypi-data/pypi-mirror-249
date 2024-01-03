import openpyxl
import csv
import os
import json
import requests

class Paths:
    def __init__(self) -> None:
        pass

    def data_txt(self, fileName):
        data = []
        with open(fileName, "r", encoding="utf-8") as f:
            data=f.read().splitlines()
        return data
    
    def data_csv(self, fileName, column):
        data = []
        with open(fileName, newline='', encoding="utf-8") as f:
            d = csv.reader(f)
            for row in d:
                data.append(row)
        if column is None:
            for row in data:
                data.append(row[0])
        else:
            try:
                index = data[0].index(column)
                for r in range(1,len(data)):
                    data[r-1] = data[r][index]
                data = data[:-1]
            except:
                pass
        return data
    
    def data_excel(self, fileName, column):
        data = []
        dataframe = openpyxl.load_workbook(fileName).active
        for r in dataframe:
            d = []
            for c in r:
                d.append(c.value)
            data.append(d)
        if column is None:
            for row in data:
                data.append(row[0])
        else:
            try:
                index = data[0].index(column)
                for r in range(1,len(data)):
                    data[r-1] = data[r][index]
                data = data[:-1]
            except:
                pass
        return data
    
    def check_extensions(self, fileName):
        try:
            if os.path.exists(fileName):
                availableExtensions = [".txt", ".csv", ".xlsx"]
                extension = fileName[-4:]
                if extension in availableExtensions:
                    return extension
                else:
                    extension = fileName[-5:]
                    if extension in availableExtensions:
                        return extension
                    else:
                        raise NameError
            else:
                raise FileNotFoundError
        except NameError:
            print("Cannot read this type of file!")
        except FileNotFoundError:
            print("Cannot find this file!")

    def check_dois(self, doi):
        if "doi.org" not in doi:
            url = 'http://dx.doi.org/' + doi
        else:
            url = doi
        headers = {"accept": "application/x-bibtex"}
        r = requests.get(url, headers = headers)
        if r.status_code == 200:
            return True
        else:
            return False
    
    def check_txt(self, fileName):
        try:
            if fileName[-4:] != ".txt":
                fileName = fileName + ".txt"
            if not os.path.exists:
                raise FileNotFoundError
            true_data = []
            false_data = []
            data = self.data_txt(fileName)
            for d in data:
                if self.check_dois(d):
                    true_data.append(d)
                else:
                    false_data.append(d)
            return true_data, false_data
        except FileNotFoundError:
            print("Cannot find this file!")

    def check_csv(self, fileName, column=None):
        try:
            if fileName[-4:] != ".csv":
                fileName = fileName + ".csv"
            if not os.path.exists:
                raise FileNotFoundError
            true_data = []
            false_data = []
            data = self.data_csv(fileName, column)
            for d in data:
                if self.check_dois(d):
                    true_data.append(d)
                else:
                    false_data.append(d)
            return true_data, false_data
        except FileNotFoundError:
            print("Cannot find this file!")
    
    def check_xlsx(self, fileName, column=None):
        try:
            if fileName[-5:] != ".xlsx":
                fileName = fileName + ".xlsx"
            if not os.path.exists:
                raise FileNotFoundError
            true_data = []
            false_data = []
            data = self.data_excel(fileName, column)
            for d in data:
                if self.check_dois(d):
                    true_data.append(d)
                else:
                    false_data.append(d)
            return true_data, false_data
        except FileNotFoundError:
            print("Cannot find this file!")

    def save_files(self):
        if not os.path.exists("output"):
            os.mkdir("output")
            print("Folder output is created!")
        if not os.path.exists("output/PDF files"):
            os.mkdir("output/PDF files")
            print("Folder output/PDF files is created!")
        if not os.path.exists("output/Database.json"):
            with open("output/Database.json", "w") as f:
                json.dump([], f, indent=0)
                print("File output/Database.json is created!")
        if not os.path.exists("output/WrongDOI.json"):
            with open("output/WrongDOI.json", "w") as f:
                json.dump([], f, indent=0)
                print("File output/WrongDOI.json is created!\n")      
        return {
            "folder" : "output",
            "folderPDF" : "output/PDF files",
            "databaseFile" : "output/Database.json",
            "wrongDOIFile" : "output/WrongDOI.json"
        }