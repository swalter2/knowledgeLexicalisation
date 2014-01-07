knowledgeLexicalisation
=======================

tool to create lemon lexicons out of natural language sentences, using a top-down or bottom-up approach


Information
=======================
This README is not up-to-date and will be corrected very soon.
Sorry for the delay.





knowledgeLexicalisation -old
=======================


For this system an English Wikipedia corpus, indexed with pylucene 3.5 is needed.
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

In order to use the MaltParser for Spanish, you have to integrate the pretrained spansih .mco file, which can be downloaded from the INSTITUT UNIVERSITARI DE LINGÜÍSTICA APLICADA
UNIVERSITAT POMPEU FABRA  http://www.iula.upf.edu/recurs01_mpars_uk.htm


Additional informations:
====================

Important to mention is, that the Dropbox link above does not always contain the up-to-date pylucene index, so in case you want to use this system and there is a problem with the index, contact me (swalter at techfak dot uni minus bielefeld dot de) and I will check the version of the index, stored in Dropbox.

In the moment two major changes are ongoing. First using MaltParser not only for English, but also for German. The second change is related to the index in order to improve the sentence selection to avoid noise.
