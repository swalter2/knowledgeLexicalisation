import os
from nltk.tokenize import word_tokenize


#Maybe have a look at
#https://github.com/clips/pattern
#http://www.clips.ua.ac.be/pages/pattern-de

class Parser():
    path_to_parser = ""
    path_to_tagger = ""
    def __init__(self,path_to_parser, path_to_tagger = None):
        self.path_to_parser = path_to_parser
        self.path_to_tagger = path_to_tagger

        
    def parse(self,list_of_sentences,path_to_save_output):

        write_string = ""
        ##########################
        ##
        ## To avoid some scripts from the parZuparser running crazy, I only parse a few Sentences at once
        ##
        ##########################
        counter = 0
        parsed_sentences = ""
        for x in list_of_sentences:
#            print ("x",x)
            x = x.encode('ascii', 'ignore')
            counter += 1
            write_string += x +"\n"
            if counter % 500 == 0:
                print "Starting with parsing 500 sentences!"
                f_out = open("/tmp/parzu_input","w")
                f_out.write(write_string)
                f_out.close()
                #cmd = self.path_to_parser+"/parzu -i plain -l -o conll < /tmp/parzu_input >"+path_to_save_output
                cmd = self.path_to_parser+"/parzu -i tagged -l -o conll < /tmp/parzu_input >"+path_to_save_output
                os.system(cmd)
                write_string = ""
                f_in = open(path_to_save_output,"r")
                for line in f_in:
                    parsed_sentences+=line
                f_in.close()
                print str(counter)+"/"+str(len(list_of_sentences))+" done"
        
        print "Starting with parsing of the final sentences!"
        f_out = open("/tmp/parzu_input","w")
        f_out.write(write_string)
        f_out.close()
        #cmd = self.path_to_parser+"/parzu -i plain -l -o conll < /tmp/parzu_input >"+path_to_save_output
        cmd = self.path_to_parser+"/parzu -i tagged -l -o conll < /tmp/parzu_input >"+path_to_save_output
        os.system(cmd)
        f_in = open(path_to_save_output,"r")
        for line in f_in:
            parsed_sentences+=line
        f_in.close()
        f_out = open(path_to_save_output,"w")
        f_out.write(parsed_sentences)
        f_out.close()
                
        print "Parsed all sentences!"

        