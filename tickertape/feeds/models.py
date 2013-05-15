from django.db import models
from django.contrib.auth.models import User
import datetime

class Group(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=200)
	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField()

	@property
	def entry_count(self):
		entry_count = 0
		user_sources = UserSource.objects.filter(group=self)
		for user_source in user_sources:
			entry_count += user_source.source.entry_count
		return entry_count

	def save(self, *args, **kwargs):
	    ''' On save, update timestamps '''
	    if not self.id:
	        self.created = datetime.datetime.today()

	    self.modified = datetime.datetime.today()
	    super(Group, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name


class Source(models.Model):
	text = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	icon_url = models.URLField(max_length=255)
	xml_url = models.URLField(max_length=200)
	html_url = models.URLField(max_length=255)
	feed_type = models.CharField(max_length=200)
	updated_parsed = models.DateTimeField(null=True, blank=True) #feed timestamp
	created = models.DateTimeField(editable=False) #database timestamp
	modified = models.DateTimeField() #database timestamp

	@property
	def entry_count(self):
		return self.entry_set.count()

	def save(self, *args, **kwargs):
	    ''' On save, update timestamps '''
	    if not self.id:
	        self.created = datetime.datetime.today()

	    self.modified = datetime.datetime.today()
	    super(Source, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title

class UserSource(models.Model):
	user = models.ForeignKey(User)
	source = models.ForeignKey(Source)	
	group = models.ForeignKey(Group, null=True, blank=True, default=None)
	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField()

	def save(self, *args, **kwargs):
	    ''' On save, update timestamps '''
	    if not self.id:
	        self.created = datetime.datetime.today()

	    self.modified = datetime.datetime.today()
	    super(UserSource, self).save(*args, **kwargs)




class Entry(models.Model):
	class Meta:
		verbose_name_plural = 'entries'
		ordering = ['published_parsed']

	source = models.ForeignKey(Source)
	feed_id = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	summary = models.TextField()
	author_name = models.CharField(max_length=255)	
	author_href = models.URLField(max_length=255)	
	author_email = models.CharField(max_length=255)
	comments_href = models.URLField(max_length=255)
	content = models.TextField()
	contributors = models.TextField()
	link = models.URLField(max_length=255)
	links = models.TextField()
	raw = models.TextField()
	created_parsed = models.DateTimeField(null=True, blank=True) #feed timestamp
	expired_parsed = models.DateTimeField(null=True, blank=True) #feed timestamp
	published_parsed = models.DateTimeField(null=True, blank=True) #feed timestamp
	updated_parsed = models.DateTimeField(null=True, blank=True) #feed timestamp
	created = models.DateTimeField(editable=False) #database timestamp
	modified = models.DateTimeField() #database timestamp

	def save(self, *args, **kwargs):
	    ''' On save, update timestamps '''
	    if not self.id:
	        self.created = datetime.datetime.today()

	    self.modified = datetime.datetime.today()
	    super(Entry, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title		