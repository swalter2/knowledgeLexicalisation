import glob, re
from nltk.tokenize import sent_tokenize

key = None
value = None
path_to_extracted_wiki_files = "..../extracted/"
sentence_output_path = ".../list_of_sentences"
path_keystore = "../keystore_out"
listOfPathes = []
listOfPathes.extend(glob.glob(path+"*/wiki_*"))
number = 0
key_store = {}
anzahl_saetze = 0
f_out = open(sentence_output_path,"w")
counter = 0
for path_to_file in listOfPathes:
    f_in = open(path_to_file,"r")
    text = ""
    counter += 1
    for line in f_in:
        if line.startswith("<doc "):
            matchObj = re.match( r'<doc id=\"([0-9]*).*title=\"(.*)\">.*', line, re.M|re.I)
            if matchObj:
                number += 1
                key =  matchObj.group(1)
                value = matchObj.group(2)
                key_store[key]=value
                
        elif line.startswith("</doc>"):
            if key != None:
                text = text.replace("\n"," ")
                sentence_array = sent_tokenize(text)
                text = ""
                for sentence in sentence_array:
                    if " " in sentence:
                        if len(sentence.split(" "))>3:
                            anzahl_saetze += 1
                            f_out.write(sentence+"\t"+key+"\n")
                key = None
                value = None
        else:
            if line != "\n":
                text += line
    print str(counter)+"/"+str(len(listOfPathes))
    f_out.flush()
    f_in.close()
    
f_out.close()  
print len(key_store)
print "number of sentences: "+str(anzahl_saetze)

f_out = open(path_keystore,"w")
for key,value in key_store.iteritems():
    f_out.write(key+"\t"+value+"\n")
f_out.close()
