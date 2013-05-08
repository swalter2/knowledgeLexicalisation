"""
Class for parsed sentences in the CONLL format, which makes it easier, to access different coloms of the CONLL format
"""
class ParsedItem():
    pos0 = ""
    pos1 = ""
    pos2 = ""
    pos3 = ""
    pos4 = ""
    pos5 = ""
    pos6 = ""
    pos7 = ""
    pos8 = ""
    pos9 = ""
    
    
    def __init__(self,i0,i1,i2,i3,i4,i5,i6,i7,i8,i9):
        self.pos0 = i0;
        self.pos1 = i1;
        self.pos2 = i2;
        self.pos3 = i3;
        self.pos4 = i4;
        self.pos5 = i5;
        self.pos6 = i6;
        self.pos7 = i7;
        self.pos8 = i8;
        self.pos9 = i9;
        
    def __str__(self):
        value = self.pos0 +" "+self.pos1 +" "+self.pos2+" "+self.pos3+" "+self.pos4+" "+self.pos5+" "+self.pos6+" "+self.pos7+" "+self.pos8+" "+self.pos9

        return "Instance of Parsed_Item class: value = %r" % value
    
    def __setAttribute__(self,name,value):
        if name == "pos0":
            self.pos0 = value
        
        if name == "pos1":
            self.pos1 = value
        
        if name == "pos2":
            self.pos2 = value
        
        if name == "pos3":
            self.pos3 = value
        
        if name == "pos4":
            self.pos4 = value
        
        if name == "pos5":
            self.pos5 = value
        
        if name == "pos6":
            self.pos6 = value
        
        if name == "pos7":
            self.pos7 = value
        
        if name == "pos8":
            self.pos8 = value
        
        if name == "pos9":
            self.pos9 = value
            
        
    def __getattr__(self,name):
        if name == "pos0":
            return self.pos0
        
        if name == "pos1":
            return self.pos1
        
        if name == "pos2":
            return self.pos2
        
        if name == "pos3":
            return self.pos3
        
        if name == "pos4":
            return self.pos4
        
        if name == "pos5":
            return self.pos5
        
        if name == "pos6":
            return self.pos6
        
        if name == "pos7":
            return self.pos7
        
        if name == "pos8":
            return self.pos8
        
        if name == "pos9":
            return self.pos9
    
        
    def __getattrInt__(self,name):
        if name == 0:
            return self.pos0
        
        if name == 1:
            return self.pos1
        
        if name == 2:
            return self.pos2
        
        if name == 3:
            return self.pos3
        
        if name == 4:
            return self.pos4
        
        if name == 5:
            return self.pos5
        
        if name == 6:
            return self.pos6
        
        if name == 7:
            return self.pos7
        
        if name == 8:
            return self.pos8
        
        if name == 9:
            return self.pos9
        

    def getPos0(self):
        return self.pos0
    def pPrint(self):
        return self.pos0 +" "+self.pos1 +" "+self.pos2+" "+self.pos3+" "+self.pos4+" "+self.pos5+" "+self.pos6+" "+self.pos7+" "+self.pos8+" "+self.pos9
    
    def __return_as_string__(self):
        return self.pos0 +" "+self.pos1 +" "+self.pos2+" "+self.pos3+" "+self.pos4+" "+self.pos5+" "+self.pos6+" "+self.pos7+" "+self.pos8+" "+self.pos9
    
    
    