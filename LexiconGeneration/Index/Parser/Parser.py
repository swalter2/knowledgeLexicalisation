#in this class, the correct parser, depending on the target language, is chosen/created and a function parse is created, which is always called from the Lookup function
import ConfigParser, MaltParser, ParzuParser, os

class Sentence_Parser():
    language = ""
    malt_parser = None
    parzu_parser = None
    
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('config.conf')
        self.language = config.get('system_language', 'language')
        
        if self.language == "English":
            
            #English Maltparser
            working_Dir = config.get('parser', 'working_Dir')
            #pretrained English model in format mco
            mco_File = config.get('parser', 'mco_file')
            maltparser_Jar = config.get('parser', 'maltparser_Jar')
            #Set true if you want to use the official Version from NLTK or False if you want to use the Malt.py in this Folder
            official_Malt_Parser=config.get('parser', 'official_Malt_Parser');
            os.environ["MALTPARSERHOME"] = config.get('parser', 'parser_dir')
            self.malt_parser = MaltParser.Parser(working_Dir, mco_File, maltparser_Jar,official_Malt_Parser)
            
        if self.language == "German":
            self.parzu_parser = ParzuParser.Parser(config.get('parser', 'parzu'))
            
        if self.language == "Spanish":
            #Spanish Maltparser
            working_Dir = config.get('parser', 'working_Dir')
            #pretrained English model in format mco
            mco_File = config.get('parser', 'spanish_mco_file')
#            mco File from http://www.iula.upf.edu/recurs01_mpars_uk.htm
            maltparser_Jar = config.get('parser', 'maltparser_Jar')
            #Set true if you want to use the official Version from NLTK or False if you want to use the Malt.py in this Folder
            official_Malt_Parser=config.get('parser', 'official_Malt_Parser');
            os.environ["MALTPARSERHOME"] = config.get('parser', 'parser_dir')
            self.malt_parser = MaltParser.Parser(working_Dir, mco_File, maltparser_Jar,official_Malt_Parser)
    
    
    def parse(self,sentence_list,path_to_save):
        if self.language == "English":
            self.malt_parser.parses_list_of_sentences(sentence_list, path_to_save)
        if self.language == "German":
            self.parzu_parser.parse(sentence_list, path_to_save)
        if self.language == "Spanish":
            self.malt_parser.parses_list_of_sentences(sentence_list, path_to_save)    
        
    
    