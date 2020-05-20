# maya_batch_add_attr
A script that add batch attributes to object

### Instructions

#### 1. install script
   add_arnold_attrs.py -> \maya\scripts
   add_arnold_attrs.ui -> \maya\Qt_dev\ui 
   add_arnold_attrs_ui.py -> \maya\Qt_dev

#### 2.  run script
   copy this into maya script editor and run
   =====================================

   import add_arnold_attrs_ui
   reload(add_arnold_attrs_ui)

   mayaWin = add_arnold_attrs_ui.getMayaMainWindow()
   dialog = add_arnold_attrs_ui.AddaDialog(mayaWin)

   =====================================

#### 3. tips
    a) checked "For Arnold" to add "mtoa_constant_" before attribute name
    b) If you select a group, the attribute will be add on the objects inside the group
