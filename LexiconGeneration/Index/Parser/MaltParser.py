import nltk
import os.path
import Malt
import sys

class Parser():
    parser = None
    work_dir = None
    
    #Set MALTPARSERHOME in .bachrc or .profile (OpenSuse) and restart Session
    def __init__(self, working_Dir, mco_File, maltparser_Jar,official_Malt_Parser):
        global parser
        global work_dir
        work_dir = working_Dir
        
        # check if /tmp/malt_output.conll exist
        if os.path.exists('/tmp/malt_output.conll'):
            print '/tmp/malt_output.conll was found'
        else:
            #Todo: Do it in a nice way
            f = file('/tmp/malt_output.conll', "w")
            f.write("")
            f.close()
            print '/tmp/malt_output.conll was created'
        
        if official_Malt_Parser==True:
            
            parser = nltk.parse.malt.MaltParser(tagger=Tagger(),working_dir=working_Dir, mco=mco_File)
            
        else:
            parser = Malt.MaltParser(tagger=Tagger(),working_dir=working_Dir, mco=mco_File)
            
            
        parser.config_malt(bin=maltparser_Jar)

    
    def parse_raw_text(self,text):
        'parses a single sentence'
        return parser.raw_parse(text)
    
    def save(self,filename):
        'saves the malt_output.conll under a given name and filepath'
        f=open("/tmp/malt_output.conll","r")
        string=""
        for line in f:
            string+=line;
        f.close()
        f=open(filename,"w")
        f.write(string)
        f.close()
    
    def parse(self,sentence_list):
        'parses a List of not pre-tagged sentences'
        return parser.parse(self.tokenize_many_sentences(sentence_list))
    
    
    
    def tokenize(self,string):
        'tokenizes a sentence and returns token'
        return nltk.word_tokenize(string)
    
    
    
    def tokenize_many_sentences(self,sentence_list):
        'creates of a list of sentences a list of tokens'
        result = []
        #where sentence_list contains a list of sentences
        for item in sentence_list:
            tokenized = self.tokenize(item)
            for token in tokenized:
                result.append(token)
        print 'tokenising in tokenize_many_sentences done'
        return result

    
    def parses_list_of_sentences(self,list_sentences,filepath):
        'expects untagged list of sentences and saves the parsed to the  given filepath'
#         string_list=[]
#         tagger=Tagger()
#         for sentence in list_sentences:
#             #print "sentence: "+sentence
#             sentence = self.clean_sentence(sentence)
#             string_list.append(tagger.tag(self.tokenize(sentence)))
            
#         parser.tagged_parse_many_sentences(string_list)
#         for x in list_sentences:
#             print ("sentence",x)
        try:
            parser.tagged_parse_many_sentences(list_sentences)
            print "parsing done"
            self.save(filepath)
            print "saved sentences"
        except:
            print "Error in parser!!"
            print "Unexpected error:", sys.exc_info()[0]
#             In order to amke sure that no old sentence is used!
            f=open("/tmp/malt_output.conll","w")
            f.write("")
            f.close()
        
    
    
    def clean_sentence(self,sentence):
        
        sentence = sentence.replace(","," ")
        sentence = sentence.replace("."," ")
        sentence = sentence.replace("!"," ")
        sentence = sentence.replace("?"," ")
        sentence = sentence.replace("("," ")
        sentence = sentence.replace(")"," ")
        sentence = sentence.replace("_"," ")
        sentence = sentence.replace("-"," ")
        sentence = sentence.replace(":"," ")
        #sentence = sentence.repalce("\""," ")
        
        while "  " in sentence:
            sentence = sentence.replace("  "," ")
            
        if sentence[len(sentence)-1:]==" ":
            sentence = sentence[:len(sentence)-1]
            
        return sentence
        
    
class Tagger():
    'Pos Tagger'
    def tag(self,token):
        tagged = nltk.pos_tag(token)
        return tagged
