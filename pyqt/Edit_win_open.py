from Edit_df_win import Ui_Edit_df_win
from PyQt5 import QtWidgets
import pandas as pd
from demo import Ui_MainWindow

line_data = []
df = pd.read_excel("C:/Users/User/pyqt/database.xlsx")
class EditWindow(QtWidgets.QMainWindow):
    def __init__(self):
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
        line_data = [Name, Num, Mass, X, Y, Z, Ixx, Iyy, Izz, Iyz, Izx, Ixy]
        print(len(line_data))
        j = 0
        for i in range(len(line_data)):

            if line_data[i]:
                j += 1
        print(j)
        if j == len(line_data):
            df.loc[len(df.index)] = [Name, Num, Mass, X, Y, Z, Ixx, Iyy, Izz, Iyz, Izx, Ixy]
            print(df)

        else:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните все пустые поля!')
            return
    def add_to_qtablewidget(self):
        rowPosition = self.table.rowCount()  # Определение количества строк в таблице
        self.table.insertRow(rowPosition)  # Вставка строки
        new = rowPosition  # Далее заполняем строку
        for i in range(len(line_data)):
            self.table.setItem(new, i, QtWidgets.QTableWidgetItem(line_data[i]))  # не менее 3-х пробелов



