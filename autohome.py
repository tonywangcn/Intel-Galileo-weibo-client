#!/usr/bin/env python
# coding=utf-8
import httplib,json,urllib,webbrowser,time
from xml.dom.minidom import parseString
from weibo import APIClient
from re import split
APP_KEY = '#####' #youre app key
APP_SECRET = '######' #youre app secret  
 # callback url, your must set this URL in your "my application->appInfos-> advanced  info"
CALLBACK_URL = 'http://arduino2automate.sinaapp.com/'
ACCOUNT = '微博账号'#your email address
PASSWORD = '微博密码'     #your pw
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
def get_code():
    conn = httplib.HTTPSConnection('api.weibo.com')
    postdata = urllib.urlencode({'client_id':APP_KEY,'response_type':'code','redirect_uri':CALLBACK_URL,'action':'submit','userId':ACCOUNT,'passwd':PASSWORD,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
    conn.request('POST','/oauth2/authorize',postdata,{'Referer':url,'Content-Type': 'application/x-www-form-urlencoded'})
    res = conn.getresponse()
    #print 'headers===========',res.getheaders()
    #print 'msg===========',res.msg
    #print 'status===========',res.status
    #print 'reason===========',res.reason
    #print 'version===========',res.version
    location = res.getheader('location')
    #print location
    code = location.split('=')[1]
    conn.close()
    #print code
    return code
def get_user_id():
	code = get_code()
	r = client.request_access_token(code).uid
	return r
def get_access_token():
	code = get_code()
	r = client.request_access_token(code)
	access_token = r.access_token # The token return by sina
	expires_in = r.expires_in
#save the access token
	client.set_access_token(access_token, expires_in)
	return client
client = get_access_token()
def get_user_info():
	r=client.get.users__show(uid=get_user_id())
	return r
def get_format_time(times):
	return time.strftime("%Y.%m.%d %H:%M:%S", time.strptime("%s"%times, "%a %b %d %H:%M:%S +0800 %Y"))
def repost(ids,text):
	test = client.get.statuses__mentions()
	print test.statuses[0].text,test.statuses[0].user.screen_name
	ids = test.statuses[0].id
	return client.post.statuses__repost(id=ids,status=text)
def post(texts):
	return client.post.statuses__update(status=texts)
def get_mention():
	test = client.get.statuses__mentions().statuses[0]
	return ('%s'+','+'%s'+','+'%s'+','+'%s'+','+'%s')%(get_format_time(test.created_at),test.id,test.user.id,test.user.screen_name,test.text)
def get_comments():
	comments = client.get.comments__to_me(count=1).comments[0].status
	return ('%s'+','+'%s'+','+'%s'+','+'%s'+','+'%s')%(get_format_time(comments.created_at),comments.id,comments.user.id,comments.user.screen_name,comments.text)
def send_comments(ids,texts):
	client.post.comments__create(id=ids,comment=texts)
def post_pic(texts):#post_pic('hello world')
	pics = open('/home/plantpark/Pictures/test.gif','rb')
	return client.upload.statuses__upload(status=texts,pic=pics)



