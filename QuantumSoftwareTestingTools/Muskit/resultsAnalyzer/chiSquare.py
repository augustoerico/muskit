import math
from datetime import datetime
from scipy.stats import chisquare
import analizerConfig as conf




def validation(observedFile, expectedFile):
    tmp = observedFile.split(chr(47))
    tmp2 = ""
    for x in range(len(tmp)-1):
        tmp2 = tmp2 + tmp[x] + chr(47)
    saveDirectory = tmp2 + "testResults.txt"
    ef = open(expectedFile, "r+")
    of = open(observedFile, "r+")
    g = open((saveDirectory), "w")
    g.write(f'-> {datetime.now().isoformat()}\n')
    num = "0,1,2,3,4,5,6,7,8,9"
    expectedDic = {"": []}
    observedDic = {"": []}
    for x in ef:
        splited = x.split(":")
        tmp = splited[1]
        if tmp[5] in num:
            expectedDic[splited[0]] = float(tmp[1:5])
        else:
           expectedDic[splited[0]] = float(tmp[1:4])

    expectedDic.pop("")

    first = True
    for x in of:
        if ".py" not in x:
            splited = x.split(":")
            tmp = splited[1]

            observedDic[splited[0]] = float(tmp[1:len(tmp)-1])

        else:
            if first == False:
                y = 0
                expectedList = list(expectedDic) # (input, output)
                observedList = list(observedDic) # (input, output)
                while y < 32: # the number of inputs
                    expectedArray = ["", ] # expected probabilities
                    observedArray = ["", ] # observed probabilities
                    n = 0
                    while n <= 2**conf.inputQubits:
                        n = n + 1
                        expectedArray.append("")
                        observedArray.append("")
                    expectedArray2 = [] # expected outputs
                    for z in expectedList:
                        tmp = z.split(", ")
                        num = tmp[1].split(")")
                        input = tmp[0].split("(")
                        if int(input[1]) == y:
                            expectedArray[int(num[0])] = expectedDic[z]
                            expectedArray2.append(num[0])
                    observedArray2 = [] # observed outputs
                    for z in observedList:
                        tmp = z.split(", ")
                        num = tmp[1].split(")")
                        input = tmp[0].split("(")
                        if int(input[1]) == y:
                            observedArray[int(num[0])] = observedDic[z]
                            observedArray2.append(num[0])

                    while "" in expectedArray:
                        expectedArray.remove("")
                    while "" in observedArray:
                        observedArray.remove("")
                    expectedArray2.sort()
                    observedArray2.sort()
                    g.write(f"=== begin: {filename[0]}, input: {y} ===\n")
                    g.write(f"exp_array_2(outputs): {expectedArray2}, obs_array_2(outputs): {observedArray2}\n")
                    if observedArray2 == expectedArray2: # expected output == observed output
                        result = chisquare(expectedArray, observedArray)
                        g.write(f"f_exp: {expectedArray}, f_obs: {observedArray}\n")
                        if result[1] < conf.p_value:
                            g.write("FILE: " + str(filename[0]) + " with input [" + str(y) + "]" + " FAILED WITH P-Value " + str(result[1]))
                            g.write("\n")
                        else:
                            if math.isnan(result[1]):
                                 p_value = 1
                            else:
                                p_value = result[1]
                            g.write("FILE: " + str(filename[0]) + " with input [" + str(y) + "]" + " VALID WITH P-Value " + str(p_value))
                            g.write("\n")
                    else:
                        inside = True
                        for z in observedArray2: # for each observed output
                            if z not in expectedArray2: # if observed output not in expected output
                                inside = False # at least 1 observed output not found in expected outputs => failed without checking p-value
                        if inside == False:
                            g.write("FILE: " + str(filename[0]) + " with input [" + str(y) + "]" + "FAILED DIRECTLY without checking P-Value (WOO)")
                            g.write("\n")
                        else: # all observed outputs are in expected outputs
                            i = 0
                            filedObservedArray = []
                            for z in expectedArray2: # for each expected output
                                if z not in observedArray2: # if expected output not found in observed outputs
                                    filedObservedArray.append(0) # probability = 0
                                else:
                                    filedObservedArray.append(observedArray[i]) # probability = current probability pointed by i
                                    i = i + 1
                            result = chisquare(expectedArray, filedObservedArray)
                            g.write(f"f_exp: {expectedArray}, f_obs_filled: {filedObservedArray}\n")
                            if result[1] < conf.p_value:
                                g.write("FILE: " + str(filename[0]) + " with input [" + str(
                                    y) + "]" + " FAILED WITH P-Value " + str(result[1]))
                                g.write("\n")
                            else:
                                if math.isnan(result[1]): # this shouldn't happen...
                                    p_value = 1
                                else:
                                    p_value = result[1]
                                g.write("FILE: " + str(filename[0]) + " with input [" + str(
                                    y) + "]" + " VALID WITH P-Value " + str(p_value))
                                g.write("\n")
                    y = y + 1
                    g.write("------ end ------\n")
            else:
                first = False
            filename = x.split(".py")
            observedDic.clear()
    g.write(f'<- {datetime.now().isoformat()}\n')
    g.close()
    return

def debug():
    """
    debug `validation` with fixed args
    """
    observed_file = "E:\\2\\muskit\\QuantumSoftwareTestingTools\\Muskit\\ExperimentalData\\QRAM\\cleanResults.txt"
    expected_file = "E:\\2\\muskit\\QuantumSoftwareTestingTools\\Muskit\\ExperimentalData\\QRAM\\QR_test_oracle.txt"
    validation(observed_file, expected_file)

if __name__ == '__main__':
    debug()
