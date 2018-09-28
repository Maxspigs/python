
import sys
import re
import datetime


# The Blog Post Data Access Object handles interactions with the Posts collection
class BlogPostDAO:
    compteur = 0

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.posts = database.posts

    # inserts the blog entry and returns a permalink for the entry
    def insert_entry(self, title, post, tags_array, author):
        print("inserting blog entry", title, post)

        # fix up the permalink to not include whitespace
        number_of_post = self.posts.find({})
        exp = re.compile('\W') # match anything not alphanumeric
        whitespace = re.compile('\s')
        temp_title = whitespace.sub("_",title)
        permalink = exp.sub('', temp_title)

        # Build a new post
        post = {
                "_id":number_of_post.count(),
                "title": title,
                "author": author,
                "body": post,
                "permalink":permalink + "_" + str(number_of_post.count()),
                "tags": tags_array,
                "comments": [],
                "date": datetime.datetime.utcnow()}

        # now insert the post
        # XXX TP1 Work Here to insert the post
        self.posts.insert_one(post)
        return permalink


    # returns an array of num_posts posts, reverse ordered by date.
    # XXX TP1 work here change function signature to implement pagination.
    def get_posts(self, num_posts, page_number):

        cursor = iter(())  # Using an empty itable for a placeholder so blog compiles before you make your changes

        # XXX TP1 Work here to get the num_posts posts
        cursor = self.posts.find()[:num_posts].skip( ( ( page_number - 1 ) * num_posts ) if page_number > 0 else 0 ).limit( num_posts )
        l = []

        for post in cursor:
            post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p") # fix up date
            if 'tags' not in post:
                post['tags'] = [] # fill it in if its not there already
            if 'comments' not in post:
                post['comments'] = []

            l.append({'title':post['title'], 'body':post['body'], 'post_date':post['date'],
                      'permalink':post['permalink'],
                      'tags':post['tags'],
                      'author':post['author'],
                      'comments':post['comments']})

        return l

    # find a post corresponding to a particular permalink
    def get_post_by_permalink(self, permalink):

        post = None
        # XXX TP1 Work here to retrieve the specified post
        post = self.posts.find({'permalink': permalink})[0]
        print("PRINTING TEST", post) #TO DO#
        if post is not None:
            # fix up date
            post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p")

        return post

    # add a comment to a particular blog post
    def add_comment(self, permalink, name, email, body):

        comment = {'author': name, 'body': body}

        if (email != ""):
            comment['email'] = email

        try:
            # XXX TP1 Work here to add the comment to the designated post. When done, modify the line below to return the number of documents updated by your modification, rather than just -1.
            number_of_document = self.posts.update_many({'permalink':permalink}, {'$push': {'comments':comment} })

            return number_of_document          # return the number of documents updated

        except:
            print("Could not update the collection, error")
            print("Unexpected error:", sys.exc_info()[0])
            return 0
