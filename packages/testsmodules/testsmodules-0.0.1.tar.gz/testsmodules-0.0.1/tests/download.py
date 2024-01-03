import os
import requests
from bs4 import BeautifulSoup
import json

class Download:
    def __init__(self):
        self.setUpScihub = False
        self.scihubAccess = False
        self.scihubUrl = ""
        self.folderName = None
        self.fileName = None
        self.isDownloaded = False
        self.isRepeatable = False
        self.SCIHUB = "https://sci-hub.41610.org/"
        self.CROSSREF = "https://api.crossref.org/works/"
        self.HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"}

    def set_is_repeatable(self, boolean):
        self.isFileNameRepeatable = boolean

    def set_save_at_folder(self, folderName):
        self.folderName = folderName
    
    def set_save_file_name(self, fileName):
        self.fileName = fileName

    def crossref(self, doi, folderName = None, fileName = None):
        if "doi.org" not in doi:
            doi = "http://dx.doi.org/" + doi
        r = requests.get(self.CROSSREF+doi)
        info = json.loads(r.text).get("message")
        title = ""
        if fileName is None:
            try:
                title = info["title"][0]
            except:    
                title = None
        links = info.get("link")
        if links is not None:
            for link in links:
                url = link["URL"]
                r = requests.get(url, headers=self.HEADERS)
                contentType = r.headers.get("Content-Type")
                if "application/pdf" in contentType:
                    self.save_file(folderName, fileName, title, r.content)
                if self.isDownloaded:
                    break

    def scihub(self, doi, folderName=None, fileName=None):
        if not self.setUpScihub:
            self.setScihub()
        if self.scihubAccess:
            url = self.scihubUrl + "/" + doi
            r = requests.get(url, headers=self.HEADERS)
            contentType = r.headers.get("Content-Type")
            title = ""
            if fileName is None:
                try:
                    re = requests.get(self.CROSSREF+doi)
                    title = json.loads(re.text).get("message").get("title")[0]
                except:    
                    title = None
            if "application/pdf" in contentType:
                self.save_file(folderName, fileName, title, r.content)
            else:
                url = self.get_url(r.text)
                if url != "":
                    r = requests.get(url, headers=self.HEADERS)
                    contentType = r.headers.get("Content-Type")
                    if "application/pdf" in contentType:
                        self.save_file(folderName, fileName, title, r.content)

    def download_from_url(self, url, folderName=None, fileName=None):
        if folderName is None:
            path = self.folderName
        else:
            path = folderName
        if os.path.exists(path):
            if path[-1] != "/":
                path += "/"
        else:
            raise ValueError("Cannot find folder to save at!")
        if fileName is None:
            fileName = self.fileName
        if fileName is None:
            fileName = url.split("/")[-1]
        pathFileName = self.prepare_pathFileName(path, fileName)
        if pathFileName is None:
            self.isDownloaded = True
        else:
            r = requests.get(url)
            with open(pathFileName, "wb") as f:
                f.write(r.content)
            self.isDownloaded = True
                
    def prepare_pathFileName(self, path, fileName):
        errorChar = ["<",">","*","?",'"',":","|", "/", "\\"]
        for e in errorChar:
            if e in fileName:
                if e == "<":
                    fileName = fileName.replace(e,"(")
                elif e== ">":
                    fileName = fileName.replace(e,")")
                else:
                    fileName = fileName.replace(e,"_")
        if fileName[-4:] != ".pdf":
            fileName = fileName + ".pdf"
        if os.path.exists(path + fileName):
            if self.isRepeatable:
                count = 1
                while os.path.exists(path + fileName[:-4] + "(" + str(count) + ")" + ".pdf"):
                    count += 1
                fileName = fileName[:-4] + "(" + str(count) + ")" + ".pdf"
            else:
                return None
        return path + fileName

    def save_file(self, folderName, fileName, title, content):
        try:
            if folderName is None:
                path = self.folderName
            else : 
                path = folderName
            if os.path.exists(path):
                if path[-1] != "/":
                    path += "/"
            else:
                raise ValueError
            if fileName is None:
                fileName = self.fileName
            if fileName is None:
                fileName = title
            if fileName is None:
                fileName = "article"
            self.fileName = fileName
            pathFileName = self.prepare_pathFileName(path, fileName)
            if pathFileName is None:
                self.isDownloaded = True
            else:
                with open(pathFileName, "wb") as f:
                    f.write(content)
                self.isDownloaded = True
        except ValueError:
            print("Cannot find folder to save at!")

    def setScihub(self):
        try:
            r = requests.get(url=self.SCIHUB, headers=self.HEADERS)
            html = BeautifulSoup(r.text, "html.parser")
            links = []
            for ul in html.findAll("ul"):
                for a in ul.findAll("a"):
                    link = a.get("href")
                    if link.startswith("https://sci-hub.") or link.startswith("http://sci-hub."):
                        links.append(link)
            for link in links:
                try:
                    r = requests.get(link, headers=self.HEADERS)
                    if r.status_code == 200:
                        self.scihubUrl = link
                        self.scihubAccess = True
                        break
                except:
                    pass
            self.setScihub = True
            if not self.scihubAccess:
                print("\nNo working Sci-Hub instance found!\nIf in your country Sci-Hub is not available consider using a VPN or a proxy")
        except:
            self.setScihub = True
            print("Cannot use scihub website in this internet server!")

    def get_url(self, text):
        pdfUrl = ""
        html = BeautifulSoup(text, "html.parser")
        idPdf = html.find(id="pdf")
        idPlugin = html.find(id="plugin")
        if idPdf is not None:
            pdfUrl = idPdf.get("src")
        elif idPlugin is not None:
            pdfUrl = idPlugin.get("src")
        if pdfUrl != "" and pdfUrl[0] != "h":
            pdfUrl = "https:" + pdfUrl
        return pdfUrl