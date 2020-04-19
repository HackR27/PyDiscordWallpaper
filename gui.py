#!/usr/bin/python
from PyQt5 import QtWidgets,QtGui
from multiprocessing import Process
import sys,shutil,cssutils,time,json
from os import system,path,curdir,mkdir,listdir

dir = path.abspath(curdir)

if 'wallpaper' not in listdir():
    mkdir('wallpaper',mode=777)

def css_writer(data):
    s = open('example.css').read()
    s += ':root {\n'
    for key in data.keys():
        s += f'\t {key}: {data[key]};\n'

    s += '\t --font:\tWhitney, Helvetica Neue, Helvetica, Arial, sans-serif;\n\t --popoutsize:\tvar(--backgroundsize);\n\t --backdropsize:\tvar(--backgroundsize);\n\t --version1_0_5:\tnone;\n}'
    return s

def copier(file):
    global dir
    values = json.load(open('discord.json'))

    destination = path.join(dir,'wallpaper','{}'.format(path.basename(file)))

    shutil.copy(file,destination)
    style = path.join('/home/mightyg/.config/BetterDiscord/themes','BasicBackground.theme.css')
    values['--background'] = 'url(http://localhost:8080/{})'.format(path.join('wallpaper',path.basename(file)))
    output = css_writer(values)
    print(output)
    fp = open(style,'w')
    fp.write(output)
    fp.close()



class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(20,500,400,100)
        self.helper()
        self.show()

    def helper(self):
        self.image = QtWidgets.QLabel(self)
        self.image.setGeometry(10,10,160,90)
        self.image_path = QtWidgets.QLineEdit(self)
        self.image_path.setReadOnly(True)
        self.image_path.setGeometry(160+15,12,250,20)
        image_button = QtWidgets.QPushButton(self)
        image_button.setGeometry(160+15,34,100,30)
        image_button.setText('Open image')
        image_button.clicked.connect(self.getFileName)
        setup_button = QtWidgets.QPushButton(self)
        setup_button.setGeometry(160+15,74,100,30)
        setup_button.setText('Set image on discord')
        setup_button.clicked.connect(self.wallpaper)

    def wallpaper(self):
        try:
            p = Process(target = copier,args = (self.filename,),name = 'copier')
            p.start()
        except AttributeError:
            print('AttributeError')
            pass





    def getFileName(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.filename = fileName
            self.image.setPixmap(QtGui.QPixmap(fileName))
            self.image.setScaledContents(True)
            self.image_path.setText(fileName)




def run():
    app = QtWidgets.QApplication(sys.argv)
    # app.aboutToQuit.connect(history)
    GUI = window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
