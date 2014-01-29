#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


from aux.rdfEngine import *
import rdflib
import glob
from SPARQLWrapper import SPARQLWrapper, JSON
import datetime
import Entry

endpoint = "http://vtentacle.techfak.uni-bielefeld.de:443/sparql/"
path_goldstandard_train = ""
path_goldstandard_test  = ""
Laenge_Goldstandard = 0

            

def createArrayEntries(path):
#    print"Load Path: "+str(path)
    entry_hm = {}
    number_of_entries = 0
    graph = loadGraph(path)
    lemon = Namespace("http://www.monnet-project.eu/lemon#")
    lexinfo = Namespace("http://www.lexinfo.net/ontology/2.0/lexinfo#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    isocat = Namespace("http://www.isocat.org/datcat/")


    result_array = []
        
    for _,_,o in graph.triples((None,lemon.entry ,None)):
            canonicalForm = None
            reference = []
            sense_arguments = []
            synBehavior_arguments = []
            frame = []
            partOfSpeech = None
            for _,_,o1 in graph.triples((o,lemon.sense ,None)):
                for _,_,o2 in graph.triples((o1,lemon.reference ,None)):
                    if o2 != None and "http://dbpedia.org" in o2:
                        reference.append(str(o2))
                    
#                #ignore subsenses for now!!!
#                for _,_,o2 in graph.triples((o1,lemon.subsense ,None)):
#                    for _,_,o3 in graph.triples((o2,lemon.reference ,None)):
#                        if str(o3) not in reference:
#                            reference.append(str(o3))
#                for _,B,o2 in graph.triples((o1,None ,None)):
#                    if "reference" not in B:
#                        
#                        if "subj" in B:
#                            sense_arguments.append(["subject",str(o2)])
#                        else:
#                            sense_arguments.append(["object",str(o2)])
            
            for _,_,o1 in graph.triples((o,lemon.synBehavior,None)):
                for _,B,o2 in graph.triples((o1,rdf.type , None)):
                    if "lemon#Frame" not in o2:
                        frame.append(o2)
                        
                for _,B,o2 in graph.triples((o1,None , None)):
                    if "#type" not in B:
                        if lexinfo in B:
                            synBehavior_arguments.append([str(B.replace(lexinfo,"")),str(o2)])
                        if isocat in B:
                            synBehavior_arguments.append([str(B.replace(isocat,"")),str(o2)])
            
            for _,_,o1 in graph.triples((o,lemon.canonicalForm ,None)):
                for _,_,o2 in graph.triples((o1,lemon.writtenRep ,None)):
                    canonicalForm = o2
                    #do not use for german!!
#                    canonicalForm = canonicalForm.encode("ascii","ignore")
#                    canonicalForm = canonicalForm.replace("\xf3","o")
#
#                    
#                    canonicalForm = canonicalForm.replace("\xc3\xbc","ue")
#                    canonicalForm = canonicalForm.replace("\xc3\xa4","ae")
#                    canonicalForm = canonicalForm.replace("\xc3\x9f","ss")
#                    canonicalForm = canonicalForm.replace("\xc3\xb6","oe")
                    
                    
            for _,_,o1 in graph.triples((o,lexinfo.partOfSpeech ,None)):
                tmp = str(o1)
                tmp = tmp.replace("http://www.lexinfo.net/ontology/2.0/lexinfo#","")
                #############
                ##
                ## To keep evaluation simple, use only noun.
                ## Same problem maybe occur with properNoun 
                ##
                #############
#                print("tmp0",tmp)
                if tmp.lower() == "commonnoun":
                    tmp = "noun"
#                print("tmp",tmp)
                partOfSpeech = tmp.lower()
                

                    
            if len(reference) != 0 and canonicalForm != None:
#                print "reference: "+str(reference)
                for ref in reference:
#                    print "ref: "+ref
                    if str(partOfSpeech) == "None":
                        partOfSpeech = "noun"
                    entry = Entry.Entry(canonicalForm.replace(" ","").lower(), str(canonicalForm), ref, frame, None, str(partOfSpeech),sense_arguments, synBehavior_arguments)
                    number_of_entries += 1
                    if entry_hm.has_key(ref):
                        tmp = entry_hm[ref]
                        if tmp != None:
                            tmp.append(entry)
                            entry_hm[ref] = tmp
                    else:
                        entry_hm[ref] = [entry]
            
    return entry_hm, number_of_entries




def calculateOverallAccuracy(key,user_lex,signature_ml, hm_ML, subject_map, object_map):
    counter = 0
    overall_value = 0
    for gold in hm_ML[key]:
        signature_tmp = str(gold.getPartOfSpeech())+" "+gold.getCanonicalForm().lower()+" "+str(gold.getSense())
        if signature_ml == signature_tmp:
            value = 0
            try:
                value = calculateAccuracy(key,user_lex, gold, subject_map, object_map)
                counter += 1
                if value > overall_value:
                    overall_value = value
            except:
                print "Error in Accuracy"
                print "Unexpected error:", sys.exc_info()[0]
                print

    return  overall_value






#####################################MAIN#########################################    
##################################################################################  
################################################################################## 
##################################################################################  


def calculateAccuracy(key,user_lex, gold, subject_map, object_map):
    points = 0
    local_points = 0
    #einen Punkt fuers korrekte Frame
    if len(gold.getFrame()) == 0:
        local_points += 1
    else:
        found_frames = 0
        for user_frame in user_lex.getFrame():
            for gold_frame in gold.getFrame():
                if user_frame == gold_frame:
                    found_frames += 1
        if found_frames >= len(gold.getFrame()):
            local_points += 1
        else:
            #also give part frames, if for example the user has one frame correct, but the second wrong
            local_points += (float(found_frames)/len(gold.getFrame()))
        
        
    #einen Punkt fuer korrekten eigenen Eintrag, d.h. ist das Subject Argument in der sense auch das Subject in synbehaviour? Nur fuer den vom user gegebenen Eintrag
    if len(user_lex.getSynBehavior_arguments()) == 0 or len(user_lex.getSense_arguments()) == 0:
        local_points += 1
    elif len(user_lex.getSynBehavior_arguments()) == len(user_lex.getSense_arguments()):
        tmp_points = 0
        #Abhaengig von den Eintraegen in Gold!!!
        #########################################
        #
        #
        #
        # 1 = sub -> obj
        # 2 = obj -> sub
        # 3 = sub -> sub
        # 4 = obj -> obj
        #
        #
        #
        #########################################
        fingerprint_user = []
        fingerprint_gold = []
        for entry_sense in user_lex.getSense_arguments():
            for entry_syn in user_lex.getSynBehavior_arguments():
                if entry_sense[1] == entry_syn[1]:
                    if "subject" in entry_sense[0] and entry_syn[0] in object_map:
                        fingerprint_user.append("1")
                    if "object" in entry_sense[0] and entry_syn[0] in subject_map:
                        fingerprint_user.append("2")
                    if "subject" in entry_sense[0] and entry_syn[0] in subject_map:
                        fingerprint_user.append("3")
                    if "object" in entry_sense[0] and entry_syn[0] in object_map:
                        fingerprint_user.append("4")
        
        for entry_sense in gold.getSense_arguments():
            for entry_syn in gold.getSynBehavior_arguments():
                if entry_sense[1] == entry_syn[1]:
                    if "subject" in entry_sense[0] and entry_syn[0] in object_map:
                        fingerprint_gold.append("1")
                    if "object" in entry_sense[0] and entry_syn[0] in subject_map:
                        fingerprint_gold.append("2")
                    if "subject" in entry_sense[0] and entry_syn[0] in subject_map:
                        fingerprint_gold.append("3")
                    if "object" in entry_sense[0] and entry_syn[0] in object_map:
                        fingerprint_gold.append("4")
        
        if len(fingerprint_user) == len(fingerprint_gold):
            correct = True
            for x in fingerprint_gold:
                if x not in fingerprint_user:
                    correct = False
            
            if correct == True:
                local_points += 1
        elif len(fingerprint_user) != len(fingerprint_gold):
            number_tmp = 0
            for x in fingerprint_gold:
                if x in fingerprint_user:
                    number_tmp += 1
            
            if number_tmp == 0:
                local_points += 0
            else:
                local_points += number_tmp / len(fingerprint_gold)
    else:
        local_points += 0
    #einen Punkt, wenn die Mappings im Synbehaviour von user_lex und gold gleich sind
    #ueberprueft und funktioniert
    if len(gold.getSynBehavior_arguments()) == 0:
        local_points += 1
    elif len(user_lex.getSynBehavior_arguments()) == len(gold.getSynBehavior_arguments()):
        found = 0
        for syn_1 in user_lex.getSynBehavior_arguments():
            for syn_2 in gold.getSynBehavior_arguments():
                if syn_1[0] == syn_2[0]:
                    found += 1

        
        if found >= len(gold.getSynBehavior_arguments()):
            local_points += 1
    else:
        local_points += 0
#                print local_points
    #ganz am Ende entweder 0 zurueck geben, oder normieren uber die 3 Punkte
    if local_points == 0:
        points = 0
    else:
        if askClassProperty(key) == True and local_points<=2.0 :
            local_points = (local_points + 0.0) / 2
        else:
            local_points = (local_points + 0.0) / 3
        points = local_points
    return  points

def evaluate(path_user_lexicon,Train_evaluation,path_goldstandard, number_of_uris = 40):
    #default: number_of_uris = 40
    print "Start evaluation"
    print
    
    adding_counter = 0

    
    Train_evaluation = True
    
    results_each_uri = []

    print "    Load user lexicon!"
    hm_UL , number_of_entries_UL= createArrayEntries(path_user_lexicon)
    print "    Done!"
    print
    print "    Load goldstandard lexicon!"
    hm_ML, number_of_entries_ML = createArrayEntries(path_goldstandard)
    print "    Done!"

    Laenge_Goldstandard = number_of_uris
##for TEST!!!
    Laenge_GoldstandardPrecision = len(hm_UL)


    ################## First Recall/Precision over given lexicon entries ##########################
    
    global_Recall = 0
    global_Precision = 0
    global_FMeasure = 0
    global_Accuracy = 0
    
    subject_map = {}
    object_map = {}
    subject_map,object_map = return_mapping()
        
    for key in hm_UL:
        
        local_Recall = 0
        local_Precision = 0
        local_FMeasure = 0
        local_Accuracy = 0
        numberOfCorrectEntries_lexicon = 0
        points = 0
        tmp_hm = {}
        used_entries = 0
        signature_hm = {}
        
        correct_user_entries = {}
        
        for user_lex in hm_UL[key]:
            signature_ml_hm = {}
            for gold in hm_ML[key]:
                #only use each user triple once!! otherwise there can be a higher recall than one!
                signature = str(user_lex.getPartOfSpeech())+" "+user_lex.getCanonicalForm().lower()+" "+str(user_lex.getSense())
                signature_ml = str(gold.getPartOfSpeech())+" "+gold.getCanonicalForm().lower()+" "+str(gold.getSense())
#                 print ("signature",signature)
#                 print ("signature_ml",signature_ml)
#                 print

                if signature not in signature_hm and signature_ml not in signature_ml_hm and gold.getPartOfSpeech() == user_lex.getPartOfSpeech() and user_lex.getCanonicalForm().lower() == gold.getCanonicalForm().lower() and user_lex.getSense()== gold.getSense():
                    numberOfCorrectEntries_lexicon+=1
                    signature_hm[signature]=""
                    signature_ml_hm[signature_ml]= ""
                    tmp_accuracy = calculateOverallAccuracy(key,user_lex,signature_ml, hm_ML, subject_map, object_map)
                    local_Accuracy += tmp_accuracy
                    entry = user_lex
                    if correct_user_entries.has_key(key):
                        tmp = correct_user_entries[key]
                        if tmp != None:
                            tmp.append(entry)
                            correct_user_entries[key] = tmp
                    else:
                        correct_user_entries[key] = [entry]


        if len(correct_user_entries) == 0:
            local_accuracy = 0
        else:
            local_Accuracy = (local_Accuracy+0.0)/numberOfCorrectEntries_lexicon


            
        if numberOfCorrectEntries_lexicon == 0:
            local_Recall = 0
            local_Precision = 0
            local_FMeasure = 0
        else:

            #use signature for number entries UL and ML.
            hm1 = {}
            for user_lex in hm_UL[key]:
                signature = str(user_lex.getPartOfSpeech())+" "+user_lex.getCanonicalForm().lower()+" "+str(user_lex.getSense())
                hm1[signature] = ""

            hm2 = {}
            for gold in hm_ML[key]:
                signature_ml = str(gold.getPartOfSpeech())+" "+gold.getCanonicalForm().lower()+" "+str(gold.getSense())
                hm2[signature_ml] = ""
                
            local_number_of_entries_UL = len(hm1)
            local_number_of_entries_ML = len(hm2)
            
            
            local_Recall = round((numberOfCorrectEntries_lexicon/float(local_number_of_entries_ML)),5)
            local_Precision = round((numberOfCorrectEntries_lexicon/float(local_number_of_entries_UL)),5)
            local_FMeasure = round((2*local_Recall*local_Precision)/(local_Precision+local_Recall),5)
            
        if local_Recall == 0:
            # in order to ignore accuracy, if no correct entry can be found, set accuracy to 1
            # as later is divided over the number of property, it normalizes itself for the overall result.
            local_Accuracy = 1
        results_each_uri.append([key,local_Recall,local_Precision,local_FMeasure,local_Accuracy])
        global_Recall += local_Recall
        global_Precision += local_Precision
        global_FMeasure += local_FMeasure
        global_Accuracy += local_Accuracy
        adding_counter += 1


#TODO: Warum werden vier EIntraege bei dataset/classes ignoriert, denn adding_counter ist vier kleiner als len(classes) 
#     global_Recall = global_Recall/adding_counter
    global_Recall = global_Recall/Laenge_Goldstandard
    print ("global_Precision",global_Precision)
    print ("Laenge_Goldstandard",Laenge_Goldstandard)
    print ("Laenge_GoldstandardPrecision",Laenge_GoldstandardPrecision)
    print ("(Laenge_Goldstandard - Laenge_GoldstandardPrecision)",(Laenge_Goldstandard - Laenge_GoldstandardPrecision))
    print ("adding_counter",adding_counter)
    #global_Precision = global_Precision+((Laenge_Goldstandard - Laenge_GoldstandardPrecision)+0.0)/Laenge_Goldstandard
    global_Precision = (global_Precision+(Laenge_Goldstandard - Laenge_GoldstandardPrecision))/Laenge_Goldstandard
    if global_Recall == 0 or global_Precision == 0:
        global_FMeasure = 0
    else:
        global_FMeasure = (2*global_Recall*global_Precision)/(global_Recall+0.0+global_Precision)
#     global_FMeasure = global_FMeasure/adding_counter
    global_Accuracy = global_Accuracy/adding_counter

    
    #Train_evaluation == True -> HTML-Datei
    #Train_evaluation == False -> TEST-Datei
    
    system_time = datetime.datetime.now()
#     filename_out_txt=path_user_lexicon.split('.')[0]+"_out.txt"
#     filename_out_html=path_user_lexicon.split('.')[0]+"_out.html"
    filename_out_txt=path_user_lexicon.replace("http://dbpedia.org/ontology/","")+"_out.txt"
    filename_out_html=path_user_lexicon.replace("http://dbpedia.org/ontology/","")+"_out.html"
    #filename_out_html="upload/out"+str(system_time)+".html"

    if Train_evaluation == True:
        #create html
        create_html_file(global_Recall,global_Precision,global_FMeasure,global_Accuracy,results_each_uri,filename_out_html,hm_ML)
        print filename_out_html
    
    if Train_evaluation == False:
        #create txt
        create_txt_file(global_Recall,global_Precision,global_FMeasure,global_Accuracy,results_each_uri,filename_out_txt)
        print filename_out_txt
    
    
            

def create_html_file(global_Recall,global_Precision,global_FMeasure,global_Accuracy,results_each_uri,filename,hm_ML):
    start_table= "<!doctype html> <html> <head> <title>Evaluation</title></head> <body> <p>Evaluation</p>"
    space="<p></p><p></p><p></p><p></p><p></p>"
    tabelle1="<table class=\"eval\" border=\"1\"><tr><th>Counter</th><th>URI</th><th>Recall</th><th>Precision</th><th>F-Measure</th><th>Accuracy</th></tr>"
    tabelle2="<table class=\"eval\" border=\"1\"><tr><th>Global Recall</th><th>Global Precision</th><th>Global F-Measure</th><th>Global Accuracy</th><th>F-Prime</th></tr>"
    f_prime = (2*global_FMeasure*global_Accuracy)/(global_Accuracy+global_FMeasure)
    inhalt_tabelle2="<tr><td>"+str(global_Recall)+"</td><td>"+str(global_Precision)+"</td><td>"+str(global_FMeasure)+"</td><td>"+str(global_Accuracy)+"</td><td>"+str(f_prime)+"</td></tr>" 
    end_tabelle="</table>"  
    ende="</body> </html>"
    string=""
    
    
    
    #results_each_uri.appen([uri_to_compare_with,Recall,Precision,FMeasure,Accuracy])
    counter = 0
    for uri,recall,precision,fmeasure,accuracy in results_each_uri:
        counter += 1
        
        string_ml = ""
        for entry in hm_ML[uri]:
            string_ml += entry.getPartOfSpeech()+" "+entry.getCanonicalForm().lower()+" "+str(entry.getSense())+" "+str(entry.getSynBehavior_arguments())+"\n"
        
        
        
        #set here uri as reference to htmlfolder and html file
        name = uri.replace("http://dbpedia.org/ontology/","")
        name = name.replace("http://dbpedia.org/property/","")
        file_name_html = "html"+name+"/"+ "PatternList" + name + ".html"
        string_bla="<tr><td>"+str(counter)+"</td><td><a href=\""+file_name_html+"\">"+uri+"</a></td><td>"+str(recall)+"</td><td>"+str(precision)+"</td><td>"+str(fmeasure)+"</td><td>"+str(accuracy)+"</td></tr>"       
        string+=string_bla                                                                                            

    outfile=open(filename,"w")
    outfile.write(start_table+space+tabelle2+inhalt_tabelle2+end_tabelle+space+tabelle1+string+end_tabelle+ende)
    outfile.close()



def create_txt_file(global_Recall,global_Precision,global_FMeasure,global_Accuracy,results_each_uri,filename):
    
    globale_uebersicht_txt= "global_Recall: "+str(global_Recall)+"; global_Precision: "+str(global_Precision)+"; global_FMeasure: "+str(global_FMeasure)+"; global_Accuracy: "+str(global_Accuracy)+";\n"
    string=""
    string += "uri;recall;precision;fmeasure;accuracy\n"
    for uri,recall,precision,fmeasure,accuracy in results_each_uri:
        string += uri+";"+str(recall)+";"+str(precision)+";"+str(fmeasure)+";"+str(accuracy)+"\n"                                                                                                  

    outfile=open(filename,"w")
    outfile.write(globale_uebersicht_txt+"\n\n"+string)
    outfile.close()


def return_mapping():
    subject_map = {}
    subject_map["http://www.lexinfo.net/ontology/2.0/lexinfo#subject"]=""
    subject_map["http://www.isocat.org/datcat/DC-2261"]=""
                
    subject_map["subject"]=""
    subject_map["DC-2261"]=""
    subject_map["copulativeArg"]=""
    
    object_map = {}
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#directObject"]=""
    object_map["http://www.isocat.org/datcat/DC-2263"]=""
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#indirectObject"]=""
    object_map["http://www.isocat.org/datcat/DC-1310"]=""
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#prepositionalObject"]=""
    object_map["http://www.isocat.org/datcat/DC-4638"]=""
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#prepositionalAdjunct"]=""
    object_map["http://www.isocat.org/datcat/DC-4622"]=""
    object_map["http://www.isocat.org/datcat/copulativeArg"]=""
    
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#possessiveAdjunct"]=""
    object_map["http://www.isocat.org/datcat/DC-4622"]=""
    object_map["possessiveAdjunct"]=""
    object_map["DC-4622"]=""
    
    object_map["directObject"]=""
    object_map["DC-2263"]=""
    object_map["indirectObject"]=""
    object_map["DC-1310"]=""
    object_map["prepositionalObject"]=""
    object_map["DC-4638"]=""
    object_map["prepositionalAdjunct"]=""
    object_map["DC-4622"]=""
    return subject_map, object_map


def create_entryTerm(entry):
    create_entryTerm = entry.split(";")[0]
    create_entryTerm = create_entryTerm.lower()
    create_entryTerm = create_entryTerm.replace("a lemon:lexicalentry","")
    create_entryTerm = create_entryTerm.replace(":","")
    create_entryTerm = create_entryTerm.replace(" ","")
    return create_entryTerm
    
    

 
 
def askClassProperty(uri):
#    print "in askClassProperty"
    uri = uri.replace("http://dbpedia.org/ontology/","")
    if uri[0].isupper():
        return True
    else:
        False
#    sparql = SPARQLWrapper(endpoint)
#    sparql.setQuery("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX owl: <http://www.w3.org/2002/07/owl#>  ASK WHERE {<"+uri+"> rdf:type owl:Class}")
#    sparql.setReturnFormat(JSON)
#    results = sparql.query().convert()
#    #print results
#    for result in results:
#        try:
#            string = str(results[result])
#            if "False" in string:
#                return False
#            
#            if "True" in string:
#                return True
#        except:
#            pass
#    return False



 
   

    