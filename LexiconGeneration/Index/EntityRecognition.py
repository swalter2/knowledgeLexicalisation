import lucene
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, IndexSearcher, Version, QueryParser
    
import IndexUtils
import sys

class eRecognition():
    
    analyzer = None
    searcher = None
    directory = None
    
    
    
    def create_index(self,path_to_index):
        path_to_file = "/home/swalter/workspace/resource"
        if self.test_existens_index(path_to_index) == False:
            print "Create new entityIndex"
            path = SimpleFSDirectory(File(path_to_index))
            writer = IndexWriter(path, analyzer, True, IndexWriter.MaxFieldLength(512))
            f = file(path_to_file,"r")
            
            for line in f:
                
                line=line.replace("\n","")
                doc = Document()
                doc.add(Field("title", line, Field.Store.YES, Field.Index.ANALYZED))
                writer.addDocument(doc)
                
            writer.close() 
        else:
            print "entityIndex already exists"
    
    def test_existens_index(self,path_to_index):
        try:
            directory = SimpleFSDirectory(File(path_to_index))
            analyzer = StandardAnalyzer(Version.LUCENE_35)
            writer = IndexWriter(directory, analyzer, False, IndexWriter.MaxFieldLength(512))
            writer.close()
            return True
        except: 
            return False
        
        
    def __init__(self, path_to_index):
        global analyzer
        global searcher
        global directory
        lucene.initVM()
        directory = SimpleFSDirectory(File(path_to_index))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        self.create_index(path_to_index)
        searcher = IndexSearcher(directory)

    
    def does_line_exist(self,line):
        return IndexUtils.does_line_exist(line.lower(), searcher, analyzer)
    
    
    def search(self,line):
        'returns array of sentences in new data type'
        #print line
        replace = str.replace
        return IndexUtils.searchWithoutWrapper(line, searcher, analyzer, replace)
    
    
    def regognise_e(self,sentence):
        #TODO: Ueberarbeiten
        #scheint nicht in der self.search funktion zu liegen der Fehler
        'gets parsed string and tries to find all entities'
        'returns new parsed sentence with updatet dependencie structure'
        
        #just to be sure.....
        if sentence[(len(sentence)-2):] == "  ":
            sentence=sentence[:(len(sentence)-2)]
        
        #print "sentence start: "+sentence
        remember = ""
        entity = ""
        remember_sentence = ""
        
        ent_ar=[]
        hm={}
        counter = 0
        for line in sentence.split("  "):
            #print line
            counter += 1
            
            word=line.split(" ")[1]
            
            #print word
            
            if remember != "":
                remember += " "+word
                if "and" not in line and "." not in line:
                    remember_sentence += "  "+line
                    print remember_sentence
            else: 
                remember=word
                if "and" not in line and "." not in line:
                    remember_sentence = line
                    print remember_sentence
            #check if word is part of index, if not forget it, if it is in index, remember it
            does_line_exists = False
            try:
                does_line_exists = self.does_line_exist(remember) 
            except Exception:
                print "Unexpected error:", sys.exc_info()[0]
                print "error in EnityRecognition self.does_line with sentence "+ remember+" \n\n"
            if does_line_exists == True and " " in remember :
                entity = remember
                entity=entity.replace(" .","")
                entity = entity.replace(" and","")
                hm[entity]=remember_sentence
                
            else:
                print "ELSE   !"
                ent_ar.append(entity)
                #print "added: "+entity
                if counter > 1:
                    remember = word
                    if "and" not in line and "." not in line:
                        remember_sentence = line
                else:
                    remember = ""
                    remember_sentence = ""
            print "first step done"
            
            #step one: see above, finde possible entitys
            
            blub = []
            for key in hm:
                blu = []
                blu.append(key)
                blu.append(hm[key])

                blub.append(blu)


            #kleinste als erstes schreiben:
        for line in blub:

            
            #print "line: "+ line
            #sort by length
            need_to_sort = False
            for i in range(0,len(blub)-1):
                if len((blub[i])[0]) > len((blub[i+1])[0]):
                    string1 = blub[i]
                    string2 = blub[i+1]
                    
                    blub[i] = string2
                    blub[i+1] = string1
                    need_to_sort = True
            if need_to_sort == False:
                break 
            # ueber array iterieren und schauen, ob  es teil eines anderen EIntrages ist, wenn nicht, dann abspeichern und spaeter wiederverwenden
        #reset hm...
        hm = {}   
        #result_array1=[]
        for tmp1 in blub:
            found = False
            for tmp2 in blub:
                if tmp1[0] in tmp2[0] and tmp1[0] != tmp2[0]:
                    
                    found = True
                    break
            if found == False:
                #result_array1.append(tmp1)
                hm[tmp1[0]] = tmp1[1]
                
            #step two: get lines for searchterm and check if len(entyty)==len(sentence(index(search_term)))

        result_list = []
        new_sentence = sentence
        for key in hm:
                
            is_entity = False
            search_array = []
            try:
                search_array = self.search(key)
            except Exception:
                import sys
                print "Unexpected error:", sys.exc_info()[0]
                print "error in EntityRecognition in self.search with key "+key+" \n\n"
            
            try:    
                for index_entry in search_array:
                    #in the index, the name and the uri are saved and seperated by :::
                    #e.g.: Berlin:::http://dbpedia.org/resource/Berlin
                    if len(key)==len(index_entry.split(":::")[0]):
                        is_entity = True
                        break
            except:
                print "Error in first for loop in Entity Recognition in recognise_e\n\n"
                

            if is_entity == True:
                tmp=[]
                tmp.append(key)
                tmp.append(hm[key])
                result_list.append(tmp)
            #step four, return new parsed sentence, which can be directly put into the gram generation 
            new_result_array = []
            
            print "1"
            try:
                if len(result_list)>0:
                    #Fehler Zugriff auf result_list funktioniert nicht
                    for tmp_array in result_list:
                        name = ""
                        for tmp in tmp_array[1].split("  "):
                            if tmp != None and tmp != "":
                                name += tmp.split(" ")[1]
                        tmp_last = (tmp_array[1].split("  "))[len(tmp_array[1].split("  "))-1]
                        
                        name_tmp = tmp_last.split(" ")[1]
                        tmp_last=tmp_last.replace(name_tmp,name)
                        number = tmp_last.split(" ")[0]
                        dep = tmp_last.split(" ")[6]
                        
                        tmp = []
                        #print tmp_array[1]
                        tmp.append(tmp_array[1])
                        tmp.append(tmp_last)
                        new_result_array.append(tmp)
                    else:
                        new_result_array = None
            except Exception:
                print Exception
                print "Unexpected error:", sys.exc_info()[0]
                print "Error in second for loop in Enity recognition in recognise_e \n\n"
                new_result_array = None
                
            if new_result_array != None:
                for tmp_array in new_result_array:
                    #print "1: "+tmp_array[0]
                    #print "2: "+tmp_array[1]
                    try:
                        new_sentence = new_sentence.replace(tmp_array[0],tmp_array[1])
                    except:
                        print("Index out of bounds in ENity Recognition regognise_e \n\n")
        return new_sentence
            
    
    
   
   
    def return_res_matches(self,sentence):
        #TODO: Ueberarbeiten
        #scheint nicht in der self.search funktion zu liegen der Fehler
        'gets parsed string and tries to find all entities'
        'returns new parsed sentence with updatet dependencie structure'
        
        #just to be sure.....
        if sentence[(len(sentence)-2):] == "  ":
            sentence=sentence[:(len(sentence)-2)]
        
        #print "sentence start: "+sentence
        remember = ""
        entity = ""
        remember_sentence = ""
        
        ent_ar=[]
        hm={}
        counter = 0
        for word in sentence.split(" "):
            #print line
            counter += 1
            
            
            
            #print word
            
            if remember != "":
                remember += " "+word
                #if "and" not in line and "." not in line:
                #    remember_sentence += "  "+line
                #    print remember_sentence
            else: 
                remember=word
                #if "and" not in line and "." not in line:
                #    remember_sentence = line
                #    print remember_sentence
            #check if word is part of index, if not forget it, if it is in index, remember it
            does_line_exists = False
            try:
                does_line_exists = self.does_line_exist(remember) 
            except Exception:
                print "Unexpected error:", sys.exc_info()[0]
                print "error in EnityRecognition self.does_line with sentence "+ remember+" \n\n"
            if does_line_exists == True and " " in remember :
                entity = remember
                entity=entity.replace(" .","")
                entity = entity.replace(" and","")
                hm[entity]=remember_sentence
                
            else:
                print "ELSE   !"
                ent_ar.append(entity)
                #print "added: "+entity
                if counter > 1:
                    remember = word
                  #  if "and" not in line and "." not in line:
                  #      remember_sentence = line
                else:
                    remember = ""
                    remember_sentence = ""
            print "first step done"
        return hm
        