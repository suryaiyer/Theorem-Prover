from CNF_converter import parser, evaluate

not_symbols = ['!', 'v', '^', '<=>', '=>', '(', ')']


# Check if KB entails a
def TT_Entails(KB, a):
    symbols = list();
    symbolParser(KB, symbols)
    symbolParser(a, symbols)
    return TT_Check_All(KB, a, symbols, {})


# Recursively check truth table for truth of KB and a
def TT_Check_All(KB, a, symbols, model):
    if len(symbols) == 0:
        if PL_True(KB, model):
            return PL_True(a, model)
        else:
            return True
    else:
        P = symbols[0]
        rest = symbols[1:len(symbols)]
        model[P] = True;
        true_check = TT_Check_All(KB, a, rest, model)
        model[P] = False;
        false_check = TT_Check_All(KB, a, rest, model)
        return true_check and false_check


# Return True if a sentence holds within a model
def PL_True(sentence, model):
    sentenceList = sentence.split(' ')
    root = parser(sentenceList)
    return evaluate(root, model)


# Parse symbols not already in symbol_list from sentence
def symbolParser(sentence, symbolsList):
    sentenceList = sentence.split(' ')
    i = 0
    while i < len(sentenceList):
        if sentenceList[i] not in not_symbols:
            if sentenceList[i][0] == '!':
                if sentenceList[i][1:len(sentenceList[i])] not in symbolsList:
                    symbolsList.append(sentenceList[i][1:len(sentenceList[i])])
            else:
                if sentenceList[i] not in symbolsList:
                    symbolsList.append(sentenceList[i])
        i = i + 1
