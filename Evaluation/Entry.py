class Entry():
    entryTerm = None
    canonicalForm = None
    #old version
#    sense = []
    sense = None
    synBehaviorFrame = None
    marker = None
    original = None
    partOfSpeech = None
    sense_arguments = []
    synBehavior_arguments = []
    def __init__(self, entryTerm = None, canonicalForm = None, reference = None, synBehaviorFrame = None, marker = None, partOfSpeech = None, sense_arguments = None, synBehavior_arguments = None):
        self.entryTerm = entryTerm
        self.canonicalForm = canonicalForm
        self.sense = reference
        self.synBehaviorFrame = synBehaviorFrame
        self.marker = marker
        self.partOfSpeech = partOfSpeech
        self.sense_arguments = sense_arguments
        self.synBehavior_arguments = synBehavior_arguments
    
    def setOriginalEntry(self,entry):
        self.original = entry
        
    def getOriginalEntry(self):
        return self.original
    
    def getEntryTerm(self):
        return self.entryTerm
        
    def getCanonicalForm(self):
        return self.canonicalForm
    
    def getSense(self):
        return self.sense
    
    def getFrame(self):
        return self.synBehaviorFrame
    
    def getPartOfSpeech(self):
        return self.partOfSpeech
    
    def getSense_arguments(self):
        return self.sense_arguments
    
    def getSynBehavior_arguments(self):
        return self.synBehavior_arguments
    
    def e_print(self):
        print str(self.canonicalForm) +"  "+ str(self.sense) +"  "+ str(self.getPartOfSpeech())