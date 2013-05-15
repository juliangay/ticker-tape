from django.contrib import admin
from models import Source, Group, Entry, UserSource

class GroupAdmin(admin.ModelAdmin):
	pass


class UserSourceAdmin(admin.ModelAdmin):
	pass

class SourceAdmin(admin.ModelAdmin):
	pass


class EntryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Entry, EntryAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(UserSource, UserSourceAdmin)
admin.site.register(Group, GroupAdmin)