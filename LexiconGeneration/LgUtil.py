import LexiconGenerator
import os, sys, ConfigParser
from Index import IndexUtils
from Util import Sparql, WordnetFunctions
from nltk.stem.wordnet import WordNetLemmatizer




def d_print(string, debug):
    if debug == True:
        print(string)
        



def create_html_table(lexico_array,hm_res_sentences,path,name,version):
    hilfsliste = {}
    lexico_array_new = []
    for item in lexico_array:
        name1 = str(item[0].split("\n")[0])
        name1 = name1.replace(" a lemon:LexicalEntry ;","")
        name1 = name1.replace(":","")
        
        if name1 in hilfsliste:
            pass
        else:
            hilfsliste[name1] = ""
            string0 = ""
            string1 = ""
            number = 0
            hilfsarray = []
            for i in lexico_array:
                try:
                    name_t = str(i[0].split("\n")[0])
                    name_t = name_t.replace(" a lemon:LexicalEntry ;","")
                    name_t = name_t.replace(":","")
                    
                    #WARNING: I added here (and above) a string, but why didnt it work without before it?
                    if str(name1) == str(name_t):
                        string0 += i[0]+"\n\n\n\n"
                        string1 += i[1]+"\n"
                        number += int(i[2])
                        hilfsarray.append(i[1])
                except:
                    pass
            tmp_array = []
            tmp_array.append(string0)
            tmp_array.append(string1)
            tmp_array.append(number)
            tmp_array.append(hilfsarray)
            lexico_array_new.append(tmp_array)
            
    web_string = ""
    counter = 0
    lexico_array = sort_array(lexico_array_new)
    web_string += "<TABLE border=\"1\"><TR><TH>#Pattern<TH>Entry"
    for item in lexico_array:
        counter += 1
        if counter < 26:
            f=file(path+"Result/"+str(version)+name+str(counter),"w")
            f.write(item[0])
            f.close()
            
            test = item[0].split("\n")[0]
            test = test.replace("a lemon:LexicalEntry ;","")
            test = test.replace(":","")
            
            f=file(path+"Result/"+str(version)+"P"+name+str(counter),"w")
            write_string = item[1]
            write_string += "\n##########################################################\n\n\n"
            
            for i in item[3]:
                #print i
                
                ##############################################################
                #I changed the pattern with a filter, and if so, the new patterns do not exist in the hm_res_sentences.
                #Therefore use try/catch to overgo the new pattern
                ##############################################################
                try:
                    write_string += hm_res_sentences[i]+"\n\n"
                except:
                    pass
                
            f.write(write_string)
            f.close()
            
            web_string+="<TR><TH><a href=\""+"Result/"+str(version)+"P"+name+str(counter)+"\">"+str(item[2])+"</a><TD><a href=\""+"Result/"+str(version)+name+str(counter)+"\">"+test+"</a>" #"\">Entry"+str(counter)+ 
    
            
    web_string += "</TABLE>"
    return web_string

def create_lexico_array(hm,uri,NumberOfPatterns):
    lmtzr = WordNetLemmatizer()
    #Note: the NumberOfPatterns in the function call is later replaced by a procent value, depending on the number of patterns included into the system
    
    config = ConfigParser.ConfigParser()
    config.read('config.conf')
    procentOfPatterns = config.getfloat("entries", "PatternProcent")
    lexico_array = []
    sparql = Sparql.Connection()
    pattern_once = 0
    
    
    #check here how many hm are given in, and set NumberOfPatterns to at least 0.1% or other value
    NumberOfPatterns = int(len(hm)/100.0*procentOfPatterns)
    
    overall_pattern_numer = 0
    for key, value in hm.iteritems():
        overall_pattern_numer += value
    
    #take max the best ten
    
    best_counter = 0
    #only for test, set very high!
    max_counter = 10000
    #highest value first
    for key, value in sorted(hm.iteritems(), key=lambda x:x[1], reverse = True):
        #only use rules, which occure more than three times
        #if int(hm[key]) >= NumberOfPatterns and int(hm[key])>1:
        best_counter += 1
            
        #only for test:
        # as procent of patterns is in [0,100] but P in[0,1} multilpy P with 100
        #if ((hm[key]/(overall_pattern_numer+0.0))*100) > procentOfPatterns and hm[key]>1:
        #if hm[key] >1:
        if (((value/(overall_pattern_numer+0.0))*100) > procentOfPatterns and best_counter < max_counter+1) or overall_pattern_numer == len(hm):
            try:
                #print "start Lexicon Entry"
                entry_array=LexiconGenerator.createLexiconEntry(key, uri, False)
                for entry in entry_array:
                    tmp_array = []
                    tmp_array.append(entry)
                    tmp_array.append(key)
                    tmp_array.append(value)
                    #print "out of createLexiconEntry: "
                    #raw_input(entry)
                    lexico_array.append(tmp_array)
                if entry == None:
                    print "Entry could not be created for pattern: "+key +"  "+str(value)
            except:
                print "Entry could not be created for pattern: "+key +"  "+str(value)
                #raw_input("wait")
        else:
            pattern_once += 1
   
    label = sparql.getLabel(uri)[0]
    print "label: "+label
    if "(" in label:
        label = label.split("(")[0]
    if label.endswith(" "):
        label = label[:-1]
#    print "len(lexico_array):"+str(len(lexico_array))
    #if len(lexico_array) == 0 or sparql.askForRange(uri) == None:
    entry = LexiconGenerator.NounPPFrame(label, uri, {})
    tmp_array = []
    tmp_array.append(entry)
    tmp_array.append("Noun created by Guessing")
    tmp_array.append(1)
    lexico_array.append(tmp_array)
    
    entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
    tmp_array = []
    tmp_array.append(entry)
    tmp_array.append("Adjective created by Guessing")
    tmp_array.append(1)
    lexico_array.append(tmp_array)
    
    entry = LexiconGenerator.NounPossisiveFrameWithoutMarker(label, uri)
    #print entry
    tmp_array = []
    tmp_array.append(entry)
    tmp_array.append("NounPossisive created by guessing")
    tmp_array.append(1)
    lexico_array.append(tmp_array)
    #print "len lexico array: "+str(len(lexico_array))
    
    #print "added"
    
    lemma = lmtzr.lemmatize(label,"v")

    entry = LexiconGenerator.TransitiveFrame(lemma, uri, {})
    tmp_array = []
    tmp_array.append(entry)
    tmp_array.append("Verb created by Wordnet")
    tmp_array.append(1)
    lexico_array.append(tmp_array)
    
    entry = LexiconGenerator.TransitiveFrame(label, uri, {})
    tmp_array = []
    tmp_array.append(entry)
    tmp_array.append("Verb created by Wordnet")
    tmp_array.append(1)
    lexico_array.append(tmp_array)
    
        
    return lexico_array , pattern_once


    
    
def sort_array(array):
    'sort that the highest number comes first'
    return (sortby(array,2, True))


def sortby(somelist, n, bool):
    nlist = [(x[n], x) for x in somelist]
    nlist.sort(reverse=bool)
    return [val for (key, val) in nlist]




#def dbpedia_filter(hm):
#    
#    #only if Filter activatet, ask via settings.ini
#    test = True
#    if test == False:
#        return hm
#    else:
#        new_hm = {}
#        for key in hm:
#            if key.endswith("  "):
#                key = key[:-2]
#            #print "pattern in Filter : "+key
#            array = key.split("  ")
#            
#            # now start with the filter
#            
#            
#            if len(array)==4:
#                if "NNP" in array[0] and "IN" in array[2] and "NNP" in array[3]:
#                    tmp = array[1]
#                    tmp_array = tmp.split(" ")
#                    tmp = tmp_array[0]+" "+tmp_array[1]+" "+tmp_array[2]+" "+tmp_array[3]+" "+tmp_array[4]+" "+tmp_array[5]+" "+tmp_array[6]+" nn _ _"
#                    new_pattern = array[0]+"  "+tmp+"  "+array[2]+"  "+array[3]
#                    
#                    if new_pattern in new_hm:
#                        value = new_hm[new_pattern]
#                        new_hm[new_pattern] = value + 1
#                    else:
#                        new_hm[new_pattern] = 1
#                        
#                        
#                ################################################
#                #This one might be wrong, see crossing patterns#
#                ################################################
#                #But maybe correct, but check pipeline, if iam loosing some water somewhere.....        
#                #0 x _ NNP NNP _ 1 nsubj _ _  
#                #1 crosses _ VBZ VBZ _ 2 null _ _  
#                #2 the _ DT DT _ 3 det _ _  
#                #3 y _ NNP NNP _ 4 nn _ _
#                #elif "NNP" in array[0] and "VBZ" in array[1] and "DT" in array[2] and "NNP" in array[3]:
#                #    new_pattern = "0 x _ NNP NNP _ 1 nsubj _ _"+"  "+array[1]+"  "+"2 y _ NNP NNP _ 3 nobj _ _"
#                #    if new_pattern in new_hm:
#                #        value = new_hm[new_pattern]
#                #        new_hm[new_pattern] = value + 1
#                #    else:
#                #        new_hm[new_pattern] = 1
#                
#                #0 x _ NNP NNP _ 1 nsubj _ _  
#                #1 and _ CC CC _ 2 cc _ _  
#                #2 his _ PRP$ PRP$ _ 3 poss _ _  
#                #3 y _ NNP NNP _ 4 conj _ _
#
#                elif "NNP" in array[0] and "CC" in array[1] and "PRP" in array[2] and "NNP" in array[3]:
#                    # do nothing
#                    pass
#                
#                #0 x _ NNP NNP _ 1 pobj _ _  
#                #1 of _ IN IN _ 2 prep _ _  
#                #2 the _ DT DT _ 3 det _ _  
#                #3 y _ NNP NNP _ 4 pobj _ _
#                elif "x" in array[0] and "IN" in array[1] and "DT" in array[2] and "y" in array[3]:
#                    # do nothing
#                    pass 
#               
#                #0 x _ NNP NNP _ 1 pobj _ _  
#                #1 and _ CC CC _ 2 cc _ _  
#                #2 the _ DT DT _ 3 det _ _  
#                #3 y _ NNP NNP _ 4 conj _ _
#                elif "x" in array[0] and "CC" in array[1] and "DT" in array[2] and "y" in array[3]:
#                    # do nothing
#                    pass 
#                
#                #0 x _ NNP NNP _ 1 pobj _ _  
#                #1 and _ CC CC _ 2 cc _ _  
#                #2 albert _ VB VB _ 3 conj _ _  
#                #3 y _ NNP NNP _ 4 dobj _ _
#                elif "NNP" in array[0] and "CC" in array[1] and "VB" in array[2] and "NNP" in array[3]:
#                    # do nothing
#                    pass 
#                
#                #0 x _ NNP NNP _ 1 conj _ _  
#                #1 and _ CC CC _ 2 cc _ _  
#                #2 the _ DT DT _ 3 det _ _  
#                #3 y _ NNP NNP _ 4 pobj _ _
#                elif "NNP" in array[0] and "CC" in array[1] and "DT" in array[2] and "NNP" in array[3]:
#                    # do nothing
#                    pass 
#
#                
#               
#                
#                else:
#                    if key in new_hm:
#                        value = new_hm[key]
#                        new_hm[key] = value + 1
#                    else:
#                        new_hm[key] = hm[key]
#                
#            elif len(array) >= 5:
#                
#                
#                if "x" in array[0] and "CC" in array[1] and "PRP$" in array[2] and "NN" in array[3] and "y" in array[4]:
#                    tmp = array[3]
#                    tmp = tmp.replace("4 ","2 ")
#                    tmp = tmp.replace("3 ","1 ")
#                    #1 husband _ NN NN _ 2 pobj _ _
#                    tmp_array = tmp.split(" ")
#                    tmp = tmp_array[0]+" "+tmp_array[1]+" "+tmp_array[2]+" "+tmp_array[3]+" "+tmp_array[4]+" "+tmp_array[5]+" "+tmp_array[6]+" nn _ _"
#                    
#                    new_pattern = "0 x _ NNP NNP _ 1 nn _ _" +"  "+tmp+"  "+"2 of _ IN IN _ 3 prep _ _"+"  "+"3 y _ NNP NNP _ 4 pobj _ _"
#                    
#                    if new_pattern in new_hm:
#                        value = new_hm[new_pattern]
#                        new_hm[new_pattern] = value + 1
#                    else:
#                        new_hm[new_pattern] = 1
#                        
#                #pattern 0 x _ NNP NNP _ 1 pobj _ _  1 the _ DT DT _ 2 det _ _  2 wife _ NN NN _ 3 dep _ _  3 of _ IN IN _ 4 prep _ _  4 y _ NNP NNP _ 5 pobj _ _
#                elif "x" in array[0] and "DT" in array[1] and "NN" in array[2] and "IN" in array[3] and "y" in array[4]:#
#
#                    tmp = array[2]
#                    tmp = tmp.replace("2 ","1 ")
#                    tmp = tmp.replace("3 ","2 ")
#                    tmp_array = tmp.split(" ")
#                    tmp = tmp_array[0]+" "+tmp_array[1]+" "+tmp_array[2]+" "+tmp_array[3]+" "+tmp_array[4]+" "+tmp_array[5]+" "+tmp_array[6]+" nn _ _"
#                    new_pattern = "0 x _ NNP NNP _ 1 nn _ _" +"  "+tmp+"  "+"2 of _ IN IN _ 3 prep _ _"+"  "+"3 y _ NNP NNP _ 4 pobj _ _"
#                    
#                    
#                    if new_pattern in new_hm:
#                        value = new_hm[new_pattern]
#                        new_hm[new_pattern] = value + 1
#                    else:
#                        new_hm[new_pattern] = 1
#                
#                
#                #pattern 0 x _ NNP NNP _ 1 pobj _ _  1 and _ CC CC _ 2 cc _ _  2 first _ JJ JJ _ 3 amod _ _  3 lady _ NN NN _ 4 conj _ _  4 y _ NNP NNP _ 5 dep _ _
#                elif "x" in array[0] and "CC" in array[1] and "JJ" in array[2] and "NN" in array[3] and "y" in array[4]:#
#
#                    tmp = array[3]
#                    tmp = tmp.replace("4 ","2 ")
#                    tmp = tmp.replace("3 ","1 ")
#                    tmp_array = tmp.split(" ")
#                    tmp = tmp_array[0]+" "+tmp_array[1]+" "+tmp_array[2]+" "+tmp_array[3]+" "+tmp_array[4]+" "+tmp_array[5]+" "+tmp_array[6]+" nn _ _"
#                    new_pattern = "0 x _ NNP NNP _ 1 nn _ _" +"  "+tmp+"  "+"2 of _ IN IN _ 3 prep _ _"+"  "+"3 y _ NNP NNP _ 4 pobj _ _"
#                    
#                    if new_pattern in new_hm:
#                        value = new_hm[new_pattern]
#                        new_hm[new_pattern] = value + 1
#                    else:
#                        new_hm[new_pattern] = 1
#                        
#                        
#                elif len(array)>=6:
#                    if "x" in array[0] and "CC" in array[1] and "PRP$" in array[2] and "JJ" in array[3] and "NN" in array[4] and "y" in array[5]:
#                        tmp = array[4]
#                        tmp = tmp.replace("5 ","2 ")
#                        tmp = tmp.replace("4 ","1 ")
#                        tmp_array = tmp.split(" ")
#                        tmp = tmp_array[0]+" "+tmp_array[1]+" "+tmp_array[2]+" "+tmp_array[3]+" "+tmp_array[4]+" "+tmp_array[5]+" "+tmp_array[6]+" nn _ _"
#                    
#                        new_pattern = "0 x _ NNP NNP _ 1 nn _ _" +"  "+tmp+"  "+"2 of _ IN IN _ 3 prep _ _"+"  "+"3 y _ NNP NNP _ 4 pobj _ _"
#                        
#                        
#                        if new_pattern in new_hm:
#                            value = new_hm[new_pattern]
#                            new_hm[new_pattern] = value + 1
#                        else:
#                            new_hm[new_pattern] = 1
#                    else:
#                        if key in new_hm:
#                            value = new_hm[key]
#                            new_hm[key] = value + 1
#                        else:
#                            new_hm[key] = hm[key]
#                        
#                
#                else:
#                    if key in new_hm:
#                        value = new_hm[key]
#                        new_hm[key] = value + 1
#                    else:
#                        new_hm[key] = hm[key]
#                
#            else:
#                if key in new_hm:
#                        value = new_hm[key]
#                        new_hm[key] = value + 1
#                else:
#                    new_hm[key] = hm[key]
#            #
#
#    return new_hm

#def replace_parsedSentence_with_x_y(parsed_sentence,x,y):
#    x_old = x
#    y_old = y
#    x = x.lower()
#    x = x.replace(" ","").capitalize()
#    y = y.lower()
#    y = y.replace(" ","").capitalize()
#    #print "x: "+x
#    #print "y: "+y
#    
##    if " " in x:
##        raw_input(" in x")
##        try:
##            #print parsed_sentence.__str__()
##            parsed_sentence = find_main_node(parsed_sentence,x)
##        except Exception:
##            print "Unexpected error:", sys.exc_info()[0]
##            print "error in replace_parsedSentence_with_x_y - find_main_node x \n\n"
##            #raw_input("wait")
##            return parsed_sentence, False
##            #raw_input("Enter key: ")
#    
##    if " " in y:
##        raw_input(" in y")
##        try:
##            parsed_sentence = find_main_node(parsed_sentence,y)
##        except Exception:
##            print "Unexpected error:", sys.exc_info()[0]
##            print "error in replace_parsedSentence_with_x_y - find_main_node y \n\n"
##            return parsed_sentence, False
##            #raw_input("Enter key: ")
#
#    
#    #d_print("new parsed_sentence created \n\n")
#    #raw_input("direct return")
#    return parsed_sentence, True
#         
        
        
        
#def find_main_node(parsed_sentence,x):
#    x = x.replace(".","")
#    #Achtung: changed in new data format
#    #d_print("In methode find_main_node")
#    if " " in x:
#        #print "print in x"
#        x = x.replace(".","")
#        x_array_tmp=x.split(" ")
#        x_array = x.split(" ")
#        sentence_with_x = []
#        counter = 0
#        for item in parsed_sentence:
#            for tmp_x in x_array:
#                if tmp_x.lower() == str(item.__getattr__("pos1")).lower():
#                    counter+=1
#                    
#                    if counter == 1:
#                        sentence_with_x.append(item)
#
#                    elif counter > 1 and sentence_with_x:
#                        #letzte abfrage, damit sicher ist, damit nicht nur ein item mit einem "  " drin steht....
#                        if len(sentence_with_x)>1:
#                            laenge = len(sentence_with_x)
#                            
#                            if int(sentence_with_x[laenge-1].__getattr__("pos0"))+1 == int(item.__getattr__("pos0")):
#                                sentence_with_x.append(item)
#                                
#                                
#                        else:
#                            if int(sentence_with_x[0].__getattr__("pos0"))+1== int(item.__getattr__("pos0")):
#                                sentence_with_x.append(item)
#                                #print IndexUtils.reverse_sentence_wrapper(sentence_with_x)
#                            else:
#                                counter = 0
#                                sentence_with_x = []
#                                
#
#        # Python array abfrage, wenn array leer sein soll, frag nach if not array und wenn array belegt sein soll, frag nach if array. da wird immer dann der boolean zuueckgegeben, ob etwas elemente enthaelt oder nicht        
#        #ACHTNG: sentence_with_x ist hier string basiert!!!
#        main_item = []
#        if len(sentence_with_x)>1:
#            for i in range(0,len(sentence_with_x)-1):
#                if sentence_with_x[i].__getattr__("pos6") == sentence_with_x[i+1].__getattr__("pos0"):
#                    main_item = sentence_with_x[i+1]
#                if sentence_with_x[i].__getattr__("pos0") == sentence_with_x[i+1].__getattr__("pos6"):
#                    main_item = sentence_with_x[i]
#        else:
#            main_item = sentence_with_x[0]
#            #works til here
#            
#            
#      
#        try:
#            if not main_item:
#                main_item = (sentence_with_x[len(sentence_with_x)-1] if len(sentence_with_x)>1 else sentence_with_x[0])
#                
#                #print "Before"
#                #if len(sentence_with_x)>1:
#                #    main_item = sentence_with_x[len(sentence_with_x)-1]
#                #else:
#                #    main_item = sentence_with_x[0]
#                
#                
#        except:
#            pass
#        
#       
#        if main_item.__str__():
#            
#            replacement = main_item.__return_as_string__()
#            
#            
#            #replacement1 ist dann der begriff aus dem rausgesuchten item
#            replacement1 = replacement.split(" ")[1]
#            
#            #und dieser begriff wird nun mit dem kompletten x ausdruck ersetzt, die dependencys bleiben aber erhalten
#            
#            replacement = replacement.replace(replacement1,x.replace(" ",""))+"  "
#            
#            new_sentence = IndexUtils.reverse_sentence_wrapper(parsed_sentence)
#            
#            new_sentence = new_sentence.replace(IndexUtils.reverse_sentence_wrapper(sentence_with_x),replacement.capitalize())
#            
#            final_sentence = IndexUtils.sentence_wrapper(new_sentence)  
#            
#            
#            
#            return final_sentence
#        else:
#            #print "in else!!!!"
#            return parsed_sentence
#    
#       
#        
#        
#        
#        
#        
#    
#    else:
#        #d_print("Only else part")
#        #d_print("In methode find_main_node - Done \n\n")
#        return parsed_sentence

