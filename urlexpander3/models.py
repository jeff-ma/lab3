from django.db import models

# Create your models here.

class Url_Address(models.Model):
	short_url = models.CharField(max_length=50)
	full_url = models.CharField(max_length=300, default="N/A")
	http_status = models.IntegerField(default=0)
	page_title = models.TextField(default="N/A")
	wayback_url = models.CharField(max_length=300, default="N/A")
	timestamp = models.CharField(max_length=50, default="N/A")
	image = models.CharField(max_length=300, default="N/A")
	created_date = models.CharField(max_length=50, default="N/A")
	updated_date = models.CharField(max_length=50, default="N/A")
	expires_date = models.CharField(max_length=50, default="N/A")
	name = models.CharField(max_length=200, default="N/A")
	organization = models.CharField(max_length=200, default="N/A")
	street1 = models.CharField(max_length=100, default="N/A")
	city = models.CharField(max_length=100, default="N/A")
	state = models.CharField(max_length=100, default="N/A")
	postal_code = models.CharField(max_length=50, default="N/A")
	country = models.CharField(max_length=100, default="N/A")
	email = models.CharField(max_length=100, default="N/A")
	telephone = models.CharField(max_length=50, default="N/A")
	fax = models.CharField(max_length=50, default="N/A")
	domain_name = models.CharField(max_length=100, default="N/A")


	def __str__(self):
		return self.short_url
