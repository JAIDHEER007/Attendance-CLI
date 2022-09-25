from bs4 import BeautifulSoup as BS

class Student:
    def __init__(self, rawData: str) -> None:
        self.rawData = rawData
        self.studentData = {}
        self.attendanceData = []
        self.totalData = []

        self.parseData()

    def parseData(self):
        soup = BS(self.rawData, 'html.parser')

        tables = soup.find_all('table')[2:]

        for row in tables[0].find_all('tr'):
            cellData = row.find_all('td')[0::2]
            self.studentData[cellData[0].text] = cellData[1].text

        for row in tables[1].find_all('tr'):
            rowData = []
            for cell in row.find_all('td'):
                rowData.append(cell.text)
            self.attendanceData.append(rowData)
        self.totalData = self.attendanceData[-1]
        self.attendanceData.pop(-1)
