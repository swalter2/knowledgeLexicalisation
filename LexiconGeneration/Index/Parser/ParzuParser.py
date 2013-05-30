import os
from nltk.tokenize import word_tokenize
import treetaggerwrapper


#Maybe have a look at
#https://github.com/clips/pattern
#http://www.clips.ua.ac.be/pages/pattern-de

class Parser():
    path_to_parser = ""
    path_to_tagger = ""
    def __init__(self,path_to_parser, path_to_tagger = None):
        self.path_to_parser = path_to_parser
        self.path_to_tagger = path_to_tagger
        
    #Very ugly, replace with other tagger - dont need it, use Treetager directly from the ParZu  skript
#    def tagg_sentences(self,list_of_sentences):
#        text = ""
#        for x in list_of_sentences:
#            x = x.encode('ascii', 'ignore')
#            tmp = word_tokenize(x)
#            counter = 0
#            for t in tmp:
#                counter += 1
#                text += t +"\n"
#            text += "####\n"
#
#        f_out = open("/tmp/tree_tagger_out","w")
#        f_out.write(text)
#        f_out.close()
#        
#        cmd = self.path_to_tagger+"/cmd/tree-tagger-german /tmp/tree_tagger_out > /tmp/result_tagger"
#        os.system(cmd)
#        
#        f_out = open("/tmp/tree_tagger_out","w")
#        f_out.write(text)
#        f_out.close()
#        string_for_parser = ""
#        f_in = open("/tmp/result_tagger","r")
#        for line in f_in:
#            if "####" in line:
#                string_for_parser += "\n"
#            else:
#                tmp = line.split("\t")
#                string_for_parser += tmp[0]+"\t"+tmp[1]+"\n"
#        f_in.close()
#        
#        f_out = open("/tmp/string_for_parser","w")
#        f_out.write(string_for_parser)
#        f_out.close()
        
    def parse(self,list_of_sentences,path_to_save_output):
#        self.tagg_sentences(list_of_sentences)
        write_string = ""
        for x in list_of_sentences:
            write_string += x +"\n"
        f_out = open("/tmp/parzu_input","w")
        f_out.write(write_string)
        f_out.close()
        cmd = self.path_to_parser+"/parzu -i plain -o conll < /tmp/parzu_input >"+path_to_save_output
        os.system(cmd)
#        ./parzu -i tagged < sample_input
        