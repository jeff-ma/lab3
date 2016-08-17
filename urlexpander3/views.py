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

# Create your views here.

@login_required(login_url="/expander3/login/")
def index(request):
    url_list = Url_Address.objects.all()
    return render(request, 'urlexpander3/index.html', {'url_list' : url_list})

#@login_required(login_url="/expander3/login/")
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
	url_list = Url_Address.objects.all()
	return render(request, 'urlexpander3/index.html', {'url_list' : url_list})

#@login_required(login_url="/expander3/login/")
@login_required
def delete(request, url_pk):
	url = get_object_or_404(Url_Address, pk=url_pk)
	url.delete()
	url_list = Url_Address.objects.all()
	return render(request, 'urlexpander3/index.html', {'url_list' : url_list})

#@ratelimit(key='ip', rate='10/m', block=True)
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

@api_view(['GET'])
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