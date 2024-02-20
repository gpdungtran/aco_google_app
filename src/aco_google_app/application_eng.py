from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QComboBox, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
import sys
import find_paths as fp 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
 
class myWidget(QWidget):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Software to support schools to drop off and pick up students')
        self.setFixedSize(640,640)

        #hbox_1 
        label_1 = QLabel("Group: ")
        self.group=QComboBox()
        self.group.addItems(['','Group 1','Group 2','Group 3','Group 4'])
        
         
         
        #hbox_2
        label_2 = QLabel("List of locations: ")
        self.place_list = QListWidget(self)
        self.place_list.setFixedSize(300,70)
        self.btn_1 = QPushButton('Add', self)
        
        #hbox_3
        label_3 = QLabel("Selected locations: ")
        self.place_chosen = QListWidget(self)
        self.place_chosen.setFixedSize(300,70) 
        self.btn_2 = QPushButton('Delete', self)
        
        #hbox_4
        self.btn_3 = QPushButton('Calculate', self)
        

        #hbox_5
        label_4 = QLabel("Optimal Path: ")
        self.label_5 = QLabel()

        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(label_1)
        hbox_1.addWidget(self.group)
    

        hbox_2 = QHBoxLayout()
        hbox_2.addWidget(label_2)
        hbox_2.addWidget(self.place_list)
        hbox_2.addWidget(self.btn_1)

        hbox_3 = QHBoxLayout()
        hbox_3.addWidget(label_3)
        hbox_3.addWidget(self.place_chosen)
        hbox_3.addWidget(self.btn_2)

        hbox_4 = QHBoxLayout()
        hbox_4.addWidget(self.btn_3)

        self.img = QLabel('', self)
        self.img.setFrameStyle(QFrame.Box)

        hbox_5 = QHBoxLayout() 
        hbox_5.addWidget(label_4)
        hbox_5.addWidget(self.label_5)
        self.label_5.setFixedSize(500, 100)
        self.label_5.setWordWrap(True) 

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_1)
        vbox.addLayout(hbox_2)
        vbox.addLayout(hbox_3)
        vbox.addLayout(hbox_4)
        vbox.addWidget(self.img)
        vbox.addLayout(hbox_5)
        self.setLayout(vbox)
 
        self.places = {}
        self.place_adress = []
        # signal
        #
        self.group.currentTextChanged.connect(self.on_combobox_changed)
        self.btn_1.clicked.connect(self.clickBtn_1)
        self.btn_2.clicked.connect(self.clickBtn_2)
        self.btn_3.clicked.connect(self.clickBtn_3)


    def clickBtn_3(self):
        BASE_URL    = 'https://maps.googleapis.com/maps/api/staticmap?'
        API_KEY     = 'AIzaSyBnEczbljpLOsESpId-YPwFWQNc4YuYLEk'
        PLACE        = ''
        PATH         = ''
        PATH_NAME    = ''
        W = self.img.width()
        H = self.img.height()
        
        for index in range(self.place_chosen.count()):
            print(self.place_chosen.item(index).text())
            name, address = self.place_chosen.item(index).text().split("-")
            self.places[name] = address 
            self.place_adress.append(address)
            #all_place_text = [ ]

        for item in self.place_adress:
            PLACE += '%7C'+item

        path_draw,path_name = fp.path_obtain(self.place_adress,"driving")
        
        for item in path_draw:
            PATH += '&path=enc:'+item

        for item in path_name:
            PATH_NAME += item[0]+' -'

            #+'\n'

        URL = (BASE_URL 
       + f'center={PLACE}'
       #+ f'&zoom={ZOOM}'
       + f'&size={W}x{H}&scale=2'
       + '&markers=color:red'+PLACE
       + PATH
       + f'&key={API_KEY}')
        
        
        # HTTP request
        
        response = requests.get(URL)
 
        # image scaled and draw
        img = QPixmap()
        img.loadFromData(response.content)
        img = img.scaled(img.width()//2, img.height()//2, Qt.KeepAspectRatio, Qt.SmoothTransformation)
 
        self.img.setPixmap(img)
        self.label_5.setText(str(PATH_NAME))
 
    def clickBtn_1(self):
        
        self.place_chosen.addItems([self.place_list.currentItem().text()])

    def clickBtn_2(self):
        lst_chosen = self.place_chosen.selectedIndexes()
    
        for modelindex in lst_chosen:
            self.place_chosen.model().removeRow(modelindex.row())

    def on_combobox_changed(self,value):
        self.place_name = []
        self.place_adress = []
        self.place_list.clear()
        line_number = 0
        if value=='':
            pass
        else:
            with open("Data/"+value+".txt") as f:
                for line in f:

                    line = line.rstrip('\n')
                    self.place_list.addItems([line])

                    if line_number == 0:
                        self.place_chosen.addItems([line])
                    
                    line_number +=1
                    
                    
                    


 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myWidget()
    w.show()
    sys.exit(app.exec_())
