#!/usr/bin/env python

"""
Python API for Product Hunt.
Unofficial Python API for Product Hunt.

@author Arindam Pradhan
@email arindampradhan10@gmail.com
"""


import re
import time
import operator
import urlparse
import requests
from bs4 import BeautifulSoup

from .utils import get_soup, comment_soup,striphtml,strp
from .constants import BASE_URL, INTERVAL_BETWEEN_REQUESTS


class PH(object):
    """The classes that parses the PH page,and builds the stories"""
    def __init__(self):
        self.more = ''

    def _next_page(self,current_page):
        """
        Get the relative url of the next page adding a ?page= query
        """
        # not in use
        return urlparse.urljoin(BASE_URL ,("?page=" + str(current_page+1) ))

    @classmethod
    def _build_product(self,soup):
        """
        Builds and returns a list of products from the front page or the given num page
        """
        all_products = []

        page = requests.get(BASE_URL).text 
        soup = BeautifulSoup(page)
        posts_html = soup.find('div',id="posts-wrapper")
        post = posts_html.find_all('li',class_=re.compile(r'(post m-hidden|post)'))


        for product in post:
            num_comments = int(product.find('span', class_="comment-count").string)
            product_id = int(product.find('div',class_="upvote")['data-vote-id'])
            upvote = int(product.find('span',class_="vote-count").string)
            product.find('span', class_="comment-count")
            published_time = product.find_parent("div",class_=re.compile(r'(day today|day)')).time['datetime']
            prod = product.find('div',class_="url")
            url  = prod.a['href']
            link = urlparse.urljoin(BASE_URL,url)
            domain =  link #requests.get(link).url ##will make it slow
            title = prod.a.string
            description = prod.find('span', class_="post-tagline description").string
            user = product.find('div', class_="user-hover-card").h3.string
            published_time = product.find_parent('div', class_=re.compile(r'(day today|day)')).time['datetime']
            submitter_card = product.find('div', class_="user-hover-card")
            submitter = submitter_card.h3.string
            submitter_id = submitter_card.find('a', {'data-component':"FollowMarker"})['data-follow-id']
            obj_product = Product(upvote,product_id,title,link,domain,submitter,submitter_id,published_time,num_comments)
            all_products.append(obj_product)
        return  all_products

    @classmethod      
    def get_products(self,limit=30,page_type=1):
        """
        Returns a list of product(s) from the passed page
        of PH.
        '' = newest stories (homepage) (default)
        'num' = page {num} products i.e 1,2,3
        'top' = most voted products of the page
        'newest' =  get the newest newest

        'limit' is the number of stories required from the given page.
        Defaults to 30. Cannot be more than 150 [change the code if you want more !].
        """
        max_limit = 150 # change it if you want more

        if page_type == "newest":
            page_type = 1
        pager = page_type
        if type(page_type) == int:
            soup = get_soup(page_type)
        else:
            page_type = 1
            soup = get_soup(page_type)

        if limit == None or limit < 1 :
            limit = 30
        products_found = 0
        products = []
        while products_found < limit:
            products = products + self._build_product(soup)
            products_found = products_found + len(products)
            if products_found >= limit or products_found >=max_limit:
                if pager == "top":
                    products = sorted(products, key=operator.attrgetter('upvote'),reverse=True) # orders in decending order
                return products[:limit]
            page_type = page_type + 1
            soup = get_soup(page_type)


class Product(object):
    """Product class represents a single product or post on PH"""
    def __init__(self, upvote,product_id,title,link,domain,submitter,\
        submitter_id,published_time,num_comments):
        self.upvote = upvote
        self.product_id = product_id
        self.title = title
        self.link = link
        self.domain = domain
        self.submitter = submitter
        self.submitter_id = submitter_id
        self.published_time = published_time
        self.num_comments = num_comments
        
    def __repr__(self):
        """
        A string representation of the class object
        """
        return '<Product: ID={0}>'.format(self.product_id)

    def _build_comments(self,soup):
        """
        For the Product,builds and returns a list of comment objects.
        """
        COMMENTS = []
        c_soup = soup.find('section',class_="modal-post--comments")

        post_show = c_soup.find('main', {"data-comment":"list"})
        num_comment = c_soup.h2.string.split(" ")[0]
        comments_htmls = post_show.find_all("div", {"data-comment":"comment"},recursive=False)
        for html_comment in comments_htmls:
            sub_comments = html_comment.find_all("span",{'class':"modal-post--comment--avatar" ,'data-popover':"hover"})
            parent_id = ""
            first_comments = sub_comments[0]
            for comment_sub in sub_comments:
                body_html = comment_sub.find_next_sibling()
                body = body_html('p')
                body = striphtml(str(body))
                time = body_html.find("span",{"data-component":"TimeAgo"})['title']
                user_id= comment_sub.find("a",{"data-component":"FollowMarker"})["data-follow-id"]
                user_name = body_html.h1.string
                user_name = strp(user_name)
                upvote = body_html.find("span",{'data-vote-count':""}).string
                upvote = strp(upvote)
                comment_id = body_html['id'].split('-')[1]
                if "upvote" in upvote.lower():
                    upvote = None
                if comment_sub == first_comments:
                    parent_id = comment_id
                a = Comment(user_id,user_name,comment_id,parent_id,body_html,body,upvote,time)
                COMMENTS.append(a)
        return COMMENTS

    @classmethod
    def get(self,product_id):
        """
        Initializes an instance of Story for given item_id.
        """
        if not product_id:
            raise Exception('Need an formid for a Story')

        soup = comment_soup(str(product_id))
        product = soup.find('div',class_="modal-post")
        title = product.find("h1").a.string
        link = product.find("h1").a['href']
        link = urlparse.urljoin(BASE_URL,link)
        upvote = int(product.find('span', class_="vote-count").string)
        posted_by = product.find('div', class_="modal-post--submitted")
        published_time = posted_by.find('span',{"data-component":"TimeAgo"})['title']
        num_comments = int(product.find("section", class_="modal-post--comments").h2.string.split(" ")[0])
        domain = requests.get(link).url
        submitter = posted_by.find('h3').string
        submitter_id = posted_by.find('a',{"data-component":"FollowMarker"})['data-follow-id']
        return Product(upvote,product_id,title,link,domain,submitter,submitter_id,published_time,num_comments)

    def get_comments(self):
        """
        Return a list of Comment(s) for the product
        """
        soup = comment_soup(self.product_id)
        return self._build_comments(soup)



class User(object):
    """Represents a user in PH"""
    def __init__(self, user_id,user_name,about,upvote,submitted,made,followers,followings,twitter):
        self.user_id = user_id
        self.user_name = user_name
        self.about = about
        self.upvote = upvote
        self.submitted = submitted
        self.made = made
        self.followers = followers
        self.followings = followings
        self.twitter = twitter

    @classmethod
    def __repr__(self):
        print """
        user_id = {0}
        user_name = {1}
        about = {2}
        twitter = {3}""".format(str(self.user_id),self.user_name,self.about,self.twitter)
        

    @classmethod
    def get(self,user_id):
        """
        Initialize an instance of a user from a given user id
        """
        if not user_id:
            raise Exception('Need an user_id for a user')

        TAG_RE = re.compile(r'<[^>]+>')
        def remove_tags(text):
            return TAG_RE.sub('', text)

        u_url = "http://www.producthunt.com/" + str(user_id)
        req = requests.get(u_url)
        u_page = req.text
        soup = BeautifulSoup(u_page)

        about = soup.find('h2',class_="page-header--subtitle").string
        user = soup.find("h1",class_="page-header--title")
        user_text =  remove_tags(str(user))
        user_name = strp(user_text.split("#")[0])

        nav = soup.find('nav',class_="page-header--navigation")
        upvote_u = nav.find_all('strong')
        u_twitter = req.url.split('/')[-1]

        # check if it is a user or org (submit or non submit)
        if len(upvote_u) == 5:
            u_num_upvote = upvote_u[0].string
            u_num_submit = upvote_u[1].string
            u_num_made = upvote_u[2].string
            u_num_followers = upvote_u[3].string
            u_num_following = upvote_u[4].string
            return User(user_id,user_name,about,u_num_upvote,u_num_submit,u_num_made,u_num_followers,u_num_following,u_twitter)
        if len(upvote_u) > 5:
            u_num_upvote = upvote_u[0].string
            u_num_submit = upvote_u[1].string
            u_num_made = upvote_u[2].string
            u_num_followers = upvote_u[-2].string
            u_num_following = upvote_u[-1].string
            return User(user_id,user_name,about,u_num_upvote,u_num_submit,u_num_made,u_num_followers,u_num_following,u_twitter)
        if len(upvote_u) == 4:
            u_num_upvote = upvote_u[0].string
            u_num_made = upvote_u[1].string
            u_num_followers = upvote_u[-2].string
            u_num_following = upvote_u[-1].string
            return User(user_id,user_name,about,u_num_upvote,None,u_num_made,u_num_followers,u_num_following,u_twitter)


    @classmethod
    def get_votes(self,limit=50,page_count_limit=""):
        """
        gives the ids of upvoted products,submitted products and made products\n
        \tparam = upvoted\n (default)
        \tparam = products\n
        \tparam = posts\n 
        """
        if page_count_limit == "":
            page_count_limit = int((limit+1)/50)
        url = BASE_URL + str(self.twitter) 
        page_count = 1
        data_ids = []

        while page_count < page_count_limit:

            current_page = requests.get(url+"?page="+str(page_count)).text
            soup  = BeautifulSoup(current_page)
            post_group = soup.find('ul',class_="posts-group")
            post_list = post_group.find_all('li',class_="post")
            for pst in post_list:
                data_id = pst.find('div',class_="upvote")['data-vote-id']
                data_ids.append(data_id)
            page_count = page_count+1
            if len(soup.find_all('li', class_="post")) is 0:
                break
        yield data_ids[:limit]

    @classmethod
    def _build_follow(self,limit,page_count_limit,follow_type):
        """
        Type is a follower or following
        """
        user_id = self.user_id
        url = "{0}{1}/{2}".format(BASE_URL,user_id,follow_type)
        page_count=1
        followers = []
        count=0
        while page_count < page_count_limit:
            current_page = requests.get(url+"?page="+str(page_count)).text
            soup  = BeautifulSoup(current_page)
            follow_group = soup.find_all("li", class_="people--person")
            
            for follow in follow_group:
                follow_id = follow.find('div', class_="user-hover-card").find('a', class_="button")['data-follow-id']
                followers.append(follow_id)
                count = count + 1
            if count >= limit:
                break
            page_count = page_count+1
            if len(soup.find('ul', class_="people").find_all('li',class_='people--person'))  == 0:
                break
        return followers[:limit]

    @classmethod
    def get_follower(self,limit=50,page_count_limit=""):
        """
        Gives the ids of followers\n
        Default limit = 50
        """
        if page_count_limit == "":
            page_count_limit = int((limit+1)/50)
        return self._build_follow(limit,page_count_limit,"followers")


    @classmethod
    def get_following(self,limit=50,page_count_limit=""):
        """
        Gives the ids of the people the user is following\n
        Default limit = 50        
        """
        if page_count_limit == "":
            page_count_limit = int((limit+1)/50)
        return self._build_follow(limit,page_count_limit,"followings")


class Comment(object):
    """Represents a comment for the discussion in a product"""
    def __init__(self, user_id,user_name,comment_id,parent_id,body_html,body,upvote,time):
        self.user_id = user_id
        self.user_name = user_name
        self.comment_id = comment_id
        self.parent_id = parent_id
        self.body_html = body_html
        self.body = body
        self.upvote = upvote
        self.time = time

    def __repr__(self):
        return '<Comment: ID={0}>'.format(self.comment_id)