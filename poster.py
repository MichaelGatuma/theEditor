from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc import WordPressPost
from crypto import dec

HOST=dec('gAAAAABd4mOlU1AG8-yfrKTvEnHQvr0FwxO0ErwP0TeAHFMVH-6-WG94JB1WU6D0BHMoq9k-6hq5vQXJjZsn6eEW4iSgps6u4UqmiWX1oeHYHCfb96q-aFfjPRD0Wyj1s2qb0LAm9xGBaQwECCTPlea0wsGdl8vPqQ==')
USR=dec('gAAAAABd4mQytL0Yjtjs16_6-AmKKVF8D_xFxn8mDhArTE6vValkdgFtNrzBdbd2UrRBqQ2SIJsJdiHebhRyhcznjbDMe5R86Q==')
SEC='gAAAAABd4mRZB0HjPIF5z0lz4I7XHTTgVyw4AT0JY6Htwwl5yk0eehiSCBShUnRppDcYfX8tSxpqWtVILsSVvwFAXY6Gmo9R9Q=='
your_blog = Client(HOST, USR, dec(SEC))

myposts=your_blog.call(posts.GetPosts())

post = WordPressPost()
post.title = 'Excavator Test'
#post.slug='excavator-test'
post.content = 'This is a post test from a python excavator'
post.id = your_blog.call(posts.NewPost(post))
post.post_status = 'publish'
your_blog.call(posts.EditPost(post.id, post))