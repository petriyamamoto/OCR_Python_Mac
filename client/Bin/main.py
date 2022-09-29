
from datetime import datetime
import sys
from threading import *
from PyQt5.QtWidgets import (
    QApplication, QWidget,QFileDialog,QTableWidgetItem,QListWidgetItem
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDate, pyqtSignal,QSize
from PyQt5.uic import loadUi
from interface import Ui_Form
from PJROCR import PJROCR
from apscheduler.schedulers.background import BackgroundScheduler
from DownLoadManager import DManager
class Window(QWidget, Ui_Form):
    clearcontent  = pyqtSignal()   
    updateCrypto  = pyqtSignal()   

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.image_path = ''
        self.lock_flag = False
        self._timer = BackgroundScheduler()
        self._timer.add_job(self.onUpdate,'interval', seconds = 5)
        self._timer.start()
        self.serverURL = self.lineEdit.text()
        self.tableWidget.setColumnWidth(0,200)
        self.tableWidget.setColumnWidth(2,30)
        self.tableWidget.setColumnWidth(6,50)
        self.listWidget.clear()
        self.listWidget.setSpacing(10)
        self.m_download_manager = DManager(self.serverURL)
        self.cryptoText = ''
    def onLoad(self):
        result = result
    def startProcess(self):
        self.clearcontent.emit()
        self.tableWidget.setRowCount(0)
        if self.image_path == '':return
        OCR_Result = PJROCR(self.image_path)
        try:
            self.no1_edit.setText(OCR_Result['root_data']['Number1'])
            self.no2_edit.setText(OCR_Result['root_data']['Number2'])
            self.cryptoText = OCR_Result['crypto']     
            self.receiver_man_edit.setText(OCR_Result['root_data']['receive_man'])
            self.check_man_edit.setText(OCR_Result['root_data']['check_man'])
            self.open_man_edit.setText(OCR_Result['root_data']['open_man'])
            sender_data = OCR_Result['sender_data']
            if len(sender_data) >= 5:
                self.sender_name_edit.setText(sender_data[0]['text'])
                self.sender_id_edit.setText(sender_data[1]['text'])
                self.sender_address_edit.setText(sender_data[2]['text'] + sender_data[3]['text'] )
                self.sender_no2_edit.setText(sender_data[4]['text'])
            elif len(sender_data) == 4:
                self.sender_name_edit.setText(sender_data[0]['text'])
                self.sender_id_edit.setText(sender_data[1]['text'])
                self.sender_address_edit.setText(sender_data[2]['text'])
                self.sender_no2_edit.setText(sender_data[3]['text'])
            elif len(sender_data) == 3:
                self.sender_id_edit.setText(sender_data[0]['text'])
                self.sender_address_edit.setText(sender_data[1]['text'])
                self.sender_no2_edit.setText(sender_data[2]['text'])

            receive_data = OCR_Result['receiver_data']
            if len(receive_data) == 5:
                self.type_edit.setText(receive_data[0]['text'])
                self.receiver_name_edit.setText(receive_data[1]['text'])
                self.receiver_id_edit.setText(receive_data[2]['text'])
                self.receiver_address_edit.setText(receive_data[3]['text'])
                self.receiver_no2_edit.setText(receive_data[4]['text'])
            elif len(receive_data) == 4:
                self.receiver_id_edit.setText(receive_data[1]['text'])
                self.receiver_address_edit.setText(receive_data[2]['text'])
                self.receiver_no2_edit.setText(receive_data[3]['text'])
            money_data = OCR_Result['money']
            if len(money_data) == 3:
                self.part1_edit.setText(money_data[0])
                self.part2_edit.setText(money_data[1])
                self.total_edit.setText(money_data[2])
            elif len(money_data) == 2:
                self.part1_edit.setText(money_data[0])
                self.part2_edit.setText(money_data[1])
            date = OCR_Result['root_data']['date']
        
            d = QDate(int(date[:4]),int(date[5:7]),int(date[8:10]))
            self.dateEdit.setDate(d)
            table_data = OCR_Result['table_body']
            
            self.tableWidget.setRowCount(len(table_data))
            row = 0

            for tableitem in table_data:
                self.addTableRow(row,tableitem)
                row += 1
            # print(OCR_Result)
            self.image_path = ''
            self.updateCrypto.emit()    
        except:
            print('StartProcess Roution Error')
    def onCryptoUpdate(self):
        self.sender_crypto_edit.setPlainText(self.cryptoText)    
        self.update()
    def onStart(self):

        if self.listWidget.currentItem():
            self.image_path = 'temp/' + self.listWidget.currentItem().text()
            # self.startProcess()
            thread = Thread(target = self.startProcess)
            thread.start()
    def addTableRow(self,row_index,row_data):
        try:
            if len(row_data) >= 8:
                for i in range(0,8):
                    self.tableWidget.setItem(row_index ,i, QTableWidgetItem(row_data[i]['text'])) 
                self.tableWidget.setItem(row_index ,2, QTableWidgetItem('个')) 
            elif len(row_data) == 7:
                    self.tableWidget.setItem(row_index ,0, QTableWidgetItem(row_data[0]['text'])) 
                    self.tableWidget.setItem(row_index ,1, QTableWidgetItem(row_data[1]['text']))  
                    self.tableWidget.setItem(row_index ,2, QTableWidgetItem('个')) 
                    for i in range(2,7):
                        self.tableWidget.setItem(row_index ,i+1, QTableWidgetItem(row_data[i]['text'])) 
        except:
            print('addTableRow Exception Error')

    def onHome(self):    
        self.stackedWidget.setCurrentIndex(0)
        self.lock_flag = True
    def onUpdate(self):
        if self.lock_flag == True: return
        print('send Request to server')
        new_file_list = self.m_download_manager.getFileList()
        for file in new_file_list:
            it = QListWidgetItem()
            it.setIcon(QIcon('resource/fileicon.png'))
            it.setText(file)
            self.listWidget.setIconSize(QSize(50,50))
            self.listWidget.addItem(it)    

    def onDetect(self):
        self.stackedWidget.setCurrentIndex(1)
        self.lock_flag = False
        self.serverURL = self.lineEdit.text()
        self.m_download_manager.setUrl(self.serverURL)
    def onListItemClicked(self,item):
        filename = item.text()
        pixmap =  QPixmap('temp/' + filename)
        self.label_3.setPixmap(pixmap.scaled(self.label_3.size()))
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.showMaximized()
    sys.exit(app.exec())
