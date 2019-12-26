# ------------------------------------------
# Variables
FONT_SIZE = -16
PAGE_ID = 1
NODES = []

class Color:
    BLACK = 16777215
    WHITE = 0

# ------------------------------------------
# Nodes

class Node:
    coords = []
    def __init__(self, a_coords):
        self.coords = a_coords

class Node_AND(Node):
    def __init__(self, a_coords, a_type, a_isNAND):
        super().__init__(a_coords)
        self.isNAND = a_isNAND
        self.outpute = [a_coords[0]+46, a_coords[1]-25]
        self.inpute = []
        self.inpute.append([a_coords[0]+1, a_coords[1]-39])
        if(a_type == 1):
            self.inpute.append([a_coords[0]+1, a_coords[1]-25])
        if(a_type == 2):
            self.inpute.append([a_coords[0]+1, a_coords[1]-30])
            self.inpute.append([a_coords[0]+1, a_coords[1]-20])
        self.inpute.append([a_coords[0]+1, a_coords[1]-11])
            
class Node_OR(Node):
    def __init__(self, a_coords, a_type, a_isNOR):
        super().__init__(a_coords)
        self.isNOR = a_isNOR
        self.outpute = [a_coords[0]+46, a_coords[1]-25]
        self.inpute = []
        self.inpute.append([a_coords[0]+1, a_coords[1]-39])
        if(a_type == 1):
            self.inpute.append([a_coords[0]+1, a_coords[1]-25])
        if(a_type == 2):
            self.inpute.append([a_coords[0]+1, a_coords[1]-30])
            self.inpute.append([a_coords[0]+1, a_coords[1]-20])
        self.inpute.append([a_coords[0]+1, a_coords[1]-11])
        
class Node_XOR(Node):
    def __init__(self, a_coords, a_type, a_isNXOR):
        super().__init__(a_coords)
        self.isNXOR = a_isNXOR
        self.outpute = [a_coords[0]+46, a_coords[1]-25]
        self.inpute = []
        self.inpute.append([a_coords[0]+1, a_coords[1]-39])
        if(a_type == 1):
            self.inpute.append([a_coords[0]+1, a_coords[1]-25])
        if(a_type == 2):
            self.inpute.append([a_coords[0]+1, a_coords[1]-30])
            self.inpute.append([a_coords[0]+1, a_coords[1]-20])
        self.inpute.append([a_coords[0]+1, a_coords[1]-11])
        
class Node_NOT(Node):
    def __init__(self, a_coords, a_invert):
        super().__init__(a_coords)
        self.invert = a_invert
        self.outpute = [a_coords[0]+46, a_coords[1]-25]
        self.inpute = [a_coords[0]+1, a_coords[1]-25]
        
class Node_Dot(Node):
    def __init__(self, a_coords):
        super().__init__(a_coords)
        self.outpute = [a_coords[0]+9, a_coords[1]-9]
        self.inpute = [a_coords[0]+9, a_coords[1]-9]
        
class Node_Switch(Node):
    def __init__(self, a_coords, a_state, a_type):
        super().__init__(a_coords)
        self.state = a_state
        self.type = a_type
        self.outpute = [a_coords[0]+46, a_coords[1]-25]

class Node_Lamp(Node):
    def __init__(self, a_coords, a_color):
        super().__init__(a_coords)
        self.color = a_color
        self.inpute = [a_coords[0]+1, a_coords[1]-25]

# ------------------------------------------
# Karnaugh Table

class Node_KarnaughTable():
    stringo = ""
    def printIt(self):
        return self.stringo[:-1]
    
    def __init__(self, a_coords, a_vars):
        # ---------------------------
        # Fill and swap elements in table
        typ = 0
        if(len(a_vars) <= 4):
            typ = 0
            while(len(a_vars) < 4):
                a_vars.append("X")
        elif(len(a_vars) <= 8):
            typ = 1
            while(len(a_vars) < 8):
                a_vars.append("X")
            a_vars[2], a_vars[3] = a_vars[3], a_vars[2]
            a_vars[6], a_vars[7] = a_vars[7], a_vars[6]
        elif(len(a_vars) <= 16):
            typ = 2
            while(len(a_vars) < 16):
                a_vars.append("X")
            a_vars[2], a_vars[3] = a_vars[3], a_vars[2]
            a_vars[6], a_vars[7] = a_vars[7], a_vars[6]
            a_vars[8], a_vars[12] = a_vars[12], a_vars[8]
            a_vars[9], a_vars[13] = a_vars[13], a_vars[9]
            a_vars[10], a_vars[15] = a_vars[15], a_vars[10]
            a_vars[11], a_vars[14] = a_vars[14], a_vars[11]
        # ---------------------------
        # Set input/output gateways
        self.inpute = []
        for i in range(typ+2):
            self.stringo += newDot([a_coords[0], a_coords[1]+i*10]) + "\n"
            self.inpute.append(NODES[-1].inpute)
        self.stringo += newDot([a_coords[0]+80, a_coords[1]]) + "\n"
        self.outpute = NODES[-1].outpute
        # ---------------------------
        # Set up NOT gates
        self.Ninpute = []
        for i in range(typ+2):
            self.stringo += newNOT([a_coords[0]+5+5*i, a_coords[1]+50]) + "\n"
            self.stringo += newDot([a_coords[0]+5+10*i, a_coords[1]+55]) + "\n"
            self.stringo += newWire(NODES[-2].outpute, NODES[-1].inpute) + "\n"
            self.stringo += newWire(self.inpute[i], NODES[-2].inpute) + "\n"
            self.Ninpute.append(NODES[-1].inpute)
        # ---------------------------
        # Fill up bool table
        boolTable = [0 for i in range(len(a_vars))]
        howMuch = 0
        for ind, i in enumerate(a_vars):
            if(i == 0 or i == "X"):
                boolTable[ind] = 1
                howMuch += 1
            elif(i == 1):
                boolTable[ind] = 0
        # ---------------------------
        # Consider 4x2/2x4 blocks
        isDone = (howMuch == 16)
        whatToConnect = []
        if(typ == 2 and not isDone):
            for i in range(4):
                if(a_vars[i-4] == 1 and a_vars[i-3] == 1 and a_vars[i-2] == 1 and a_vars[i-1] == 1 and a_vars[i] == 1 and a_vars[i+1] == 1 and a_vars[i+2] == 1 and a_vars[i+3] == 1):
                    for j in range(8): 
                        if(boolTable[i-4+j] == 0):
                            boolTable[i-4+j] = 1
                            howMuch += 1
                    if(i == 0):
                        whatToConnect.append(self.Ninpute[1])
                    elif(i == 1):
                        whatToConnect.append(self.Ninpute[0])
                    elif(i == 2):
                        whatToConnect.append(self.inpute[1])
                    elif(i == 3):
                        whatToConnect.append(self.inpute[0])
                    if(howMuch == 16):
                        isDone = True
                        break
                if(a_vars[i-1] == 1 and a_vars[i] == 1 and a_vars[i+3] == 1 and a_vars[i+4] == 1 and a_vars[i+7] == 1 and a_vars[i+8] == 1 and a_vars[i+11] == 1 and a_vars[i+12] == 1): 
                    toCheck = [i-1, i, i+3, i+4, i+7, i+8, i+11, i+12]
                    for j in toCheck:
                        if(boolTable[j] == 0):
                            boolTable[j] = 1
                            howMuch += 1
                    if(i == 0):
                        whatToConnect.append(self.Ninpute[3])
                    elif(i == 1):
                        whatToConnect.append(self.Ninpute[2])
                    elif(i == 2):
                        whatToConnect.append(self.inpute[3])
                    elif(i == 3):
                        whatToConnect.append(self.inpute[2])
                    if(howMuch == 16):
                        isDone = True
                        break
        if(len(whatToConnect) == 1):
            self.stringo += newWire(whatToConnect[0], self.outpute) + "\n"
            
# ------------------------------------------
# Settings

def canvasColor(a_color = Color.BLACK):
    if(a_color == Color.BLACK):
        return "39 16777215"

def inputUnconnected(a_type = 0):
    return "47 %s" % a_type

def gridSpacing(a_viewGrid = 1, a_wid = 6, a_hei = 6):
    return "40 %s %s %s" % (a_viewGrid, a_wid, a_hei)

def gridSize(a_wid = 800, a_hei = 600):
    return "50 %s %s" % (a_wid, a_hei)

def simulationRate(a_type = 0, a_hz = 100):
    return "51 %s %s" % (a_type, a_hz)

def fontType(a_name = "Terminal", a_size = FONT_SIZE, a_weight = 700, a_italic = 0):
    return "30\n%s\n%s\n%s\n%s\n%s" % (a_name, a_size, a_weight, a_italic, 255)

# ------------------------------------------
# Node creation

def newPage():
    global PAGE_ID
    PAGE_ID += 1
    return "38 %s" % (PAGE_ID-1)

def newText(a_text, a_cords, a_type=0, a_filename="\\NUL"):
    return "22 %s %s %s %s %s %s\n%s" % (a_cords[0], a_cords[1], a_cords[0]+6*len(a_text), a_cords[1]+FONT_SIZE, a_type, a_filename, a_text)

def newAND(a_cords, a_type=0, a_isNAND=0):
    NODES.append(Node_AND(a_cords, a_type, a_isNAND))
    return "3 %s %s %s %s %s %s" % (a_cords[0], a_cords[1], a_cords[0]+49, a_cords[1]-49, a_type, a_isNAND)
    
def newOR(a_cords, a_type=0, a_isNOR=0):
    NODES.append(Node_OR(a_cords, a_type, a_isNOR))
    return "4 %s %s %s %s %s %s" % (a_cords[0], a_cords[1], a_cords[0]+49, a_cords[1]-49, a_type, a_isNOR)
    
def newXOR(a_cords, a_type=0, a_isNXOR=0):
    NODES.append(Node_XOR(a_cords, a_type, a_isNXOR))
    return "35 %s %s %s %s %s %s" % (a_cords[0], a_cords[1], a_cords[0]+49, a_cords[1]-49, a_type, a_isNXOR)

def newNOT(a_cords, a_invert=0):
    NODES.append(Node_NOT(a_cords, a_invert))
    return "5 %s %s %s %s %s" % (a_cords[0], a_cords[1], a_cords[0]+49, a_cords[1]-49, a_invert)
    
def newSwitch(a_cords, a_state=1, a_type=0):
    NODES.append(Node_Switch(a_cords, a_state, a_type))
    return "8 %s %s %s %s %s %s" % (a_cords[0], a_cords[1], a_cords[0]+49, a_cords[1]-49, a_state, a_type)
    
def newLamp(a_cords, a_color=0):
    NODES.append(Node_Lamp(a_cords, a_color))
    return "7 %s %s %s %s %s %s" % (a_cords[0], a_cords[1], a_cords[0]+49, a_cords[1]-49, a_color, 1)
    
def newDot(a_cords):
    NODES.append(Node_Dot(a_cords))
    return "10 %s %s %s %s %s %s" % (a_cords[0], a_cords[1], a_cords[0]+17, a_cords[1]-17, 0, 0)
    
def newKarnaughTable(a_cords, a_vars):
    NODES.append(Node_KarnaughTable(a_cords, a_vars))
    return NODES[-1].printIt()

def newWire(a_cords1, a_cords2):
    return "1 %s %s %s %s" % (a_cords1[0], a_cords1[1], a_cords2[0], a_cords2[1])

# ------------------------------------------
# Functions

def defaultSettings(a_file):
    prepare = [
        canvasColor(),
        inputUnconnected(),
        gridSpacing(),
        gridSize(),
        simulationRate(),
        fontType(),
        "1\n2\n1"
    ]
    a_file.write("\n".join(prepare)+"\n")

def createFile(a_name):
    file = open(a_name + ".lgi", "w")
    file.write("41 2 0\n")
    whatToDo = [
        newPage(),
        newText("Zobaczymy czy knorr dziala XD", [100, 100]),
        newSwitch([150, 150]),
        newSwitch([150, 200]),
        newSwitch([150, 250]),
        newSwitch([150, 300]),
        newKarnaughTable([250, 250],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]),
        newWire(NODES[0].outpute, NODES[-1].inpute[0]),
        newWire(NODES[1].outpute, NODES[-1].inpute[1]),
        newWire(NODES[2].outpute, NODES[-1].inpute[2]),
        newWire(NODES[3].outpute, NODES[-1].inpute[3]),
        newLamp([350, 250]),
        newWire(NODES[-2].outpute, NODES[-1].inpute),
    ]
    file.write("\n".join(whatToDo)+'\n')
    defaultSettings(file)
    file.write("49\n")
    file.close()
createFile("test")
