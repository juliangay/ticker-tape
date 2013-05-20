from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import UploadOpmlFileForm
from models import Source, Group, Entry, UserSource
import xml.etree.ElementTree as ET
import feedparser
from time import mktime
from datetime import datetime


@login_required
def upload_opml_file(request):
    if request.method == 'POST':
        form = UploadOpmlFileForm(request.POST, request.FILES)
        if form.is_valid():
        	#opml_file = request.FILES['file'].read()
        	#tree = ET.parse(opml_file)
        	#root = tree.getroot()
        	#for outline in root.iter('outline'):
			#	source = Source(user=request.user, xml_url=outline.get('xmlUrl'))
			#	source.save()

			Source.objects.all().delete()
			Group.objects.all().delete()

			group = None
			for event, elem in ET.iterparse(request.FILES['file']):
				#import pdb; pdb.set_trace()
				if elem.tag == 'body':
					outlines = list(elem)

					for outline in outlines:
						if 'xmlUrl' not in outline.attrib:
							group = Group(user=request.user, name=outline.attrib['title']) 
							group.save()

							children = list(outline)
							for child in children:
								source = Source()
								source.text = child.attrib['text']
								source.title = child.attrib['title']
								source.feed_type = child.attrib['type'] 
								source.xml_url = child.attrib['xmlUrl']
								source.html_url = child.attrib['htmlUrl']
								source.save()

								user_source = UserSource(user=request.user, source=source, group=group)
								user_source.save()		
						elif 'xmlUrl' in outline.attrib:
							print outline.attrib
							source = Source()
							source.text = outline.attrib['text']
							source.title = outline.attrib['title']
							source.feed_type = outline.attrib['type'] 
							source.xml_url = outline.attrib['xmlUrl']
							source.html_url = outline.attrib['htmlUrl']
							source.save()	

							user_source = UserSource(user=request.user, source=source)
							user_source.save()		

			return HttpResponseRedirect( reverse('entries') )
    else:
        form = UploadOpmlFileForm()

    return render_to_response('feeds/upload_opml.html', {'form': form}, context_instance=RequestContext(request)) 



@login_required
def entries(request, source_id=None, entries_per_page=200):
	user_sources = UserSource.objects.filter(user=request.user)
	if source_id:
		entry_list = Entry.objects.filter(source__usersource__user=request.user,source=source_id).order_by('-published_parsed')
	else:
		entry_list = Entry.objects.filter(source__usersource__user=request.user).order_by('-published_parsed')

	paginator = Paginator(entry_list, entries_per_page)
	groups = Group.objects.filter(user=request.user)

	page = request.GET.get('page')
	try:
		entries = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		entries = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		entries = paginator.page(paginator.num_pages)

	return render_to_response('feeds/entries.html', {'user_sources': user_sources, 'groups': groups, 'entries': entries}, context_instance=RequestContext(request))


@login_required
def pull_feeds(request):
	sources = Source.objects.filter(usersource__user=request.user)

	for source in sources:
		if source.xml_url:
			d = feedparser.parse(source.xml_url)

			#update source with attributes from feed
			if 'icon' in d.feed:
				source.icon_url = d.feed.icon
			if 'updated_parsed' in d.feed and d.feed.updated_parsed is not None:
				source.updated_parsed = datetime.fromtimestamp(mktime(d.feed.updated_parsed))
			source.save()

			#print [field for field in d]
			for e in d['entries']:
				if 'published_parsed' in e:
					entry_published_date = datetime.fromtimestamp(mktime(e.published_parsed)) #feed timestamp
					if source.updated_parsed is None or entry_published_date>source.updated_parsed:
						entry = Entry(source=source, title=e.title, raw=e)
						if 'author_detail' in e:
							if 'name' in e.author_detail:
								entry.author_name = e.author_detail.name	
							if 'href' in e.author_detail:
								entry.author_href = e.author_detail.href
							if 'email' in e.author_detail:
								entry.author_email = e.author_detail.email
						if 'comments' in e:
							entry.comments_href = e.comments
						if 'content' in e:
							entry.content = e.content
						if 'contributors' in e:
							entry.contributors = e.contributors
						if 'link' in e:
							entry.link = e.link
						if 'links' in e:
							entry.links = e.links
						if 'created_parsed' in e:
							entry.created_parsed = datetime.fromtimestamp(mktime(e.created_parsed)) #feed timestamp
						if 'expired_parsed' in e:
							entry.expired_parsed = datetime.fromtimestamp(mktime(e.expired_parsed)) #feed timestamp
						if 'published_parsed' in e:
							entry.published_parsed = datetime.fromtimestamp(mktime(e.published_parsed)) #feed timestamp
						if 'updated_parsed' in e:
							entry.updated_parsed = datetime.fromtimestamp(mktime(e.updated_parsed)) #feed timestamp

						if 'summary' in e:
							entry.summary = e.summary
						entry.save()
				else:
					print 'Entry with no Publication date: %s' % e

	return HttpResponseRedirect( reverse('entries') )
