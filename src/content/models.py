from django.db import models

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

def upload_location(instance, filename, **kwargs):
	file_path = 'content/{author_id}/{title}-{filename}'.format(
			author_id=str(instance.author.id), title=str(instance.content_title), filename=filename
		) 
	return file_path


class CMSAuthorContent(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_title = models.CharField(max_length=30,null=False,blank=True)
    content_body = models.TextField(max_length=300, null=False, blank=True)
    content_summary = models.TextField(max_length=60, null=False, blank=True)
    content_file_pdf = models.FileField(upload_to=upload_location, null=False, blank=True)
    content_category = models.CharField(max_length=50, null=False, blank=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.content_title


@receiver(post_delete, sender=CMSAuthorContent)
def submission_delete(sender, instance, **kwargs):
	instance.content_file_pdf.delete(False)

def pre_save_content_post_receiever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.content_title)

pre_save.connect(pre_save_content_post_receiever, sender=CMSAuthorContent)