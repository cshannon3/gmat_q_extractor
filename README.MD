

## first download pdf 
## second split pdf with https://smallpdf.com/split-pdf, saving only explanations for each question type
## Third use k2pdfopt application located in downloards to convert 2column pdfs to 1
##  Forth use pdftotext.exe -layout examplepdf.pdf to get a text file of the questions
## Fifth clean the data, look for repeating parts, page headers etc
## finally can use this program to extract question info into models
## next use pymongo to load questions to mongodb or save as json
