![Product News API](https://github.com/arindampradhan/ProductHunt_API/master/PH.jpg)

Unofficial API for Product Hunt
This API is created for educational purposes.I thought to do this project as I am learning python.
The official api can be found on the developer website of product hunt.Highly recommend using that.


Features
========

- Compatible with Python 2 (2.7+).
- Supports page(num)
- Retrieve comments from posts (`[Product].get_comments()`)
- Pagination support for comments ( parent_id and comment_id for 2 level pagination)
- Get post details for any Product (`[Product].get(12839)`)
- Gets the User info ,Product info , Front page extraction
- gets the User followers and the following ids
- get ids of the upvoted product, followers and following from user
- Ordering Products posts by top [most upvote] ,newest ,page number
- Get the timestamp ,urls,ids ,html_body of the comment portion and much more. 

Installation
============

	python setup.py install

Usage
=====

** NOTE: ** The product max limit have been set to 150.You can vary with any number between that.To change the max_limit refer to ProductHunt_API/ph/ph.py  


### Using `PH`

####Initialize with `PH`
	
	from ph import PH
	ph = PH
	for product in ph.get_products(45,"top"):
	    print (product.title,product.link)
	

### Using `User`

####Initialize a user with `User.get()` method	

	from ph import User
	user = User.get(67477)
	
	user.get_follower() # gives the list of followers

	user.get_following() # gives the list of the people the user if following

	user.get_votes() # product id list of the product user has upvoted


###Using `Product`

Initialize with `Product.get()` method
	
	from ph import Product
	product = Product.get(12839)

	comments = product.get_comments()
	for comment in comments:
		print "\n{0} commented:".format(comment.user_name)
		print comment.body


API Reference
========

## Class: `PH`

### Get products from product hunt

#### `get_products`

**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |
| `limit` | integer | No | Number of stories required from the given page. Max limit has been kept to 150 | 30
| `product_type` | string | No | Returns the products from this page. One of `(empty string)`, `newest`, `top`, `{num}` | `(empty string)` (newest) |

**Example:**

	from ph import PH
	ph = PH()
	ph.get_stories(story_type='newest', limit=10)


## `User`

### Get a user from product hunt

#### `get`
**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |
| `user_id` | integer | Yes | The user id of the user profile on product hunt | None |

**Example**

	from ph import User
	user = User.get(2)

### Get followers of the initialized user `returns [list]`

#### `get_follower`
**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |

**Example**

	from ph import User
	user = User.get(2)
	user = User.get_follower()


### Get followers of the initialized user `returns [list]`

#### `get_following`
**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |

**Example**

	from ph import User
	user = User.get(2)
	user = User.get_following()


## `Product`

### Get a product post from product hunt

#### `get`

**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |
| `product_id` | integer | Yes | product id of the post on product hunt | None |

**Example**

	from ph import Product
	product = Product.get(12838)


## Comment

### Get product comments for the intialized Product

#### `get_comments`

**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |

**Example**

	from ph import Product
	product = Product.get(12838)
	product.get_comments()


## Class: `Product`

###Each `Product` has the following properties

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

###Each `Comment` has the following properties

- **user_id** - id of the commenter
- **user_name** - name of the commenter
- **comment_id** - the comment's id
- **parent_id** - the discussion starts with the parent id [person who starts the discussion has the comment_id == parent_id]
- **body_html** - the html of the comment
- **body** -  comment in text
- **upvote** - upvotes for the comment
- **time** - time when the comment was published


## Class: `User`

###Each `User` has the following properties

- **user_id** = user_id -  the user's id
- **user_name** = user_name - the user name of the profile
- **about** = about - about the user's profile
- **upvote** = upvote - number of products upvoted by user
- **submitted** = submitted - number of products submitted by user
- **made** = made - number of products made by the user
- **followers** = followers - number of followers of the user profile
- **followings** = followings - number of profiles the user is following
- **twitter** = twitter - twitter profile name of the user


TODO
====

* add tests
* add examples 
* add coverage
