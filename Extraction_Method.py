from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import spacy
nlp = spacy.load("en_core_web_md")
from spacy.symbols import dobj
from spacy.matcher import Matcher
from pprint import pprint
from spacy.matcher import DependencyMatcher
from spacy import displacy



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

#initialising the matcher with shared vocab
matcher = Matcher(nlp.vocab)
matcher2 = DependencyMatcher(nlp.vocab)

SearchText = []
# Query to obtain links
query = 'my goal is to'
# SearchText = [] # Initiate empty list to capture final results# Specify number of pages on google search, each page contains 10 #links
n_pages = 15
for page in range(1, n_pages):
    url = "http://www.google.com/search?q=" + query + "&start=" + str((page - 1) * 10)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    search = soup.find_all('div', class_="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc")
    # extracting the text content from each class where description is
    for h in search:
        SearchText.append(h.text)


GoalsDataFrame = pd.DataFrame({"Text":SearchText}, dtype= str)

#Writing pattern for finding what comes after "my goal is to"
VerbNoun = [{"LOWER": 'my'},{"LEMMA": 'goal'},{"LOWER": "is"},{"LOWER": "to"},{"POS":"VERB"},{"POS": "NOUN"},{"POS": "PROPN", "OP": "?"}]
VerbProun = [{"LOWER": 'my'},{"LEMMA": 'goal'},{"LOWER": "is"},{"LOWER": "to"},{"POS":"VERB"},{"POS": "PROPN"}]
# VerbSubj = [{"LOWER": 'my'},{"LOWER": 'goal'},{"LOWER": "is"},{"LOWER": "to"},{"POS":"VERB"},{"Dep": "nsubj"}]
# VerbObj = [{"LOWER": 'my'},{"LOWER": 'goal'},{"LOWER": "is"},{"LOWER": "to"},{"POS":"VERB"},{"Dep": "dobj"}]
pattern = [
    {
        "RIGHT_ID": "anchor_to",
        "RIGHT_ATTRS": {"ORTH": "to"}
    },
    {
        "LEFT_ID": "anchor_to",
        "REL_OP": ">",
        "RIGHT_ID": "founded_verb",
        "RIGHT_ATTRS": {"POS": "VERB"},
    },
    {
        "LEFT_ID": "founded_verb",
        "REL_OP": ">",
        "RIGHT_ID": "founded_noun",
        "RIGHT_ATTRS": {"POS": "NOUN"},
    },
    {
        "LEFT_ID": "founded_verb",
        "REL_OP": ">",
        "RIGHT_ID": "founded_subject",
        "RIGHT_ATTRS":{"DEP": "nsubj"},
    },
    {
        "LEFT_ID": "founded_verb",
        "REL_OP": ">",
        "RIGHT_ID": "to_object",
        "RIGHT_ATTRS": {"DEP": "dobj"},
    },
    {
        "LEFT_ID": "to_object",
        "REL_OP": ">",
        "RIGHT_ID": "founded_object_modifier",
        "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "compound"]}},
    }
]
pattern2 = [
    {
        "RIGHT_ID": "anchor_goal",
        "RIGHT_ATTRS": {"ORTH": "goal"}
    },
    {
        "LEFT_ID": "anchor_goal",
        "REL_OP": ">",
        "RIGHT_ID": "to_subject",
        "RIGHT_ATTRS": {"POS": "VERB"},
    },
    {
        "LEFT_ID": "to_subject",
        "REL_OP": ">",
        "RIGHT_ID": "to_object",
        "RIGHT_ATTRS": {"DEP": "dobj"},
    },
    {
        "LEFT_ID": "to_object",
        "REL_OP": ">",
        "RIGHT_ID": "founded_object_modifier",
        "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "compound"]}},
    }
]
# if possible_subject.dep == dobj and possible_subject.head.pos_ == "VERB":

#Adding pattern to the matcher
matcher.add("MyGoalIsto",[VerbNoun,VerbProun])
matcher2.add("Pattern", [pattern, pattern2])

My_Goal_Is_To = []
for text in GoalsDataFrame["Text"]:
    doc = nlp(text)
    matches = matcher(doc)
    matches2 = matcher2(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        My_Goal_Is_To.append(span.text)
    for start, end in matches2:
        span2 = doc[start:end]
        My_Goal_Is_To.append(span2.text)

print(My_Goal_Is_To)

Goals_List = []

def Goals_Extraction(Text, List):
 for doc in Text.apply(nlp):
         for possible_subject in doc:
             #Removing stop words within the pipeline
            if possible_subject.is_stop == False and possible_subject.is_digit == False:
                #Finding pairs of words with head verb and its child
                if possible_subject.dep == dobj and possible_subject.head.pos_ == "VERB":
                    List.append([doc.text, [possible_subject.head.text, possible_subject.text]])


Goals_Extraction(GoalsDataFrame["Text"], Goals_List)

Goals_ExtractedDF = pd.DataFrame(Goals_List, columns=("Sentence", "Goal Pair"))

print(Goals_ExtractedDF)



assert "MyGoalIsto" in matcher
#
# i = 0
# for doc in GoalsDataFrame["Text"].apply(nlp):
#     docnumber = i + 1
#     matches = matcher(doc)
#
#
# for doc in GoalsDataFrame["Text"].apply(nlp):
#    for docrow in doc:
#     matches = matcher(doc)
#     for match_id, start, end in matches:
#         print("Match found:", doc[start:end].text)

        # # Write a pattern for full iOS versions ("iOS 7", "iOS 11", "iOS 10")
        # pattern = [{'TEXT': "iOS"}, {'IS_DIGIT': True}]
        #
        # # Add the pattern to the matcher and apply the matcher to the doc
        # matcher.add('IOS_VERSION_PATTERN', None, pattern)
        # matches = matcher(doc)
        # print('Total matches found:', len(matches))
        #
        # # Iterate over the matches and print the span text
        # for match_id, start, end in matches:
        #     print('Match found:', doc[start:end].text)



