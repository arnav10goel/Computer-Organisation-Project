import string
from binaryencoding import *
from general_info import *
from registers import *
from instruction_info import *

alphanum = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
alphanum.append('_')
def varValid(list_of_variables_declared, list_of_variables_called):
    for i in range(len(list_of_variables_declared)):
        var = list_of_variables_declared[i]
        for j in var:
            if j not in alphanum:
                return [-1,var]
        try:
            int(var)
            return [-2, var]
        except:
            a = 'hello'
        if var in valid_syntax:
            return [-4, var]
        if (list_of_variables_declared.count(var) != 1):
            return [-5, var]
    
    for i in range(len(list_of_variables_called)):
        if list_of_variables_called[i] not in list_of_variables_declared:
            return [-3, list_of_variables_called[i]]
    
    return [0,0]

def labelValid(list_of_labels_declared, list_of_labels_called):
    for i in range(len(list_of_labels_declared)):
        label = list_of_labels_declared[i]
        for j in label:
            if j not in alphanum:
                return [-1,label]
        try:
            int(label)
            return [-2, label]
        except:
            a = 'hello'
        if label in valid_syntax:
            return [-4, label]
        if (list_of_labels_declared.count(label) != 1):
            return [-5, label]
    
    for i in range(len(list_of_labels_called)):
        if list_of_labels_called[i] not in list_of_labels_declared:
            return [-3, list_of_labels_called[i]]
    return [0,0]

def register_validity(register):
    if register in listofregisters:
        return True
    else:
        return False

def imm_validity(imm):
    if (imm >= 0 and imm <= 255):
        return True
    else:
        return False