from datetime import datetime
import urllib.request
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import ssl
import os

os.chdir('/Users/martinmurzenkov/OSSU_Computer_Science/Intro_CS/Introduction_to_Computer_Science/11_Understanding_Program_Efficiency_P2')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def normalize_line(text:str) -> str : # Returns word+space line of lowercase characters
    output = list()
    text = text.lower()
    is_last_char = False
    for char in text :
        ascii_val = ord(char)
        if 97 <= ascii_val <= 122 :
            output.append(char)
            is_last_char = True
        else :
            if is_last_char :
                output.append(' ')
                is_last_char = False
    
    return ''.join(output)    

class NewsStory(object) :
    def __init__(self, guid:str, title:str, description:str, link:str, pubdate:str) -> None:
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = datetime.strptime(pubdate, '%a, %d %b %Y %H:%M:%S')
    def get_guid(self) :
        return self.guid
    def get_title(self) :
        return self.title
    def get_description(self) :
        return self.description
    def get_link(self) :
        return self.link
    def get_pubdate(self) :
        return self.pubdate

def process(url:str) -> list[NewsStory] : 
    output = list()
    data = urllib.request.urlopen(url, context=ctx).read().decode()
    tree = ET.fromstring(data)
    items = tree.findall('channel/item')
    for item in items :
        title = item.find('title').text
        link = item.find('link').text
        guid = item.find('guid').text
        pubdate = item.find('pubDate').text[:-4]
        description_unsorted = item.find('description').text
        soup = BeautifulSoup(description_unsorted, 'html.parser')
        description_sorted = soup.get_text('\n')
        output.append(NewsStory(guid, title, description_sorted, link, pubdate))
    return output

class Trigger(object):
    def evaluate(self, story: NewsStory) -> bool :
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError
    
class PhraseTrigger(Trigger) :
    def __init__(self, phrase:str) -> None:
        self.phrase = phrase
    def is_phrase_in(self, text:str) -> bool :
        return normalize_line(self.phrase) in normalize_line(text)
    
class TitleTrigger(PhraseTrigger) :
    def evaluate(self, story: NewsStory) -> bool :
        return PhraseTrigger.is_phrase_in(self, story.get_title())
    def __str__(self):
        return 'TitleTrigger(' + self.phrase + ')'

class DescriptionTrigger(PhraseTrigger) :
    def evaluate(self, story: NewsStory) -> bool :
        return PhraseTrigger.is_phrase_in(self, story.get_description())
    def __str__(self):
        return 'DescriptionTrigger(' + self.phrase + ')'
    
class TimeTrigger(Trigger) : # Should be ETS
    def __init__(self, time:str) -> None:
        self.time = datetime.strptime(time, '%d %b %Y %H:%M:%S')

class BeforeTrigger(TimeTrigger) :
    def evaluate(self, story: NewsStory) -> bool:
        return self.time > story.get_pubdate
    def __str__(self):
        return 'BeforeTrigger(' + self.time.__str__() + ')'
    
class AfterTrigger(TimeTrigger) :
    def evaluate(self, story: NewsStory) -> bool:
        return self.time < story.get_pubdate()
    def __str__(self):
        return 'AfterTrigger(' + self.time.__str__() + ')'

class NotTrigger(Trigger) :
    def __init__(self, trigger:Trigger) -> None :
        self.trigger = trigger
    def evaluate(self, news:NewsStory) -> bool :
        return not self.trigger.evaluate(news) 
    def __str__(self):
        return 'NotTrigger(' + self.trigger.__str__() + ')'

class AndTrigger(Trigger) :
    def __init__(self, trigger1:Trigger, trigger2:Trigger) -> None :
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, news:NewsStory) :
        return self.trigger1.evaluate(news) and self.trigger2.evaluate(news)
    def __str__(self):
        return 'AndTrigger(' + self.trigger1.__str__() + ' , ' + self.trigger2.__str__() + ')'

class OrTrigger(Trigger) :
    def __init__(self, trigger1:Trigger, trigger2:Trigger) -> None :
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, news:NewsStory) :
        return self.trigger1.evaluate(news) or self.trigger2.evaluate(news)
    def __str__(self):
        return 'OrTrigger(' + self.trigger1.__str__() + ' , ' + self.trigger2.__str__() + ')'

def filter_stories(stories:list[NewsStory], triggerlist:list[Trigger]) -> list[NewsStory] : # Returns list of news that meet our parametres
    output = list()
    for story in stories :
        for trigger in triggerlist:
            if trigger.evaluate(story) :
                output.append(story)
    return output

def define_trigger(name:str, target_val:str, memory:dict[str:Trigger]) -> Trigger : 
    if name == 'TITLE' :
        if len(target_val) !=1 :
            raise ValueError ('Unvalid command in text document: TITLE')
        return TitleTrigger(target_val[0])
    elif name == 'DESCRIPTION' :
        if len(target_val) !=1 :
            raise ValueError ('Unvalid command in text document: DESCRIPTION')
        return DescriptionTrigger(target_val[0])
    elif name == 'AFTER' :
        if len(target_val) !=1 :
            raise ValueError ('Unvalid command in text document: AFTER')
        return AfterTrigger(target_val[0])
    elif name == 'BEFORE' :
        if len(target_val) !=1 :
            raise ValueError ('Unvalid command in text document: BEFORE')
        return BeforeTrigger(target_val[0])
    elif name == 'NOT' :
        if len(target_val) !=1 :
            raise ValueError ('Unvalid command in text document: NOT')
        return NotTrigger(memory[target_val[0]])
    elif name == 'AND' :
        if len(target_val) !=2 :
            raise ValueError ('Unvalid command in text document: AND')
        return AndTrigger(memory[target_val[0]], memory[target_val[1]])
    elif name == 'OR' :
        if len(target_val) !=2 :
            raise ValueError ('Unvalid command in text document: OR')
        return OrTrigger(memory[target_val[0]], memory[target_val[1]])

def read_trigger_config(filename:str) -> list[Trigger] : # takes trigger configuration file
    output = list()

    triggers_file = open(filename)
    lines = []
    for line in triggers_file:
        line = line.strip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    
    triggers_dict = dict()
    for line in lines :
        words = line.split(',')
        if not words[0] == 'ADD' :
            triggers_dict[words[0]] = define_trigger(words[1], words[2:], triggers_dict)
        else :
            for trigger in words[1:] :
                output.append(triggers_dict[trigger])
    return output
            
if __name__ == '__main__' :
    target_stories = filter_stories(
        process('http://news.google.com/?output=rss'), read_trigger_config('triggers.txt')
        )
    for story in target_stories :
        print(story.get_title())
        print(story.get_pubdate())