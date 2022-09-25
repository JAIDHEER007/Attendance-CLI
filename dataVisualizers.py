class dataVisualizer:
    def __init__(self, student):
        self.__student = student

    def printAttPercent(self):
        print("Name:", self.__student.studentData['Student Name'])
        print("Roll Number:", self.__student.studentData['RollNo'])
        print("Attendance Percent:", self.__student.totalData[-1], "%")
    

    def printAttTable(self):
        print("Name:", self.__student.studentData['Student Name'])
        print("Roll Number:", self.__student.studentData['RollNo'])

        rows, cols = len(self.__student.attendanceData), len(self.__student.attendanceData[0])
        colWidths = [-1] * cols
        colWidthSum = 0
        for i in range(cols):
            for j in range(rows):
                colWidths[i] = max(len(self.__student.attendanceData[j][i]), colWidths[i])
            colWidths[i] += 4
            colWidthSum += colWidths[i]

        for i in range(rows):
            rowView = []
            print('-' * (colWidthSum + 6))
            for j in range(cols):
                rowView.append(self.__student.attendanceData[i][j].center(colWidths[j], ' '))
            print("|", '|'.join(rowView), "|", sep='')
        print('-' * (colWidthSum + 6))

        totalView = []
        totalView.append(self.__student.totalData[0].center((colWidths[0] + colWidths[1] + 1), ' '))
        totalView.append(self.__student.totalData[1].center(colWidths[2], ' '))
        totalView.append(self.__student.totalData[2].center(colWidths[3], ' '))
        totalView.append(self.__student.totalData[3].center(colWidths[4], ' '))

        print("|", '|'.join(totalView), "|", sep='')
        print('-' * (colWidthSum + 6))
