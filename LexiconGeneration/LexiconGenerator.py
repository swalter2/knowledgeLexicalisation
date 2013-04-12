from nltk.stem.wordnet import WordNetLemmatizer
from Util import Levenshtein, Sparql
from Util import WordnetFunctions as wn

def createLexiconEntry(rule,uri,Wiktionary, term = None):
    lmtzr = WordNetLemmatizer()


    if rule[len(rule)-2:] == "  ":
        rule = rule[:len(rule)-2:]

    
    marker = {}
    term = ""
    for item in rule.split("  "):
            
        if ("in" in item.split(" ")[3].lower() or "to" in item.split(" ")[3].lower()) and item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
            marker[item.split(" ")[1]]=""
            
        elif item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
                term += item+"  "
    if term.endswith("  "):
        term = term[:-2]
                
    #print "before creating entry term"     
    entry_term = ""
    if "  " in term:
        for x in term.split("  "):
            entry_term += x.split(" ")[1]+" "
        if entry_term.endswith(" "):
            entry_term = entry_term[:-1]
    else:
        entry_term = term.split(" ")[1]
        
    #print "rule "+rule
    #print "term "+term
    #print "entry_term "+entry_term 
    #raw_input("wait")
    #verb is defined via vbn, vbd, vbg, vbz, vb => " vb"
    if " vb" in term:
        if marker.has_key("to") or "vbn" in term  or "vbg" in term  or "vbd" in term  or marker.has_key("on"):
            lemma = lmtzr.lemmatize(entry_term,"v")
            return [AdjectivePredicateFrame(entry_term,uri, marker),TransitiveFrame(lemma, uri,marker)]
        else:
            return [TransitiveFrame(entry_term, uri,marker)]
            
        print
    else:
        #print "no verb"
        #print "rule "+rule
        #print "term "+term
        #print "entry_term "+entry_term    
        if marker.has_key("of"):  
            return [NounPossisiveFrame(entry_term,uri)]
        else:
            return [NounPPFrame(entry_term,uri,marker)]
#
#                
#        
#    
#    
#    
#    
#    marker = {}
#    
#    ###print "rule: "+rule
#    syn_behaviorx=""
#    syn_behaviory=""
#    noun_bool = False
#    if term == None:
#        term = ""
#        for item in rule.split("  "):
#            
#            #hier abfragen, ob pos3 ein TO oder IN ist und wenn ja, zum array marker hinzufuegen
#            if item.split(" ")[1]!="x" and item.split(" ")[1]!="y" and item.split(" ")[3].lower()!="in" and item.split(" ")[3].lower()!="to" and ("dt" not in item and "the" not in item):
#                
#                #delet here if item contains DT and the so that crosses and not crosses the is created.
#                if len(item.split(" "))>1:
#                    term += item.split(" ")[1]+" "
#                    try:
#                        if "nn" in term.split(" ")[3]:
#                            noun_bool = True
#                    except:
#                        pass
#                else:
#                    ##print "term:"+item
#                    term = item
#                    
#            if ("in" in item.split(" ")[3].lower() or "to" in item.split(" ")[3].lower()) and item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
#                marker[item.split(" ")[1]]=""
#    else:
#        for item in rule.split("  "):
#            if ("in" in item.split(" ")[3].lower() or "to" in item.split(" ")[3].lower()) and item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
#                marker[item.split(" ")[1]]=""
#                
#                
#            
#    
#    if term.endswith(" "):
#        term = term[:-1]
#    elif term.startswith(" "):
#        term = term[1:]
#    
#    #print "term: "+term
#    
#    if term == "and" or len(term)<3:
#        return None
#    if term != "":
#        
#        frame_term = ""
#        
#        
#        tag,tag_array = wn.return_Informations(term)
#        partOfSpeech = None
#    
#        
#        if tag == "VERB" and noun_bool == False:
#            frame_term = "TransitiveFrame"
#            partOfSpeech = "verb"
#            term_other_form = term
#            #thats the first appended verb
#            term = tag_array[0]
#            
#        elif tag == "NOUN" or noun_bool == True:
#            frame_term = "NounPPFrame"
#            partOfSpeech = "noun"
#        elif tag == "ADJ":
#            frame_term = "AdjectivePPFrame"
#            partOfSpeech = "adjective"
#        elif tag == "NONE":
#            frame_term = "NounPPFrame"
#            partOfSpeech = "noun"
#        
#        
#        #print "tag: "+tag
#        #print "frame_term: "+frame_term   
#        #print "tag_array: "+str(tag_array) 
#        
#        
#        if frame_term == "NounPPFrame":
#            if uri == None:
#                return None
#            else:
#                #print "uri: "+uri
#                return createNounPPFrameEntry(rule,uri)
#        
#        
#        
#
#        for item in rule.split("  "):  
#            #print item     
#            if "x" in item:
#                x_space = "x_"+item.split(" ")[7]
#                ##print "x_space: " + x_space
#                try:
#                    syn_behaviorx="isocat:DC-"+str(hm[item.split(" ")[7]])+" :"+x_space+ " ;"
#                except:
#                    syn_behaviorx="isocat:DC-"+"NONE"+" :"+x_space+ " ;"
#                
#            if "y" in item:
#                #y in isocat is now for the number, which I still need to recive
#                y_space = "y_"+item.split(" ")[7]
#                ##print "y_space: " + y_space
#                try:
#                    syn_behaviory="isocat:DC-"+str(hm[item.split(" ")[7]])+" :"+y_space+ " ;"
#                except:
#                    syn_behaviory="isocat:DC-"+"NONE"+" :"+y_space+ " ;"
#        
#        if "[[" in term:
#            return None
#        term = term.lower()
#        #print "term2: "+term
#        lexicon=":"+term.replace(" ", "").lower()+" a lemon:LexicalEntry ; \nlemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;"
#        #
#        #if term_other_form != "" and term_original_form !="" and term_plural == True:
#        #    lexicon += "\n"+"lemon:otherForm [ lemon:writtenRep \""+ term_original_form.lower() +"\"@en ] ;"
#        #    
#        #elif term_other_form != "" and term_original_form !="" and term_plural == False:
#        #    lexicon += "\n"+"lemon:otherForm [ lemon:writtenRep \""+ term_other_form.lower() +"\"@en ] ;"
#        
#        #raw_input("wait")
#        #print
#        #print
#        sense = ""
#        
#        if "VERB" in frame_term.lower():
#            lexicon += "\n"+"lemon:synBehavior [ rdf:type lemon:TransitiveFrame ;\n" + syn_behaviorx+"\n"+syn_behaviory+"\n"+"] ;\n" 
#            #ontology_uri = find_ontology_uri(term, property_list)
#            #if ontology_uri == None:
#            #    #return None
#            #    if uri == None:
#            #        return None
#            #    else:
#            #        ontology_uri = uri
#            lexicon +="lexinfo:partOfSpeech lexinfo:verb ;\n"
#            sense = "lemon:sense [ lemon:reference <"+uri+"> ;\nlemon:subjOfProp :"+x_space+" ;\nlemon:objOfProp :"+y_space+" ; ] ."
#        
#        elif "NOUN" in frame_term.lower():
#            if len(marker)>0:
#                
#                #lemon:synBehavior [ lemon:frame lexicon:NounPPFrame ;
#                #     lexinfo:prepositionalObject :x_pobj ;
#                #     lexinfo:prepositionalObject :y_pobj ] ; 
#                     
#                     
#                lexicon += "\n"+"lemon:synBehavior [ lemon:frame lexinfo:NounPPFrame ;\n" 
#                m_counter = 0
#                for key in marker:
#                    m_counter += 1
#                    #lexicon += "lexinfo:prepositionalObject :marker_"+str(m_counter)+" ;\n"
#                    if m_counter == len(marker):
#                        lexicon += "lexinfo:prepositionalObject :marker_"+str(m_counter)+" ];\n"
#                    else:
#                        lexicon += "lexinfo:prepositionalObject :marker_"+str(m_counter)+" ;\n"
#                lexicon += " ]; \n"
#                lexicon +="lexinfo:partOfSpeech lexinfo:noun ;\n"
#            
#            
#            #ontology_uri = find_ontology_uri(term, class_list)
#            #if ontology_uri == None:
#            #    #return None
#            #    if uri == None:
#            #        return None
#            #    else:
#            #        ontology_uri = uri
#            sense = "lemon:sense [ lemon:reference <"+uri+"> ;] ."
#            
#
#        elif "ADJ" in frame_term.lower():
#            #ontology_uri = find_ontology_uri(term, class_list)
#            #if ontology_uri == None:
#            #    #return None
#            #    if uri == None:
#            #        return None
#            #    else:
#            #        ontology_uri = uri
#            lexicon += "\n"+"lemon:synBehavior [ rdf:type lexinfo:AdjectivePPFrame ;\n" + syn_behaviorx+"\n"+syn_behaviory+"\n"+"] ;\n" 
#            sense = "lemon:sense [ lemon:reference <"+uri+"> ;\nlemon:subjOfProp :"+x_space+" ;\nlemon:objOfProp :"+y_space+" ; ] ."
#            lexicon +="lexinfo:partOfSpeech lexinfo:adjective ;\n"
#            
#
#        lexicon += sense
#    
#        if "NOUN" in frame_term.lower():
#            m_counter = 0
#            for key in marker:
#                m_counter += 1
#                lexicon += "\n:"+"marker_"+str(m_counter)+" lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+key+"\"] ]."
#        elif len(marker)<=2:
#            m_counter = 0
#            for key in marker:
#                m_counter += 1
#                if m_counter == 1:
#                    lexicon += "\n:"+x_space.replace(" ","")+" lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+key+"\"] ]."
#                if m_counter == 2 and y_space !="":
#                    lexicon += "\n:"+y_space.replace(" ","")+" lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+key+"\"] ]."
#
#        if "ADJ" in frame_term.lower() or "VERB" in frame_term.lower() or "NOUN" in frame_term.lower():
#            return lexicon
#    else:
#        
#        return None
#
##uri = "http://dbpedia.org/ontology/spouse"
###print createLexiconEntry(rule,uri)



def createLexiconEntryForEntity(entity,uri):
    
    
    entry = ":"+entity.replace(" ","").lower()+" a lemon:LexicalEntry ; \n lemon:canonicalForm [ lemon:writtenRep \""+entity.lower()+"\"@en ] ;"
    entry += "lexinfo:partOfSpeech lexinfo:properNoun ; \n"
    entry += "lemon:sense [ lemon:reference <"+uri+"> ].\n" 
    return entry
    



def createNounPPFrameEntry(pattern,uri):
    #pattern ist immer lower()
    array = pattern.split("  ")
    entry_term = ""
    marker = []

    for a in array:
        if "x" not in a and "y" not in a and "nn" in a and ("dobj" in a or "nn" in a or "pobj" in a):
            entry_term = a.split(" ")[1]

        if ("in" in a.split(" ")[3] or "to" in a.split(" ")) and a.split(" ")[1]!="x" and a.split(" ")[1]!="y":

            marker.append(a.split(" ")[1])

    #if entry_term.endswith(" "):
    #    entry_term = entry_term[:-1]
    #elif entry_term.beginswith(" "):
    #    entry_term = entry_term[1:]
        
    if len(entry_term)<3:
        return None
               
    entry = ":"+entry_term.replace(" ","").lower()+" a lemon:LexicalEntry ; "
    entry +="\nlemon:canonicalForm [ lemon:writtenRep \""+entry_term.lower()+"\"@en ] ;\n"
    entry +="lemon:synBehavior [ rdf:type lexinfo:NounPPFrame ;\n"
    entry +="isocat:copulativeArg :xargument ;\n"
    entry +="isocat:possessiveAdjunct :yargument ;\n"
    entry +="] ;\n"
    entry +="lemon:sense [ lemon:reference <"+uri+"> ;\n"
    entry +="lemon:subjOfProp :xargument ;\n"
    entry +="lemon:objOfProp :yargument ; ] ;\n"
    entry +="lexinfo:partOfSpeech lexinfo:noun ."
    if len(marker)>0:
        entry +="\n:y_pobj lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+marker[0]+"\"] ]."

    return entry


def createNounPPFrameEntryWordnet(uri):
    sparql = Sparql.Connection()
    label = sparql.getLabel(uri)[0]
    result_array = []
    array = wn.return_synsetsNoun(label)
    
    for a in array:
        tag,tag_array = wn.return_Informations(a)
        frame = None
        partOfSpeech = None
        
        if tag == "VERB":
            frame = "TransitiveFrame"
            partOfSpeech = "verb"
        elif tag == "NOUN":
            frame = "NounPPFrame"
            partOfSpeech = "noun"
        elif tag == "ADJ":
            frame = "AdjectivePPFrame"
            partOfSpeech = "adjective"
        elif tag == "NONE":
            frame = "NounPPFrame"
            partOfSpeech = "noun"
        
        for item in tag_array:
            entry = ":"+item.lower().replace(" ","")+" a lemon:LexicalEntry ; "
            entry +="\nlemon:canonicalForm [ lemon:writtenRep \""+item.lower()+"\"@en ] ;\n"
            entry +="lemon:synBehavior [ rdf:type lexinfo:"+frame+" ;\n"
            entry +="isocat:copulativeArg :x_nn ;\n"
            entry +="isocat:DC-4638 :y_pobj ;\n"
            entry +="] ;\n"
            entry +="lemon:sense [ lemon:reference <"+uri+"> ;\n"
            entry +="lemon:subjOfProp :x_nn ;\n"
            entry +="lemon:objOfProp :y_pobj ; ] ;\n"
            entry +="lexinfo:partOfSpeech lexinfo:"+partOfSpeech+" ."
            result_array.append(entry) 
        
        
    
    #for x in array:
   # 
   #     entry = ":"+x.replace(" ","").lower()+" a lemon:LexicalEntry ; "
   #     entry +="\nlemon:canonicalForm [ lemon:writtenRep \""+x.lower()+"\"@en ] ;\n"
   #     entry +="lemon:synBehavior [ rdf:type lexinfo:NounPPFrame ;\n"
   #     entry +="isocat:copulativeArg :x_nn ;\n"
   #     entry +="isocat:DC-4638 :y_pobj ;\n"
   #     entry +="] ;\n"
   #     entry +="lemon:sense [ lemon:reference <"+uri+"> ;\n"
   #     entry +="lemon:subjOfProp :x_nn ;\n"
   #     entry +="lemon:objOfProp :y_pobj ; ] ;\n"
   #     entry +="lexinfo:partOfSpeech lexinfo:noun ."
   #     
   #     result_array.append(entry)

    return result_array




def createClassEntry(uri):
    sparql = Sparql.Connection()
    label = sparql.getLabel(uri)[0]
    result_array = []
    array = wn.return_synsetsNoun(label)
    
    for entry in array:
        entry = entry.replace("_"," ")
        lexEntry = ":"+entry.replace(" ","").lower()+" a lemon:LexicalEntry ;\n"
        lexEntry += "lemon:canonicalForm [ lemon:writtenRep \""+entry.lower()+"\"@en ; isocat:DC-1298 isocat:DC-1387 ] ;\n"
        lexEntry += "lemon:sense [ lemon:reference <"+uri+"> ] ;\n"
        lexEntry += "isocat:DC-1345 isocat:DC-1333  ."
        result_array.append(lexEntry)
    
    return result_array

def create_isocat():
    hm = {}
    
    hm["nsubj"] = 2261 
    hm["dobj"] = 2263
    hm["iobj"] = 1310
    hm["pobj"] = 4638
    hm["dep"] = 2323
    hm["amod"] = 2269
    hm["det"] = 1272
    hm["nn"] = 2261   
    hm["prep"] = 2271
    hm["punct"] = 1372
    hm["root"] = 3460
    hm["rel"] = 2317
    hm["ref"] = 3751
    hm["cc"] = 2272
    hm["conj"] = 3132
    hm["aux"] = 3095
    
    return hm


def find_ontology_uri(pattern,ontologyEntryList):
    'returns uri from travel ontology frame'
    
    if ontologyEntryList == None:
        return None
    
    
    nld = Levenshtein.calculate_normalized_levenshtein_distance
    for key in ontologyEntryList:
        if pattern.lower() == key.replace("http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#;","").lower():
            return key
        elif pattern.lower() in key.lower() or key.replace("http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#;","").lower() in pattern.lower():
            return key
        
    #if non is found, split up, if I know, that there is a _ in the pattern, or use the whole pattern with NLD
    for key in ontologyEntryList:
        if nld(pattern.lower(),key.replace("http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#;","").lower()) >0.6:
            return key
        
    if " " in pattern:
        array_gold = pattern.split("_")
        for item in array_gold:
            for key in ontologyEntryList:
                if nld(item.lower(),key.replace("http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#;","").lower()) >0.6:
                    return key
    #raw_input("wait 2")
    return None


def NounPossisiveFrame(term,reference):
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ];\n" 
    entry += "lemon:sense [ lemon:reference <"+reference+"> ;\n"
    entry += "lemon:subjOfProp :arg1 ;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:NounPossessiveFrame ;\n"
    entry += "lexinfo:copulativeArg :arg2 ;\n"  
    entry += "lexinfo:possessiveAdjunct :arg1 ] ;\n"
    entry += "lexinfo:partOfSpeech lexinfo:noun .\n"
    entry += ":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \"of\"] ]."
    return entry

def NounPossisiveFrameWithoutMarker(term,reference):
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ];\n" 
    entry += "lemon:sense [ lemon:reference <"+reference+"> ;\n"
    entry += "lemon:subjOfProp :arg1 ;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:NounPossessiveFrame ;\n"
    entry += "lexinfo:copulativeArg :arg2;\n"
    entry += "lexinfo:possessiveAdjunct :arg1 ] ;\n"
    entry += "lexinfo:partOfSpeech lexinfo:noun ."
    return entry
  
def TransitiveFrame(term, reference,marker):
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
    #entry += "lemon:otherForm [ lemon:writtenRep "married"@en ;\n" 
    #entry += " lexinfo:verbMood lexinfo:participle ;\n"
    #entry += "lexinfo:aspect   lexinfo:perfective ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:TransitiveFrame ;\n"
    entry += "lexinfo:subject      :arg1 ;\n"
    entry += " lexinfo:directObject :arg2 ] ;\n"
    entry += "lemon:sense [ lemon:reference <"+reference+">;\n"
    entry += "lemon:subjOfProp :arg1;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    if len(marker) == 0:
        entry += "lexinfo:partOfSpeech lexinfo:verb ."
    else:
        entry += "lexinfo:partOfSpeech lexinfo:verb .\n"
        for x in marker:
            entry +=":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry


def AdjectivePredicateFrame(term, reference, marker):
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:AdjectivePredicateFrame ;\n"
    entry += "lexinfo:copulativeSubject :arg1;\n"
    entry += "lexinfo:attributiveArg :arg1 ];\n"
    entry += "lemon:sense [ lemon:reference <"+reference+">;\n"
    entry += "lemon:subjOfProp :arg1;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    if len(marker) == 0:
        entry += "lexinfo:partOfSpeech lexinfo:adjective ."
    else:
        entry += "lexinfo:partOfSpeech lexinfo:adjective .\n"
        for x in marker:
            entry +=":arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry

def AdjectivePPFrame(term, reference, marker):
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:AdjectivePPFrame ;\n"
    entry += "lexinfo:copulativeSubject   :arg1;\n"
    entry += "lexinfo:prepositionalObject :arg2 ];\n"
    entry += "lemon:sense [ lemon:reference <"+reference+"> ] ;\n"
    if len(marker) == 0:
        entry += "lexinfo:partOfSpeech lexinfo:adjective ."
    else:
        entry += "lexinfo:partOfSpeech lexinfo:adjective .\n"
        for x in marker:
            entry +=":arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry


def NounPPFrame(term,reference,marker):
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
    entry += "lemon:sense [ lemon:reference <"+reference+"> ;\n"
    entry += "lemon:subjOfProp :arg1 ;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:NounPPFrame ;\n"
    entry += "lexinfo:copulativeArg :arg1 ;\n"
    entry += "lexinfo:prepositionalAdjunct :arg2] ;\n"
    if len(marker) == 0:
        entry += "lexinfo:partOfSpeech lexinfo:noun ."
    else:
        entry += "lexinfo:partOfSpeech lexinfo:noun .\n"
        for x in marker:
            entry +=":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry

