# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\0.Code\amazontools\resource\ui\amazon.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 600)
        Form.setMinimumSize(QtCore.QSize(480, 600))
        Form.setMaximumSize(QtCore.QSize(480, 600))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.input = QtWidgets.QLineEdit(self.frame)
        self.input.setMinimumSize(QtCore.QSize(0, 30))
        self.input.setObjectName("input")
        self.gridLayout.addWidget(self.input, 0, 0, 1, 1)
        self.submit = QtWidgets.QPushButton(self.frame)
        self.submit.setEnabled(False)
        self.submit.setMinimumSize(QtCore.QSize(40, 32))
        self.submit.setMaximumSize(QtCore.QSize(40, 32))
        self.submit.setObjectName("submit")
        self.gridLayout.addWidget(self.submit, 0, 2, 1, 1)
        self.dropdown = QtWidgets.QComboBox(self.frame)
        self.dropdown.setMinimumSize(QtCore.QSize(70, 30))
        self.dropdown.setMaximumSize(QtCore.QSize(70, 30))
        self.dropdown.setObjectName("dropdown")
        self.dropdown.addItem("")
        self.dropdown.addItem("")
        self.dropdown.addItem("")
        self.gridLayout.addWidget(self.dropdown, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.editor = QtWidgets.QPlainTextEdit(Form)
        self.editor.setObjectName("editor")
        self.verticalLayout.addWidget(self.editor)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.status = QtWidgets.QLabel(self.widget)
        self.status.setStyleSheet("")
        self.status.setObjectName("status")
        self.horizontalLayout.addWidget(self.status)
        self.repeat = QtWidgets.QPushButton(self.widget)
        self.repeat.setMinimumSize(QtCore.QSize(60, 30))
        self.repeat.setMaximumSize(QtCore.QSize(60, 30))
        self.repeat.setDefault(False)
        self.repeat.setObjectName("repeat")
        self.horizontalLayout.addWidget(self.repeat)
        self.horizontalLayout.setStretch(0, 9)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        self.input.textChanged['QString'].connect(Form.input_check_slot)
        self.submit.clicked.connect(Form.submit_slot)
        self.repeat.clicked.connect(Form.editor_repeat_slot)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "亚马逊关键词挖掘机 Q:519999189"))
        self.input.setPlaceholderText(_translate("Form", "请输入,多个查询用,隔开 Eg:cotton,lace"))
        self.submit.setText(_translate("Form", "查询"))
        self.dropdown.setItemText(0, _translate("Form", "挖掘深度"))
        self.dropdown.setItemText(1, _translate("Form", "等级1"))
        self.dropdown.setItemText(2, _translate("Form", "等级2"))
        self.status.setText(_translate("Form", "等待查询..."))
        self.repeat.setText(_translate("Form", "去除重复"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

