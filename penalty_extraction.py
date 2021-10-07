import spacy 
nlp = spacy.load('en_core_web_lg')
def convertToDollar(text):
    """
    Convert Rs to USD as Spacy does not recognize Indian Currency that well
    Input: Text
    Output: Text where units of currency are converted from INR to $
    """
    text = text.replace("Rs.","$")
    text = text.replace("Rs","$")   
    text = text.replace("Rupees","$")    
    text = text.replace("Rupee","$")
    text = text.replace("rupees","$")
    text = text.replace("rupee","$")
    text = text.replace("rs.","$")
    text = text.replace("rs","$")
    text = text.replace("₹","$")
    return text 


def extractPenaltyAmount(text):
    """
    Extract all the monetray information present in the casefile
    Input: CaseFile Text (Preferably the penalty tagged text)
    Output: List of penalty information
    Output can contain numerals, words, currency units as well as associated punctuation and other non monetary numerals
    suc
    """
    text = convertToDollar(text)
    doc = nlp(text)
    money = []
    qFlag = False
    quantity = []
    for i in doc:
        if str(i) == "penalty":
            qFlag = True
        
        if i.ent_type_ == "QUANTITY" or i.ent_type_ == "CARDINAL":
            quantity.append(i)
        
            
        if i.ent_type_ == "MONEY":
            if qFlag:
                if quantity:
                    for j in quantity:
                        money.append(j)
                qFlag = False
                quantity = []
            if str(i) == '$':
                continue
            money.append(i)
    return money

def getCleanPenalty(text):
    """
    Function to extract the penalty levied on a given case file 
    Input: CaseFile Text (Preferably the penalty tagged text)
    Output:Penalty Amount
    """
    penalty = extractPenaltyAmount(text)
    penalty = [str(i) for i in penalty]
    penalty = [''.join([i for i in j if i.isalnum()]) for j in penalty]
    penalty_num = 0
    penalty_index = 0
    for j,i in enumerate(penalty):
        if i.isnumeric():
            penalty_num = i
            penalty_index = j 
    if penalty_index < len(penalty) -1:
        return penalty_num
    return 0



penalty = getCleanPenalty(data)

print("Penalty is:",penalty)