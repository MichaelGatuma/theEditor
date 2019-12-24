import urllib
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import xmlrpclib
#from xmlrpc import client
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from crypto import *
import traceback
import os

########################### Read Me First ###############################
'''
------------------------------------------ DETAILS --------------------------------
Description
===========
Add new posts to WordPress remotely using Python using XMLRPC library provided by the WordPress.
------------------------------------------ DETAILS --------------------------------		
'''


class Custom_WP_XMLRPC:
    def post_article(self, wpUrl, wpUserName, wpPassword, articleTitle, articleCategories, articleContent, articleTags,
                     PhotoUrl):
        try:
            self.path = os.getcwd() + "\\images\\00000001.jpg"
            self.articlePhotoUrl = PhotoUrl
            self.wpUrl = wpUrl
            self.wpUserName = wpUserName
            self.wpPassword = wpPassword
            # Download File
            f = open(self.path, 'wb')
            f.write(urllib.urlopen(self.articlePhotoUrl).read())
            f.close()
            # Upload to WordPress
            client = Client(self.wpUrl, self.wpUserName, self.wpPassword)
            filename = self.path
            # prepare metadata
            data = {'name': 'picture.jpg', 'type': 'image/jpg', }

            # read the binary file and let the XMLRPC library encode it into base64
            with open(filename, 'rb') as img:
                data['bits'] = xmlrpc_client.Binary(img.read())
            response = client.call(media.UploadFile(data))
            attachment_id = response['id']
            # Post
            post = WordPressPost()
            post.title = articleTitle
            post.content = articleContent
            post.terms_names = {'post_tag': articleTags, 'category': articleCategories}
            post.post_status = 'publish'
            post.thumbnail = attachment_id
            post.id = client.call(posts.NewPost(post))
            #print 'Post Successfully posted. Its Id is: ', post.id
        except Exception as e:
            print traceback.format_exc()
            return 0
        return post.id


#########################################
# POST & Wp Credentials Detail #
#########################################

# Url of Image on the internet
coverPhotoUrl = 'http://i1.tribune.com.pk/wp-content/uploads/2013/07/584065-twitter-1375197036-960-640x480.jpg'
# Dont forget the /xmlrpc.php cause thats your posting adress for XML Server
hostUrl = dec('gAAAAABd4mOlU1AG8-yfrKTvEnHQvr0FwxO0ErwP0TeAHFMVH-6-WG94JB1WU6D0BHMoq9k-6hq5vQXJjZsn6eEW4iSgps6u4UqmiWX1oeHYHCfb96q-aFfjPRD0Wyj1s2qb0LAm9xGBaQwECCTPlea0wsGdl8vPqQ==')
# WordPress Username
usr = dec('gAAAAABd4mQytL0Yjtjs16_6-AmKKVF8D_xFxn8mDhArTE6vValkdgFtNrzBdbd2UrRBqQ2SIJsJdiHebhRyhcznjbDMe5R86Q==')
# WordPress Password
sec = 'gAAAAABd4mRZB0HjPIF5z0lz4I7XHTTgVyw4AT0JY6Htwwl5yk0eehiSCBShUnRppDcYfX8tSxpqWtVILsSVvwFAXY6Gmo9R9Q=='

#########################################
# Creating Class object & calling the xml rpc custom post Function
#########################################
xmlrpc_object = Custom_WP_XMLRPC()
# On Post submission this function will print the post id
#xmlrpc_object.post_article(hostUrl, usr, dec(sec), 'Title', ['Test','Category'], 'Body Content', ['Tags','Tags again'],
 #                          coverPhotoUrl)

def post(articleTitle,articleCategories,articleContent,articleTags):
    return Custom_WP_XMLRPC().post_article(hostUrl, usr, dec(sec), articleTitle, articleCategories, articleContent, articleTags,
                           coverPhotoUrl)

