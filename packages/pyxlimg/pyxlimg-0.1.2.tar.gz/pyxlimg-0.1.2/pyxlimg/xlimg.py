from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Union
import zipfile
from PIL import Image
import io
import re

if TYPE_CHECKING:
    from xlimg import Element


class Element:
    def __init__(
        self,
        name: str,
        parent: Element = None,
        root: Element = None,
    ) -> None:
        self.name = name
        if parent != None:
            self.parent = parent
        if root != None:
            self.root = root

    @property
    def sheetFolder(self) -> str:
        return "xl/worksheets/"

    @property
    def wookbookinfo(self) -> str:
        return "xl/workbook.xml"

    @property
    def relayFolder(self) -> str:
        return "xl/worksheets/_rels/"

    @property
    def drawingFolder(self) -> str:
        return "xl/drawings/_rels/"

    @property
    def mediaFolder(self) -> str:
        return "xl/media/"

    @property
    def sheetfileExtension(self) -> str:
        return ".xml"

    @property
    def relayfileExtension(self) -> str:
        return ".xml.rels"

    @property
    def drawingfileExtension(self) -> str:
        return ".xml.rels"


class Picture(Element):
    def Image(self) -> Image.Image:
        z = zipfile.ZipFile(self.root.name)
        img: Image.Image = Image.open(io.BytesIO(z.read(self.mediaFolder + self.name)))
        z.close()
        # img.show()
        return img


class Sheet(Element):
    def __init__(
        self, name: str, displayName: str, parent: Element, root: Element
    ) -> None:
        super().__init__(name=name, parent=parent, root=root)
        self.displayName = displayName
        self.Pictures = self.__Pictures()

    def __Pictures(self) -> list[Picture]:
        try:
            f = self.root.zf.open(
                self.relayFolder + self.name + self.relayfileExtension, "r"
            )
            relsdata: str = f.read(-1)
            f.close()
        except KeyError:
            relsdata: str = ""
        relsdata: str = str(relsdata)
        startindex = str(relsdata).find('/drawing"', 1)
        if startindex == -1:
            return []
        startindex = str(relsdata).find("Target=", startindex)
        finalindex = str(relsdata).find('"/>', startindex)
        startindex = str(relsdata).rfind("/", startindex, finalindex) + 1
        finalindex = str(relsdata).rfind(".", startindex, finalindex)
        self.drawingfilename = relsdata[startindex:finalindex]
        res: list[Picture] = []
        buf: Union[Picture, None] = None
        while True:
            buf = self.__Picture(len(res))
            if buf.name == "":
                break
            res.append(buf)
        # todo drawing relation
        return res

    def __Picture(self, Index: int) -> Picture:
        try:
            f = self.root.zf.open(
                self.drawingFolder + self.drawingfilename + self.drawingfileExtension,
                "r",
            )
            relsdata: str = f.read(-1)
            f.close()
        except KeyError:
            relsdata: str = ""
        relsdata: str = str(relsdata)
        startindex: int = 1
        for time in range(Index + 1):
            startindex = relsdata.find('/image"', startindex + 1)
            if startindex == -1:
                return Picture(name="", parent=self, root=self.parent)
        startindex = relsdata.find("Target=", startindex)
        finalindex = relsdata.find('"/>', startindex)
        startindex = relsdata.rfind("/", startindex, finalindex) + 1
        return Picture(relsdata[startindex:finalindex], parent=self, root=self.parent)


class ImageBook(Element):
    def __init__(self) -> None:
        super().__init__(name="")
        self.zf: zipfile.ZipFile
        self.Sheets: list[Sheet] = []

    def open(self, fileName: str) -> None:
        self.zf: zipfile.ZipFile = zipfile.ZipFile(fileName)
        self.name = fileName
        self.Sheets = self.__Sheets()

    def __del__(self) -> None:
        self.zf.close()

    def __Sheets(self) -> list[Sheet]:
        res: list[Sheet] = []
        DisplayNames: list[str] = self.getDisplayNames()
        for item in self.getSheetNames():
            res.append(
                Sheet(
                    name=item,
                    displayName=DisplayNames[int(re.sub(r"\D", "", item)) - 1],
                    parent=self,
                    root=self,
                )
            )
        return res

    def getDisplayNames(self) -> list[str]:
        res: list[str] = []
        try:
            f = self.zf.open(self.wookbookinfo, "r")
            relsdata: str = f.read(-1)
            f.close()
        except KeyError:
            relsdata: str = ""
        relsdata = str(relsdata)
        startIndex: int = relsdata.find("<sheets>")
        finalIndex: int = relsdata.find("</sheets>")
        cutFinishIndex = startIndex
        while True:
            findString = 'name="'
            cutStartIndex = relsdata.find(findString, cutFinishIndex, finalIndex)
            if cutStartIndex == -1:
                break
            cutStartIndex += len(findString)
            findString = '"'
            cutFinishIndex = relsdata.find(findString, cutStartIndex, finalIndex)
            res.append(relsdata[cutStartIndex:cutFinishIndex])
        return res

    def getImageList(self) -> list[str]:
        res: list[str] = []
        for name in self.__zf.namelist():
            if name.startswith(self.mediaFolder):
                res.append(name)
        return res

    def getImagePathsFromSheet(self):
        pass

    def getSheetPaths(self) -> list[str]:
        res: list[str] = []
        for name in self.zf.namelist():
            if name.startswith(self.sheetFolder):
                if not name.startswith(self.relayFolder):
                    res.append(name)
        return res

    def getSheetNameFromSheetPath(self, sheet: str) -> str:
        return sheet.replace(self.sheetFolder, "").replace(self.sheetfileExtension, "")

    def getSheetNames(self) -> list[str]:
        source: list[str] = self.getSheetPaths()
        response: list[str] = []
        for item in source:
            response.append(self.getSheetNameFromSheetPath(item))
        return response

    def getRelayPaths(self) -> list[str]:
        source: list[str] = self.getSheetNames
        responcse: list[str] = []
        for item in source:
            responcse.append(self.getRelayPathFromSheetName(item))

    def getRelayPathFromSheetName(self, sheetname: str) -> str:
        return self.relayFolder + sheetname

    def getImagePathsFromRelay():
        pass


if __name__ == "__main__":
    pass
