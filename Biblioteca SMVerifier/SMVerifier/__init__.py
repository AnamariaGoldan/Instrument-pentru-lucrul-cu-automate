'''

    Aceasta este o librarie pentru validarea tipurilor automatelor si pentru verificarea acceptarii unor cuvinte de catre automate.
    Tipurile cu care lucreaza biblioteca sunt:
            Automate finite deterministe - abrevierea folosită : DFA (eng : Deterministic Finite Automata)
            Automate finite nedeterministe (inclusiv cu ε-tranziții) - abrevierea folosită : NFA (eng : Nondeterministic Finite Automata)
            Automate Büchi deterministe - abrevierea folosită : DBA (eng : Deterministic Büchi Automata)
            Automate Büchi nedeterministe - abrevierea folosită : NBA (eng : Nondeterministic Büchi Automata)
            Automate stiva deterministe - abrevierea folosită : DPDA (eng : Deterministic Pushdown Automata)
            Automate stiva (inclusiv nedeterministe) - abrevierea folosită : PDA (eng : Pushdown Automata)
            Automate liniar marginite - abrevierea folosită : LBA (eng : Linear Bounded Automata)
            Automate Turing (deterministe, cu o singura banda) - abrevierea folosită : TM (eng : Turing Machine)
    Pentru a verifica daca un automat creat este de tipul X, trebuie abelata functia check_if_X(), unde X este abrevierea automatului.
    Functiile pentru validarea tipului unui automat returneaza valoarea True sau False.
    Pentru a verifica daca un automat creat de tipul X accepta un sir de simboluri, trebuie apelata functia check_input_in X(), unde X este abrevierea automatului.
    Functiile pentru verificarea acceptarii unui cuvant de catre un automat returneaza (False,[]) sau (True,[lista_colutii]), unde lista_solutii contine solutiile parsarii cuvantului; o solutie reprezinta un drum de stari.

    -------------------Conventii------------------------
    În cazul automatelor LBA, marcatorul drept (eng: right end marker) este reprezentat de Φ (phi, caractere unicode : \u03A6), iar marcatorul stâng (eng: left end marker) este reprezentat de Γ (gamma, caractere unicode : \u0393).
    În cazul automatelor TM, spațiul liber (eng: blank symbol) este reprezentat de Δ (delta, caractere unicode : \u0394).


    -------------------Change Log-----------------------
    0.0.1 (24/06/2021)

    Copyright 2021 Anamaria Goldan

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


def check_if_DFA(automata : dict):
    """
        Verifica daca automatul primit ca parametru reprezinta un automat de tipul DFA.
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a',.. ] }, ..}
            }
        :return: True in cazul in care automatul reprezinta un automat DFA, sau False in caz contrar
    """

    # Se verifica sintaxa automatului. Prima etapa de verificare
    if _Private.check_syntax(automata) == 0:
        return False
    # Se verifica daca automatul reprezinta un graf de tranzitii valid. A doua etapa de verificare
    if _Private.check_structure_of_data(0,automata) == 0:
        return False

    # extragerea datelor din automat
    transitions = automata["transitions"]

    # Se verifica daca automatul este unul de tipul DFA si daca fiecare tranzitie respecta formatul 'a', fara a contine epsilon. A treia etapa de verificare
    for key in transitions.keys():
        value_for_key = []
        transition_for_key = transitions[key]
        for list_value in transition_for_key.values():
            for value in list_value:
                if value in value_for_key or value=="\u03B5" or len(value)>1:
                    return False
                else:
                    value_for_key.append(value)

    return True


def check_input_in_DFA(input : str, automata : dict):
    """
        Verifica daca automatul primit ca parametru accepta inputul primit ca parametru si returneaza solutia in caz de acceptare al cuvantului.
        :param input : cuvantul care se doreste a fi verificat in contextul acceptarii de catre automat
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a',.. ] }, ..}
            }
        :return: (True, [solutie]) in cazul in care automatul este un automat de tipul DFA si accepta cuvantul input, sau (False, []) in caz contrar
    """

    # Se verifica daca automatul primit ca parametru este un automat de tipul DFA valid. Prima etapa de verificare.
    if check_if_DFA(automata) == 0:
        return (False,[])

    # extragerea datelor din automat
    initial_states = automata["initial_states"]
    final_states = automata["final_states"]
    transitions = automata["transitions"]
    solution = []

    # Parsarea cuvantului
    if len(input)==0 and initial_states[0] in final_states:
        solution.append([initial_states[0]])
        return (True,solution)
    if len(input)==0 and initial_states[0] not in final_states:
        return (False,[])
    state = initial_states[0]
    temporar_solution = []
    for character in input:
        found = 0
        if state in transitions.keys():
            transition_state = transitions[state]
        else:
            return (False,[])
        temporar_solution.append(state)
        for new_state,values in transition_state.items():
            if found == 0:
                if character in values:
                    state = new_state
                    found += 1
        if found == 0:
            return (False,[])
    if state in final_states:
        temporar_solution.append(state)
        solution.append(temporar_solution)
        return (True,solution)
    else:
        return (False,[])


def check_if_NFA(automata : dict):
    """
        Verifica daca automatul primit ca parametru reprezinta un automat de tipul NFA.
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a',.. ] }, ..}
            }
        :return: True in cazul in care automatul reprezinta un automat NFA, sau False in caz contrar
    """

    # Se verifica sintaxa automatului. Prima etapa de verificare
    if _Private.check_syntax(automata) == 0:
        return False

    # Se verifica daca automatul reprezinta un graf de tranzitii valid. A doua etapa de verificare
    if _Private.check_structure_of_data(0,automata) == 0:
        return False

    # extragerea datelor din automat
    transitions = automata["transitions"]
    # Se verifica daca automatul este unul de tipul NFA si daca fiecare tranzitie respecta formatul 'a'. A treia etapa de verificare
    #epsilon este "\u03B5"
    for key in transitions.keys():
        transition_for_key = transitions[key]
        for list_value in transition_for_key.values():
            for value in list_value:
                if len(value)>1:
                    return False
    return True


def check_input_in_NFA(input :str, automata : dict):
    """
        Verifica daca automatul primit ca parametru accepta inputul primit ca parametru si returneaza solutia in caz de acceptare al cuvantului.
        :param input : cuvantul care se doreste a fi verificat in contextul acceptarii de catre automat
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a',.. ] }, ..}
            }
        :return: (True, [solutie]) in cazul in care automatul este un automat de tipul NFA si accepta cuvantul input, sau (False, []) in caz contrar
    """

    # Se verifica daca automatul primit ca parametru este un automat de tipul NFA valid. Prima etapa de verificare.
    if check_if_NFA(automata) == 0:
        return (False, [])

    # extragerea datelor din automat
    initial_states = automata["initial_states"]
    final_states = automata["final_states"]
    transitions = automata["transitions"]
    solution =[]

    # Parsarea cuvantului
    if len(input) == 0 and initial_states[0] in final_states:
        solution.append([initial_states[0]])
        return (True,solution)
    temporar_solution = []
    list_of_one=[]
    _Private.compute_solutions_for_input_in_NFA(input,0,initial_states[0],final_states,transitions,list_of_one,temporar_solution,solution)
    if 1 in list_of_one:
        return (True,solution)
    else:
        return (False,[])


def check_if_PDA(first_symbol : str, automata : dict):
    """
        Verifica daca automatul primit ca parametru reprezinta un automat de tipul PDA.
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a,b→z',.. ] }, ..}
            }
        :return: True in cazul in care automatul reprezinta un automat PDA, sau False in caz contrar
    """
    # Se verifica sintaxa automatului. Prima etapa de verificare
    if _Private.check_syntax(automata) == 0:
        return False

    # Se verifica daca automatul reprezinta un graf de tranzitii valid. A doua etapa de verificare
    if _Private.check_structure_of_data(0,automata) == 0 or len(first_symbol) != 1 or len(first_symbol[0]) != 1 or first_symbol[0]!="z":
        return False

    if len(first_symbol)!= 1:
        return False

    # extragerea datelor din automat
    transitions = automata["transitions"]

    # Se verifica daca automatul este unul de tipul PDA si daca fiecare tranzitie respecta formatul 'a,b→z'. A treia etapa de verificare
    found_first_symbol = 0
    for key in transitions.keys():
        transition_for_key = transitions[key]
        for list_value in transition_for_key.values():
            for value in list_value:
                if len(value) <= 5 or (value[1]!=',' or value[3:5]!="->") or (value[5]=="\u03B5" and len(value)>6):
                    return False
                if (value[1]=="," and value[2]==first_symbol[0] and value[3:5]=="->") or (value[3:5]=="->" and value[5]!="\u03B5" and first_symbol[0] in value[5:]):
                    found_first_symbol =1

    '''if found_first_symbol == 0:
        return False'''
    return True


def check_if_DPDA(first_symbol : str, automata : dict):
    """
        Verifica daca automatul primit ca parametru reprezinta un automat de tipul DPDA.
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a,b→z',.. ] }, ..}
            }
        :return: True in cazul in care automatul reprezinta un automat DPDA, sau False in caz contrar
    """

    # Se verifica daca automatul este unul PDA (care include automatele DPDA)
    if check_if_PDA(first_symbol,automata) == 0:
        return False

    # extragerea datelor din automat
    transitions = automata["transitions"]
    # Se verifica daca automatul este unul de tipul DPDA si daca fiecare tranzitie respecta formatul 'a,b→z'. A treia etapa de verificare
    for key in transitions.keys():
        transition_for_key = transitions[key]
        value_for_key=[]
        for list_value in transition_for_key.values():
            for value in list_value:
                new_value = value[:3]
                new_value_1 = "\u03B5"+new_value[1:]
                new_value_2 = new_value[:2]+"\u03B5"
                if new_value in value_for_key or new_value_1 in value_for_key or new_value_2 in value_for_key:
                    return False
                if new_value[0]=="\u03B5":
                    subs = new_value[1:]
                    res = [i for i in value_for_key if subs in i]
                    if len(res) != 0:
                        return False
                if new_value[2]=="\u03B5":
                    subs = new_value[:2]
                    res = [i for i in value_for_key if subs in i]
                    if len(res) != 0:
                        return False
                value_for_key.append(new_value)
    return True


def check_input_in_DPDA(input : str, first_symbol : str, automata : dict):
    """
        Verifica daca automatul primit ca parametru accepta inputul primit ca parametru si returneaza solutia in caz de acceptare al cuvantului.
        :param input : cuvantul care se doreste a fi verificat in contextul acceptarii de catre automat
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a,b→z',.. ] }, ..}
            }
        :return: (True, [solutie]) in cazul in care automatul este un automat de tipul DPDA si accepta cuvantul input, sau (False, []) in caz contrar
    """

    # Se verifica daca automatul primit ca parametru este un automat de tipul DPDA valid. Prima etapa de verificare.
    if check_if_DPDA(automata) == 0:
        return (False,[])

    # extragerea datelor din automat
    initial_states = automata["initial_states"]
    final_states = automata["final_states"]
    transitions = automata["transitions"]
    solution =[]
    stack = []
    stack.append(first_symbol[0])
    actual_state = initial_states[0]
    poz = 0

    # Parsarea cuvantului
    temporar_solution = []
    while( poz <= len(input) ):
        if poz == len(input) and actual_state in final_states:
            # am parcurs si ultimul element din input si am ajuns intr-o stare finala
            temporar_solution.append(actual_state)
            solution.append(temporar_solution)
            return (True,solution)
        if poz < len(input):
            character = input[poz]
        found = 0
        if actual_state not in transitions.keys():
            return (False,[])
        transition_state = transitions[actual_state]
        temporar_solution.append(actual_state)
        for new_state, values in transition_state.items():
            for value in values:
                # cazul in care a, a -> ceva
                if found == 0:
                    if len(input)!=0 and value[0]==character and len(stack)>0 and value[2]==stack[len(stack)-1] :
                        actual_state = new_state
                        stack.pop()
                        poz += 1
                        found = 1
                        if value[5:] !="\u03B5":
                            for elem in value[:4:-1]:
                                stack.append(elem)
                        break
                    # cazul in care a, \u03B5 -> ceva
                    elif len(input)!=0 and value[0]==character and value[2]=="\u03B5":
                        actual_state = new_state
                        found = 1
                        poz += 1
                        if value[5:] !="\u03B5":
                            for elem in value[:4:-1]:
                                stack.append(elem)
                        break
                    # cazul in care \u03B5, a -> ceva
                    elif value[0]=="\u03B5" and len(stack)>0 and value[2]==stack[len(stack)-1]:
                        actual_state = new_state
                        stack.pop()
                        found = 1
                        if value[5:] !="\u03B5":
                            for elem in value[:4:-1]:
                                stack.append(elem)
                        break
                    # cazul in care \u03B5, \u03B5 -> ceva
                    elif value[0]=="\u03B5" and value[2]=="\u03B5":
                        actual_state = new_state
                        found = 1
                        if value[5:] !="\u03B5":
                            for elem in value[:4:-1]:
                                stack.append(elem)
                        break
        if found == 0:
            return (False,[])

    return (False,[])


def check_input_in_PDA(input : str, first_symbol : str, automata : dict):
    """
        Verifica daca automatul primit ca parametru accepta inputul primit ca parametru si returneaza solutia in caz de acceptare al cuvantului.
        :param input : cuvantul care se doreste a fi verificat in contextul acceptarii de catre automat
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a,b→z',.. ] }, ..}
            }
        :return: (True, [solutie]) in cazul in care automatul este un automat de tipul PDA si accepta cuvantul input, sau (False, []) in caz contrar
    """

    # Se verifica daca automatul primit ca parametru este un automat de tipul PDA valid. Prima etapa de verificare.
    if check_if_PDA(automata) == 0:
        return (False, [])

    # extragerea datelor din automat
    initial_states = automata["initial_states"]
    final_states = automata["final_states"]
    transitions = automata["transitions"]
    solution =[]

    # Parsarea cuvantului
    if len(input)==0:
        empty_input = 1
    else:
        empty_input = 0

    list_of_one = []
    stack = []
    stack.append(first_symbol[0])
    temporar_solution = []
    _Private.compute_solutions_for_input_in_PDA(stack,input, 0, initial_states[0], first_symbol, final_states, transitions, list_of_one,empty_input,temporar_solution,solution)
    if 1 in list_of_one:
        return (True,solution)
    else:
        return (False,[])


def check_if_TM(automata : dict):
    """
        Verifica daca automatul primit ca parametru reprezinta un automat de tipul TM.
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a→A,D',.. ] }, ..}
            }
        :return: True in cazul in care automatul reprezinta un automat TM, sau False in caz contrar
    """

    # Se verifica sintaxa automatului. Prima etapa de verificare
    if _Private.check_syntax(automata) == 0:
        return False

    # delta \u0394 blank symbol

    # Se verifica daca automatul reprezinta un graf de tranzitii valid. A doua etapa de verificare
    if _Private.check_structure_of_data(0,automata) == 0:
        return False

    # extragerea datelor din automat
    final_states = automata["final_states"]
    transitions = automata["transitions"]

    # Se verifica daca automatul este unul de tipul TM si daca fiecare tranzitie respecta formatul 'a→A,D'. A treia etapa de verificare
    final_state_complete = 0
    for key in transitions.keys():
        value_for_key = []
        transition_for_key = transitions[key]
        for new_state, list_value in transition_for_key.items():
            for value in list_value:
                #value e de forma 'a→A,D', unde D = R/L
                if (value[0] in value_for_key) or len(value)!=6 or value[1:3]!="->" or value[4]!="," or (value[5]!="L" and value[5]!="R") or value[0]=="\u03B5" or value[3]=="\u03B5":
                    return False
                else:
                    value_for_key.append(value[0])
                if value[0]=="\u0394" and value[3]!="\u0394":
                    return False
                if new_state in final_states and value[0]=="\u0394":
                    final_state_complete = 1

    if final_state_complete == 0:
        return False

    return True


def check_input_in_TM(input : str, automata : dict):
    """
        Verifica daca automatul primit ca parametru accepta inputul primit ca parametru si returneaza solutia in caz de acceptare al cuvantului.
        :param input : cuvantul care se doreste a fi verificat in contextul acceptarii de catre automat
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a→A,D',.. ] }, ..}
            }
        :return: (True, [solutie]) in cazul in care automatul este un automat de tipul TM si accepta cuvantul input, sau (False, []) in caz contrar
    """

    # Se verifica daca automatul primit ca parametru este un automat de tipul TM valid. Prima etapa de verificare.
    if check_if_TM(automata) == 0:
        return (False,[])

    # extragerea datelor din automat
    initial_states = automata["initial_states"]
    final_states = automata["final_states"]
    transitions = automata["transitions"]
    solution = []

    # Crearea bandei de lucrul pentru automatul TM
    tape=[]
    for character in input:
        tape.append(character)
    tape.append("\u0394")
    # tape.append("\u0394")

    # Parsarea cuvantului
    temporar_solution = []
    actual_state = initial_states[0]
    poz = 0
    all_states_traveled =""
    while actual_state not in final_states:
        all_states_traveled += actual_state
        # Verificam daca, in incercarea parsarii cuvantului, automatul tinde sa nu se mai opreasca
        res = _Private.longest_substring(all_states_traveled)
        res = res[:5]
        if all_states_traveled.count(res) > 50:
            # Cazul in care se observa comportament care duce la neoprirea automatului
            return (False,[])
        found = 0
        if actual_state in transitions.keys():
            transition_state = transitions[actual_state]
        else:
            return (False,[])
        temporar_solution.append(actual_state)
        for new_state, values in transition_state.items():
            for value in values:
                if found == 0:
                    if value[0]==tape[poz]:
                        tape[poz]=value[3]
                        if value[5]=='R':
                            poz += 1
                            if poz==len(tape):
                                tape.append("\u0394")
                        if value[5]=='L' and poz > 0:
                            poz -= 1
                        found = 1
                        actual_state = new_state
                        break
        if found == 0:
            return (False,[])

    if actual_state not in final_states:
        return (False,[])
    else:
        temporar_solution.append(actual_state)
        solution.append(temporar_solution)
    return (True,solution)


def check_if_LBA(automata : dict):
    """
        Verifica daca automatul primit ca parametru reprezinta un automat de tipul LBA.
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a→A,D',.. ] }, ..}
            }
        :return: True in cazul in care automatul reprezinta un automat LBA, sau False in caz contrar
    """

    # Se verifica sintaxa automatului. Prima etapa de verificare
    if _Private.check_syntax(automata) == 0:
        return False
    # left end marker \u0393 gamma
    # right end marker \u03A6 phi

    # Se verifica daca automatul reprezinta un graf de tranzitii valid. A doua etapa de verificare
    if _Private.check_structure_of_data(0,automata) == 0:
        return False

    # extragerea datelor din automat
    initial_states = automata["initial_states"]
    final_states = automata["final_states"]
    transitions = automata["transitions"]

    # Se verifica daca automatul este unul de tipul LBA si daca fiecare tranzitie respecta formatul 'a→A,D'. A treia etapa de verificare
    left_marker_find = 0
    right_marker_find = 0
    for key in transitions.keys():
        transition_for_key = transitions[key]
        for new_state, list_value in transition_for_key.items():
            for value in list_value:
                #value e de forma a->A,R
                if len(value)!=6 or value[1:3]!="->" or value[4]!="," or (value[5]!="L" and value[5]!="R" and value[5]!="S") or value[0]=="\u03B5" or value[3]=="\u03B5":
                    return False
                #left end marker
                if value[0]=="\u0393" and (value[3]!="\u0393" or value[5]!="R"):
                    return False
                #right end marker
                if value[0]=="\u03A6" and (value[3]!="\u03A6" or value[5]!="L"):
                    return False
                if value[0]!="\u0393" and value[0]!="\u03A6" and (value[3]=="\u0393" or value[3]=="\u03A6"):
                    return False
                if key == initial_states[0] and value[0]=="\u0393":
                    left_marker_find = 1
                if new_state in final_states and value[0]=="\u03A6":
                    right_marker_find = 1
    if left_marker_find == 0 or right_marker_find == 0:
        return False

    return True


def check_input_in_LBA(input : str, automata : dict):
    """
        Verifica daca automatul primit ca parametru accepta inputul primit ca parametru si returneaza solutia in caz de acceptare al cuvantului.
        :param input : cuvantul care se doreste a fi verificat in contextul acceptarii de catre automat
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a→A,D',.. ] }, ..}
            }
        :return: (True, [solutie]) in cazul in care automatul este un automat de tipul LBA si accepta cuvantul input, sau (False, []) in caz contrar
    """

    # Se verifica daca automatul primit ca parametru este un automat de tipul LBA valid. Prima etapa de verificare.
    if check_if_LBA(automata) == 0:
        return (False, [])

    # extragerea datelor din automat
    initial_states = automata["initial_states"]
    final_states = automata["final_states"]
    transitions = automata["transitions"]
    solution = []

    # Crearea bandei de lucrul pentru automatul LBA
    tape = []
    tape.append("\u0393")
    for character in input:
        tape.append(character)
    tape.append("\u03A6")

    # Parsarea cuvantului
    list_of_one = []
    all_states_traveled = ""
    temporar_solution = []
    _Private.compute_solutions_for_input_in_LBA(all_states_traveled,0,tape, 0, initial_states[0], final_states, transitions, list_of_one,temporar_solution,solution)
    if 1 in list_of_one:
        return (True,solution)
    else:
        return (False,[])


def check_if_DBA(automata : dict):
    """
        Verifica daca automatul primit ca parametru reprezinta un automat de tipul DBA.
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a',.. ] }, ..}
            }
        :return: True in cazul in care automatul reprezinta un automat DBA, sau False in caz contrar
    """
    # Se verifica daca automatul este de tipul DFA, tipul automatelor DBA este inclus in tipul automatelor DFA
    if check_if_DFA(automata)==0:
        return False

    # extragerea datelor din automat
    final_states = automata["final_states"]
    transitions = automata["transitions"]

    # Se verifica daca automatul este unul de tipul DBA si daca fiecare tranzitie respecta formatul 'a', fara a contine epsilon. A treia etapa de verificare
    if _Private.check_if_infinite(final_states,transitions)==0:
        return False
    else:
        return True


def check_input_in_DBA(input : str, automata : dict):
    """
        Verifica daca automatul primit ca parametru accepta inputul primit ca parametru si returneaza solutia in caz de acceptare al cuvantului.
        :param input : cuvantul care se doreste a fi verificat in contextul acceptarii de catre automat
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a',.. ] }, ..}
            }
        :return: (True, [solutie]) in cazul in care automatul este un automat de tipul DBA si accepta cuvantul input, sau (False, []) in caz contrar
    """
    #aceeasi solutie ca la automatul DFA
    return check_input_in_DFA(input, automata)


def check_if_NBA(automata :dict):
    """
        Verifica daca automatul primit ca parametru reprezinta un automat de tipul NBA.
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a',.. ] }, ..}
            }
        :return: True in cazul in care automatul reprezinta un automat NBA, sau False in caz contrar
    """

    # Se verifica sintaxa automatului. Prima etapa de verificare
    if _Private.check_syntax(automata) == 0:
        return False

    # Se verifica daca automatul reprezinta un graf de tranzitii valid. A doua etapa de verificare
    if _Private.check_structure_of_data(1,automata) == 0:
        return False

    # extragerea datelor din automat
    final_states = automata["final_states"]
    transitions = automata["transitions"]
    # Se verifica daca automatul este unul de tipul NBA si daca fiecare tranzitie respecta formatul 'a'. A treia etapa de verificare
    for key in transitions.keys():
        transition_for_key = transitions[key]
        for list_value in transition_for_key.values():
            for value in list_value:
                if "\u03B5" in list_value or len(value)>1:
                    return False
    if _Private.check_if_infinite(final_states,transitions)==0:
        return False
    else:
        return True


def check_input_in_NBA(input : str, automata : dict):
    """
        Verifica daca automatul primit ca parametru accepta inputul primit ca parametru si returneaza solutia in caz de acceptare al cuvantului.
        :param input : cuvantul care se doreste a fi verificat in contextul acceptarii de catre automat
        :param automata: automatul care trebuie verificat, ce trebuie sa respecte structura :
            {
                "all_states" : [ x, ..]
                "initial_states" : [ x ]
                "final_states" : [ x, ..]
                "transitions" : { state_from : { state_to : [ 'a',.. ] }, ..}
            }
        :return: (True, [solutie]) in cazul in care automatul este un automat de tipul NBA si accepta cuvantul input, sau (False, []) in caz contrar
    """
    # Se verifica daca automatul primit ca parametru este un automat de tipul NBA valid. Prima etapa de verificare.
    if check_if_NBA(automata) == 0:
        return (False, [])


    # extragerea datelor din automat
    initial_states = automata["initial_states"]
    final_states = automata["final_states"]
    transitions = automata["transitions"]
    solution = []
    initial_states_set = set(initial_states)
    final_states_set = set(final_states)

    # Parsarea cuvantului
    if len(input)==0:
        common = initial_states_set & final_states_set
        if common:
            solution.append([common.pop()])
            return (True,solution)
        else:
            return (False,[])
    for init_state in initial_states:
        new_initial_states = []
        new_initial_states.append(init_state)
        temporar_solution = []
        list_of_one = []
        _Private.compute_solutions_for_input_in_NFA(input, 0, new_initial_states[0], final_states, transitions, list_of_one,temporar_solution,solution)
        if 1 in list_of_one:
            return (True,solution)
    return (False,[])





class _Private:
    # Functii private
    def check_syntax(automata : dict):
        # Prima etapa de verificare. Se verifica sintaxa structurii ce se doreste a reprezenta un automat
        if isinstance(automata,dict) and len(automata) == 4 and all(x in automata.keys() for x in ["all_states", "initial_states","final_states","transitions"]) and isinstance(automata["all_states"],list) and isinstance(automata["initial_states"],list) and isinstance(automata["final_states"],list) and isinstance(automata["transitions"],dict):
            for v in automata["all_states"]:
                if not isinstance(v,str):
                    return False
            for v in automata["initial_states"]:
                if not isinstance(v,str):
                    return False
            for v in automata["final_states"]:
                if not isinstance(v,str):
                    return False
            for key,val in automata["transitions"].items():
                if not isinstance(key,str):
                    return False
                else:
                    for subkey,subval in val.items():
                        if not ( isinstance(subkey,str) and isinstance(subval,list)):
                            return False
                        else:
                            for i in subval:
                                if not isinstance(i,str):
                                    return False
            return True
        else:
            return False
        
    def check_structure_of_data(multiple_initial_states: int, automata: dict):
        # A doua etapa de verificare. Se verifica daca automatul reprezinta un graf de tranzitii valid, fara stari izolate, dar cu posibilitatea existemtei a cate un drum de la o stare initiala la toate stari finale
        all_states = automata["all_states"]
        initial_states = automata["initial_states"]
        final_states = automata["final_states"]
        transitions = automata["transitions"]

        checked = dict()
        checked_final = dict()
        for i in all_states:
            checked[i] = 0
        for i in final_states:
            checked_final[i] = 0

        if multiple_initial_states == 0:
            if len(all_states) == 0 or len(initial_states) != 1 or len(final_states) == 0 or len(transitions) == 0:
                return False
        else:
            if len(all_states) == 0 or len(initial_states) < 1 or len(final_states) == 0 or len(transitions) == 0:
                return False

        for init_state in initial_states:
            if init_state not in all_states:
                return False
            if init_state not in transitions.keys() and init_state not in final_states:
                return False
        for key in transitions.keys():
            if key not in all_states:
                return False
            transition_key = transitions[key]
            for transition_state in transition_key.keys():
                if transition_state not in all_states or len(transition_key[transition_state]) != len(
                        set(transition_key[transition_state])):
                    return False
                if transition_state not in final_states and transition_state not in initial_states:
                    if transition_state != key:
                        checked[transition_state] = 1
                        checked[key] = 1
                if transition_state in final_states:
                    if not (transition_state == key and key not in initial_states):
                        checked_final[transition_state] = 1
                        checked[transition_state] = 1
                        checked[key] = 1
                if transition_state in initial_states:
                    if not (transition_state == key and key not in final_states):
                        checked[key] = 1

        for fin_state in final_states:
            if checked_final[fin_state] == 0 and fin_state not in initial_states:
                return False
        for i in checked.keys():
            if checked[i] == 0:
                return False
        return True

    def compute_solutions_for_input_in_NFA(input, current_position, current_state, final_states, transitions,list_of_one, temporar_solution, solution):

        if current_position > len(input):
            return False
        if current_position == len(input) and current_state not in final_states and len(input) != 0:
            return False
        if current_position == len(input) and current_state in final_states:
            list_of_one.append(1)
            pre_temporar_solution = temporar_solution.copy()
            pre_temporar_solution.append(current_state)
            solution.append(pre_temporar_solution)
            return True
        if current_state in transitions.keys():
            transition_state = transitions[current_state]
        else:
            return False
        pre_temporar_solution = temporar_solution.copy()
        pre_temporar_solution.append(current_state)
        found = 0
        for new_state, values in transition_state.items():
            if len(input) != 0 and input[current_position] in values:
                _Private.compute_solutions_for_input_in_NFA(input, current_position + 1, new_state, final_states, transitions,
                                                   list_of_one, pre_temporar_solution, solution)
                found += 1
            if "\u03B5" in values and new_state != current_state:
                _Private.compute_solutions_for_input_in_NFA(input, current_position, new_state, final_states, transitions,
                                                   list_of_one, pre_temporar_solution, solution)
                found += 1
        if found == 0:
            return False

    def compute_solutions_for_input_in_PDA(stack, input, current_position, current_state, first_symbol, final_states,transitions, list_of_one, empty_input, temporar_solution, solution):

        if current_position > len(input):
            return False
        '''if current_position == len(input) and current_state not in final_states:
            return False'''
        if current_position == len(input) and current_state in final_states:
            list_of_one.append(1)
            pre_temporar_solution = temporar_solution.copy()
            pre_temporar_solution.append(current_state)
            solution.append(pre_temporar_solution)
            return True
        '''if current_position == len(input):
            current_position -= 1'''
        if current_state in transitions.keys():
            transition_state = transitions[current_state]
        else:
            return False
        pre_temporar_solution = temporar_solution.copy()
        pre_temporar_solution.append(current_state)
        found = 0
        for new_state, values in transition_state.items():
            for value in values:
                if empty_input != 1 and current_position < len(input) and value[0] == input[current_position] and len(
                        stack) > 0 and value[2] == stack[len(stack) - 1]:
                    new_stack = stack.copy()
                    new_stack.pop()
                    if value[5:] != "\u03B5":
                        for elem in value[:4:-1]:
                            new_stack.append(elem)
                    _Private.compute_solutions_for_input_in_PDA(new_stack, input, current_position + 1, new_state, first_symbol,
                                                       final_states, transitions, list_of_one, empty_input,
                                                       pre_temporar_solution, solution)
                    found += 1
                if empty_input != 1 and current_position < len(input) and value[0] == input[current_position] and value[
                    2] == "\u03B5":
                    new_stack = stack.copy()
                    if value[5:] != "\u03B5":
                        for elem in value[:4:-1]:
                            new_stack.append(elem)
                    _Private.compute_solutions_for_input_in_PDA(new_stack, input, current_position + 1, new_state, first_symbol,
                                                       final_states, transitions, list_of_one, empty_input,
                                                       pre_temporar_solution, solution)
                    found += 1
                if value[0] == "\u03B5" and len(stack) > 0 and value[2] == stack[len(stack) - 1]:
                    new_stack = stack.copy()
                    new_stack.pop()
                    if value[5:] != "\u03B5":
                        for elem in value[:4:-1]:
                            new_stack.append(elem)
                    _Private.compute_solutions_for_input_in_PDA(new_stack, input, current_position, new_state, first_symbol,
                                                       final_states, transitions, list_of_one, empty_input,
                                                       pre_temporar_solution, solution)
                    found += 1
                if value[0] == "\u03B5" and value[2] == "\u03B5":
                    new_stack = stack.copy()
                    if value[5:] != "\u03B5":
                        for elem in value[:4:-1]:
                            new_stack.append(elem)
                    _Private.compute_solutions_for_input_in_PDA(new_stack, input, current_position, new_state, first_symbol,
                                                       final_states, transitions, list_of_one, empty_input,
                                                       pre_temporar_solution, solution)
                    found += 1
        if found == 0:
            return False

    def longest_substring(str):
        # returneaza cel mai lung substring care se repeta dintr-un string
        n = len(str)
        matrix = [[0 for x in range(n + 1)]
                  for y in range(n + 1)]
        res = ""
        res_length = 0
        i = 0
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if str[i - 1] == str[j - 1] and matrix[i - 1][j - 1] < (j - i):
                    matrix[i][j] = matrix[i - 1][j - 1] + 1
                    if matrix[i][j] > res_length:
                        res_length = matrix[i][j]
                        i = max(i, i)
                else:
                    matrix[i][j] = 0
        if res_length > 0:
            for i in range(i - res_length + 1, i + 1):
                res = res + str[i - 1]

        return res

    def compute_solutions_for_input_in_LBA(all_states_traveled, count_when_loop, tape, current_position, current_state,final_states, transitions, list_of_one, temporar_solution, solution):

        new_all_states_traveled = all_states_traveled + current_state
        if count_when_loop % 10 == 0:
            res = _Private.longest_substring(new_all_states_traveled)
            res = res[:5]
            if new_all_states_traveled.count(res) > 50:
                return False
        if current_position < 0 or current_position >= len(tape):
            return False
        if current_state in final_states:
            list_of_one.append(1)
            pre_temporar_solution = temporar_solution.copy()
            pre_temporar_solution.append(current_state)
            solution.append(pre_temporar_solution)
            return True
        if current_state in transitions.keys():
            transition_state = transitions[current_state]
        else:
            return False
        pre_temporar_solution = temporar_solution.copy()
        pre_temporar_solution.append(current_state)
        found = 0
        for new_state, values in transition_state.items():
            for value in values:
                if value[0] == tape[current_position]:
                    new_tape = tape.copy()
                    new_tape[current_position] = value[3]
                    if value[5] == "R":
                        _Private.compute_solutions_for_input_in_LBA(new_all_states_traveled, count_when_loop + 1, new_tape,
                                                           current_position + 1, new_state, final_states, transitions,
                                                           list_of_one, pre_temporar_solution, solution)
                        found += 1
                    if value[5] == "L":
                        _Private.compute_solutions_for_input_in_LBA(new_all_states_traveled, count_when_loop + 1, new_tape,
                                                           current_position - 1, new_state, final_states, transitions,
                                                           list_of_one, pre_temporar_solution, solution)
                        found += 1
                    if value[5] == "S":
                        _Private.compute_solutions_for_input_in_LBA(new_all_states_traveled, count_when_loop + 1, new_tape,
                                                           current_position, new_state, final_states, transitions,
                                                           list_of_one, pre_temporar_solution, solution)
                        found += 1
        if found == 0:
            return False

    def check_if_infinite(final_states, transitions):
        graph = dict()
        for key in transitions.keys():
            list_transition = []
            transition_state = transitions[key]
            for new_state in transition_state.keys():
                list_transition.append(new_state)
            graph[key] = list_transition
        cicluri = [[state] + path for state in graph for path in _Private.dfs(graph, state, state)]

        fin_state_set = set(final_states)
        for cycle in cicluri:
            cycle_set = set(cycle)
            if (fin_state_set & cycle_set):
                return True
        return False

    def dfs(graph, start, end):
        fringe = [(start, [])]
        while fringe:
            state, path = fringe.pop()
            if path and state == end:
                yield path
                continue
            if state not in graph:
                continue
            for next_state in graph[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path + [next_state]))
