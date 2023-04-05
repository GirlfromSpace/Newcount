from PyQt5 import QtWidgets, QtCore
from demo import Ui_MainWindow
from autorisation import Ui_Dialog
import sys
import openpyxl
import pandas as pd
from docxtpl import DocxTemplate
import Edit_win_open
import grafic
import setup_db
import add_row
from Edit_df_win import Ui_Edit_df_win
df = pd.read_excel("./database.xlsx")
# окно авторизации
class autorisation(QtWidgets.QDialog):
    def __init__(self):
        super(autorisation, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.checkpsw)

    # проверка данных
    def checkpsw(self):
        loginValue = self.ui.login.text()
        passwordValue = self.ui.password.text()
        if loginValue != 'admin' or passwordValue != '12345':
            QtWidgets.QMessageBox.information(self, 'Ошибка', 'Неправильный логин или пароль')
        else:
            self.gotowindow()

    # и переход к главному окну
    def gotowindow(self):
        self.close()
        self.MyWindow = mywindow()
        self.MyWindow.showMaximized()

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)
        setup_db.setup_table_data(self)
        # подключение меню для добавления строк
        self.ui_main.new_2.triggered.connect(self.go_to_edit_win)
        #add_row.add_to_qtablewidget(self, EditWindow.l)
        # кнопка меню для удаления строк
        self.ui_main.delete_2.triggered.connect(self.del_row)
        self.ui_main.save_file.triggered.connect(self.save_df)
        #Подключение к слоту внесения изменения в базу данных
        self.ui_main.jornal.triggered.connect(self.open_jornal)
        #подключение к слоту сохранения файла в excel
        self.ui_main.save_as.triggered.connect(self.save_as_excel)
        #сохранение отчета в ворд
        self.ui_main.report.triggered.connect(self.save_word)
    #функция перехода к окну добавления строк
    def go_to_edit_win(self):
        self.EdWindow = Edit_win_open.EditWindow()
        self.EdWindow.show()
    def del_row(self):
        self.GFWindow = grafic.PlotWindow()
        self.GFWindow.show()
    #функция выгружающая таблицу как excel файл
    def save_as_excel(self):
        rows = self.ui.tableWidget.rowCount()
        if not rows:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Нечего сохранять.')
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Excel', '.', 'Excel(*.xlsx)')
        if not path:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Не указан файл для сохранения.')
            return
        columnHeaders = []
        # создать список заголовков столбцов
        for j in range(self.ui.tableWidget.model().columnCount()):
            columnHeaders.append(self.ui.tableWidget.horizontalHeaderItem(j).text())
        df2 = pd.DataFrame(columns=columnHeaders)
        # создать набор записей объекта dataframe
        for row in range(self.ui.tableWidget.rowCount()):
            for col in range(self.ui.tableWidget.columnCount()):
                df2.at[row, columnHeaders[col]] = self.ui.tableWidget.item(row, col)
        df2.to_excel(path, index=False)
        msg = QtWidgets.QMessageBox.information(self, 'Ok', 'Файл успешно сохранен!')
    # Сохраненение данных и журнал изменений
    def open_jornal(self):
        print('Jornal')
    # Сохраненение данных и журнал изменений
    def save_df(self):
        rows = self.ui.tableWidget.rowCount()
        if not rows:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Нечего сохранять.')
            return
        columnHeaders = []
        # создать список заголовков столбцов
        for j in range(self.ui.tableWidget.model().columnCount()):
            columnHeaders.append(self.ui.tableWidget.horizontalHeaderItem(j).text())

        df2 = pd.DataFrame(columns=columnHeaders)

        # создать набор записей объекта dataframe
        for row in range(self.ui.tableWidget.rowCount()):
            for col in range(self.ui.tableWidget.columnCount()):
                df2.at[row, columnHeaders[col]] = self.ui.tableWidget.item(row, col)
        path = "./database.xlsx"
        df.to_excel(path, index=False)
        msg = QtWidgets.QMessageBox.information(self, 'Ok', 'Файл успешно сохранен!')
    # функция выгружающая отчет в word
    def save_word(self):
        df3 = df.values.tolist()
        print(df3)
        data_for_word =[]
        for item in df3:
            data_for_word.append({
            'name': item[0],
            'mass': item[1],
            'x_val': item[2],
            'y_val': item[3],
            'z_val': item[4],
            'Ix_val': item[5],
            'Iy_val': item[6],
            'Iz_val': item[7],
            'Iyz_val': item[8],
            'Izx_val': item[9],
            'Ixy_val': item[10]
            })

        doc = DocxTemplate("template.docx")
        context = {'tbl_contents': data_for_word}
        print (context)
        doc.render(context)
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Docx', '.', 'Docx(*.docx)')
        if not path:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Не указан файл для сохранения.')
            return
        doc.save(path)
class EditWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.line_data = []
        super(EditWindow, self).__init__()
        self.ui = Ui_Edit_df_win()
        self.ui.setupUi(self)
        self.ui.save_btn.clicked.connect(self.add_row)

    #добавляем строку из lineEdit
    def add_row(self):
        Name = self.ui.name_Value.text()
        Num = self.ui.num_Value.text()
        Mass = self.ui.mass_Value.text()
        X = self.ui.x_Value.text()
        Y = self.ui.y_Value.text()
        Z = self.ui.z_Value.text()
        Ixx = self.ui.Ixx_Value.text()
        Iyy = self.ui.Iyy_Value.text()
        Izz = self.ui.Izz_Value.text()
        Iyz = self.ui.Iyz_Value.text()
        Izx = self.ui.Izx_Value.text()
        Ixy = self.ui.Ixy_Value.text()
        self.line_data = [Name, Num, Mass, X, Y, Z, Ixx, Iyy, Izz, Iyz, Izx, Ixy]
        j = 0
        for i in range(len(self.line_data)):
            if self.line_data[i]:
                j += 1
        if j == len(self.line_data):
            df.loc[len(df.index)] = [Name, Num, Mass, X, Y, Z, Ixx, Iyy, Izz, Iyz, Izx, Ixy]
        else:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните все пустые поля!')
            return
        mywindow.save_df(self)
        setup_db.setup_table_data(self)
if __name__=="__main__":
    app = QtWidgets.QApplication([])
    applicaton = autorisation()
    applicaton.show()

    sys.exit(app.exec())
