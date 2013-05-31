import ConfigParser, Sparql
import LexiconGenerator

def getLabel(uri,en_de_lexicon):
    config = ConfigParser.ConfigParser()
    config.read('config.conf')
    sparql=Sparql.Connection()
    label = sparql.getLabel(uri)[0]
    if "(" in label:
        label = label.split("(")[0]
    if label.endswith(" "):
        label = label[:-1]
        
    if config.get('system_language', 'language') == "English":
        return [label]
    elif config.get('system_language', 'language') == "German":
        if label.lower() in en_de_lexicon:
            label_array = en_de_lexicon[label]
            return label_array
        else:
            return [label]
        
def createEntries(uri,en_de_lexicon):
    label_array = getLabel(uri,en_de_lexicon)
    lemonEntries = []
    try:
        for label in label_array:
            entry = LexiconGenerator.NounPPFrame(label, uri, {})
            lemonEntries.append(entry)
            entry = LexiconGenerator.NounPossisiveFrameWithoutMarker(label, uri)
            lemonEntries.append(entry)
            entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
            lemonEntries.append(entry)
            entry = LexiconGenerator.TransitiveFrame(label, uri, {})
            lemonEntries.append(entry)
    except:
        pass
    return lemonEntries