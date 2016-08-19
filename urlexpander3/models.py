from django.db import models

# Create your models here.

class Url_Address(models.Model):
	short_url = models.CharField(max_length=50)
	full_url = models.CharField(max_length=300, default="none")
	http_status = models.IntegerField(default=404)
	page_title = models.TextField(default="none")
	wayback_url = models.CharField(max_length=300, default="none")
	timestamp = models.CharField(max_length=50, default="none")
	image = models.CharField(max_length=300, default="none")

	def __str__(self):
		return self.short_url
