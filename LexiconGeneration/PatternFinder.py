tmp_number = None





def find_pattern_between_x_and_y(x,y,parsed_sentence):
    #######Always Fast, if the normal algorithm should be used!!!!!!#######
    baseline = False
    ######################################################################
    x_original = x
    y_original = y
    x = x.replace(" ","")
    y = y.replace(" ","")
    number_x = 0
    dep_x = 0
    number_y = 0
    dep_y = 0

    foundx = False
    foundy = False
    for item in parsed_sentence:
        if x.lower() in item.__getattr__("pos1").lower():
            number_x = int(item.__getattr__("pos0"))
            dep_x = int(item.__getattr__("pos6"))
            foundx = True
        if y.lower() in item.__getattr__("pos1").lower():
            number_y = int(item.__getattr__("pos0"))
            dep_y = int(item.__getattr__("pos6"))
            foundy = True
            
    if foundy == False and y_original.contains(" "):
        for item in parsed_sentence:
            for item1 in y_original.split(" "):
                if item1.lower() == item.__getattr__("pos1").lower():
                    number_y = int(item.__getattr__("pos0"))
                    dep_y = int(item.__getattr__("pos6"))
                    y = item1
                    break
                
                
    if foundx == False and x_original.contains(" "):
        for item in parsed_sentence:
            for item1 in x_original.split(" "):
                if item1.lower() ==  item.__getattr__("pos1").lower():
                    number_x = int(item.__getattr__("pos0"))
                    dep_x = int(item.__getattr__("pos6"))
                    x = item1
                    break
    
    
    if number_x < number_y:
       
        if baseline:
            print"###############################"
            print"###############################"
            print "Baseline activated"
            print"###############################"
            print"###############################"
            print
            return create_pattern(x,y,parsed_sentence[number_x-1:number_y-1])
        else:
            return pathfinding(x,dep_x,y,dep_y,parsed_sentence)         
        
    elif number_y < number_x :
        if baseline:
            print"###############################"
            print"###############################"
            print "Baseline activated"
            print"###############################"
            print"###############################"
            print
            return create_pattern(x,y,parsed_sentence[number_y-1:number_x-1])
        else:
            return  pathfinding(y,dep_y,x,dep_x,parsed_sentence)
    


            
            
def pathfinding(x,dep_x,y,dep_y,parsed_sentence):
    #y and y_dep are the ones, which occur first in the sentence
    
    #There could be the case, that x and y are direct connected through one other word
    
    if dep_x == dep_y:
        result = []
        position_x = 0
        position_y = 0
        position_counter = 1
        
        for item in parsed_sentence:
            position_counter += 1
            if x.lower() == str(item.__getattr__("pos1")).lower():
                result.append(item)
                position_x = position_counter
            elif y.lower() == str(item.__getattr__("pos1")).lower():
                result.append(item)
                position_y = position_counter
            elif str(dep_x) == str(item.__getattr__("pos0")):
                result.append(item)
                
        if position_y < position_x:
            result = result[::-1]
    
        return create_pattern(x,y,result)
    
    
    
    
    #from end of sentence to begin of sentence
    result = []
    cancel_counter = 20        
    start_nummer = dep_y
    
    
    global tmp_number
    tmp_number = start_nummer
    item_list_end_begin = []
    generated_final_string = ""
    for i in range(0,cancel_counter):
        if x.lower() == generated_final_string:
            pass
        else:
            go_on = True
            for item in parsed_sentence:
                if str(tmp_number) == str(item.__getattr__("pos0")) and go_on == True:
                    #global tmp_number
                    tmp_number = str(item.__getattr__("pos6"))
                    generated_final_string = str(item.__getattr__("pos1").lower())
                    item_list_end_begin.append(item)
                    go_on = False
               
    for item in parsed_sentence:
        if str(item.__getattr__("pos1")).lower() == y.lower():
            item_list_end_begin = [item]+item_list_end_begin
            break
                    
    #from begin of sentence to end
    start_nummer = dep_x
    
    #global tmp_number
    tmp_number = start_nummer
    
    generated_final_string = ""
    item_list_begin_end = []
    for i in range(0,cancel_counter):
        if y.lower() == generated_final_string:
            pass
        else:
            go_on = True
            for item in parsed_sentence:
                if str(tmp_number) == str(item.__getattr__("pos0")) and go_on == True:
                    #global tmp_number
                    tmp_number = str(item.__getattr__("pos6"))
                    generated_final_string = str(item.__getattr__("pos1").lower())
                    item_list_begin_end.append(item)
                    go_on = False
                    
    for item in parsed_sentence:
        if str(item.__getattr__("pos1")).lower() == x.lower():
            item_list_begin_end = [item]+item_list_begin_end
            break
                    
    #merge item_list_begin_end and item_list_end_begin    
    #two cases
    
    
    #First Case: There is a direct path between x and y, then return this path 
    for item_list in [item_list_end_begin,item_list_begin_end]:
        found_x = False
        found_y = False
        position_x = 0
        position_y = 0
        position_counter = 1
        for item in item_list:
            if str(item.__getattr__("pos1").lower())==x.lower():
                found_x = True
                position_x = position_counter
            elif str(item.__getattr__("pos1").lower())==y.lower():
                found_y = True
                position_y = position_counter
                
            position_counter += 1
                
        if found_x == True and found_y == True:
            
            #rotaed always in a way, that x is first
            if position_y < position_x:
                item_list = item_list[::-1]
    
            return create_pattern(x,y,item_list)
    
    
    #If First case did not return, we are automatically in this case
    #Second Case: No direct path, have to merge path from both existing pathes
    
    int_end_begin = 0
    int_begin_end = 0
    go_on = True
    for positiona, item1 in enumerate(item_list_end_begin):
        for positionb, item2 in enumerate(item_list_begin_end):
            if str(item1.__getattr__("pos1").lower()) == str(item2.__getattr__("pos1").lower()):
                #+1, because otherwise, the element which is equal would not be used in the pattern, so it is enaugh, if ONE has the add to one
                int_end_begin = positiona+1
                int_begin_end = positionb
                go_on = False
                break
        if go_on == False:
            break

    #original
    new_a = item_list_end_begin[:int_end_begin]
    new_b = item_list_begin_end[:int_begin_end]

    

    result = new_a + new_b
    result = result[::-1]
    
    
    
    return create_pattern(x,y,result)



    
def create_pattern(x,y,item_list):
    #constrain one and two
    #if len(item_list)<3 or len(item_list) > 8:
    if len(item_list)<3 or len(item_list) > 10:
        return None
    
    pattern = ""
    number_counter = 0
    
    #constraint 4, dont allow a pattern with lenght three and only a prep between x and y
    if len(item_list) == 3:
        
        if item_list[1].__getattr__("pos7").lower() == "prep":
            return None
        if item_list[1].__getattr__("pos3").lower() == "cd":
            return None
        if "num" in item_list[1].__getattr__("pos7").lower():
            return None
        
        ####for Test######
        if item_list[1].__getattr__("pos3").lower() == "nn":
            return None
        #################
        
#        if item_list[1].__getattr__("pos7").lower() == "number":
#            return None
#        if item_list[1].__getattr__("pos7").lower() == "num":
#            return None


        #constraint 5: same if there is only a to between x and y or an in
        #print item_list[1].__getattr__("pos4")
        if item_list[1].__getattr__("pos4").lower() == "in" or item_list[1].__getattr__("pos4").lower() == "to":
            return None
    
    #constraint 6: dont allow such pattern: 0 x _ nnp nnp _ 1 pobj _ _  1 from _ in in _ 2 prep _ _  2 to _ to to _ 3 dep _ _  3 y _ nnp nnp _ 4 pobj _ _  4
    if len(item_list) == 4:
        if item_list[1].__getattr__("pos4").lower() == "in" and item_list[2].__getattr__("pos4").lower() == "to":
            return None
        if item_list[1].__getattr__("pos4").lower() == "in" and item_list[2].__getattr__("pos4").lower() == "in":
            return None
        if item_list[1].__getattr__("pos4").lower() == "to" and item_list[2].__getattr__("pos4").lower() == "in":
            return None
        if item_list[1].__getattr__("pos7").lower() == "tmod" and "num" in item_list[2].__getattr__("pos7").lower():
            return None
        if item_list[1].__getattr__("pos3").lower() == "nnp" and "num" in item_list[2].__getattr__("pos7").lower():
            return None
        ####for Test######
        if item_list[1].__getattr__("pos3").lower() == "nn" and item_list[2].__getattr__("pos3").lower() == "nn":
            return None
        if item_list[1].__getattr__("pos3").lower() == "cc" and item_list[2].__getattr__("pos3").lower() == "nn":
            return None
        if item_list[1].__getattr__("pos3").lower() == "nn" and item_list[2].__getattr__("pos3").lower() == "cc":
            return None
        #################
       
    
    for item in item_list:
        pattern += item.__return_as_string__()+"  "
        number1 = str(item.__getattr__("pos0"))
        number2 = str(item.__getattr__("pos6"))
        pattern = pattern.replace(number1+" ",str(number_counter)+" ")
        pattern = pattern.replace(number2+" ",str(number_counter+1)+" ")
        number_counter+=1
        #constraint 3 if x or why are parsed as nn, return none
        if item.__getattr__("pos1").lower() == x.lower() and item.__getattr__("pos7").lower() == "nn":
            return None
        if item.__getattr__("pos1").lower() == y.lower() and item.__getattr__("pos7").lower() == "nn":
            return None

    

    if pattern.endswith("  "):
        pattern = pattern[:-2]
    
    pattern = pattern.lower()
    pattern__new = ""
    for p in pattern.split("  "):
        counter = 0
        new_string = ""
        for p1 in p.split(" "):
            if counter == 1:
                p1 = p1.replace(x.lower(),"x")
                p1 = p1.replace(y.lower(),"y")
                new_string+=p1+" "
            else:
                new_string += p1 +" "
            counter +=1
        if new_string.endswith(" "):
            new_string = new_string[:-1]
        
        pattern__new += new_string+"  "
    if pattern__new.endswith("  "):
        pattern__new = pattern__new[:-2]
    #print "pattern: "+pattern
    #print "pattern: "+pattern__new
    
    if pattern__new.count(" x ") != 1 or pattern__new.count(" y ") != 1 or "0 " not in pattern__new:
        return None
    #if " x " not in pattern__new or " y " not in pattern__new or "0 " not in pattern__new:
        #return None
    
    return pattern__new