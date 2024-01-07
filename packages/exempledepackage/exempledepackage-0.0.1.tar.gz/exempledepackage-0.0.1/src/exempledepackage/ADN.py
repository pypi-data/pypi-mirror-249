def presence_de_A(seq):
    for carc in seq:
        if carc =="A":
            return True
    return False

def postion_AT(seq): # seq = séquence de l'ADN
    i = 1
    if presence_de_A(seq) == True:
        for carac in seq[0: len(seq) -1]:
            if carac == "A":
                if seq[i] == "T":
                    return i - 1
            i = i + 1

def position(code, seq):
    d = ""
    i = 0
    j = 0
    print(seq)
    print(code)
    for carac in seq[0: len(seq)-len(code) + 1]:
        while seq[i] == code[j] and j < len(code):
            d = d + code[j]
            print(d)
            i = i + 1
            j = j + 1
            

        if d == code:
            return i - 1
        d = ""
        i = i + 1
        
    return "rien"


print(position("CCG", "CTCCGTT"))