import math
from copy import deepcopy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFrame
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPolygon
from PyQt5.QtCore import Qt, QPoint, QRect, QLineF, QLine
from Nodes_and_Transition_classes import Nodes,Transition
import globals

class MyWidget(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.list_nodes = []
        self.list_transitions = []
        self.actual_App_State = []
        self.actual_App_State.append([[],[]])

    def exists_differences(self,first_list, second_list):
        if len(first_list) != len(second_list) :
                return 1
        else:
                for index in range(len(first_list)):
                        if first_list[index].get_all_info() != second_list[index].get_all_info():
                                return 1
        return 0

    def append_in_App_State(self,l_nodes,l_transitions):
            if self.exists_differences(l_nodes,self.actual_App_State[len(self.actual_App_State)-1][0]) == 1 or self.exists_differences(l_transitions,self.actual_App_State[len(self.actual_App_State)-1][1]) ==1:
                self.actual_App_State.append([deepcopy(l_nodes), deepcopy(l_transitions)])

    def afisare_stiva(self):
        #print(len(self.actual_App_State))
        for elem in self.actual_App_State:
                nodes = elem[0][:]
                transitions = elem[1][:]
                if nodes:
                        print("Nodes [ ",end="")
                        for n in nodes:
                                print(n.getId(),end=",")
                        print(" ]")
                if transitions:
                        print("Transitions [ ",end="")
                        for t in transitions:
                                print(t.getNodeFrom(), t.getNodeTo(),t.getValues(),end=",")
                        print(" ]")

    def actualizare_globals(self):
        no_of_states = len(self.list_nodes)
        if no_of_states >= 0 and no_of_states <= 10:
                globals.nodes_size = 50
        elif no_of_states >= 11 and no_of_states <= 20:
                globals.nodes_size = 40
        elif no_of_states >= 21 and no_of_states <= 30:
                globals.nodes_size = 30
        elif no_of_states >= 31:
                globals.nodes_size = 20
        for n in self.list_nodes:
                n.changeSize(globals.nodes_size)
        globals.actual_node = no_of_states
        
    def actualizare_liste(self):
        if len(self.actual_App_State) > 0:
                self.list_nodes = deepcopy(self.actual_App_State[len(self.actual_App_State)-1][0])
                self.list_transitions = deepcopy(self.actual_App_State[len(self.actual_App_State)-1][1])

    def getElemByIdList(self,id):
        for c in self.list_nodes:
                if c.getId()==id:
                        return c

    def checkIfAlreadyExists(self,node_from,node_to):
        for t in self.list_transitions:
                if t.getNodeFrom() == node_from and t.getNodeTo() == node_to:
                        return self.list_transitions.index(t)
        return -1

    def mousePressEvent(self, event):
        self.actualizare_liste()
        '''print(" adaugare nod inainte")
        self.afisare_stiva()'''
        if event.button() == Qt.LeftButton:
            ok_for_drawing = 1
            for node in self.list_nodes:
                    if (event.x() >= node.getX() - 2 * node.getSize() - 20) and (event.x() <= node.getX() + 2 * node.getSize() + 20) and (event.y() >= node.getY() - 2 * node.getSize() - 20) and (event.y() <= node.getY() + 2 * node.getSize() + 20):
                            ok_for_drawing = 0
                            break
            if ok_for_drawing == 1:
                    #print("am apasat", event.x(), event.y())
                    self.actualizare_globals()
                    self.list_nodes.append(Nodes(event.x(), event.y(),globals.actual_node, str(globals.current_state_type), globals.nodes_size))
                    self.actualizare_globals()
                    #self.actual_App_State.append([deepcopy(self.list_nodes),deepcopy(self.list_transitions)])
                    self.append_in_App_State(self.list_nodes,self.list_transitions)
                    '''print(" adaugare nod dupa")
                    self.afisare_stiva()'''
                    self.repaint()

    def paintEvent(self, event):
        self.actualizare_liste()
        painter = QPainter(self)
        for c in self.list_nodes:
                if c.getType() == "initial state":
                        painter.setPen(QPen(QColor(0,0,0,150), (c.getSize() / 10) - 2, Qt.SolidLine))
                        painter.setBrush(QBrush(QColor(0, 255, 0,100), Qt.SolidPattern))
                        painter.drawEllipse(QPoint(c.getX(), c.getY()), c.getSize(), c.getSize())
                        painter.setPen(QPen(QColor(0,0,0,150), (c.getSize() / 10) - 2, Qt.SolidLine))
                        painter.setBrush(QBrush(QColor(0, 255, 0,100), Qt.SolidPattern))
                        painter.drawEllipse(QPoint(c.getX(), c.getY()), c.getSize()-((c.getSize() / 10)+2), c.getSize()-((c.getSize() / 10)+2))
                        #painter.drawText(QPoint(c.getX() - 5, c.getY() + 5), str(c.getId()))
                if c.getType() == "final state":
                        painter.setPen(QPen(QColor(0,0,0,150), (c.getSize() / 10) - 2, Qt.SolidLine))
                        painter.setBrush(QBrush(QColor(74, 148, 222,100), Qt.SolidPattern))
                        painter.drawRect(c.getX()-c.getSize()*1.8/2, c.getY()-c.getSize()*1.8/2, c.getSize()*1.8, c.getSize()*1.8)
                        #painter.drawText(QPoint(c.getX()-5 , c.getY()+5), str(c.getId()))
                if c.getType() == "inital & final state":
                        painter.setPen(QPen(QColor(0,0,0,150), (c.getSize() / 10) - 2, Qt.SolidLine))
                        painter.setBrush(QBrush(QColor(0, 255, 0,100), Qt.SolidPattern))
                        painter.drawRect(c.getX()-c.getSize()*1.8/2, c.getY()-c.getSize()*1.8/2, c.getSize()*1.8, c.getSize()*1.8)
                        painter.setPen(QPen(QColor(0,0,0,150), (c.getSize() / 10) - 2, Qt.SolidLine))
                        painter.setBrush(QBrush(QColor(0, 255, 0,100), Qt.SolidPattern))
                        painter.drawRect(c.getX()-c.getSize()*1.8/2+((c.getSize() / 10)+2), c.getY()-c.getSize()*1.8/2+((c.getSize() / 10)+2), c.getSize()*1.8-2*((c.getSize() / 10)+2), c.getSize()*1.8-2*((c.getSize() / 10)+2))
                        #painter.drawText(QPoint(c.getX() - 5, c.getY() + 5), str(c.getId()))
                if c.getType() == "normal state":
                        painter.setPen(QPen(QColor(0,0,0,150), (c.getSize() / 10) - 2, Qt.SolidLine))
                        painter.setBrush(QBrush(QColor(255, 255, 80,150), Qt.SolidPattern))
                        painter.drawEllipse(QPoint(c.getX(), c.getY()), c.getSize(), c.getSize())
                font = QtGui.QFont()
                font.setBold(True)
                painter.setFont(font)
                painter.setPen(Qt.black)
                painter.setBrush(Qt.black)
                painter.drawText(QPoint(c.getX() - 5, c.getY() + 5), str(c.getId()))


        for t in self.list_transitions:
                node_from = self.getElemByIdList(t.getNodeFrom())
                node_to = self.getElemByIdList(t.getNodeTo())
                if node_from.getX()!= node_to.getX() and node_from.getY()!= node_to.getY():
                        m = float((node_to.getY()-node_from.getY())/(node_to.getX()-node_from.getX()))

                if node_from.getX()<node_to.getX() and math.fabs(node_from.getY() - node_to.getY())>8:
                        x_start = node_from.getX()+ min(int((math.fabs(node_from.getX()-node_to.getX()))/(300/node_from.getSize() + 7)),node_from.getSize()-5)
                        y_start = int(m*(x_start - node_from.getX())+node_from.getY())
                        x_end = node_to.getX() - min(int((math.fabs(node_from.getX()-node_to.getX()))/(300/node_from.getSize() + 7)),node_from.getSize()-5)
                        y_end = int(m * (x_end - node_from.getX()) + node_from.getY())
                        #print("caz 1   ",m)

                if node_from.getX()>node_to.getX() and math.fabs(node_from.getY() - node_to.getY())>8:
                        x_start = node_from.getX() - min(int((math.fabs(node_from.getX()-node_to.getX()))/(300/node_from.getSize() + 7)),node_from.getSize()-5)
                        y_start = int(m*(x_start - node_from.getX())+node_from.getY())
                        x_end = node_to.getX() + min(int((math.fabs(node_from.getX()-node_to.getX()))/(300/node_from.getSize() + 7)),node_from.getSize()-5)
                        y_end = int(m * (x_end - node_from.getX()) + node_from.getY())
                        #print("caz 2   ",m)

                if math.fabs(node_from.getX()-node_to.getX())<=8:
                        x_start = node_from.getX()
                        x_end = node_to.getX()
                        if node_from.getY() > node_to.getY():
                                y_start = node_from.getY() - (node_from.getSize()/2)
                                y_end = node_to.getY() + (node_to.getSize()/2)
                        if node_from.getY() < node_to.getY():
                                y_start = node_from.getY() + (node_from.getSize()/2)
                                y_end = node_to.getY() - (node_to.getSize()/2)
                        #print("caz 3")

                if math.fabs(node_from.getY() - node_to.getY())<=8:
                        y_start = node_from.getY()
                        y_end = node_to.getY()
                        if node_from.getX() < node_to.getX():
                                x_start = node_from.getX() + (node_from.getSize()/2)
                                x_end = node_to.getX() - (node_to.getSize()/2)
                        if node_from.getX() > node_to.getX():
                                x_start = node_from.getX() - (node_from.getSize()/2)
                                x_end = node_to.getX() + (node_to.getSize()/2)
                        #print("caz 4")

                if node_from.getCenter() != node_to.getCenter():
                        #print(node_from.getX(),node_from.getY(),"  ",node_to.getX(),node_to.getY())
                        #print("x si y start",x_start,y_start)
                        #print("x si y end",x_end,y_end)
                        painter.setRenderHint(QPainter.Antialiasing)
                        arrowSize = node_from.getSize()/2
                        painter.setPen(QtCore.Qt.black)
                        painter.setBrush(QtCore.Qt.black)
                        line = QLine(QPoint(x_end,y_end), QPoint(x_start,y_start))
                        angle = math.atan2(-line.dy(), line.dx())
                        arrowP1 = QPoint(line.p1() + QPoint(math.sin(angle + (math.pi / 2.75)) * arrowSize, math.cos(angle + (math.pi / 2.75)) * arrowSize))
                        arrowP2 = QPoint(line.p1() + QPoint(math.sin(angle + math.pi - (math.pi / 2.75)) * arrowSize,math.cos(angle + math.pi - (math.pi / 2.75)) * arrowSize))
                        arrowHead = QPolygon([line.p1(),arrowP1,arrowP2])
                        painter.drawLine(line)
                        middle_x = int((node_from.getX() + node_to.getX())/2)
                        middle_y = int((node_from.getY()+node_to.getY())/2)
                        if t.getNodeFrom() > t.getNodeTo() and self.checkIfAlreadyExists(t.getNodeTo(),t.getNodeFrom())!= -1:
                                pas = max((node_from.getSize()/10) * 4,11)
                                middle_y = middle_y + pas
                                painter.setPen(QtCore.Qt.red)
                                painter.setBrush(QtCore.Qt.red)
                        else:
                                pas = - max((node_from.getSize()/10) * 4,11)
                        painter.drawPolygon(arrowHead)
                        #print(t.getNodeFrom(),t.getNodeTo(),t.getValues())
                        font = QtGui.QFont()
                        font.setBold(True)
                        font.setPointSize(node_from.getSize()/10+5)
                        painter.setFont(font)
                        for val in t.getValues():
                                painter.drawText(QPoint(middle_x,middle_y),val)
                                middle_y = middle_y + pas
                elif node_from.getCenter() == node_to.getCenter():
                        #x_start = node_from.getX()+node_from.getSize()
                        #draw arc
                        painter.setRenderHint(QPainter.Antialiasing)
                        painter.setPen(QtCore.Qt.black)
                        painter.setBrush(QtCore.Qt.white)
                        painter.drawArc(node_from.getX(),node_from.getY()-node_from.getSize()*1.5-2-int(60/node_from.getSize()),node_from.getSize()*1.5+8-int(60/node_from.getSize()),node_from.getSize()*1.5,300*16,240*16)
                        painter.setBrush(QtCore.Qt.black)
                        #draw sageata
                        arrowSize = (node_from.getSize() / 2)+3+int(20/node_from.getSize())
                        line = QLine(QPoint(node_from.getX()+node_from.getSize()-5, node_from.getY()-10), QPoint(node_from.getX()+node_from.getSize()+(node_from.getSize() / 2)+5, node_from.getY()-10))
                        angle = math.atan2(-line.dy(), line.dx())
                        arrowP1 = QPoint(line.p1() + QPoint(math.sin(angle + (math.pi / 2.75)) * arrowSize,math.cos(angle + (math.pi / 2.75)) * arrowSize))
                        arrowP2 = QPoint(line.p1() + QPoint(math.sin(angle + math.pi - (math.pi / 2.75)) * arrowSize,math.cos(angle + math.pi - (math.pi / 2.75)) * arrowSize))
                        arrowHead = QPolygon([line.p1(), arrowP1, arrowP2])
                        painter.drawPolygon(arrowHead)
                        #draw values
                        font = QtGui.QFont()
                        font.setBold(True)
                        font.setPointSize(node_from.getSize() / 10 + 5)
                        painter.setFont(font)
                        pas = - max((node_from.getSize()/10) * 4, 11)
                        middle_x = node_from.getX()+node_from.getSize()-10
                        middle_y = node_from.getY()-node_from.getSize()
                        for val in t.getValues():
                                painter.drawText(QPoint(middle_x,middle_y),val)
                                middle_y = middle_y + pas




class SMVerifier(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1850, 978)
        Dialog.setMinimumSize(QtCore.QSize(1500, 964))
        Dialog.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_box = QtWidgets.QGroupBox(Dialog)
        self.title_box.setMinimumSize(QtCore.QSize(1500, 55))
        self.title_box.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.title_box.setStyleSheet("QGroupBox {\n"
"    border: 1px rgd(100,100,100);\n"
"}")
        self.title_box.setTitle("")
        self.title_box.setObjectName("title_box")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.title_box)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.undo_button = QtWidgets.QPushButton(self.title_box)
        self.undo_button.setMinimumSize(QtCore.QSize(151, 41))
        self.undo_button.setMaximumSize(QtCore.QSize(151, 41))
        self.undo_button.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(74, 148, 222, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(74, 148, 222);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(74, 148, 222);\n"
"    border-right: rgb(74, 148, 222);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(85, 170, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(74, 148, 222);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(74, 148, 222);\n"
"    border-right: rgb(74, 148, 222);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(74, 148, 222);\n"
"    font: 75 16pt \"Georgia\";\n"
"    border-color: rgb(62, 124, 186);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom: rgb(62, 124, 186);\n"
"    border-right: rgb(62, 124, 186);\n"
"}")
        self.undo_button.setObjectName("undo_button")
        self.horizontalLayout.addWidget(self.undo_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.title = QtWidgets.QLabel(self.title_box)
        self.title.setMinimumSize(QtCore.QSize(441, 51))
        self.title.setMaximumSize(QtCore.QSize(441, 51))
        self.title.setStyleSheet("font: 75 20pt \"Georgia\";\n"
"color: rgb(74, 148, 222);")
        self.title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.title.setObjectName("title")
        self.horizontalLayout.addWidget(self.title)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.clear_button = QtWidgets.QPushButton(self.title_box)
        self.clear_button.setMinimumSize(QtCore.QSize(151, 41))
        self.clear_button.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(74, 148, 222, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(74, 148, 222);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(74, 148, 222);\n"
"    border-right: rgb(74, 148, 222);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(85, 170, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(74, 148, 222);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(74, 148, 222);\n"
"    border-right: rgb(74, 148, 222);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(74, 148, 222);\n"
"    font: 75 16pt \"Georgia\";\n"
"    border-color: rgb(62, 124, 186);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom: rgb(62, 124, 186);\n"
"    border-right: rgb(62, 124, 186);\n"
"}")
        self.clear_button.setObjectName("clear_button")
        self.horizontalLayout.addWidget(self.clear_button)
        self.verticalLayout.addWidget(self.title_box)
        self.state_box = QtWidgets.QGroupBox(Dialog)
        self.state_box.setMinimumSize(QtCore.QSize(1442, 55))
        self.state_box.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.state_box.setStyleSheet("QGroupBox {\n"
"    border: 1px rgd(100,100,100);\n"
"    \n"
"    background-color: rgb(74, 74, 74);\n"
"}")
        self.state_box.setTitle("")
        self.state_box.setObjectName("state_box")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.state_box)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.state_box)
        self.label_2.setMinimumSize(QtCore.QSize(125, 40))
        self.label_2.setMaximumSize(QtCore.QSize(125, 40))
        self.label_2.setStyleSheet("font: 75 12pt \"Georgia\";color:rgb(200, 255, 200);background-color: rgb(74, 74, 74);")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.choose_state_type = QtWidgets.QComboBox(self.state_box)
        self.choose_state_type.setMinimumSize(QtCore.QSize(170, 40))
        self.choose_state_type.setMaximumSize(QtCore.QSize(170, 40))
        self.choose_state_type.setStyleSheet("font: 75 11pt \"Georgia\";\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(0, 170, 0)")
        self.choose_state_type.setObjectName("choose_state_type")
        self.choose_state_type.addItem("")
        self.choose_state_type.addItem("")
        self.choose_state_type.addItem("")
        self.choose_state_type.addItem("")
        self.horizontalLayout_2.addWidget(self.choose_state_type)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label_3 = QtWidgets.QLabel(self.state_box)
        self.label_3.setMinimumSize(QtCore.QSize(115, 40))
        self.label_3.setMaximumSize(QtCore.QSize(115, 40))
        self.label_3.setStyleSheet("font: 75 12pt \"Georgia\";color:rgb(200, 255, 200);background-color: rgb(74, 74, 74);")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.state_to_delete = QtWidgets.QComboBox(self.state_box)
        self.state_to_delete.setMinimumSize(QtCore.QSize(60, 40))
        self.state_to_delete.setMaximumSize(QtCore.QSize(60, 40))
        self.state_to_delete.setStyleSheet("font: 75 11pt \"Georgia\";\n"
                                           "    background-color: rgb(255, 255, 255);\n"
                                           "    color: rgb(0, 170, 0)")
        self.state_to_delete.setObjectName("state_to_delete")
        self.horizontalLayout_2.addWidget(self.state_to_delete)
        self.delete_state_button = QtWidgets.QPushButton(self.state_box)
        self.delete_state_button.setMinimumSize(QtCore.QSize(80, 40))
        self.delete_state_button.setMaximumSize(QtCore.QSize(80, 40))
        self.delete_state_button.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 255, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 12pt \"Georgia\";\n"
"    border-color: rgb(0, 204, 0);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(0, 204, 0);\n"
"    border-right: rgb(0, 204, 0);\n"
"}\n"
"QPushButton:hover{\n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 255, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 12pt \"Georgia\";\n"
"    border-color: rgb(0, 204, 0);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(0, 204, 0);\n"
"    border-right: rgb(0, 204, 0);\n"
"}\n"
"QPushButton:pressed{\n"
"    \n"
"    background-color: rgb(0, 255, 0);\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(0, 204, 0);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom: rgb(0, 204, 0);\n"
"    border-right: rgb(0, 204, 0);\n"
"}")
        self.delete_state_button.setObjectName("delete_state_button")
        self.horizontalLayout_2.addWidget(self.delete_state_button)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.label_4 = QtWidgets.QLabel(self.state_box)
        self.label_4.setMinimumSize(QtCore.QSize(185, 40))
        self.label_4.setMaximumSize(QtCore.QSize(185, 40))
        self.label_4.setStyleSheet("font: 75 12pt \"Georgia\";color:rgb(200, 255, 200);background-color: rgb(74, 74, 74);")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.transition_from = QtWidgets.QComboBox(self.state_box)
        self.transition_from.setMinimumSize(QtCore.QSize(60, 40))
        self.transition_from.setMaximumSize(QtCore.QSize(60, 40))
        self.transition_from.setStyleSheet("font: 75 11pt \"Georgia\";\n"
                                           "    background-color: rgb(255, 255, 255);\n"
                                           "    color: rgb(0, 170, 0)")
        self.transition_from.setObjectName("transition_from")
        self.horizontalLayout_2.addWidget(self.transition_from)
        self.label_5 = QtWidgets.QLabel(self.state_box)
        self.label_5.setMinimumSize(QtCore.QSize(30, 40))
        self.label_5.setMaximumSize(QtCore.QSize(30, 40))
        self.label_5.setStyleSheet("font: 75 12pt \"Georgia\";color:rgb(200, 255, 200);background-color: rgb(74, 74, 74);")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.transition_to = QtWidgets.QComboBox(self.state_box)
        self.transition_to.setMinimumSize(QtCore.QSize(60, 40))
        self.transition_to.setMaximumSize(QtCore.QSize(60, 40))
        self.transition_to.setStyleSheet("font: 75 11pt \"Georgia\";\n"
                                         "    background-color: rgb(255, 255, 255);\n"
                                         "    color: rgb(0, 170, 0)")
        self.transition_to.setObjectName("transition_to")
        self.horizontalLayout_2.addWidget(self.transition_to)
        self.label_6 = QtWidgets.QLabel(self.state_box)
        self.label_6.setMinimumSize(QtCore.QSize(110, 40))
        self.label_6.setMaximumSize(QtCore.QSize(110, 40))
        self.label_6.setStyleSheet("font: 75 12pt \"Georgia\";color:rgb(200, 255, 200);background-color: rgb(74, 74, 74);")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.transition_value = QtWidgets.QLineEdit(self.state_box)
        self.transition_value.setMinimumSize(QtCore.QSize(150, 40))
        self.transition_value.setMaximumSize(QtCore.QSize(150, 40))
        self.transition_value.setStyleSheet("QLineEdit{\n"
"    font: 12pt \"Georgia\";\n"
"    color: rgb(255, 255, 255);\n"
"    border-color:  rgb(200, 255, 200);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"background-color: rgb(74, 74, 74);\n"
"}\n"
"QLineEdit:hover{\n"
"    font: 12pt \"Georgia\";\n"
"    color: rgb(255, 255, 255);\n"
"    border-color:rgb(0, 255, 0);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"background-color: rgb(74, 74, 74);\n"
"}")
        self.transition_value.setObjectName("transition_value")
        self.horizontalLayout_2.addWidget(self.transition_value)
        self.epsilon_button = QtWidgets.QPushButton(self.state_box)
        self.epsilon_button.setMinimumSize(QtCore.QSize(30, 40))
        self.epsilon_button.setMaximumSize(QtCore.QSize(30, 40))
        self.epsilon_button.setStyleSheet("QPushButton{\n"
                                          "    background-color: rgb(255, 255, 255);\n"
                                          "    font: 75 14pt \"Georgia\";\n"
                                          "    border-color: rgb(0, 0, 0);\n"
                                          "    border-width : 2px;\n"
                                          "}\n"
                                          "QPushButton:hover{\n"
                                          "    background-color:  rgb(200, 255, 200);\n"
                                          "    font: 75 14pt \"Georgia\";\n"
                                          "    border-color:  rgb(0, 0, 0);\n"
                                          "    border-width : 2px;\n"
                                          "}\n"
                                          "QPushButton:pressed{\n"
                                          "    background-color:rgb(200, 255, 200);\n"
                                          "    font: 75 16pt \"Georgia\";\n"
                                          "    border-color: rgb(0, 0, 0);\n"
                                          "    border-width : 2px;\n"
                                          "}")
        self.epsilon_button.setObjectName("epsilon_button")
        self.epsilon_button.setToolTip('epsilon')
        self.horizontalLayout_2.addWidget(self.epsilon_button)
        self.delta_button = QtWidgets.QPushButton(self.state_box)
        self.delta_button.setMinimumSize(QtCore.QSize(30, 40))
        self.delta_button.setMaximumSize(QtCore.QSize(30, 40))
        self.delta_button.setStyleSheet("QPushButton{\n"
                                        "    background-color: rgb(255, 255, 255);\n"
                                        "    font: 75 14pt \"Georgia\";\n"
                                        "    border-color: rgb(0, 0, 0);\n"
                                        "    border-width : 2px;\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "    background-color:  rgb(200, 255, 200);\n"
                                        "    font: 75 14pt \"Georgia\";\n"
                                        "    border-color:  rgb(0, 0, 0);\n"
                                        "    border-width : 2px;\n"
                                        "}\n"
                                        "QPushButton:pressed{\n"
                                        "    background-color:rgb(200, 255, 200);\n"
                                        "    font: 75 16pt \"Georgia\";\n"
                                        "    border-color: rgb(0, 0, 0);\n"
                                        "    border-width : 2px;\n"
                                        "}")
        self.delta_button.setObjectName("delta_button")
        self.delta_button.setToolTip('Blank symbol on TM : delta')
        self.horizontalLayout_2.addWidget(self.delta_button)
        self.phi_button = QtWidgets.QPushButton(self.state_box)
        self.phi_button.setMinimumSize(QtCore.QSize(30, 40))
        self.phi_button.setMaximumSize(QtCore.QSize(30, 40))
        self.phi_button.setStyleSheet("QPushButton{\n"
                                      "    background-color: rgb(255, 255, 255);\n"
                                      "    font: 75 14pt \"Georgia\";\n"
                                      "    border-color: rgb(0, 0, 0);\n"
                                      "    border-width : 2px;\n"
                                      "}\n"
                                      "QPushButton:hover{\n"
                                      "    background-color:  rgb(200, 255, 200);\n"
                                      "    font: 75 14pt \"Georgia\";\n"
                                      "    border-color:  rgb(0, 0, 0);\n"
                                      "    border-width : 2px;\n"
                                      "}\n"
                                      "QPushButton:pressed{\n"
                                      "    background-color:rgb(200, 255, 200);\n"
                                      "    font: 75 16pt \"Georgia\";\n"
                                      "    border-color: rgb(0, 0, 0);\n"
                                      "    border-width : 2px;\n"
                                      "}")
        self.phi_button.setObjectName("phi_button")
        self.phi_button.setToolTip('Right end marker on LBA : phi')
        self.horizontalLayout_2.addWidget(self.phi_button)
        self.gamma_button = QtWidgets.QPushButton(self.state_box)
        self.gamma_button.setMinimumSize(QtCore.QSize(30, 40))
        self.gamma_button.setMaximumSize(QtCore.QSize(30, 40))
        self.gamma_button.setStyleSheet("QPushButton{\n"
                                        "    background-color: rgb(255, 255, 255);\n"
                                        "    font: 75 14pt \"Georgia\";\n"
                                        "    border-color: rgb(0, 0, 0);\n"
                                        "    border-width : 2px;\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "    background-color:  rgb(200, 255, 200);\n"
                                        "    font: 75 14pt \"Georgia\";\n"
                                        "    border-color:  rgb(0, 0, 0);\n"
                                        "    border-width : 2px;\n"
                                        "}\n"
                                        "QPushButton:pressed{\n"
                                        "    background-color:rgb(200, 255, 200);\n"
                                        "    font: 75 16pt \"Georgia\";\n"
                                        "    border-color: rgb(0, 0, 0);\n"
                                        "    border-width : 2px;\n"
                                        "}")
        self.gamma_button.setObjectName("gamma_button")
        self.gamma_button.setToolTip('Left end marker on LBA : gamma')
        self.horizontalLayout_2.addWidget(self.gamma_button)
        self.add_trasition_button = QtWidgets.QPushButton(self.state_box)
        self.add_trasition_button.setMinimumSize(QtCore.QSize(80, 40))
        self.add_trasition_button.setMaximumSize(QtCore.QSize(80, 40))
        self.add_trasition_button.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 255, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 12pt \"Georgia\";\n"
"    border-color: rgb(0, 204, 0);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(0, 204, 0);\n"
"    border-right: rgb(0, 204, 0);\n"
"}\n"
"QPushButton:hover{\n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 255, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 12pt \"Georgia\";\n"
"    border-color: rgb(0, 204, 0);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(0, 204, 0);\n"
"    border-right: rgb(0, 204, 0);\n"
"}\n"
"QPushButton:pressed{\n"
"    \n"
"    background-color: rgb(0, 255, 0);\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(0, 204, 0);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom: rgb(0, 204, 0);\n"
"    border-right: rgb(0, 204, 0);\n"
"}")
        self.add_trasition_button.setObjectName("add_trasition_button")
        self.horizontalLayout_2.addWidget(self.add_trasition_button)
        self.verticalLayout.addWidget(self.state_box)
        self.verifier_box = QtWidgets.QGroupBox(Dialog)
        self.verifier_box.setMinimumSize(QtCore.QSize(1442, 55))
        self.verifier_box.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verifier_box.setStyleSheet("QGroupBox {\n"
"    border: 1px rgd(100,100,100);\n"
"}")
        self.verifier_box.setTitle("")
        self.verifier_box.setObjectName("verifier_box")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.verifier_box)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.verifier_box)
        self.label_7.setMinimumSize(QtCore.QSize(135, 40))
        self.label_7.setMaximumSize(QtCore.QSize(135, 40))
        self.label_7.setStyleSheet("font: 75 12pt \"Georgia\";color:rgb(255, 255, 255);")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.choose_sm = QtWidgets.QComboBox(self.verifier_box)
        self.choose_sm.setMinimumSize(QtCore.QSize(100, 40))
        self.choose_sm.setMaximumSize(QtCore.QSize(100, 40))
        self.choose_sm.setStyleSheet("font: 75 11pt \"Georgia\";\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(66, 132, 198);")
        self.choose_sm.setObjectName("choose_sm")
        self.choose_sm.addItem("")
        self.choose_sm.addItem("")
        self.choose_sm.addItem("")
        self.choose_sm.addItem("")
        self.choose_sm.addItem("")
        self.choose_sm.addItem("")
        self.choose_sm.addItem("")
        self.choose_sm.addItem("")
        self.choose_sm.addItem("")
        self.horizontalLayout_3.addWidget(self.choose_sm)
        self.check_sm_type_button = QtWidgets.QPushButton(self.verifier_box)
        self.check_sm_type_button.setMinimumSize(QtCore.QSize(360, 40))
        self.check_sm_type_button.setMaximumSize(QtCore.QSize(360, 40))
        self.check_sm_type_button.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(74, 148, 222, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(74, 148, 222);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(74, 148, 222);\n"
"    border-right: rgb(74, 148, 222);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(85, 170, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(74, 148, 222);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(74, 148, 222);\n"
"    border-right: rgb(74, 148, 222);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(74, 148, 222);\n"
"    font: 75 16pt \"Georgia\";\n"
"    border-color: rgb(62, 124, 186);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom: rgb(62, 124, 186);\n"
"    border-right: rgb(62, 124, 186);\n"
"}")
        self.check_sm_type_button.setObjectName("check_sm_type_button")
        self.horizontalLayout_3.addWidget(self.check_sm_type_button)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.label_8 = QtWidgets.QLabel(self.verifier_box)
        self.label_8.setMinimumSize(QtCore.QSize(145, 40))
        self.label_8.setMaximumSize(QtCore.QSize(145, 40))
        self.label_8.setStyleSheet("font: 75 12pt \"Georgia\";color:rgb(255, 255, 255);")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        self.input = QtWidgets.QLineEdit(self.verifier_box)
        self.input.setMinimumSize(QtCore.QSize(300, 40))
        self.input.setMaximumSize(QtCore.QSize(300, 40))
        self.input.setStyleSheet("QLineEdit{\n"
"    font: 14pt \"Georgia\";\n"
"    color: rgb(255, 255, 255);\n"
"    border-color: rgb(74, 148, 222);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"}\n"
"QLineEdit:hover{\n"
"    font: 14pt \"Georgia\";\n"
"    color: rgb(255, 255, 255);\n"
"    border-color: rgb(0, 255, 255);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"}")
        self.input.setObjectName("input")
        self.horizontalLayout_3.addWidget(self.input)
        self.check_input_buton = QtWidgets.QPushButton(self.verifier_box)
        self.check_input_buton.setMinimumSize(QtCore.QSize(200, 40))
        self.check_input_buton.setMaximumSize(QtCore.QSize(200, 40))
        self.check_input_buton.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(74, 148, 222, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(74, 148, 222);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(74, 148, 222);\n"
"    border-right: rgb(74, 148, 222);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(85, 170, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    font: 75 14pt \"Georgia\";\n"
"    border-color: rgb(74, 148, 222);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom:rgb(74, 148, 222);\n"
"    border-right: rgb(74, 148, 222);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(74, 148, 222);\n"
"    font: 75 16pt \"Georgia\";\n"
"    border-color: rgb(62, 124, 186);\n"
"    border-width : 1px;\n"
"    border-style:inset;\n"
"    border-radius:20px;\n"
"    border-bottom: rgb(62, 124, 186);\n"
"    border-right: rgb(62, 124, 186);\n"
"}")
        self.check_input_buton.setObjectName("check_input_buton")
        self.horizontalLayout_3.addWidget(self.check_input_buton)
        self.verticalLayout.addWidget(self.verifier_box)
        self.design_box = QtWidgets.QGroupBox(Dialog)
        self.design_box.setMinimumSize(QtCore.QSize(1442, 778))
        self.design_box.setStyleSheet("QGroupBox {\n"
"    border: 1px rgd(100,100,100);\n"
"}")
        self.design_box.setTitle("")
        self.design_box.setObjectName("design_box")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.design_box)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        ##
        self.draw_areea = MyWidget(self.design_box)
        self.draw_areea.setMinimumSize(QtCore.QSize(1000, 765))
        self.draw_areea.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.draw_areea.setObjectName("draw_areea")
        self.horizontalLayout_4.addWidget(self.draw_areea)
        self.response = QtWidgets.QPlainTextEdit(self.design_box)
        self.response.setMinimumSize(QtCore.QSize(350, 765))
        self.response.setMaximumSize(QtCore.QSize(350, 16777215))
        self.response.setStyleSheet("font: 75 14pt \"Georgia\";color:rgb(255, 255, 255);")
        self.response.setObjectName("response")
        self.horizontalLayout_4.addWidget(self.response)
        self.verticalLayout.addWidget(self.design_box)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.undo_button.setText(_translate("Dialog", "UNDO"))
        self.title.setText(_translate("Dialog", "SM Designer&Verifier"))
        self.clear_button.setText(_translate("Dialog", "CLEAR"))
        self.label_2.setText(_translate("Dialog", "Choose state:"))
        self.choose_state_type.setItemText(0, _translate("Dialog", "initial state"))
        self.choose_state_type.setItemText(1, _translate("Dialog", "final state"))
        self.choose_state_type.setItemText(2, _translate("Dialog", "inital & final state"))
        self.choose_state_type.setItemText(3, _translate("Dialog", "normal state"))
        self.label_3.setText(_translate("Dialog", "Delete state:"))
        self.delete_state_button.setText(_translate("Dialog", "Delete"))
        self.label_4.setText(_translate("Dialog", "Add transition from:"))
        self.label_5.setText(_translate("Dialog", " to:"))
        self.label_6.setText(_translate("Dialog", " with value:"))
        self.epsilon_button.setText(_translate("Dialog", "ε"))
        self.delta_button.setText(_translate("Dialog", "Δ"))
        self.phi_button.setText(_translate("Dialog", "Φ"))
        self.gamma_button.setText(_translate("Dialog", "Γ"))
        self.add_trasition_button.setText(_translate("Dialog", "Add"))
        self.label_7.setText(_translate("Dialog", "Check for type:"))
        self.choose_sm.setItemText(0, _translate("Dialog", "All"))
        self.choose_sm.setItemText(1, _translate("Dialog", "DFA"))
        self.choose_sm.setItemText(2, _translate("Dialog", "NFA"))
        self.choose_sm.setItemText(3, _translate("Dialog", "DPDA"))
        self.choose_sm.setItemText(4, _translate("Dialog", "PDA"))
        self.choose_sm.setItemText(5, _translate("Dialog", "LBA"))
        self.choose_sm.setItemText(6, _translate("Dialog", "TM"))
        self.choose_sm.setItemText(7, _translate("Dialog", "DBA"))
        self.choose_sm.setItemText(8, _translate("Dialog", "NBA"))
        self.check_sm_type_button.setText(_translate("Dialog", "CHECK AUTOMATA\'S TYPE"))
        self.label_8.setText(_translate("Dialog", "Check for input:"))
        self.check_input_buton.setText(_translate("Dialog", "CHECK INPUT"))
        self.response.setPlainText(_translate("Dialog", "The answer will be displayed here"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = SMVerifier()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
