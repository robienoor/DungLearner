import csv 
import sys
from post import post


def readPostsCSV(posts):
    path = 'AnnotatedPosts.csv'

    with open(path,  "rt", encoding= 'utf8') as f:
        reader = csv.reader(f, delimiter=',')

        # Need to make sure we skip the first line which contains the rows
        next(f)
        for row in reader:
            review = row[0]
            posExp = int(row[1])
            negExp = int(row[2])
            symOK = int(row[3])
            symNOK = int(row[4])
            noSE = int(row[5])
            SE = int(row[6])
            rating = int(row[7])
            drug = row[9]
            newPost = post( review, posExp, negExp, symOK, symNOK, noSE, SE, rating, drug)
            posts.append(newPost)



def gatherReviews():
    posts = []
    readPostsCSV(posts)
    return posts


