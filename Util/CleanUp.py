def clean_x_y(x,y):
    x = clean_string(x)
    y = clean_string(y)
    return x , y

def clean_string(token):
    if "\xe2" in token: 

        token = ""
    if "\xc3" in token:

        token = ""
    token = token.replace(" .", " ")
    token = token.replace("&", " ")
    token = token.replace("\" ", " ")
    token = token.replace("[", " ")
    token = token.replace("]", " ") #token=token.replace("-", "")
    token = token.replace("(", " ")
    token = token.replace(")", " ")
    token = token.replace("_", " ")
    token = token.replace("&#39;", " ")
    token = token.replace("&quot;", " ")
    token = token.replace(":", " ")
    token = token.replace("!", " ") #token=token.replace(".", "")
    token = token.replace(":", " ")
    token = token.replace("+", " ") #token=token.replace("-", "")
    token = token.replace("^", " ")
    token = token.replace("_", " ") #token=token.replace(".", "")
    token = token.replace("'", " ")
    token = token.replace("~", " ")
    token = token.replace("*", " ")
    token = token.replace("?", " ")
    token = token.replace(",", " ")
    token = token.replace(";", " ")
    token = token.replace("'", " ")
    token = token.replace("}", " ")
    token = token.replace("{", " ")
    token = token.replace("&#x95", "")
    
    while "  " in token:
        token = token.replace("  "," ")
    if len(token)>1:
        if token[len(token)-1:]==" ":
            token = token[:len(token)-1]
    return token
