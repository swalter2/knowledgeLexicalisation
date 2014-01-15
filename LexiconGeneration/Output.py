# -*- coding: utf-8 -*- 
import codecs, os


def generate_html(mapping_pattern_entry_list,sentence_list,path,name):
    path_folder = path+"html/"
    f_out = codecs.open(path + "PatternList" + name.replace("http://dbpedia.org/ontology","") + ".html", "w","utf-8")
    
    os.mkdir(path_folder)
    
    lexicon_entry_list = {}
    
#     for key,value in mapping_pattern_entry_list.iteritems():
#         try:
#             for entry in value:
#                 try:
#                     print hm_res_sentences[entry[0]] 
#                 except: 
#                     pass
#         except:
#             pass

    for key,value in mapping_pattern_entry_list.iteritems():
        try:
            for entry in value:
                try:
                    value_pattern = entry[1]
                    if lexicon_entry_list.has_key(key):
                        t_value = lem_entries_hm[key]
                        t_value += value_pattern
                        lexicon_entry_list[key] = t_value
                    else:
                        lexicon_entry_list[key] = value_pattern
                except: 
                    pass
        except:
            pass
    
    string = "<html><head><title>Beschreibung der Seite</title></head><body>"

    counter = 0
    for key, value_pattern in sorted(lexicon_entry_list.iteritems(), key=lambda x:x[1], reverse = True):
        output = ""
        try:
            for entry in mapping_pattern_entry_list[key]:
                for x in entry:
                    output += str(x)+"  "
        except:
            pass
        file_name = path_folder +str(counter)+".txt"
        f_output = codecs.open(file_name, "w","utf-8")
        f_output.write(output)
        f_output.close()
        counter += 1
        string += "<a href=\""+file_name+"\">"+key+"</a> "+ str(value_pattern)+ "<br>"


    string += "</body> </html>"
    
    f_out.write(string)
    f_out.close()










def createPatternFile(uri, path, name, hm):
    f_out = codecs.open(path + "PatternList" + name.replace("http://dbpedia.org/ontology","") + ".txt", "w","utf-8")
    write_string = ""
#     overall_pattern_number = 0
#     for key, value in hm.iteritems():
#         overall_pattern_number += value
        
        
    different_pattern = 0
    hm_new = {}
    hm_test = {}
    for key, value in hm.iteritems():  
              
#         We want to igrnore alle patterns, whcih occour only once in the corpus
        if value > 1:
            different_pattern += 1
            hm_new[key] = value
            
#             new_pattern = normalisePattern(key)
            new_pattern = key
            if hm_test.has_key(new_pattern):
                hm_test[new_pattern] = hm_test[new_pattern]+value
            else:
                hm_test[new_pattern] = value
            
    
    hm = {}
    hm = hm_new
    hm_new = {}
    alpha = 0.8
    
    overall_pattern_number = 0
    for key, value in hm_test.iteritems():
        overall_pattern_number += value
    
    f_out.write("Overall number: " + str(overall_pattern_number) + " Different patterns: " + str(different_pattern) + "\n\n\n")

            
    
    for key, value in sorted(hm_test.iteritems(), key=lambda x:x[1], reverse=True):
#         p = value / (overall_pattern_number + 0.0)
#         p_prime = (value - alpha) / (overall_pattern_number + 0.0)
#         p_3 = (overall_pattern_number + 0.0)/value
        
        #write_string+="Pattern: "+key+"\t Occurrences: "+str(value)+"\t P(x|Property): "+str(p)+"\n"
#         write_string += key + "\t" + str(value) + "\t" + uri + "\t" + str(math.log(p)) + "\t" + str(math.log(p_prime)) +"  "+ str(math.log(p_3)) +"\n"
        try:
            f_out.write(key + "\t" + str(value) + "\t" + uri +"\n")
        except:
            pass
#             we do not care about entries, which have wired lemmas

    f_out.write(write_string)
    f_out.close()
    return hm, overall_pattern_number























# def create_html_table(lexico_array,hm_res_sentences,path,name,version):
#     """
#     Creates the html file, which makes it easier to look at the pattern and the corresponding sentences and lexicon entries
#     """
#     hilfsliste = {}
#     lexico_array_new = []
#     for item in lexico_array:
#         name1 = str(item[0].split("\n")[0])
#         name1 = name1.replace(" a lemon:LexicalEntry ;","")
#         name1 = name1.replace(":","")
#         
#         if name1 in hilfsliste:
#             pass
#         else:
#             hilfsliste[name1] = ""
#             string0 = ""
#             string1 = ""
#             number = 0
#             hilfsarray = []
#             for i in lexico_array:
#                 try:
#                     name_t = str(i[0].split("\n")[0])
#                     name_t = name_t.replace(" a lemon:LexicalEntry ;","")
#                     name_t = name_t.replace(":","")
#                     
#                     if str(name1) == str(name_t):
#                         string0 += i[0]+"\n\n\n\n"
#                         string1 += i[1]+"\n"
#                         number += int(i[2])
#                         hilfsarray.append(i[1])
#                 except:
#                     pass
#             tmp_array = []
#             tmp_array.append(string0)
#             tmp_array.append(string1)
#             tmp_array.append(number)
#             tmp_array.append(hilfsarray)
#             lexico_array_new.append(tmp_array)
#             
#     web_string = ""
#     counter = 0
#     lexico_array = sort_array(lexico_array_new)
#     web_string += "<TABLE border=\"1\"><TR><TH>#Pattern<TH>Entry"
#     for item in lexico_array:
#         counter += 1
#         if counter < 26:
#             f=file(path+"Result/"+str(version)+name+str(counter),"w")
#             f.write(item[0])
#             f.close()
#             
#             test = item[0].split("\n")[0]
#             test = test.replace("a lemon:LexicalEntry ;","")
#             test = test.replace(":","")
#             
#             f=file(path+"Result/"+str(version)+"P"+name+str(counter),"w")
#             write_string = item[1]
#             write_string += "\n##########################################################\n\n\n"
#             
#             for i in item[3]:
#                 #print i
#                 
#                 ##############################################################
#                 #I changed the pattern with a filter, and if so, the new patterns do not exist in the hm_res_sentences.
#                 #Therefore use try/catch to overgo the new pattern
#                 ##############################################################
#                 try:
#                     write_string += hm_res_sentences[i]+"\n\n"
#                 except:
#                     pass
#                 
#             f.write(write_string)
#             f.close()
#             
#             web_string+="<TR><TH><a href=\""+"Result/"+str(version)+"P"+name+str(counter)+"\">"+str(item[2])+"</a><TD><a href=\""+"Result/"+str(version)+name+str(counter)+"\">"+test+"</a>" #"\">Entry"+str(counter)+ 
#     
#             
#     web_string += "</TABLE>"
#     return web_string