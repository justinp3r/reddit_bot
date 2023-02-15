import praw
import time
import random
from praw.models import MoreComments
from praw.reddit import Submission

def border(word):
    #making sure the format is always on fleek
    if len(word)%2!=0:
        word+=" "
    wordcount = len(word)
    eachSide = round((65-wordcount)/2)
    charAll = str(eachSide*"-")
    print(charAll+word+charAll)

#declaring how many triggerwords there are and how they look like
def triggerWords():
    count = int(input("how many trigger words should the bot have?    "))
    for i in range(count):
        trigger_words.append(input(f"enter trigger word {i+1}/{count}:                        "))

#declaring how many replies there are and how they look like
def responseList():
    count = int(input("how many responses should the bot throw out?   "))
    for i in range(count):
        responses.append(input(f"enter response {i+1}/{count}:                            "))
        
#bot starten
def run_bot(subreddit_name):
    global trigger_words
    global comment_ids
    global responses
    subreddit = reddit.subreddit(subreddit_name)
    timeout_start = time.time()

    #While loop is runnning until the timer stops
    while time.time() < timeout_start + runningtimeMin:
        count = 0
        border("bot is ready")
        #bot will run for n posts
        for submission in subreddit.hot(limit=askpostnumber):
            #Nummer für printelement definieren:
            count += 1
            #printing out the current title of post
            print(f"{count}.{submission.title}")

            #for loop is iterating through every comment
            submission.comments.replace_more(limit=50)
            for comment in submission.comments:
                comments(submission)

                #second for loop is iterating through the responses of the responses
                for second_level_comment in comment.replies:
                    comments_second_layer(comment)

#this function returns the number of words a trigger comment is having
def regulate_string_entries(comment_lower, trigger_words):
    io = 0
    comment_lower = comment_lower.split(" ")
    for i in range(len(comment_lower)):
        if comment_lower[i] in trigger_words:
            io += 1
    return io

#this function will comment and print out a data table of informations to the comment that triggered the bot
def answer(comment, comment_lower, sort):
#>Splitten bei " " damit man Wörter zählt
    global trigger_words
    global comment_ids
    global responses
    commentsplitcounter = comment_lower.split(" ")
    print(f"  user:     {comment.author}")
    print(f"  comment:  {comment.body}")
    print(f"  words:    {len(commentsplitcounter)}")
    print(f"  trigger:  {regulate_string_entries(comment_lower, trigger_words)}")
    print(f"  sort:     {sort}")
    comment_ids.append(comment)
    answer = random.choice(responses)
    comment.reply(answer)
    print(f"  replied:  {answer}")
    print(f"  id:       {comment}\n")

#this function checks if theres a comment we have already replied
def comments(submission):
    for comment in submission.comments:
        if hasattr(comment, "body"):
            comment_lower = comment.body.lower()
            if regulate_string_entries(comment_lower, trigger_words) > 0:
                #check if theres a comment that we have alreade replied to
                if comment not in comment_ids:
                    answer(comment, comment_lower, "main comment")
                    time.sleep(60)

def comments_second_layer(comment):
    for second_level_comment in comment.replies:
                    second_level_comment_lower = second_level_comment.body.lower()
                    if regulate_string_entries(second_level_comment_lower, trigger_words) > 0:
                        if second_level_comment not in comment_ids:
                            answer(second_level_comment, second_level_comment_lower, "reply comment")
                            time.sleep(60)

#main method starts here---------
border("important")
print("Note: none of your data will be saved or transfered.\n"+
        "For the next actions you need your client id, client secret,\nuser agent,username and password.")
border("starting setup")
reddit = praw.Reddit(
    client_id=input("enter client id:           "),
    client_secret=input("enter client secret id:    "),
    user_agent=input("enter user agent:          "),
    username = input("enter username:            "),
    password = input("enter password:            ")
)
border("setup successful!")

trigger_words = []
comment_ids = []  #comment_ids saves all the comments of already answered trigger comments
responses = []
asksub= input("What subreddit do you want to check?           ") 
askpostnumber= int(input("How many posts do you want to scan?            "))
runningtimeMin = int(input("How many Minutes do you want the bot runnning? "))*60
triggerWords()
responseList()
run_bot(asksub)
border("done!")