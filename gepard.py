import os
import sys

version = "indev4"
try:
    filePath = r""+str(sys.argv[1])+""
    mode = 0
except:
    mode = 1
code = []
codeLines = []
# function for getting file type

def getFileType(path):
    par = path[::-1]
    output = ""
    for x in par:
        if x != ".":
            output += x
        else:
            output += x
            break
    return output[::-1]

# messaging functions

def error(line, msg, file):
    print("error in line: " + str(codeLines[line - 1] + 1) + " (" + msg + ")")
def warning(msg, line = 0,):
    if line == 0:
        print("warning " + "(" + msg + ")")
    else:
        print("warning in line: " + str(line + 1) + " (" + msg + ")")
def info(msg, line = 0,):
    if line == 0:
        print("information " + "(" + msg + ")")
    else:
        print("information in line: " + str(line + 1) + " (" + msg + ")")
# optimizing the code that my code can understand it better

def optimizeCodeForRun(codeToOptimize):
    optimizedCode = []
    stri = ""
    for z,x in enumerate(codeToOptimize):
        if x[0:2] == "//":
            continue
        optimizedCode.append(stri)
        codeLines.append(z)
        stri = ""
        inString = False
        inBrackets = 0
        for y in x:
            if y == '"':
                if not inString:
                    inString = True
                    stri += y
                else:
                    inString = False
                    stri += y
            elif y == "(":
                if not inString:
                    inBrackets += 1
                stri += y
            elif y == ")":
                if not inString:
                    inBrackets -= 1
                stri += y
            elif y == ",":
                if not inString and inBrackets == 0:
                    optimizedCode.append(stri)
                    codeLines.append(z)
                    stri = ""
                else:
                    stri += y
            elif y == " " or y == "	":
                if not inString and inBrackets == 0:
                    optimizedCode.append(stri)
                    codeLines.append(z)
                    stri = ""
                else:
                    stri += y
            else:
                stri += y
    optimizedCode.append(stri)
    for z,x in enumerate(optimizedCode):
        if optimizedCode[z][0:1] == '"' and optimizedCode[z][len(optimizedCode[z]) - 1:len(optimizedCode[z])] == '"':
            continue
        elif optimizedCode[z][0:1] == '(' and optimizedCode[z][len(optimizedCode[z]) - 1:len(optimizedCode[z])] == ')':
            continue
        else:
            optimizedCode[z] = x.replace(" ", "")
    return optimizedCode

# function for executing the code

def runCode(file):
    file.append("")
    file.append("")
    file.append("")
    if mode == 0:
        if getFileType(filePath) != ".gprd":
            print("error while trying to read file(cannot execute " + getFileType(filePath) + " file)")
            return 6
    varNames = []
    varVals = []
    print("your code is now running, gepard version: " + version)
    print()
    counter = 0

    def createVar(variable, value = None):
        varNames.append(variable)
        varVals.append(value)

    def setVar(variable, value):
        varVals[varNames.index(variable)] = value

    def getVarValue(variable):
        return varVals[varNames.index(variable)]

    def calculate(calculation):
        inString = False
        calculation = calculation[1:(len(calculation) - 1)]
        splitted_calculation = []
        arithmeticsigns = ["+","-","*","/"]
        stri = ""
        for x in calculation:
            if x in arithmeticsigns or x == " ":
                if not inString:
                    splitted_calculation.append(stri)
                    splitted_calculation.append(x)
                    stri = ""
                else:
                    stri += x
            elif x == '"':
                stri += x
                if inString:
                    inString = False
                else:
                    inString = True
            else:
                stri += x
        splitted_calculation.append(stri)
        for z,x in enumerate(splitted_calculation):
            if x == "" or x == " ":
                del splitted_calculation[z]
        for z,x in enumerate(splitted_calculation):
            number = False
            try:
                number = int(x)
            except:
                pass
            try:
                number = float(x)
            except:
                pass
            if x in arithmeticsigns:
                continue
            elif number != False:
                continue
            elif len(x) > 0:
                if x[0] == '"' and x[-1] == '"':
                    continue
                else:
                    if not x == " ":
                        if type(varVals[varNames.index(x)].replace(" ","")) == int:
                            splitted_calculation[z] = varVals[varNames.index(x)]
                        else:
                            splitted_calculation[z] = '"' + varVals[varNames.index(x)] + '"'
        calculation = ""
        for x in splitted_calculation:
            variabletofixstrerror = x
            calculation += str(variabletofixstrerror)
        return(eval(calculation))

    createVar("true", True)
    createVar("false", False)
    createVar ("input_value")

    while counter < len(file):
        if file[counter] == "log":
            printVal = file[counter + 1]
            if printVal[0] == '"' and printVal[len(printVal) - 1] == '"':
                print(printVal[1:(len(printVal) - 1)])
            elif printVal[0] == '(' and printVal[-1] == ')':
                try:
                    print(calculate(printVal))
                except:
                    error(counter + 1, "cannot calculate " + printVal, file)
            else:
                if printVal in varNames:
                    print(getVarValue(printVal))
                else:
                    if not printVal == "NaN":
                        try:
                            print(int(file[counter + 1]))
                        except:
                            error(counter + 1, file[counter + 1] + " is not defined", file)
                    else:
                        print()
            counter += 1
        elif file[counter] == "var":
            if file[counter + 2] == "=":
                if not file[counter + 1] in varNames:
                    varVal = file[counter + 3]
                    if varVal[0] == '"' and varVal[len(varVal) - 1] == '"':
                        createVar(file[counter + 1], varVal[1:(len(varVal) - 1)])
                    elif varVal[0] == '(' and varVal[len(varVal) - 1] == ')':
                        try:
                            createVar(file[counter + 1], calculate(varVal))
                        except:
                            error(counter + 1, "cannot calculate " + file[counter + 3], file)
                    else:
                        if varVal in varNames:
                            createVar(file[counter + 1], getVarValue(varVal))
                        else:
                            try:
                                createVar(file[counter + 1], int(varVal))
                            except:
                                error(counter + 1, varVal + " is not defined", file)
                else:
                    error(counter + 1, file[counter + 1] + " does already exist", file)
                counter += 3
            else:
                if not file[counter + 1] in varNames:
                    createVar(file[counter + 1])
                else:
                    error(counter + 1, file[counter + 1] + " does already exist", file)
                counter += 1
        elif file[counter][0:2] == "//":
            pass
        elif file[counter][0:2] == "--":
            command = file[counter][2:len(file[counter])]
            if command == "run":
                info("the code is already running", counter)
            elif command == "exit":
                return 1
            elif command == "version":
                print(version)
            else:
                error(counter, "the command " + command + " does not exist", file)
        elif file[counter] == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
        elif file[counter] == "input":
            if file[counter + 1][0] == '"' and file[counter + 1][-1] == '"':
                setVar("input_value" , input(file[counter + 1][1:-1]))
            elif file[counter + 1][0] == '(' and file[counter + 1][-1] == ')':
                try:
                    setVar("input_value" , input(calculate(file[counter + 1])))
                except:
                    error(counter, "cannot calculate " + file[counter + 1], file)
            else:
                if file[counter + 1] in varNames:
                    setVar("input_value", input(getVarValue(file[counter + 1])))
                else:
                    try:
                        setVar("input_value", input(int(file[counter + 1])))
                    except:
                        error(counter, file[counter + 1] + " is not defined", file)
            counter += 1
        else:
            if file[counter] != "":
                if file[counter + 1] == "=":
                    if file[counter] in varNames:
                        varVal = file[counter + 2]
                        if varVal[0] == '"' and varVal[len(varVal) - 1] == '"':
                            setVar(file[counter], varVal[1:(len(varVal) - 1)])
                        elif varVal[0] == '(' and varVal[len(varVal) - 1] == ')':
                            try:
                                setVar(file[counter], calculate(varVal))
                            except Exeption as e:
                                error(counter + 1, "cannot calculate " + file[counter + 2], file)
                        else:
                            if varVal in varNames:
                                setVar(file[counter], getVarValue(varVal))
                            else:
                                try:
                                    setVar(file[counter], int(varVal))
                                except:
                                    error(counter + 1, file[counter + 1] + " is not defined", file)
                    else:
                        error(counter + 1, file[counter] + " is not defined", file)
                    counter += 2
                else:
                    error(counter, file[counter] + " is an unknown syntax", file)
        counter += 1
    return 0
if mode == 0:
    # open the filepath for the code file
    try:
        with open(filePath) as codeFile:
            for line in codeFile:
                code.append(line.rstrip())
    except:
        print("error while trying to read file (invalid filepath)")
        exit()
elif mode == 1:
    # in mode 1 you have to write code by yourself in the terminal instead of reading it out from a filepath
    x = None
    while x != "--run":
        x = input("> ")
        if x != "--run":
            code.append(x)
# optimizing the code that my script can execute it
code = optimizeCodeForRun(code)
# executeing the code
x = runCode(code)
print()
print("your code finished with exit code: " + str(x))
