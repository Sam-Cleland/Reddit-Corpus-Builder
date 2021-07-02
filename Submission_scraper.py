# -*- coding: utf-8 -*-
"""
Author: Sam Cleland
Date Created: 02/07/2021
Last Updated: 
    
Basic bot to scrape text in titles and submission body of reddit submissions. Note that the script needs credentials 
to be stored in the praw.ini file. An example praw.ini file is included in this repositiry This bot was originally 
designed to collect text data for a corpus building assignment.
"""

# Importing libraries
import praw
import pandas as pd
import os

print("praw.ini file needs to be saved to this location: ")
print(praw.__file__)

# Creating a authorised PRAW reddit instance, this allows the text scraper to access any functionality
# that a regular user account can. For security purposes I have removed my client and password information. 
# Steps to create a authorised instance are found here: 
# 'https://praw.readthedocs.io/en/latest/getting_started/authentication.html'
reddit = praw.Reddit(site_name='corpusbot') 
print(reddit.user.me())

# subreddit_name to gather posts from
subreddit_name = "PrequelMemes"
# This sections defines some 'global' values which will be used by the subreddit.search() function.
search_list = 'obi-wan, darth' # list of keywords to search for in post titles.
search = list(search_list.split(',')) # splits the list so it can be iterated through
lim = 10 # number of posts to take when calling subreddit.search()
sortsub = 'top' # can be one of: relevance, hot, top, new, comments. These are descriptors for how reddit sorts & displays content.

# The PRAW subreddit instance provides a set a functions which are able to interact with the subreddit.
sub = reddit.subreddit(subreddit_name) # set instance of subreddit
# display some basic information about the subreddit
print(sub.display_name)
print(sub.subscribers)

# Function for writing the title and text contents of a reddit post into its own text file.
def write_text_file(sub_id, sub_title, sub_text):
        file_name = sub_id # Filename is the unique post id
        try: # tries to open a new text file
            f = open(file_name+'.txt', 'x', encoding="utf-8") # if the file doesn't exist will write text to the file.
            f.write(sub_title) # write title text to file
            f.write(sub_text) # write body text to text file
            f.close() # closes the open text file
        except: # If the file exists it will ignore the above steps. This step is to prevent 'FileExists' errors when there
            # are multiple keywords in the post title.
            pass

# creating a list for each column in what will become the pandas data frame.
post_id=[] # unique identifier for each post
search_term=[] # search term that was found in title
post_title=[] # full post title
time=[] # time post was made
link_flair=[] # tagging 'keyword' used for sorting and filtering posts
num_upvotes=[] # number of upvotes the post has
upvote_ratio=[] # the ratio of upvotes to downvotes the post has
num_comments=[] # number of comments on post
post_text=[] # any text contained in the body of the post, this doesn't include links to outside sources

# Set directory for text files to be saved
os.makedirs(os.path.join(subreddit_name)) # make directory to store individual txt files
os.chdir(subreddit_name) # change directory
for i in range(len(search)): # iterate through each keyword 
    for submission in sub.search(query=search[i], sort=sortsub, time_filter='all', limit=lim): # searches each submission returned by the search.
        # appends the submission values to their repsective lists
        post_id.append(submission.id)
        search_term.append(search[i])
        post_title.append(submission.title)
        time.append(submission.created_utc)
        link_flair.append(submission.link_flair_text)
        num_upvotes.append(submission.score)
        upvote_ratio.append(submission.upvote_ratio)
        num_comments.append(submission.num_comments)
        post_text.append(submission.selftext) # this is an empty string if the post is a web link
        # Calls the function to convert this submission instances into a text file
        write_text_file(submission.id, submission.title, submission.selftext)
           
# Creates a pandas data frame from the lists, this can be exported as a csv for further analysis
data_frame = pd.DataFrame(
    {'post_id': post_id,
     'search term': search_term,
     'post_title': post_title,
     'time': time,
     'link_flair': link_flair,
     'num_upvotes': num_upvotes,
     'upvote_ratio': upvote_ratio,
     'num_comments': num_comments,
     'post text': post_text
    })

os.chdir('../') # return to directory containing .py file
# saves the pandas datafram as a csv
data_frame.to_csv(subreddit_name+'.csv',header=True)
# prints the first ten rows of the dataframe so user can check the program has worked.
data_frame.head(10)  