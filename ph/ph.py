 #!/usr/bin/env python

"""
Python API for Product Hunt.
Unofficial Python API for Product Hunt.

@author Arindam Pradhan
@email arindampradhan10@gmail.com
"""


import re
import time

import urlparse
import requests
from bs4 import BeautifulSoup

from .utils import get_soup, comment_soup
from .constants import BASE_URL, INTERVAL_BETWEEN_REQUESTS

class PH(object):
    """The classes that parses the PH page,and builds the stories"""
    def __init__(self):
        self.more = ''    


    def _next_page(self,url,current_page):
        """
        Get the relative url of the next page adding a ?page= query
        """
        # soup is not needed
        return url + "?page=" + str(current_page+1)

    @classmethod
    def _build_product(self,soup):
        """
        Builds and returns a list of product from the front page
        """

        all_products = []


        page = requests.get(BASE_URL).text 
        soup = BeautifulSoup(page)
        posts_html = soup.find('div',id="posts-wrapper").find('div',class_="posts")
        post = posts_html.find_all('li',class_=re.compile(r'(post hidden-post|post)'))


        for product in post:
            upvote = int(product.find('span', class_="vote-count").string)
            published_time = product.find_parent("div",class_=re.compile(r'(day today|day)')).time['datetime']
            prod = product.find('div',class_="url")
            url  = prod.a['href']
            link = urlparse.urljoin(BASE_URL,url)
            domain = requests.get(link).url
            title = prod.a.string
            description = prod.find('span', class_="post-tagline description").string
            user = product.find('div', class_="user-hover-card").h3.string
            product_id = product.find('a', class_="view-discussion")['data-id']
            num_comments = int(product.find('p',class_="comment-count").string)
            published_time = product.find_parent('div', class_=re.compile(r'(day today|day)')).time['datetime']
            submitter = product.find('div', class_="user-hover-card").h3.string
            submitter_id = product.find_all('a')[-1]['data-follow-id']

            product = (upvote,product_id,title,link,domain,submitter,submitter_id,published_time,num_comments)
            all_products.append(product)
        return all_products

    @classmethod      
    def get_products(self,page_num='page1',limit=30):
        """
        Yields a list of stories from the passed page
        of PH.
        'product_type' can be:
        \t'page2' = page 2 products
        \t'page3' = page 2 products
        \t'page4' = page 2 products

        'limit' is the number of stories required from the given page.
        Defaults to 30. Cannot be more than 30.
        """
        page_num = page_num[-1]
        if limit == None or limit < 1 or limit > 30:
            limit = 30
        products_found = 0

        while products_found < limit:
            soup = get_soup(page_num)
            products =  self._build_product(soup)    

            for product in products:
                yield product         
                products_found += 1

                if products_found == limit:
                    return 


class Product(object):
    """Product class represents a single product or post on PH"""
    def __init__(self, upvote,product_id,title,link,domain,submitter,\
        submitter_id,published_time,num_comments):
        super(Product, self).__init__()
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
        c_soup = soup
        c_soup.find('div',class_="post_show")

        post_show = c_soup.find('div',class_="post-show")
        num_comment = post_show.find('h2', class_="subhead")
        comment_htmls = post_show.find_all('div',class_= re.compile(r'^(comment|comment child)$'))

        #regex for comment extraction compile outside for faster for loop
        regex = re.compile(r"<a.*?</a>", re.IGNORECASE)
        reg_div = re.compile(r"(?s)<div(?: [^>]*)?>(.*?)<\/div>")

        for comment_html in comment_htmls:
            c_upvote = comment_html.find('span',class_="vote-count").string
            c_id = comment_html['data-comment-id']
            p_id = comment_html.find_parent('div',class_="comment-thread")['data-parent-id'] # parent id
            c_flag = (c_id == p_id)
            #getting comment using regex
            
            c_comment = str(comment_html.find('div',class_="actual-comment"))
            c_comment = str(regex.sub("",c_comment))
            c_comment = str(reg_div.findall(c_comment)[0])
            c_user = comment_html.find('h2', class_="comment-user-name").a.string
            
            # creating and appending to the class method
            comment = Comment(c_id,p_id,c_flag,c_user,c_comment,comment_html,c_upvote) 
            COMMENTS.append(comment)
        return COMMENTS

    @classmethod
    def formid(self,product_id):
        """
        Initializes an instance of Story for given item_id.    Initialize the instance by giving the product_id
        """
        if not product_id:
            raise Exception('Need an product_id for a Story')

        soup = comment_soup(product_id)
        product = soup.find('div',class_="comments-header")
        
        upvote = int(product.find('span', class_="vote-count").string)
        posted_by = product.find('span', class_="posted-by")
        published_time = posted_by.find('abbr')['title']

        post_user = product.find('span', class_="post-user")        
        submitter = post_user.find('div', class_="user-hover-card").h3.string
        submitter_id = post_user.find_all('a')[-1]['data-follow-id']

        post_info = product.find('div', class_="post-info")
        link = post_info.find('a', class_="post-url")['href']
        link = urlparse.urljoin(BASE_URL,link)
        domain = requests.get(link).url
        print upvote,post_info,submitted
        title = post_info.a.string
        description = post_info.find('span', class_="post-tagline description").string
        num_comments = int(soup.find_all('h2', class_="subhead")[1].string.split(" ")[0])
        Product(upvote,product_id,title,link,domain,submitter,submitter_id,published_time,num_comments)
        return Product



    def comments(self):
        """
        Return a list of Comment(s) for the product
        """
        soup = comment_soup(self.product_id)
        return self._build_comments(soup)


class Comment(object):
    """Represents a comment for the discussion in a product"""
    def __init__(self, comment_id,parent_id,flag,user,body,body_html,upvote):
        super(Comment, self).__init__()
        self.comment_id = comment_id
        self.parent_id = parent_id
        self.flag = flag # whether it is a parent comment or not
        self.user = user
        self.body = body
        self.body_html = body_html
        self.upvote = upvote

    def __repr__(self):
        return '<Comment: ID={0}>'.format(self.comment_id)
        

class User(object):
    """Represents a user in PH"""
    def __init__(self, user_id,data,name,about):
        super(User, self).__init__()
        self.user_id = user_id
        self.data = data
        self.name = name
        self.about = about

    def __repr__(self):
        return '{0} {1} {2}'.format(self.user_id,self.name,self.about)

    @classmethod
    def userid(self,user_id):
        """
        Initialize an instance of a user from a given user id
        """
        if not user_id:
            raise Exception('Need an user_id for a user')

        TAG_RE = re.compile(r'<[^>]+>')
        def remove_tags(text):
            return TAG_RE.sub('', text)

        u_url = "http://www.producthunt.com/" + str(user_id)
        u_page = requests.get(u_url).text
        u_soup = BeautifulSoup(u_page)
        u_soup = u_soup.find('div',class_="main-content")

        about = u_soup.find('h2',class_="page-header--subtitle").string
        user = u_soup.find("h1",class_="page-header--title")
        user_text =  remove_tags(str(user))

        user_id = int(user_text.split("#")[1])
        user_name = user_text.split("#")[0]

        nav = u_soup.find('nav',class_="page-header--navigation")
        upvote_u = nav.find_all('strong')

        u_num_upvote = upvote_u[0].string
        u_num_submit = upvote_u[1].string
        u_num_made = upvote_u[2].string
        u_num_followers = upvote_u[3].string
        u_num_following = upvote_u[4].string
        data(u_num_upvote,u_num_submit,u_num_made,u_num_followers,u_num_following)
        User(user_id,data,user_name,about)

    def vote_ids(self,user_id,param=""):
        """
        gives the ids of upvoted products,submitted products and made products\n
        \tparam = upvoted\n (default)
        \tparam = products\n
        \tparam = posts\n 
        """
        if not user_id:
            raise Exception('Need an user_id for a user,create the userid first')

        url = "http://www.producthunt.com/"+ str(user_id) + str(param) 
        page_count=1
        data_ids = []
        while 1:
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
        return data_ids

    def follow_ids(url,param="followers"):   
        """
        gives the ids of followers and followings
        \t followers\n
        \t followings\n
        """
        url = "http://www.producthunt.com/" + str(param) 
        page_count=1
        follow_ids = []
        while 1:
            current_page = requests.get(url+"?page="+str(page_count)).text
            soup  = BeautifulSoup(current_page)
            follow_group = soup.find_all("li", class_="people--person")
            
            for follow in follow_group:
                follow_id = follow.find('div', class_="user-hover-card").find('a', class_="button")['data-follow-id']
                follow_ids.append(follow_id)
            page_count = page_count+1
            if len(soup.find('ul', class_="people").find_all('li',class_='people--person'))  == 0:
                break
        return follow_ids

class data(object):
    """data created by the user"""
    def __init__(self, upvote,submitted,made,followers,followings):
        super(data, self).__init__()
        self.upvote = upvote
        self.submitted = submitted
        self.made = made
        self.followers = followers
        self.followings = followings

    def __repr__(self):
        return 'upvote:{1} submitted:{2} made:{3} followers:{4} followings:{5}'.format(self.upvote,self.submitted,self.made,self.followers,self.followings)
