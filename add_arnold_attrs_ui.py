"""
import sys
sys.path.append("$NETHOME/maya/Qt_Dev")

import add_arnold_attrs_ui
reload(add_arnold_attrs_ui)

mayaWin = add_arnold_attrs_ui.getMayaMainWindow()
dialog = add_arnold_attrs_ui.AddaDialog(mayaWin) 
"""
# Aternatively, run this script directly from Cutter.
'''
isMaya = False
try:
	from PyQt4.QtCore import *
	from PyQt4.QtGui import *
	from PyQt4 import uic
except ImportError:
'''
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *
isMaya = True
import maya.OpenMayaUI as omui
import shiboken2
		
import sys
import os
import math
from connection_utils import *
import add_arnold_attrs as adda
reload (adda)

#________________________________________________________
# getMayaMainWindow
#________________________________________________________

def getMayaMainWindow():
	winPtr = omui.MQtUtil.mainWindow() #Returns Maya's main window.
	return shiboken2.wrapInstance(long(winPtr), QWidget) 
	#shiboken.wrapInstance(address, type)
	#Creates a Python wrapper for a C++ object instantiated at a given memory address 
	#- the returned object type will be the same given by the user.

#________________________________________________________
#               Widget Names
#________________________________________________________
#               iconLabel
#
#               attr_name_lineEdit
#               arnold_checkBox
#
#               data_type_comboBox
#               add_mode_comboBox
#               min_max_checkBox
#
#               f_dv_doubleSpinBox
#   f_min_doubleSpinBox      f_max_doubleSpinBox
#              
#               i_dv_spinBox
#   i_min_spinBox            i_max_spinBox
#
# c_dv_r_doubleSpinBox   c_dv_g_doubleSpinBox   c_dv_b_doubleSpinBox
# c_mix_r_doubleSpinBox  c_mix_g_doubleSpinBox  c_mix_b_doubleSpinBox
# c_man_r_doubleSpinBox  c_man_g_doubleSpinBox  c_man_b_doubleSpinBox
#               
#	label_16				path_lineEdit_2
#				loop_checkBox_2
#
#               add_group_checkBox
#               pushButton
#				
#				del_name_lineEdit_3
#				pushButton_2
#________________________________________________________

class AddaDialog(QDialog):
	def __init__(self, parent=None):
		super(AddaDialog, self).__init__(parent)
		
		self.pathToIcon = os.path.join(os.path.dirname(__file__), 'icons', 'magic_circle_icon.jpg') #<<< Create Icon
		pathToUi = os.path.join(os.path.dirname(__file__), 'ui', 'add_arnold_attrs.ui')
		'''
		if isMaya == False:
			self.ui = uic.loadUi(pathToUi,self)
			self.setWindowFlags(Qt.WindowStaysOnTopHint)
		else:
		'''
		loader = QUiLoader()
		self.ui = loader.load(pathToUi, self)
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		self.makeConnections()
		self.ui.show()
		
	#________________________________________________
	def makeConnections(self):
		#------------------------------------------------
		'''
		pixmap = QPixmap(self.pathToIcon)
		pixmap_resized = pixmap.scaled(400, 225)
		self.ui.iconLabel.setPixmap (pixmap_resized)
		self.ui.iconLabel.setMask (pixmap_resized.mask())
		'''
		#------------------------------------------------
		self.ui.add_mode_comboBox.currentIndexChanged.connect(self.changeMode)
		self.ui.data_type_comboBox.currentIndexChanged.connect(self.changeMode)
		self.ui.pushButton.clicked.connect(self.doitAction)
		self.ui.pushButton_2.clicked.connect(self.doieAction_2)
	#________________________________________________
	
	def changeMode(self):
		#------------------------------------------------
		if self.ui.add_mode_comboBox.currentText() == 'random' :
			self.ui.min_max_checkBox.setChecked(True)
			self.ui.min_max_checkBox.setEnabled(False)
		else:
			self.ui.min_max_checkBox.setEnabled(True)

		if self.ui.data_type_comboBox.currentText() == 'file' :
			self.ui.min_max_checkBox.setChecked(False)
			self.ui.min_max_checkBox.setEnabled(False)
		#------------------------------------------------
		self.index = {
			'color' : 0,
			'float' : 1,
			'int' : 2,
			'file' : 3
		}
		self.ui.data_type_stackedWidget.setCurrentIndex(self.index.get(self.ui.data_type_comboBox.currentText()))

		#------------------------------------------------

		if self.ui.data_type_comboBox.currentText() == 'file' and self.ui.add_mode_comboBox.currentText() == 'const' :
			self.ui.label_16.setText('File path')
		else :
			self.ui.label_16.setText('Folder path')
	#________________________________________________
	def doitAction(self):

		self.dataType = self.ui.data_type_comboBox.currentText()
		if self.dataType == 'float':
			self.dv = self.ui.f_dv_doubleSpinBox.value()
			self.min = self.ui.f_min_doubleSpinBox.value()
			self.max = self.ui.f_max_doubleSpinBox.value()
		elif self.dataType == 'int':
			self.dv = self.ui.i_dv_spinBox.value()
			self.min = self.ui.i_min_spinBox.value()
			self.max = self.ui.i_max_spinBox.value()
		elif self.dataType == 'color':
			self.dv = (self.ui.c_dv_r_doubleSpinBox.value(),
					   self.ui.c_dv_g_doubleSpinBox.value(),
					   self.ui.c_dv_b_doubleSpinBox.value())
			self.min = (self.ui.c_min_r_doubleSpinBox.value(),
						self.ui.c_min_g_doubleSpinBox.value(),
						self.ui.c_min_b_doubleSpinBox.value())
			self.max = (self.ui.c_max_r_doubleSpinBox.value(),
						self.ui.c_max_g_doubleSpinBox.value(),
						self.ui.c_max_b_doubleSpinBox.value())
		elif self.dataType == 'file':
			self.dv = self.ui.path_lineEdit_2.text()
			self.min_max = ('file', self.dv)

		else:
			self.dv = 0
			self.min_max = 'none'
			
		if self.ui.min_max_checkBox.isChecked() == True :
			self.min_max = (self.min,self.max)
		else :
			self.min_max = 'none'

		if self.dataType == 'file':
			self.dv = self.ui.path_lineEdit_2.text()
			self.min_max = ('file', self.dv)

		adda.batchAddAttr(self.dataType,
						  self.ui.attr_name_lineEdit.text(),
						  self.dv , self.ui.add_mode_comboBox.currentText(),
						  self.min_max, self.ui.arnold_checkBox.isChecked())
		
	#________________________________________________

	def doieAction_2(self):
		adda.deleteAttr(self.ui.del_name_lineEdit_3.text())		
		
#========================================================		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	dialog = MatrixDialog()
	dialog.show()
	sys.exit(app.exec_())
