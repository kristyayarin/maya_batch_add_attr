# -*- coding: utf-8 -*-
import maya.cmds as cmds
from random import uniform
# addAttr -ln "floatattr"  -at double  -min 1 -max 4 -dv 1 |RenderManProgram1|RenderManProgram1Shape;


mode = {
	'const' : lambda value,min_max: value,
	'random' :  lambda value,min_max : myRandom(min_max)
}

def myRandom(min_max):

	if (type(min_max[0]) == tuple):
		newValue = (uniform(min_max[0][0],min_max[1][0]),uniform(min_max[0][1],min_max[1][1]),uniform(min_max[0][2],min_max[1][2]))
	else:
		newValue = uniform(min_max[0], min_max[1])
	return newValue
	
#===========================================================================================	
def add_float(shape, attrname, value, min_max):	
	if cmds.attributeQuery(attrname, node=shape, exists=True) == False:
		if min_max == 'none':
			cmds.addAttr(shape, ln=attrname, sn=attrname,nn=attrname, k=True, at='double', dv=value)
		else:
			cmds.addAttr(shape, ln=attrname, sn=attrname,nn=attrname, k=True, at='double',min=min_max[0], max=min_max[1], dv=value)				
	else:
		cmds.setAttr(shape + '.' + attrname, value)

#===========================================================================================

def add_int(shape, attrname, value, min_max):
	value = int(value)
	if cmds.attributeQuery(attrname, node=shape, exists=True) == False:
		if min_max == 'none':
			cmds.addAttr(shape, ln=attrname, sn=attrname, at='long')
		else:
			cmds.addAttr(shape, ln=attrname, sn=attrname, at='long', min=min_max[0], max=min_max[1])
	else:
		cmds.setAttr(shape + '.' + attrname, value)


#===========================================================================================

def add_color(shape, attrname, value, min_max = 'none'):
	if cmds.attributeQuery(attrname + 'R', node=shape, exists=True) == False:
		cmds.addAttr(shape, ln=attrname, sn=attrname, nn = attrname, at='float3', usedAsColor=True)
		cmds.addAttr(shape, ln=attrname + 'R', sn=attrname + 'R',nn=attrname + 'R', p = attrname, at='float', dv = value[0])
		cmds.addAttr(shape, ln=attrname + 'G', sn=attrname + 'G',nn=attrname + 'R', p = attrname, at='float', dv = value[1])
		cmds.addAttr(shape, ln=attrname + 'B', sn=attrname + 'B',nn=attrname + 'R', p = attrname, at='float', dv = value[2])
	else:
		cmds.setAttr(shape + '.' + attrname + 'R', value[0])
		cmds.setAttr(shape + '.' + attrname + 'G', value[1])
		cmds.setAttr(shape + '.' + attrname + 'B', value[2])
	

attrType = {
	'float' : add_float,
	'int' : add_int,
	'color' : add_color
}

#===========================================================================================


def deleteAttr(attrname):
	selections = cmds.ls(sl=True)
	shapes = cmds.listRelatives(selections)
	for shape in shapes:
		if cmds.attributeQuery(attrname, node=shape, exists=True) == True:
			cmds.deleteAttr(shape, at = attrname)

#===========================================================================================

def batchAddAttr(dataType, attributename, defult_value, modeType, min_max, Ai):

	# decide attribute name
	if Ai == True:
		attrname = 'mtoa_constant_' + attributename
	else:
		attrname = attributename

	selections = cmds.ls(sl=True)
	shapes = cmds.listRelatives(selections)

	if len(selections) == 0:
			print('Cannot find a shape to add attribute')
	if shapes == None:
		shapes = selections

	value = mode.get(modeType)(defult_value,min_max)

	for obj in shapes:
		value = mode.get(modeType)(defult_value,min_max)
		attrType.get(dataType)(obj, attrname, value, min_max)
	




