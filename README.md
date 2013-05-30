knowledgeLexicalisation
=======================

tool to create lemon lexicons out of natural language sentences, using a top-down or bottom-up approach



For the programm an english wikipedia corpus, index with pylucene 3.5 is needed.
This corpus/index can be (already prepared) found here:

https://www.dropbox.com/sh/ea2ivzmn9y1fs7m/8C944h2bzp

You also find in this folder a second Index, which contains many sentences, related to the lexicalization campain of QALD3(www.sc.cit-ec.uni-bielefeld.de/qald).
This sentences are already parsed with the pretrained MaltParser(http://www.maltparser.org/)

As I am currently in the process to adapt this project to German and Spanish, of course one would need a German ans Spanish corpora as well.
All will be provieded in the above Dropox link soon.




Dependencies:
====================

For this project you need the German ParZu parser (https://github.com/rsennrich/parzu) and also the TreeTagger (http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/).
Please do not forget to set the correct path to the german.par in TreeTagger in the ParZu folder under preprocessor/treetagger-wrapper.py 
