
import json

class QuestionModel:
    def __init__(self, questionNumber = -1, pagenum = -1, bookID = 0):
        self.questionText = ""
        self.questionNumber = questionNumber
        self.answerOptions  = []
        self.questionOptions = []
        self.correctAnswer = -1
        self.questionType = ""
        self.questionSubtypes = []
        self.answerExplanation = ""
        self.pagenum = pagenum
        self.bookID = bookID

    def getInfo(self):
        

        print("{}. {}".format(self.questionNumber, self.questionText))
        #print(self.answersToString())
        print(self.answerOptions)
        print(self.correctAnswer)
        print(self.questionType)
        print(self.questionSubtypes)
        
    def getJson(self):
        data = {}
        data["question_number"] = self.questionNumber
        data["question_type"] = self.questionType
        data["question_subtypes"] = self.questionSubtypes
        data["question_text"] = self.questionText
        data["answer_options"] = self.answerOptions
        data["correct_answer"] = self.correctAnswer
        data["explanation_text"] = self.answerExplanation
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
    
    
    def addQuestionChoice(self, ans, optionnum = 5):
        ans = ans.strip()
        ans = ans.strip("\n")

        if len(ans) !=0:
            if optionnum > len(self.questionOptions)-1:
                self.questionOptions.append(ans)
            else:
                self.questionOptions[optionnum] += " " +ans
        
            
    
    def answersToString(self):
        answstring = ""
        #answert = ["(A)", "(B)", "(C)", "(D)", "(E)"]
        for index,ans in enumerate(self.questionOptions):
            answstring += index + " " + ans + "\n"
            
        for index,ans in enumerate(self.answerOptions):
            #if (index< len(answert)):
            #   answstring += answert[index] + "  "  + ans + "\n"
            answstring += index + " " + ans + "\n"
        return answstring



f = open("quantitativeReview2018ProblemSolvingpages91to150_k2opt.txt", 'rt', encoding="utf-8")
#f = open("quantitativeReview2018Wileypages91to150_k2opt.txt", 'rt', encoding="utf-8")
questionTypes = ["Arithmetic", "Geometry", "Algebra"]
questionnum = 1
currentpage = 88
questions = []
 # need to change these to enums and switch funct
inQuestion= False
inAnswer = False
inQuestionChoice = False
inExplanation = False
ansNum = 0
qchoiceNum = 0

answerchoices = ["(A)", "(B)", "(C)", "(D)", "(E)"]
correctanswerchoices = ["A.", "B.", "C.", "D.", "E."]
questionchoices = ["I.", "II.", "III."]

for line in f:
    line = line.strip()

    if line == str(currentpage):
        currentpage+=1
        pass
    elif line[0:len(str(questionnum))+1] == "{}.".format(questionnum) and not inQuestion:
        ## initilize new question
        ## add 
        #print(line)
        inQuestion = True
        inAnswer = False
        c = QuestionModel(questionnum, currentpage)
        questions.append(c)
        questions[-1].questionText += line[len(str(questionnum))+2:].strip() + " "
        pass
    
    elif inQuestion:
        if "(A)" in line:
            # in answer section
            #questions[-1].addAnswer(line.strip()[3:], ansNum)
            inQuestion = False
            inQuestionChoice = False
            inAnswer = True
            ansNum = 0
            qchoiceNum = 0
            pass
        elif inQuestionChoice:
            if qchoiceNum+1 < len(questionchoices) and questionchoices[qchoiceNum+1] in line:
            # next ques choice
                qchoiceNum +=1
                questions[-1].addQuestionChoice(line.strip()[len(questionchoices[qchoiceNum]):], qchoiceNum)
            else:
                questions[-1].addQuestionChoice(line, qchoiceNum)
        
            
        elif line[0:2]== "I.":
            questions[-1].addQuestionChoice(line.strip()[2:], qchoiceNum)
            inQuestionChoice = True
            qchoiceNum = 0

            
        else:
            # Still in question
            try:
                questions[-1].questionText += line.strip() + " "
                pass
            except:
                pass
        pass
            
        

    if inAnswer:
        # if on the last answer check if in the explanation yet
        if ansNum+1 == len(answerchoices):
            for qtype in questionTypes:
                if qtype in line:
                    questions[-1].questionType = qtype
                    questions[-1].questionSubtypes = line[len(qtype)+1:].split(";")
                    inAnswer = False
                    inExplanation= True

        elif answerchoices[ansNum+1] in line:
            # next answer choice
            ansNum +=1
        if inAnswer:
            questions[-1].addAnswer(line.strip()[3:], ansNum)
        pass
    elif inExplanation:
        try:
            questions[-1].answerExplanation += line.strip() + " "
            pass
        except:
            pass
    if ("The correct answer is" in line):
        #print(line[-2])
        questions[-1].correctAnswer = correctanswerchoices.index(line[-2:])
        questionnum +=1
        inExplanation= False
        pass
    # The only other scenario should be you are in the answer explanation part.. if the txt is clean
    # else:
    #     try:
    #         questions[-1].answerExplanation += line.strip() + " "
    #         pass
    #     except:
    #         pass

    


print(len(questions))
data = {}
data["problem_solving"]=[]
for q in questions:
    #q.getInfo()
    data["problem_solving"].append(q.getJson())

with open('probsolv.json', 'w') as outfile:  
    json.dump(data, outfile)