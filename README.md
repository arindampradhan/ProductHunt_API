This is my attempt to create an api just for learning purposes.
The official api can be found on the developer website of product hunt.


Features
============

- Compatible with Python 2 (2.7+).
- Supports page(num)
- Retrieve comments from posts (flat list for now) (`[product].get_comments()`)
- Pagination support for comments
- Handles external posts, self posts and job posts
- Get post details for any post (`Product.fromid(7024626)`)
- user info
- get ids of the followers and following from user


Each `Product` has the following properties

- **upvote** - product's upvote 
- **product_id** - the id of the product
- **title** - the title of the product post
- **link** - the link for the product in the producthunt query format 
- **domain** - the real url or domain of the product
- **submitter** - the name of the submitter
- **submitter_id** - the if of the submitter
- **published_time** - published time of the product post
- **num_comments** - the number of comment on the post


## Class: `Comment`

Each `Comment` has the following properties

- **comment_id** - the comment's item id
- **parent_id** - the comment's parent id (who started the comment)
- **flag** - whether the comment is a parent comment or not
- **user** - user's name who submitted the post
- **time_ago** - time when it was submitted
- **body** - text representation of comment (unformatted)
- **body_html** - html of comment, may not be valid
- **upvote** - upvote for the comment

## Class: `User`

Each `User` has the following properties

        self.user_id = user_id
        self.data = data
        self.name = name
        self.about = about





TODO
==========

* add test
* get error catches 

