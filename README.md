![Product News API](https://github.com/arindampradhan/ProductHunt_API/blob/master/PH.png)

Unofficial API for Product Hunt
This API is created for educational purposes.I thought to do this project as I am learning python.
The official api can be found on the developer website of product hunt.Highly recommend using that.

**Important:** This project is no longer supported, the html of the website changes very often..
Any ways check out my new api for [Hacker News](https://github.com/arindampradhan/yaaHN).It is more stable.

Features
========

- Compatible with Python 2 (2.7+).
- Supports page(num)
- Retrieve comments from posts. `[Product].get_comments()`
- Pagination support for comments ` parent_id and comment_id for 2 level pagination`
- Get post details for any Product. `[Product].get(12839)`
- Gets the User info ,Product info , Front page extraction
- gets the User followers and the following ids
- get ids of the upvoted product, followers and following from user
- Ordering Products posts by top [most upvote] ,newest ,page number
- Get the timestamp ,urls,ids ,html_body of the comment portion and much more. 

Installation
============
Just clone the repo

	python setup.py install

Usage
=====

**NOTE:** The product max_limit have been set to 150.
You can vary with any number between that.To change the max_limit refer to ./ProductHunt_API/ph/ph.py .  


### Using `PH`

####Initialize with `PH`
	
	from ph import PH
	ph = PH
	for product in ph.get_products(45,"top"):
	    print (product.title,product.link)


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
	ph.get_products(limit=30,page_type="newest")

	ph.get_products(limit=30,page_type="top")

## Class: `User`

### Get a user from product hunt

#### `get`
**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |
| `user_id` | integer | Yes | The user id of the user profile on product hunt | None |

**Example**

	from ph import User
	user = User.get(2)


### Get following and followers  of the initialized user `returns [list]`

#### `get_following` and `get_follower`
**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |
|||||
**Example**

	from ph import User
	user = User.get(2)
	user.get_following()
	
	user.get_follower()


## Class: `Product`

### Get a product post from product hunt

#### `get`

**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |
| `product_id` | integer | Yes | product id of the post on product hunt | None |

**Example**

	from ph import Product
	product = Product.get(12838)


## Class: `Comment`

### Get product comments for the intialized Product

#### `get_comments`

**Parameters:**

| Name | Type | Required | Description | Default |
| ---- | ---- | -------- | ----------- | ------- |
|||||
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

- **user_id** -  the user's id
- **user_name** - the user name of the profile
- **about** - about the user's profile
- **upvote** - number of products upvoted by user
- **submitted** - number of products submitted by user
- **made** - number of products made by the user
- **followers** - number of followers of the user profile
- **followings** - number of profiles the user is following
- **twitter** - twitter profile name of the user


TODO
====

* add tests
* add examples 
* add coverage
