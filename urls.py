from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('fiesta.views',
        (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<eventpk>[1-9]\d*)/$','event_detail','fiesta_event_detail_view'),
        (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$','event_day','event_day_view'),
        (r'^(?P<year>\d{4})/(?P<month>\w{3})/$','event_month'),
        (r'^(?P<year>\d{4})/$','event_year'),
        (r'^main/(\d+)/$','main'),
        (r'^main/$','main'),
        #(r'^main/(\d+)/(\d+)/(prev|next)/$', 'main'),
        #(r'^main/(\d+)/(\d+)/$', 'main'),
        #(r'^main/$', 'main'),
        (r'^attending/$','attend'),
        (r'^year/(\d+)/$','year'),
        (r'^month/(\d+)/(\d+)/$','month'),
        (r'^day/(\d+)/(\d+)/(\d+)/$','day'),
        (r'^detail/(\d+)/(\d+)/(\d+)/(\d+)/$','detail'),
        (r'^search/$','search'),
        (r'^searchresults/$','search_results'),
        (r'^members/$','members'),
        (r'^contact/$','contact'),
        (r'^manage/$','manage'),
        (r'^create_event_edit/(\d+)/$','create_event_edit'),
        (r'^add_event/$','add_event'),
        (r'^create_event/$','create_event'),
        (r'^delete_event/$','delete_event'),
        #(r'^search/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<v_parish>\w*)/(?P<v_event_type>\w*)/(?P<v_cost>\w*)/$','filter_event_day'),
)





