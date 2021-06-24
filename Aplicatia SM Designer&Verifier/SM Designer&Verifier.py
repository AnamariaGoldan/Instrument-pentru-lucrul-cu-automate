# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtWidgets
import sys
from app_interface import SMVerifier
import globals
from Nodes_and_Transition_classes import Nodes,Transition
from PyQt5.QtCore import QTimer
from SMVerifier import *

global no_of_states,initial_states,final_states,first_symbol,transitions,what_check,input_check,type_check

def afisare_solutie(solution):
    solution.sort(key=len)
    tranzitii = ""
    for sol in solution:
        for state in sol:
            tranzitii = tranzitii + state + "-"
        tranzitii = tranzitii[:-1]
        tranzitii += "; "
    tranzitii = tranzitii[:-2]
    return tranzitii


def clear_data():
    global no_of_states,all_states, initial_state,final_states,first_symbol,transitions,what_check,input_check,type_check
    no_of_states = 0
    all_states = []
    initial_state =[]
    final_states =[]
    first_symbol=[]
    transitions=dict()
    what_check=""
    input_check=""
    type_check=""

def create_data(last_node,list_nodes,list_transitions,whatCheck,inputCheck,typeCheck):
    global no_of_states, all_states, initial_state, final_states, first_symbol, transitions, what_check, input_check, type_check
    no_of_states = last_node
    all_states = [chr(48 + i) for i in range(no_of_states)]
    first_symbol.append("z")
    what_check = whatCheck
    input_check = inputCheck
    type_check = typeCheck
    for state in list_nodes:
        if state.getType()=="initial state" or state.getType()=="inital & final state":
            initial_state.append(str(state.getId()))
        if state.getType()=="final state" or state.getType()=="inital & final state":
            final_states.append(str(state.getId()))

    for transition in list_transitions:
        transitions[str(transition.getNodeFrom())]=dict()
        #print(transition.value)

    for transition in list_transitions:
        node_from = str(transition.getNodeFrom())
        node_to = str(transition.getNodeTo())
        transitions[node_from][node_to]=transition.getValues()

    '''print(no_of_states)
    print(initial_state)
    print(final_states)
    print(first_symbol)
    print(transitions)
    print(what_check)
    print(input_check)
    print(type_check)'''

def algorithms(no_of_states,initial_state,final_states,first_symbol,transitions,what_check,input_check,type_check,all_states):
    #print(no_of_states,initial_state,final_states,first_symbol,transitions,what_check,input_check,type_check,all_states)
    #All,DFA,NFA,DPDA,PDA,TM,LBA,DBA,NBA
    response_type_check = "Inputted state machine is of type "
    response_input_check = ""
    automata = dict()
    automata["all_states"] = all_states
    automata["initial_states"] = initial_state
    automata["final_states"] = final_states
    automata["transitions"] = transitions
    #print(automata)
    first_found = 0
    all_found = 0
    #DFA
    if type_check=="DFA" or type_check=="All":
        if check_if_DFA(automata) == 1:
            response_type_check += "DFA, "
            all_found += 1
            if what_check == "input" and first_found == 0:
                return_value = check_input_in_DFA(input_check,automata)
                if return_value[0] == 1:
                    response_input_check += "The input was accepted by the state machine. State path(s) : "
                    response_input_check += afisare_solutie(return_value[1])
                else:
                    response_input_check += "The input was not accepted by the state machine."
                first_found = 1
        else:
            if type_check!="All":
                response_type_check = "Inputted state machine is not of type DFA."

    #NFA
    if type_check=="NFA" or type_check=="All":
        if check_if_NFA(automata) == 1:
            response_type_check += "NFA, "
            all_found += 1
            if what_check == "input" and first_found == 0:
                return_value = check_input_in_NFA(input_check,automata)
                print(return_value)
                if return_value[0] == 1:
                    response_input_check += "The input was accepted by the state machine. State path(s) : "
                    response_input_check += afisare_solutie(return_value[1])
                else:
                    response_input_check += "The input was not accepted by the state machine."
                first_found = 1
        else:
            if type_check!="All":
                response_type_check = "Inputted state machine is not of type NFA."

    #DPDA
    if type_check=="DPDA" or type_check=="All":
        if check_if_DPDA(first_symbol,automata) == 1:
            response_type_check += "DPDA, "
            all_found += 1
            if what_check == "input" and first_found == 0:
                return_value = check_input_in_DPDA(input_check, first_symbol, automata)
                if return_value[0] == 1:
                    response_input_check += "The input was accepted by the state machine. State path(s) : "
                    response_input_check += afisare_solutie(return_value[1])
                else:
                    response_input_check += "The input was not accepted by the state machine."
                first_found = 1
        else:
            if type_check!="All":
                response_type_check = "Inputted state machine is not of type DPDA."

    #PDA
    if type_check=="PDA" or type_check=="All":
        if check_if_PDA(first_symbol,automata) == 1:
            response_type_check += "PDA, "
            all_found += 1
            if what_check == "input" and first_found == 0:
                return_value = check_input_in_PDA(input_check, first_symbol, automata)
                if return_value[0] == 1:
                    response_input_check += "The input was accepted by the state machine. State path(s) : "
                    response_input_check += afisare_solutie(return_value[1])
                else:
                    response_input_check += "The input was not accepted by the state machine."
                first_found = 1
        else:
            if type_check!="All":
                response_type_check = "Inputted state machine is not of type PDA."

    #TM
    if type_check=="TM" or type_check=="All":
        if check_if_TM(automata) == 1:
            response_type_check += "TM, "
            all_found += 1
            if what_check == "input" and first_found == 0:
                return_value = check_input_in_TM(input_check, automata)
                if return_value[0] == 1:
                    response_input_check += "The input was accepted by the state machine. State path(s) : "
                    response_input_check += afisare_solutie(return_value[1])
                else:
                    response_input_check += "The input was not accepted by the state machine."
                first_found = 1
        else:
            if type_check!="All":
                response_type_check = "Inputted state machine is not of type TM."

    #LBA
    if type_check=="LBA" or type_check=="All":
        if check_if_LBA(automata) == 1:
            response_type_check += "LBA, "
            all_found += 1
            if what_check == "input" and first_found == 0:
                return_value = check_input_in_LBA(input_check, automata)
                if return_value[0] == 1:
                    response_input_check += "The input was accepted by the state machine. State path(s) : "
                    response_input_check += afisare_solutie(return_value[1])
                else:
                    response_input_check += "The input was not accepted by the state machine."
                first_found = 1
        else:
            if type_check!="All":
                response_type_check = "Inputted state machine is not of type LBA."

    #DBA
    if type_check=="DBA" or type_check=="All":
        if check_if_DBA(automata) == 1:
            response_type_check += "DBA, "
            all_found += 1
            if what_check == "input" and first_found == 0:
                return_value = check_input_in_DBA(input_check, automata)
                if return_value[0] == 1:
                    response_input_check += "The input was accepted by the state machine. State path(s) : "
                    response_input_check += afisare_solutie(return_value[1])
                else:
                    response_input_check += "The input was not accepted by the state machine."
                first_found = 1
        else:
            if type_check!="All":
                response_type_check = "Inputted state machine is not of type DBA."

    #NBA
    if type_check=="NBA" or type_check=="All":
        if check_if_NBA(automata) == 1:
            response_type_check += "NBA, "
            all_found += 1
            if what_check == "input" and first_found == 0:
                return_value = check_input_in_NBA(input_check, automata)
                if return_value[0] == 1:
                    response_input_check += "The input was accepted by the state machine. State path(s) : "
                    response_input_check += afisare_solutie(return_value[1])
                else:
                    response_input_check += "The input was not accepted by the state machine."
                first_found = 1
        else:
            if type_check!="All":
                response_type_check = "Inputted state machine is not of type NBA."

    #print(response_type_check)

    if type_check == "All" and all_found == 0:
        response_type_check = "Inputted state machine is not of any of the selected types."
    else:
        if all_found != 0:
            response_type_check = response_type_check[:-2]
            response_type_check += "."

    #print(response_type_check)
    final_response = response_type_check +  " " + response_input_check
    print(final_response)
    return final_response


class SMVerifierI(SMVerifier,QDialog):
    def __init__(self):
        super(SMVerifierI, self).__init__()
        globals.init()
        clear_data()
        self.setupUi(self)
        self.update_current_state_type()
        self.actual_state_in_sm = 0
        self.response.clear()
        self.response.insertPlainText("The answer will be displayed here")
        self.response.repaint()
        #print(self.choose_state_type.currentText())
        #update in timp real pt combobox-uri
        self.qTimer = QTimer()
        self.qTimer.setInterval(1000)  # 1000 ms = 1 s
        self.qTimer.timeout.connect(self.changeComboBoxesValues)
        self.qTimer.start()
        #funtionalitate buton UNDO
        self.undo_button.clicked.connect(self.undo_function)
        # funtionalitate buton CLEAR
        self.clear_button.clicked.connect(self.clear_function)
        # funtionalitate buton Delete state
        self.delete_state_button.clicked.connect(self.delete_state_function)
        # funtionalitate buton Add transition
        self.add_trasition_button.clicked.connect(self.add_transition_function)
        #functionalitate choose_state_type combo box
        self.choose_state_type.currentIndexChanged.connect(self.update_current_state_type)
        #functionalitate checm sm buton
        self.check_sm_type_button.clicked.connect(lambda : self.check_sm_function(option=0))
        # functionalitate checm input buton
        self.check_input_buton.clicked.connect(lambda : self.check_sm_function(option=1))
        # functionalitate buton epsilon
        self.epsilon_button.clicked.connect(self.add_epsilon_to_value)
        # funtionalitate buton delta
        self.delta_button.clicked.connect(self.add_delta_to_value)
        # funtionalitate buton phi
        self.phi_button.clicked.connect(self.add_phi_to_value)
        # funtionalitate buton gamma
        self.gamma_button.clicked.connect(self.add_gamma_to_value)


    def add_epsilon_to_value(self):
        self.transition_value.setText(self.transition_value.text() + "ε")
        self.transition_value.repaint()

    def add_delta_to_value(self):
        self.transition_value.setText(self.transition_value.text() + "Δ")
        self.transition_value.repaint()

    def add_phi_to_value(self):
        self.transition_value.setText(self.transition_value.text() + "Φ")
        self.transition_value.repaint()

    def add_gamma_to_value(self):
        self.transition_value.setText(self.transition_value.text() + "Γ")
        self.transition_value.repaint()

    def check_sm_function(self,option):
        self.draw_areea.actualizare_liste()
        self.draw_areea.actualizare_globals()
        clear_data()
        #type option
        if option == 0:
            create_data(globals.actual_node,self.draw_areea.list_nodes,self.draw_areea.list_transitions,"type","",self.choose_sm.currentText())
        #input option
        if option == 1:
            create_data(globals.actual_node, self.draw_areea.list_nodes, self.draw_areea.list_transitions, "input", self.input.text(),self.choose_sm.currentText())
        global no_of_states, all_states, initial_state, final_states, first_symbol, transitions, what_check, input_check, type_check
        response =  algorithms(no_of_states, initial_state, final_states, first_symbol, transitions, what_check,input_check, type_check,all_states)
        print("{")
        print("    'all_states' : ",all_states,',')
        print("    'initial_state' : ", initial_state,',')
        print("    'final_states' : ", final_states, ',')
        print("    'transitions' : ", transitions)
        print("}")
        self.response.clear()
        self.response.insertPlainText(response)
        self.response.repaint()



    def changeComboBoxesValues(self):
        self.draw_areea.actualizare_liste()
        self.draw_areea.actualizare_globals()
        if self.actual_state_in_sm != globals.actual_node:
            self.state_to_delete.clear()
            self.transition_from.clear()
            self.transition_to.clear()
            for val in range(globals.actual_node):
                self.state_to_delete.addItem(str(val))
                self.transition_from.addItem(str(val))
                self.transition_to.addItem(str(val))
            self.actual_state_in_sm = globals.actual_node
            self.state_to_delete.repaint()
            self.transition_from.repaint()
            self.transition_to.repaint()

    def undo_function(self):
        if len(self.draw_areea.actual_App_State) > 1:
            self.draw_areea.actual_App_State.pop()
            self.repaint()

    def clear_function(self):
        self.draw_areea.actual_App_State.append([[],[]])
        self.repaint()


    def update_current_state_type(self):
        #print(self.choose_state_type.currentText())
        globals.current_state_type = self.choose_state_type.currentText()

    def delete_state_function(self):
        #self.transition_value.setText(self.transition_value.text() + "d")
        #self.transition_value.repaint()
        self.draw_areea.actualizare_liste()
        self.draw_areea.actualizare_globals()
        state_to_delete = self.state_to_delete.currentText()

        if state_to_delete:
            state_to_delete_int = int(state_to_delete)
            copie_list_transition = self.draw_areea.list_transitions[:]
            for t in copie_list_transition:
                if t.getNodeFrom()==state_to_delete_int or t.getNodeTo()==state_to_delete_int:
                    self.draw_areea.list_transitions.remove(t)
            c = self.draw_areea.getElemByIdList(state_to_delete_int)
            self.draw_areea.list_nodes.remove(c)
            for c in self.draw_areea.list_nodes:
                if c.getId() > state_to_delete_int:
                    c.changeId(c.getId()-1)

            for t in self.draw_areea.list_transitions:
                if t.getNodeFrom() > state_to_delete_int:
                    t.changeNodeFrom(t.getNodeFrom()-1)
                if t.getNodeTo() > state_to_delete_int:
                    t.changeNodeTo(t.getNodeTo()-1)

            self.draw_areea.actualizare_globals()
            #self.draw_areea.actual_App_State.append([deepcopy(self.draw_areea.list_nodes),deepcopy(self.draw_areea.list_transitions)])
            self.draw_areea.append_in_App_State(self.draw_areea.list_nodes,self.draw_areea.list_transitions)
            self.changeComboBoxesValues()
            self.repaint()

    def add_transition_function(self):
        self.draw_areea.actualizare_liste()
        self.draw_areea.actualizare_globals()
        node_from = int(self.transition_from.currentText())
        node_to = int(self.transition_to.currentText())
        value = str(self.transition_value.text())
        if len(value)!=0 :
            index =  self.draw_areea.checkIfAlreadyExists(node_from,node_to)
            if index != -1:
                self.draw_areea.list_transitions[index].updateValues(value)
            else:
                self.draw_areea.list_transitions.append(Transition(node_from,node_to,value))
            #self.draw_areea.actual_App_State.append([deepcopy(self.draw_areea.list_nodes),deepcopy(self.draw_areea.list_transitions)])
            self.draw_areea.append_in_App_State(self.draw_areea.list_nodes, self.draw_areea.list_transitions)
            self.repaint()


app = QApplication(sys.argv)
mainwindow = SMVerifierI()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)

widget.setMaximumSize(16777215,16777215)
widget.setMinimumSize(1500,964)
widget.resize(1850, 978)
widget.show()
app.exec_()
