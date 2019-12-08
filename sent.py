
import json
## first download pdf from libgen
## second split pdf with https://smallpdf.com/split-pdf, saving only explanations for each question type
## Third use k2pdfopt application located in downloards to convert 2column pdfs to 1
##  Forth use pdftotext.exe -layout examplepdf.pdf to get a text file of the questions
## Fifth clean the data, look for repeating parts, page headers etc
## finally can use this program to extract question info into models
## next use pymongo to load questions to mongodb

## Then the hard part of creating value with the question bank

## TODO figure out how to create and link pictures of each question to models so
## can use those for actual ui
class SentenceCompQuestionModel:
    def __init__(self, questionNumber = -1, pagenum = -1, bookID = 1):
        self.questionText = ""
        self.questionNumber = questionNumber
        self.answerOptions  = []
        self.correctAnswer = -1
        self.questionTypes = []
        self.explanationText = ""
        self.answerExplanations = []
        self.pagenum = pagenum
        self.bookID = bookID

    def getInfo(self):
        

        print("{}. {}".format(self.questionNumber, self.questionText))
        #print(self.answersToString())
        print(self.answerOptions)
        print(self.correctAnswer)

        
    def getJson(self):
        data = {}
        data["question_number"] = self.questionNumber
        data["question_types"] = self.questionTypes
        #data["formatted_correctly"]= True if (len(self.questionTypes)>0 and len(self.answerExplanations)>0) else False
        data["question_text"] = self.questionText
        data["answer_options"] = self.answerOptions
        data["correct_answer"] = self.correctAnswer
        data["explanation_text"] = self.explanationText
        data["answer_explanations"] = self.answerExplanations
       
        data["page_num"] = self.pagenum
        return data
        #print(data)


      
    

    
    def addAnswer(self, ans, optionnum = 5):
        ans = ans.strip()
        ans = ans.strip("\n")

        if len(ans) !=0:
            if optionnum > len(self.answerOptions)-1:
                self.answerOptions.append(ans)
            else:
                self.answerOptions[optionnum] += " " +ans
    
    
    def addAnswerExplanation(self, ans, optionnum = 5):
        ans = ans.strip()
        ans = ans.strip("\n")

        if len(ans) !=0:
            if optionnum > len(self.answerExplanations)-1:
                self.answerExplanations.append(ans)
            else:
                self.answerExplanations[optionnum] += " " +ans
        
            
    
    def answersToString(self):
        answstring = ""
        #answert = ["(A)", "(B)", "(C)", "(D)", "(E)"]

        for index,ans in enumerate(self.answerOptions):
            #if (index< len(answert)):
            #   answstring += answert[index] + "  "  + ans + "\n"
            answstring += index + " " + ans + "\n"
        return answstring
    



f = open("gmatOfficial2019SenteneCompletionpages94to105and735to813_k2opt.txt", 'rt', encoding="utf-8")

questionTypes = ["Idiom", "Logical Predication", "Agreement", "Parallelism",
"Rhetorical Construction", "Grammatical Construction", "Verb Form", "Diction", "Category",
"Comparison", "Sentence Structure"  ]


questionTypesCheck = "Idiom Logical predication Agreement Parallelism Rhetorical construction Grammatical construction Verb form Diction Category Comparison Sentence structure" 
qnums = [84, 100, 669, 806] # start and end of set 1, then start and end of set 2
pnums = [89, 99,730,807] # start and end of set 1, then start and end of set 2
questionnum = 84
currentpage = 89
questions = []
 # need to change these to enums and switch funct
inQuestion= False
inAnswer = False
inExplanation = False
ansNum = 0
qchoiceNum = 0

answerchoices = ["(A)", "(B)", "(C)", "(D)", "(E)"]
correctanswerchoices = ["A", "B", "C", "D", "E"]

# S

for line in f:
    line = line.strip()
    if line == str(currentpage):

        currentpage+=1
        
        if currentpage == 100:
            currentpage = 730
        #print("Current page:  " + str(currentpage))
        pass
    elif line[0:2]== "SC":
        # header text, want to omit those lines
        pass

    ## Question
    elif line[0:len(str(questionnum))+1] == "{}.".format(questionnum) and not inQuestion:
        #print("Question Num:  " + str(questionnum))
        ## initilize new question
        ## add 
        #print(line)
        inQuestion = True
        inAnswer = False
        c = SentenceCompQuestionModel(questionnum, currentpage)
        questions.append(c)
        questions[-1].questionText += line[len(str(questionnum))+2:].strip() + " "
        pass
    
    elif inQuestion:
        if "(A)"  ==  line[0:3]:
            #print("Ans A  " + line)
            # in answer section
            questions[-1].addAnswer(line.strip()[3:], ansNum)
            inQuestion = False
            inAnswer = True
            ansNum = 0
            qchoiceNum = 0
            pass   
        else:
            # Still in question
            try:
                questions[-1].questionText += line.strip() + " "
                pass
            except:
                pass
        pass
    elif inAnswer:
        # if on the last answer check if in the explanation yet
        if ansNum+1 == len(answerchoices):
            
            try:
                qtypes = line.split(";")
                if questionTypes.index(qtypes[0].capitalize()) != -1:
                    #print(qtypes)
                    questions[-1].questionTypes = qtypes
                    inAnswer = False
                    inExplanation= True
                pass
            except:
                pass
            pass
        elif answerchoices[ansNum+1] in line:
            # next answer choice
            ansNum +=1
            questions[-1].addAnswer(line.strip()[3:], ansNum)
        elif inAnswer:
            #print(line)
            questions[-1].addAnswer(line.strip(), ansNum)
        pass
    elif inExplanation:
        if qchoiceNum < len(correctanswerchoices) and line[0:1] == correctanswerchoices[qchoiceNum]:
            #print("Answe:  " + line)
            line = line[1:].strip()
            qchoiceNum+=1
        try:
            if qchoiceNum == 0:
                #print("Exp text  " + line)
                questions[-1].explanationText += line.strip() + " "
            else:
                questions[-1].addAnswerExplanation(line, qchoiceNum-1)
            pass
        except:
            pass
    if ("The correct answer is" in line):
        #print(correctanswerchoices.index(line[-2]))
        questions[-1].correctAnswer = correctanswerchoices.index(line[-2])

        questionnum +=1
        #print(questionnum)
        if questionnum == 101:
            questionnum = 669
        qchoiceNum = 0
        inExplanation= False
        pass
    # The only other scenario should be you are in the answer explanation part.. if the txt is clean
    

    


print(len(questions))
data = {}
data["sentence_comprehension"]=[]
for q in questions:
    #q.getInfo()
    if(len(q.questionTypes)>0 and len(q.answerExplanations)>0):
        data["sentence_comprehension"].append(q.getJson())
    
    

with open('sdata.json', 'w') as outfile:  
    json.dump(data, outfile)