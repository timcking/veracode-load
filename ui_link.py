# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_link.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainDialog(object):
    def setupUi(self, MainDialog):
        MainDialog.setObjectName("MainDialog")
        MainDialog.resize(305, 299)
        self.verticalLayout = QtWidgets.QVBoxLayout(MainDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(MainDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.textSandboxId = QtWidgets.QLineEdit(MainDialog)
        self.textSandboxId.setObjectName("textSandboxId")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.textSandboxId)
        self.label = QtWidgets.QLabel(MainDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.textTicketId = QtWidgets.QLineEdit(MainDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textTicketId.sizePolicy().hasHeightForWidth())
        self.textTicketId.setSizePolicy(sizePolicy)
        self.textTicketId.setObjectName("textTicketId")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.textTicketId)
        self.label_2 = QtWidgets.QLabel(MainDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.textFlaw = QtWidgets.QTextEdit(MainDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textFlaw.sizePolicy().hasHeightForWidth())
        self.textFlaw.setSizePolicy(sizePolicy)
        self.textFlaw.setMaximumSize(QtCore.QSize(16777215, 192))
        self.textFlaw.setAcceptRichText(False)
        self.textFlaw.setObjectName("textFlaw")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.textFlaw)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonLink = QtWidgets.QPushButton(MainDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonLink.sizePolicy().hasHeightForWidth())
        self.buttonLink.setSizePolicy(sizePolicy)
        self.buttonLink.setObjectName("buttonLink")
        self.horizontalLayout.addWidget(self.buttonLink)
        self.buttonClose = QtWidgets.QPushButton(MainDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonClose.sizePolicy().hasHeightForWidth())
        self.buttonClose.setSizePolicy(sizePolicy)
        self.buttonClose.setObjectName("buttonClose")
        self.horizontalLayout.addWidget(self.buttonClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MainDialog)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)

    def retranslateUi(self, MainDialog):
        _translate = QtCore.QCoreApplication.translate
        MainDialog.setWindowTitle(_translate("MainDialog", "Link Flaws to Tickets"))
        self.label_3.setText(_translate("MainDialog", "Sandbox ID"))
        self.label.setText(_translate("MainDialog", "Citrix Ticket ID"))
        self.label_2.setText(_translate("MainDialog", "Flaws"))
        self.textFlaw.setPlaceholderText(_translate("MainDialog", "Paste flaw ID\'s here"))
        self.buttonLink.setText(_translate("MainDialog", "Link"))
        self.buttonClose.setText(_translate("MainDialog", "Close"))

