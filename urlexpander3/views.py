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
import requests
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from mysite.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# Create your views here.

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url="/expander3/login/")
def index(request):
    url_list = Url_Address.objects.all()
    return render(request, 'urlexpander3/index.html', {'url_list' : url_list})

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url="/expander3/login/")
def expand(request):
	shorter_url = request.POST['shorter_url']
	html = urlopen(shorter_url)
	soup = BeautifulSoup(html, 'html.parser')
	url = Url_Address()
	url.short_url = shorter_url
	url.full_url = html.geturl()
	url.http_status = html.getcode()
	url.page_title = soup.html.head.title.contents[0]
	wayback_api = "https://archive.org/wayback/available?url=" + url.full_url
	response = requests.get(wayback_api)
	data = response.json()
	if len(data['archived_snapshots']) > 0:
		url.wayback_url = data['archived_snapshots']['closest']['url']
		url.timestamp = data['archived_snapshots']['closest']['timestamp']
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
	url_list = Url_Address.objects.all()
	return render(request, 'urlexpander3/index.html', {'url_list' : url_list})

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url="/expander3/login/")
def delete(request, url_pk):
	connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = connection.get_bucket('info344lab3')
	k = Key(bucket)
	k.key = 'image' + str(url_pk) + '.jpg'
	bucket.delete_key(k)
	url = get_object_or_404(Url_Address, pk=url_pk)
	url.delete()
	url_list = Url_Address.objects.all()
	return render(request, 'urlexpander3/index.html', {'url_list' : url_list})

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url="/expander3/login/")
@api_view(['GET', 'POST'])
def url_listing(request, format=None):
	if request.method == 'GET':
		urls = Url_Address.objects.all()
		serializer = Url_AddressSerializer(urls, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = Url_AddressSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url="/expander3/login/")
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
		url.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)