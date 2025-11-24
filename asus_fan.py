#!/usr/bin/python
import sys, api, os
from PyQt6.QtWidgets import  QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel, QTabWidget
from PyQt6.QtCore import QTimer

def edit_ok_click():
     api.wfan(edit.text())
def pwm_changed():
    pwm_aaaa = int(pwm.currentIndex()) + 1
    if api.pwm() != pwm_aaaa:
        api.wpwm(str(pwm_aaaa))
def startservice():
    os.system("systemctl start fan_service")
    statusdef()
def stopservice():
    os.system("systemctl stop fan_service")
    statusdef()
def createservice():
    os.system("cp /home/yancat/asus_fan/fan_service.service /etc/systemd/system")
    os.system("systemctl daemon-reload")
    statusdef()

app = QApplication(sys.argv)

tabs = QTabWidget()
tabs.setWindowTitle("ASUS风扇控制器")
tabs.resize(300,250)
#=========================================================
tab1 = QVBoxLayout()

fan_label = QLineEdit()
fan_label.setReadOnly(True)
fan_label.setText(f"名字:{api.name()}")
fan_label.setStyleSheet("background: transparent; border: none;")
tab1.addWidget(fan_label)

temp_input = QLineEdit()
temp_input.setReadOnly(True)
temp_input.setStyleSheet("background: transparent; border: none;")
tab1.addWidget(temp_input)

fan_input = QLineEdit()
fan_input.setReadOnly(True)
fan_input.setStyleSheet("background: transparent; border: none;")
tab1.addWidget(fan_input)

pwm = QComboBox()
pwm.addItems(["PWM模式：手动模式(1)", "PWM模式：自动模式(2)"])
pwm.currentIndexChanged.connect(pwm_changed)
tab1.addWidget(pwm)

text = QLineEdit()
text.setReadOnly(True)
text.setText("改转速，0-255")
text.setStyleSheet("background: transparent; border: none;")
tab1.addWidget(text)

edit = QLineEdit()
tab1.addWidget(edit)

edit_ok = QPushButton("OK")
edit_ok.clicked.connect(edit_ok_click)
tab1.addWidget(edit_ok)


tab1_ = QWidget()
tab1_.setLayout(tab1)
tabs.addTab(tab1_, "风扇控制")
#-------------------------------------------------------------------------------------------
tab2 = QVBoxLayout()

servicename = QLineEdit()
servicename.setReadOnly(True)
servicename.setText("温控服务")
servicename.setStyleSheet("background: transparent; border: none;")
tab2.addWidget(servicename)

serviceinfo = QLineEdit()
serviceinfo.setReadOnly(True)
serviceinfo.setText("大于70度时风扇全速运行直到降温至60度以下")
serviceinfo.setStyleSheet("background: transparent; border: none;")
tab2.addWidget(serviceinfo)

status = QLineEdit()
status.setReadOnly(True)
status.setStyleSheet("background: transparent; border: none;")
tab2.addWidget(status)

start = QPushButton("启动服务")
start.clicked.connect(startservice)
tab2.addWidget(start)

stop = QPushButton("停止服务")
stop.clicked.connect(stopservice)
tab2.addWidget(stop)

create= QPushButton("创建服务")
create.clicked.connect(createservice)
tab2.addWidget(create)

tab2_ = QWidget()
tab2_.setLayout(tab2)
tabs.addTab(tab2_, "服务控制")
#-------------------------------------------------------------------------------------------
tab3 = QVBoxLayout()

name = QLineEdit()
name.setReadOnly(True)
name.setText("By 猫小炎")
name.setStyleSheet("background: transparent; border: none;")
tab3.addWidget(name)

email = QLineEdit()
email.setReadOnly(True)
email.setText("frz114514@icloud.com")
email.setStyleSheet("background: transparent; border: none;")
tab3.addWidget(email)

tab3_ = QWidget()
tab3_.setLayout(tab3)
tabs.addTab(tab3_, "关于")
#=========================================================
tabs.show()

def update_data():
    temp_input.setText(f"温度:{api.temp()}")
    if api.pwm() == 2: fan_input.setText(f"转速:{api.fan()}")
    elif api.pwm() == 1: fan_input.setText("转速:(手动调整)")
    else: fan_input.setText("转速:错误！")
    pwm.setCurrentIndex(api.pwm() - 1)
timer = QTimer()
timer.timeout.connect(update_data)
timer.start(1000)
#-------------------------------------------------------------------------------------------
def statusdef():
    status.setText(f"服务状态:{api.service_status()}")
timer_status = QTimer()
timer_status.timeout.connect(statusdef)
timer_status.start(5000)
#=========================================================
sys.exit(app.exec())
timer.stop()
timer_status.stop()
app.quit()