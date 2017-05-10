from .models import Url_Address
from django.shortcuts import render, get_object_or_404
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json
from .serializers import Url_AddressSerializer
from ratelimit.decorators import ratelimit
from boto.s3.connection import S3Connection
from boto.s3.connection import Bucket
from boto.s3.key import Key
from mysite.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import dateutil.parser
import re

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
# Create your views here.

#@ratelimit(key='ip', rate='10/m', block=True)
#@login_required(login_url="/expander3/login/")
def index(request):
    url_list = Url_Address.objects.all().order_by('-id')
    return render(request, 'urlexpander3/index.html', {'url_list' : url_list})

#@ratelimit(key='ip', rate='10/m', block=True)
#@login_required(login_url="/expander3/login/")
def expand(request):
	shorter_url = request.POST['shorter_url']
	pattern = re.compile("^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
	url_match = pattern.match(shorter_url)
	# Check if url is valid
	if url_match is None:
		invalid_url = shorter_url
		url_list = Url_Address.objects.all().order_by('-id')
		return render(request, 'urlexpander3/index.html', {'url_list' : url_list, 'invalid_url' : invalid_url})
	if not shorter_url.startswith("http"):
		shorter_url = "http://" + shorter_url
	try:
		html = requests.get(shorter_url, headers=headers)
	except:
		invalid_url = shorter_url
		url_list = Url_Address.objects.all().order_by('-id')
		return render(request, 'urlexpander3/index.html', {'url_list' : url_list, 'invalid_url' : invalid_url})
	soup = BeautifulSoup(html.text, 'html.parser')
	url = Url_Address()
	url.short_url = shorter_url
	url.full_url = html.url
	url.http_status = html.status_code
	if hasattr(soup.html, "head"):
		url.page_title = soup.html.head.title.contents[0]
	whois_api = "http://www.whoisxmlapi.com/whoisserver/WhoisService?domainName=" + url.short_url + "&username=cru&password=1234567890&outputFormat=JSON"
	whois_response = requests.get(whois_api)
	whois_data = whois_response.json()
	url.domain_name = whois_data['WhoisRecord']
	if "registrant" in whois_data['WhoisRecord']:
		if "createdDate" in whois_data['WhoisRecord']:
			url.created_date = dateutil.parser.parse(whois_data['WhoisRecord']['createdDate']).date()
		if "updatedDate" in whois_data['WhoisRecord']:
			url.updated_date = dateutil.parser.parse(whois_data['WhoisRecord']['updatedDate']).date()
		if "expiresDate" in whois_data['WhoisRecord']:
			url.expires_date = dateutil.parser.parse(whois_data['WhoisRecord']['expiresDate']).date()
		url.name = whois_data['WhoisRecord']['registrant']['name']
		if "organization" in whois_data['WhoisRecord']['registrant']:
			url.organization = whois_data['WhoisRecord']['registrant']['organization']
		if "street1" in whois_data['WhoisRecord']['registrant']:
			url.street1 = whois_data['WhoisRecord']['registrant']['street1']
		if "city" in whois_data['WhoisRecord']['registrant']:
			url.city = whois_data['WhoisRecord']['registrant']['city']
		if "state" in whois_data['WhoisRecord']['registrant']:
			url.state = whois_data['WhoisRecord']['registrant']['state']
		if "postalCode" in whois_data['WhoisRecord']['registrant']:
			url.postal_code = whois_data['WhoisRecord']['registrant']['postalCode']
		if "country" in whois_data['WhoisRecord']['registrant']:
			url.country = whois_data['WhoisRecord']['registrant']['country']
		url.email = whois_data['WhoisRecord']['registrant']['email']
		if "telephone" in whois_data['WhoisRecord']['registrant']:
			url.telephone = whois_data['WhoisRecord']['registrant']['telephone']
		if "fax" in whois_data['WhoisRecord']['registrant']:
			url.fax = whois_data['WhoisRecord']['registrant']['fax']
	else:
		if "registrant" in whois_data['WhoisRecord']['registryData']:
			if "createdDate" in whois_data['WhoisRecord']['registryData']:
				url.created_date = dateutil.parser.parse(whois_data['WhoisRecord']['registryData']['createdDate']).date()
			if "updatedDate" in whois_data['WhoisRecord']['registryData']:
				url.updated_date = dateutil.parser.parse(whois_data['WhoisRecord']['registryData']['updatedDate']).date()
			if "expiresDate" in whois_data['WhoisRecord']['registryData']:
				url.expires_date = dateutil.parser.parse(whois_data['WhoisRecord']['registryData']['expiresDate']).date()
			url.name = whois_data['WhoisRecord']['registryData']['registrant']['name']
			if "organization" in whois_data['WhoisRecord']['registryData']['registrant']:
				url.organization = whois_data['WhoisRecord']['registryData']['registrant']['organization']
			if "street1" in whois_data['WhoisRecord']['registryData']['registrant']:
				url.street1 = whois_data['WhoisRecord']['registryData']['registrant']['street1']
			if "city" in whois_data['WhoisRecord']['registryData']['registrant']:
				url.city = whois_data['WhoisRecord']['registryData']['registrant']['city']
			if "state" in whois_data['WhoisRecord']['registryData']['registrant']:
				url.state = whois_data['WhoisRecord']['registryData']['registrant']['state']
			if "postalCode" in whois_data['WhoisRecord']['registryData']['registrant']:
				url.postal_code = whois_data['WhoisRecord']['registryData']['registrant']['postalCode']
			if "country" in whois_data['WhoisRecord']['registryData']['registrant']:
				url.country = whois_data['WhoisRecord']['registryData']['registrant']['country']
			url.email = whois_data['WhoisRecord']['registryData']['registrant']['email']
			if "telephone" in whois_data['WhoisRecord']['registryData']['registrant']:
				url.telephone = whois_data['WhoisRecord']['registryData']['registrant']['telephone']
			if "fax" in whois_data['WhoisRecord']['registryData']['registrant']:
				url.fax = whois_data['WhoisRecord']['registryData']['registrant']['fax']
	url.domain_name = whois_data['WhoisRecord']['domainName']
	wayback_api = "https://archive.org/wayback/available?url=" + url.full_url
	wayback_response = requests.get(wayback_api)
	wayback_data = wayback_response.json()
	if len(wayback_data['archived_snapshots']) > 0:
		url.wayback_url = wayback_data['archived_snapshots']['closest']['url']
		wayback_timestamp = wayback_data['archived_snapshots']['closest']['timestamp']
		url.timestamp = dateutil.parser.parse(wayback_timestamp[:8]).date() 
	url.save()
	api_key = 'ak-bd2y1-5f3zw-5n7qq-wz0q6-j3str'
	phantom_url = "https://PhantomJsCloud.com/api/browser/v2/" + api_key + "/?request={url:'" + url.full_url + "', renderType:'jpg',outputAsJson:false}"
	image = requests.get(phantom_url)
	connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = connection.get_bucket('info344lab3')
	k = Key(bucket)
	k.key = 'image' + str(url.id) + '.jpg'
	k.set_metadata('Content-Type', 'image/jpg')
	k.set_contents_from_string(image.content)
	url.image = k.key
	url.save()
	url_list = Url_Address.objects.all().order_by('-id')
	return render(request, 'urlexpander3/index.html', {'url_list' : url_list})

#@ratelimit(key='ip', rate='10/m', block=True)
#@login_required(login_url="/expander3/login/")
def delete(request, url_pk):
	connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = connection.get_bucket('info344lab3')
	k = Key(bucket)
	k.key = 'image' + str(url_pk) + '.jpg'
	bucket.delete_key(k)
	url = get_object_or_404(Url_Address, pk=url_pk)
	url.delete()
	url_list = Url_Address.objects.all().order_by('-id')
	return render(request, 'urlexpander3/index.html', {'url_list' : url_list})

#@ratelimit(key='ip', rate='10/m', block=True)
#@login_required(login_url="/expander3/login/")
@api_view(['GET', 'POST'])
def url_listing(request, format=None):
	if request.method == 'GET':
		url_list = Url_Address.objects.all().order_by('-id')
		serializer = Url_AddressSerializer(urls, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		shorter_url = request.data['short_url']
		html = urlopen(shorter_url)
		soup = BeautifulSoup(html, 'html.parser')
		url = Url_Address()
		url.short_url = shorter_url
		url.full_url = html.geturl()
		url.http_status = html.getcode()
		url.page_title = soup.html.head.title.contents[0]
		wayback_api = "https://archive.org/wayback/available?url=" + url.full_url
		wayback_response = requests.get(wayback_api)
		wayback_data = wayback_response.json()
		if len(wayback_data['archived_snapshots']) > 0:
			url.wayback_url = wayback_data['archived_snapshots']['closest']['url']
			url.timestamp = wayback_data['archived_snapshots']['closest']['timestamp']
			request.data['wayback_url'] = url.wayback_url
			request.data['timestamp'] = url.timestamp
		url.save()
		api_key = 'ak-bd2y1-5f3zw-5n7qq-wz0q6-j3str'
		phantom_url = "https://PhantomJsCloud.com/api/browser/v2/" + api_key + "/?request={url:'" + url.full_url + "', renderType:'jpg',outputAsJson:false}"
		image = requests.get(phantom_url)
		connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
		bucket = connection.get_bucket('info344lab3')
		k = Key(bucket)
		k.key = 'image' + str(url.id) + '.jpg'
		k.set_metadata('Content-Type', 'image/jpg')
		k.set_contents_from_string(image.content)
		url.image = k.key
		url.save()
		request.data['full_url'] = url.full_url
		request.data['http_status'] = url.http_status
		request.data['page_title'] = url.page_title
		request.data['image'] = url.image
		serializer = Url_AddressSerializer(data=request.data)
		if serializer.is_valid():
#			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@ratelimit(key='ip', rate='10/m', block=True)
#@login_required(login_url="/expander3/login/")
@api_view(['GET', 'DELETE'])
def url_detail(request, pk, format=None):
	try:
		url = Url_Address.objects.get(pk=pk)
	except Url_Address.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = Url_AddressSerializer(url)
		return Response(serializer.data)

	elif request.method == 'DELETE':
		connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
		bucket = connection.get_bucket('info344lab3')
		k = Key(bucket)
		k.key = 'image' + str(pk) + '.jpg'
		bucket.delete_key(k)
		url.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)