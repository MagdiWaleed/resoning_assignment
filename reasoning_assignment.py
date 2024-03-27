import re
import string

def eliminate_imps(str):

    pattern1 = r'([a-zA-Z]\([a-zA-Z]\))\s*(->)'  
    replacement1 = r'~ \1 OR'
    step = re.sub(pattern1, replacement1, str)
 
    pattern2 = r'([a-zA-Z]\([a-zA-Z]\))\s*(<->)\s*([a-zA-Z]\([a-zA-Z]\))'  
    replacement2 = r'~ \1 OR \3 AND \1 OR ~ \3'
    result =re.sub(pattern2, replacement2, step)
    return result





def Demorgan(str):
    #pattern_and = r"~\(([a-zA-Z]\([a-zA-Z]\))\s*AND\s*([a-zA-Z]\([a-zA-Z]\))\)"
    pattern_and = r"~\((.*?)AND(.*?)\)"
    pattern_or = r"~\((.*?)OR(.*?)\)"
    # pattern_or = r"~\(([a-zA-Z]\([a-zA-Z]\))\s*OR\s*([a-zA-Z]\([a-zA-Z]\))\)"
    
    replace_and = r'(~\1 OR ~\2)'
    replace_or = r'(~\1 AND ~\2)'
    
    step = re.sub(pattern_and, replace_and, str)
    result = re.sub(pattern_or, replace_or, step)
    
    return result

def fix_negation(str):
 result = str.replace("~~", "")
 return result



def standardize(str):
 
    scopes = re.split(r'(\W+)', str)
 
    variable_letters = list(string.ascii_lowercase)

    current_variables = {}

    for i in range(len(scopes)):
        scope = scopes[i]

       
        if scope.startswith(('AA', 'EE')):
          
            variable = scope[2]

            
            if variable in current_variables.values():
                for v in variable_letters:
                    if v not in current_variables.values():
                        new_variable = v
                        break

                
                for j in range(i, len(scopes)):
                    scopes[j] = scopes[j].replace(variable, new_variable)

                current_variables[scope[:2]] = new_variable
            else: 
                current_variables[scope[:2]] = variable

    result = ''.join(scopes)

    return result

def prenex(str):
    Adder = ""
    pattern1 = r"AA[a-z]\("
    pattern2 = r"EE[a-z]\("
    univ = re.findall(pattern1,str)
    exist = re.findall(pattern2,str)
    letters = []
    for i in univ:
         letters.append(i[2])
    for i in exist:
         letters.append(i[2])

    matches = re.findall('[AE][AE][a-z]',str)
    step = str.replace(matches[0], "")
    result = step.replace(matches[1], "")
    for i in matches:
        Adder = Adder + i
    result = Adder + result
    return result


def skolem(str):
    pattern = r'EE([a-z])'  
    match = re.search(pattern, str)  


    if match:
        letter = match.group(1)  
        if match.start() == 0:
            
            step = str.replace(letter, 'c') 
            result = step.replace('EE', '') 
            return  result
        else:
            letter_index = match.start()+2
            new = str[:letter_index] + str[letter_index+1:]
            step = new.replace(letter, 'f(x)') 
            result = step.replace('EE', '') 
            return result
    else:
        return str  

def eliminate_universal(str):
    result = str[:2] + str[3:]
    return result.replace("AA","")

print("We will be using the logical expression following logical expression to test the functions: ( AAx (~P(x) -> q(x)) OR EEx ~(s(x) AND m(x)) )")
default = "AAx(~P(x) -> q(x)) OR EEx~(s(x)ANDm(x))"

step1 = eliminate_imps(default)
print("step 1 :" , step1)
step2=Demorgan(step1)
print("step 2: ",step2)
step3=fix_negation(step2)
print("step 3: ",step3)
step4=standardize(step3)
print("step 4: ",step4)
step5 = prenex(step4)
print("step 5: ",step5)
step6 = skolem(step5)
print("step 6: ",step6)
step7 = eliminate_universal(step6)
print("step 7: ",step7)