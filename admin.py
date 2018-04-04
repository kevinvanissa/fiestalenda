from django.contrib import admin
from fiesta.models import Event, Ad, Contact


class EventAdmin(admin.ModelAdmin):
    list_display= ["title","description","event_start_date","cost","venue","number_attending","event_type","city_or_town","parish","thumbnail_","size","created","creator"]
    list_filter = ["event_type","event_start_date","parish","cost_range"]

    def get_form(self, request, obj=None, **kwargs):
            self.exclude = []	
            self.exclude.append('number_attending')
            self.exclude.append('thumbnail')
            self.exclude.append('thumbnail2')
            self.exclude.append('cost_range')
            self.exclude.append('width')
            self.exclude.append('height')
            return super(EventAdmin, self).get_form(request, obj, **kwargs)


class AdAdmin(admin.ModelAdmin):
    list_display=["title","url","body","ad_start_date","ad_end_date","how_often","adthumbnail_","size","active","creator","created"]
    list_filter =["ad_start_date","ad_end_date","active"]

    def get_form(self, request, obj=None, **kwargs):
                self.exclude = []	
                self.exclude.append('thumbnail')
                self.exclude.append('thumbnail2')
                self.exclude.append('pic_width')
                self.exclude.append('pic_height')
                return super(AdAdmin, self).get_form(request, obj, **kwargs)

class ContactAdmin(admin.ModelAdmin):
    list_display=["subject","message","sender"]
    list_filter = ["sender"]



admin.site.register(Event, EventAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Contact, ContactAdmin)



