def return_wiktionary_emtries(label):
    f = open("/home/swalter/Development/Wiktionary.tsv","r")
    
    array = []
    for item in f:
        item = item.replace("\n","")
        if label.lower() in item.lower() and "english" in item.lower():
            if " " in item:
                begrif = item.split("\t")[1]
                array.append(begrif)
                
    f.close()

    return array


def return_wiktionary_entries_hm(array):
    f = open("/home/swalter/Development/Wiktionary.tsv","r")
    print "imported Wiktionary"
    hm = {}
    for label in array:
        for item in f:
            item = item.replace("\n","")
            if "["+label.lower()+"]" in item.lower() and "english" in item.lower():
                if " " in item:
                    #print "line: "+ item
                    begrif = item.split("\t")[1]
                    hm[begrif]=""
                    #print "item: "+begrif
                
    f.close()
    print "returns wiktionary entries"
    #print "Label: "+label
    #raw_input("Lines")
    return hm


def return_wiktionary_entries_hm_given(array,wiki, saved_wiki_entries):
    print "imported Wiktionary"
    outtakes = {"from","and","me","are","is","before","after","on","can","have","here","to","while","you","like","with","where","has","i","the","that","or","please", "which", "one","two","three","four", "five", "six", "seven", "eight", "nine", "what", "after"}
    lower = str.lower
    hm = {}
    array = [item for item in array if item not in outtakes and len(item)>2]
    print "array "+str(array)
    
    for label in array:
        if label in saved_wiki_entries:
            if " " in saved_wiki_entries[label]:
                for item in saved_wiki_entries[label].split(" "):
                    hm[item]=""
            else:
                hm[saved_wiki_entries[label]] = ""
        else:
            for item in wiki:
            
            #TODO that need way to much time, because always the whole wiki is iteritemend.. maybe only add lines to wiki, if english is part of the line?!
                if "["+lower(label)+"]" in lower(item) and "english" in lower(item):
                    if " " in item:
                        #print "line: "+ item
                        a = item.split("\t")[1]
                        hm[a]=""
                        if label in saved_wiki_entries:
                            saved_wiki_entries[label] = saved_wiki_entries[label]+" "+a
                        else:
                            saved_wiki_entries[label]=a

    print "returns wiktionary entries"
    return saved_wiki_entries, hm