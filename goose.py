#!/usr/bin/python
#https://github.com/smithandrewa/
import os
import re
from datetime import datetime
import pdb
import praw
import socket

#-----------vars---------------
target_subreddit = 'UBreddit'
praw_profile = 'bot1'
comment_message = 'Honk!'
current_working_dir = "/home/pi/goose_bot/"
#------------------------------

#set date & time
dt = datetime.now()

#ensure correct workspace
os.chdir(current_working_dir)
print('UB Goose Bot is Running...')
print('Workspace is: ' + str(os.getcwd()))

#create reddit instance
reddit = praw.Reddit(praw_profile)
subreddit = reddit.subreddit(target_subreddit)
print("READ ONLY TF: " + str(reddit.read_only))
print("SUBREDDIT: " + subreddit.display_name)

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False
    with open('gooseLog.txt', 'a') as l:
        l.write(str(dt) + ': ' + 'INTERNET FAILURE' + '\n')

#main function
def gooseSubmissionChecker():
    if not os.path.isfile('gooseLog.txt'):
        with open('gooseLog.txt', 'w') as l:
            l.write('Init...\n')
            l.write(str(dt) + ': ')
    else:
        with open('gooseLog.txt', 'a') as l:
            l.write(str(dt) +  ": ")
    if not os.path.isfile('posts_replied_to.txt'):
        posts_replied_to = []
        print("Creating File: posts_replied_to.txt")
    else:
        with open('posts_replied_to.txt', 'r') as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split('\n')
            posts_replied_to = list(filter(None, posts_replied_to))
    try:
        for submission in subreddit.new(limit=50):
            if submission.id not in posts_replied_to:
                if re.search('goose', submission.title, re.IGNORECASE):
                    submission.reply(comment_message)
                    print("Goose Bot Honks at:", submission.title)
                    posts_replied_to.append(submission.id)
                elif re.search('geese', submission.title, re.IGNORECASE):
                    submission.reply(comment_message)
                    print("Goose Bot Honks at:", submission.title)
                    posts_replied_to.append(submission.id)
                elif re.search('goose', submission.selftext, re.IGNORECASE):
                    submission.reply(comment_message)
                    print("Goose Bot Honks at:", submission.title)
                    posts_replied_to.append(submission.id)
                elif re.search('geese', submission.selftext, re.IGNORECASE):
                    submission.reply(comment_message)
                    print("Goose Bot Honks at:", submission.title)
                    posts_replied_to.append(submission.id)
            gooseCommentChecker(submission)
    except:
            print('Error, Aborting')
            with open('gooseLog.txt', 'a') as l:
                l.write('Error, Aborting' + '\n')
    finally:
        with open('posts_replied_to.txt', 'w') as f:
            for post_id in posts_replied_to:
                f.write(post_id + "\n")
                print('Updating: posts_replied_to.txt')
        with open('gooseLog.txt', 'a') as l:
            l.write('Complete!' + '\n')

#checks for comments to original submission
def gooseCommentChecker(submission):
    if not os.path.isfile('comments_replied_to.txt'):
        comments_replied_to = []
        print("Creating File: comments_replied_to.txt")
    else:
        with open('comments_replied_to.txt', 'r') as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split('\n')
            comments_replied_to = list(filter(None, comments_replied_to))
    for comment in submission.comments.list():
        if comment.id not in comments_replied_to:
            if re.search('goose', comment.body, re.IGNORECASE):
                comment.reply(comment_message)
                print("Goose Bot Honks at Comment:", comment.body)
                comments_replied_to.append(comment.id)
            if re.search('geese', comment.body, re.IGNORECASE):
                comment.reply(comment_message)
                print("Goose Bot Honks at Comment:", comment.body)
                comments_replied_to.append(comment.id)
    with open('comments_replied_to.txt', 'w') as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")
            print('Updating: comments_replied_to.txt')

def run_goose():
    if is_connected():
        gooseSubmissionChecker()
        print('Complete')
    else:
        print('INTERNET FAILURE')

run_goose()
