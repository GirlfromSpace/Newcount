import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QPixmap, QImage, QIcon, QColor
import openpyxl
from demo import Ui_MainWindow
import datetime
from jornal import Ui_jornal
user = 'Бабешкина Е.Н.'
class TestModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        super().__init__(parent)

        self.__data = data
        self.__headers = headers
        self.__image_file = 'Ok.png'
        self.getPixmap()

    def getPixmap(self):
        try:
            with open(self.__image_file):
                image = QImage(self.__image_file)
                self.__pixmap = QPixmap(image)
        except FileNotFoundError:
            self.__pixmap = QPixmap(26, 26)
            self.__pixmap.fill(QColor('green'))
            print(self.__pixmap)

    def rowCount(self, parent=QModelIndex()):
        return len(self.__data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.__data[0])

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.__data[row][column]

        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.__data[row][column]

        if role == Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            return self.__data[row][column]

        if role == Qt.DecorationRole:
            icon = QIcon(self.__pixmap)
            return icon

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.__data[row][column] = value
            self.dataChanged.emit(index, index)
            line = f'ИЗМЕНЕНА ЯЧЕЙКА: строка:{row} колонка:{column} пользователем {user} в {datetime.datetime.now()}'
            print(line)
            file = open("jornal.txt", "a")
            file.write(line + '\n'+'\n')
            file.close()
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return 'Not implemented'
            else:
                return  str(section + 1)

    def insertRows(self, position, rows, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        for j in range(rows):
            default_row = [f'row{i}-{j}' for i in range(self.columnCount())]
            self.__data.insert(position, default_row)
        self.endInsertRows()
        line =f'ДОБАВЛЕНА СТРОКА:{position+1} пользователем {user} в {datetime.datetime.now()}'
        print(line)
        file = open("jornal.txt", "a")
        file.write(line + '\n'+ '\n')
        file.close()
        return True

    # +++
    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for _ in range(rows):
            del self.__data[position]
        self.endRemoveRows()
        line =f'УДАЛЕНА СТРОКА:{position+1} пользователем {user} в {datetime.datetime.now()}'
        print(line)
        file = open("jornal.txt", "a")
        file.write(line + '\n'+'\n')
        file.close()
        return True

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        path = "./database.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        list_values = list(sheet.values)
        data = list_values[1:]
        headers = list_values[0]
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)
        self.model = TestModel(data, headers)  # MyTableModel(data, headers)
        self.ui_main.tableView.setModel(self.model)

        self.ui_main.del_row.clicked.connect(lambda: self.model.removeRows(0, 1))
        self.ui_main.add_row.clicked.connect(lambda: self.model.insertRows(0, 1))
        # Подключение к слоту внесения изменения в базу данных
        self.ui_main.jornal.triggered.connect(self.open_jornal)
        #Сохранение данных
        self.ui_main.save_file.triggered.connect(self.save_df)
    def open_jornal(self):
        self.jornal = jornal()
        self.jornal.show()
    def save_df(self):
        pass

class jornal(QtWidgets.QTextEdit):
    def __init__(self):
        super(jornal, self).__init__()
        self.ui_sec = Ui_jornal()
        self.ui_sec.setupUi(self)
        file = open("./jornal.txt", "r")
        fil = file.read()
        self.ui_sec.textEdit.setText(fil)
        print('Jornal')





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.showMaximized()
    sys.exit(app.exec_())