from django.shortcuts import  render_to_response, get_object_or_404
from fiesta.models import Event, Contact, Ad, get_parishes, get_types, get_costs, get_times
#from django.template import RequestContext
from django.core.context_processors import csrf
from django.conf import settings
import datetime, time,calendar,random
#import random
from django.forms import ModelForm, DateField
#from django.forms.extras import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget 
from django.contrib.auth.decorators import login_required
from django.db.models import DateTimeField

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage

#from datetime import date, datetime, timedelta
#import calendar,time



mnames = "PlaceHolder January February March April May June July August September October November December"
mnames = mnames.split()

def event_detail(request, year, month, day, eventpk):
    date_stamp = time.strptime(year+month+day, "%Y%b%d")
    event_start_date_args =  datetime.date(*date_stamp[:3])
    event = get_object_or_404(Event, event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month, event_start_date__day=event_start_date_args.day, id=eventpk)
    return render_to_response('fiesta/event_detail.html',{'event': event,'media_url':settings.MEDIA_URL})


def event_day(request, year,month,day):
    date_stamp = time.strptime(year+month+day,"%Y%b%d")
    event_start_date_args = datetime.date(*date_stamp[:3])
    event_for_day = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month,event_start_date__day=event_start_date_args.day)
    return render_to_response('fiesta/event_day.html',{'event_day':event_for_day})

def event_month(request,year,month):
    date_stamp = time.strptime(year+month,"%Y%b")
    event_start_date_args = datetime.date(*date_stamp[:3])
    event_for_month = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month)
    return render_to_response('fiesta/event_month.html',{'event_month':event_for_month})

def event_year(request,year):
    date_stamp = time.strptime(year,"%Y")
    event_start_date_args = datetime.date(*date_stamp[:3])
    event_for_year = Event.objects.filter(event_start_date__year=event_start_date_args.year)
    return render_to_response('fiesta/event_year.html',{'event_year':event_for_year})

#--------------------------------------------------------------

#class MyModelForm(ModelForm):
    #def __init__(self, data=None, **keyw):
        #super(MyModelForm, self).__init__(data, **keyw)
        #split_widget = forms.SplitDateTimeWidget()
        #split_widget.widgets[0].attrs = {'class': 'vDateField'}
        #split_widget.widgets[1].attrs = {'class': 'vTimeField'}
        #self.fields["timestamp"].widget = split_widget
    #class Meta:
        #model = models.MyModel

#class EventForm(ModelForm):
    #def __init__(self, data=None,**keyw):
        #super(EventForm,self).__init__(data,**keyw)
        #split_widget = SplitDateTimeWidget(date_format='%Y-%m-%d', time_format='%I:%M%p')
        #split_widget.widgets[0].attrs = {'class':'vDateField'}
        #split_widget.widgets[1].attrs = {'class':'vTimeField'}
        #self.fields["event_start_date"].widget = split_widget
        #self.fields["event_end_date"].widget = split_widget

    #class Meta:
        #model = Event
        #exclude = ["thumbnail","thumbnail2","number_attending","creator","width","height","cost_range"]


#class EventForm(ModelForm):
    ##event_start_date = DateField(widget=SelectDateWidget())
    #event_start_date = DateField(widget=SplitDateTimeWidget())
    #class Meta:
        #model = Event''
        #exclude = ["thumbnail","thumbnail2","number_attending","creator","width","height","cost_range"]
        


    #def __init__(self, *args, **kwargs):
        #super(EventForm, self).__init__(*args,**kwargs)
        #self.fields["event_start_date"].widget = widgets.AdminDateWidget


class EventForm(ModelForm):
    #event_start_date = DateField(widget=SplitDateTimeWidget(date_format='%Y-%m-%d', time_format='%I:%M%p'))
    #event_end_date = DateField(widget=SplitDateTimeWidget(date_format='%Y-%m-%d', time_format='%I:%M%p'))
    #event_start_date = forms.DateField(('%d/%m/%Y,',),label='Start Date',required=True,
            #widget=forms.DateTimeInput(format='%d/%m/%Y',attrs={
                #'class':'input',
                #'readonly':'readonly',
                #'size':'15'
                #})
            #)
    class Meta:
        model = Event
        exclude = ["thumbnail","thumbnail2","number_attending","creator","width","height","cost_range"]
        

@login_required
def manage(request):
    """Manage events for specific user  """
    events = Event.objects.filter(creator=request.user)
    d = dict(events=events,user=request.user,form=EventForm())
    d.update(csrf(request))
    return render_to_response("fiesta/manage.html",d)

def create_date_time(s):
    d = datetime.datetime(*time.strptime(s,"%Y-%m-%d %H:%M%p")[0:6])
    return d

def create_date_time_string(year,month,day,time):
    s = ""
    s = year + "-" + month + "-" + day + " " + time
    return s

def handle_uploaded_file(f):
    filename = f._get_name()
    destination = open(settings.MEDIA_ROOT + "images/" + str(filename),'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return "images/" + str(filename)

@login_required
def add_event(request):
    #title = request.POST.get('title')
    #limitedtextarea = request.POST.get('limitedtextarea')
    #cost = request.POST.get('cost_range')
    #year = request.POST.get('year')
    #month = request.POST.get('month')
    #day = request.POST.get('day')
    #time = request.POST.get('time')
    #endyear = request.POST.get('endyear')
    #endmonth = request.POST.get('endmonth')
    #endday = request.POST.get('endday')
    #endtime = request.POST.get('endtime')
    #city_town = request.POST.get('city_town')
    #etype = request.POST.get('etype')
    #venue = request.POST.get('venue')
    #parish = request.POST.get('parish')
    ##flyer = request.POST.get('flyer')
    #flyer = handle_uploaded_file(request.FILES['flyer'])    
    #start_date = create_date_time(create_date_time_string(year,month,day,time))  
    #end_date = create_date_time(create_date_time_string(endyear,endmonth,endday,endtime))  
    #event = Event(title=title,description=limitedtextarea,cost=cost,event_start_date=start_date,event_end_date=end_date,city_or_town=city_town,parish=parish,flyer=flyer,venue=venue,creator=request.user) 
    #event.save()
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
    if form.is_valid():
        new_event=form.save(commit=False)
        new_event.creator=request.user
        new_event.save()
        return HttpResponseRedirect(reverse("fiesta.views.manage"))
    else:
       form = EventForm()
    return render_to_response('fiesta/create_event.html',{'form':form,
        })


class ContactForm(ModelForm):
    class Meta:
        model = Contact


def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.save()
            return HttpResponseRedirect('/eventcal/main') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render_to_response('fiesta/contact.html', {
        'form': form,
    })



@login_required
def create_event_edit(request,pk):
    event = Event.objects.get(pk=pk)
    form = EventForm(instance=event)
    delete_key = pk

    nyear, nmonth, nday = time.localtime()[:3] 
    tommorrow = datetime.datetime.now() + datetime.timedelta(days=1) 
    tyear, tmonth, tday =  tommorrow.timetuple()[:3]
    today  = datetime.datetime.now()
    weekday = today.weekday()
    current_date_str = [nyear,nmonth,nday,tday,weekday]


    ads_to_display = get_ads()
    upcoming_events = get_upcoming_events(request.user)

    #return render_to_response('fiesta/event_create_edit.html',dict(form=form))
    return render_to_response('fiesta/create_event_edit.html',dict(form=form,upcoming_events=upcoming_events,ads_lst=ads_to_display,current_date_str=current_date_str,media_url=settings.MEDIA_URL,delete_key=delete_key))


@login_required
def create_event(request):
    ads_to_display = get_ads()
    nyear, nmonth, nday = time.localtime()[:3] 
    tommorrow = datetime.datetime.now() + datetime.timedelta(days=1) 
    tyear, tmonth, tday =  tommorrow.timetuple()[:3]
    today  = datetime.datetime.now()
    weekday = today.weekday()
    current_date_str = [nyear,nmonth,nday,tday,weekday]
    year_lst = [nyear,nyear+1]
    month_lst =[]
    day_lst = []
    parish_lst = get_parishes()
    type_lst = get_types()
    #cost_lst = get_costs()
    time_lst = get_times()   
    upcoming_events = get_upcoming_events(request.user)


    for n in range(1,13):
        month_lst.append(n)
    for n in range(1,32):
        day_lst.append(n)
    return render_to_response('fiesta/create_event.html',dict(form=EventForm(),upcoming_events=upcoming_events,ads_lst=ads_to_display,current_date_str=current_date_str,year_lst=year_lst,month_lst=month_lst,day_lst=day_lst,parish_lst=parish_lst,type_lst=type_lst,time_lst=time_lst,media_url=settings.MEDIA_URL,user=request.user))

@login_required
def delete_event(request):
    pk = request.POST.get("delete")
    event = Event.objects.get(pk=pk)
    if request.user == event.creator:
        event.delete()
    return render_to_response('fiesta/manage.html',{})





def get_ads():
    all_ads = list(Ad.objects.all())
    random.shuffle(all_ads)
    return all_ads[:3]

def get_upcoming_events(user=None):
    today = datetime.datetime.now()
    if user == None:
        return Event.objects.filter(event_start_date__gte=today).order_by('event_start_date')[:5]
    else:    
        return Event.objects.filter(event_start_date__gte=today,creator=user).order_by('event_start_date')[:5]

def main(request,year=None,change=None):
    nyear, nmonth, nday = time.localtime()[:3] 
    year_plus_one = nyear + 1
    year_current = nyear
    if year == None :
        year = nyear
    else:
        year = int(year)
    months_year = dict() 
    cal = calendar.Calendar(6)
    upcoming_events_lst = get_upcoming_events()

    #first_ad = random.choice(all_ads)    
    #second_ad = random.choice(all_ads)    
    #third_ad = random.choice(all_ads)    
    #all_ads = list(all_ads)
    ads_to_display = get_ads()
    for month in range(1,13):
        month_days = cal.itermonthdays(year,month)
        lst =[[]]
        week = 0
        for day in month_days:
           events = current = False
           if day:
               events = Event.objects.filter(event_start_date__year=year, event_start_date__month=month,event_start_date__day=day)
               if day == nday and year == nyear and month == nmonth:
                   current = True
           lst[week].append((day,events,current))
           if len(lst[week]) == 7:
               lst.append([])
               week += 1
        months_year[month]=lst
    return render_to_response("fiesta/main.html",dict(year_months_lst=months_year,year=year,year_plus_one=year_plus_one,year_current=year_current,month_names=mnames,upcoming_events=upcoming_events_lst,ads_lst=ads_to_display,media_url=settings.MEDIA_URL,user=request.user))


def mainBackup(request, year, month, change=None):
    """Listing of days in `month`."""
    year, month = int(year), int(month)

    # apply next / previous change
    if change in ("next", "prev"):
        now, mdelta = date(year, month, 15), timedelta(days=31)
        if change == "next":   mod = mdelta
        elif change == "prev": mod = -mdelta

        year, month = (now+mod).timetuple()[:2]

    # init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0

    # make month lists containing list of days for each week
    # each day tuple will contain list of entries and 'current' indicator
    for day in month_days:
        entries = current = False   # are there entries for this day; current day?
        if day:
            entries = Event.objects.filter(date__year=year, date__month=month, date__day=day)
            if day == nday and year == nyear and month == nmonth:
                current = True

        lst[week].append((day, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render_to_response("cal/month.html", dict(year=year, month=month, user=request.user,
                        month_days=lst, mname=mnames[month-1]))


def members(request):
    return render_to_response('fiesta/members.html',dict(user=request.user))

def year(request,year,change=None):
    year = int(year)
    event_for_year = Event.objects.filter(event_start_date__year=year)
    return render_to_response('fiesta/event_year.html',dict(event_year=event_for_year,user=request.user))


def month(request,year,month):
    year = int(year)
    month = int(month)
    event_for_month = Event.objects.filter(event_start_date__year=year,event_start_date__month=month)
    return render_to_response('fiesta/event_month.html',dict(event_month=event_for_month,user=request.user))

def day(request,year,month,day):
    year = int(year)
    month = int(month)
    day = int(day)
    upcoming_events_lst = get_upcoming_events()
    ads_to_display = get_ads()
    ev_date = datetime.date(year,month,day) 
    current_date_str  = ev_date.strftime("%A %B %d %Y")  
    event_for_day = Event.objects.filter(event_start_date__year=year,event_start_date__month=month,event_start_date__day=day)
    return render_to_response('fiesta/event_day.html',dict(media_url=settings.MEDIA_URL,event_day=event_for_day,current_date=current_date_str,upcoming_events=upcoming_events_lst,ads_lst=ads_to_display,user=request.user))

def detail(request,year,month,day,eventpk):
    year = int(year)
    month = int(month)
    day = int(day)
    eventpk=int(eventpk)
    specific_event = get_object_or_404(Event, event_start_date__year=year,event_start_date__month=month, event_start_date__day=day, id=eventpk)
    upcoming_events_lst = get_upcoming_events()
    event_address = specific_event.get_address() 
    ads_to_display = get_ads()
    #return render_to_response('fiesta/event_detail.html',{'event': event,'media_url':settings.MEDIA_URL})
    #event_for_day = Event.objects.filter(event_start_date__year=year,event_start_date__month=month,event_start_date__day=day)
    return render_to_response('fiesta/event_detail.html',dict(event=specific_event,media_url=settings.MEDIA_URL,upcoming_events=upcoming_events_lst,ads_lst=ads_to_display,ev_address=event_address,user=request.user))


def search(request):
    ads_to_display = get_ads()
    nyear, nmonth, nday = time.localtime()[:3] 
    tommorrow = datetime.datetime.now() + datetime.timedelta(days=1) 
    tyear, tmonth, tday =  tommorrow.timetuple()[:3]
    today  = datetime.datetime.now()
    weekday = today.weekday()
    current_date_str = [nyear,nmonth,nday,tday,weekday]
    year_lst = [nyear,nyear+1]
    month_lst =[]
    day_lst = []
    parish_lst = get_parishes()
    type_lst = get_types()
    cost_lst = get_costs()
   
    for n in range(1,13):
        month_lst.append(n)
    for n in range(1,32):
        day_lst.append(n)
    return render_to_response('fiesta/search.html',dict(search_form=None,ads_lst=ads_to_display,current_date_str=current_date_str,year_lst=year_lst,month_lst=month_lst,day_lst=day_lst,parish_lst=parish_lst,type_lst=type_lst,cost_lst=cost_lst,media_url=settings.MEDIA_URL,user=request.user))



def search_results(request):

    ads_to_display = get_ads()
    argumentDict = {}

    queries_without_page = request.GET.copy()
    if queries_without_page.has_key('page'):
        del queries_without_page['page']


    title = request.GET.get('title')
    etype = request.GET.get('etype')
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    cost_range = request.GET.get('cost_range')
    parish = request.GET.get('parish')
    quickyear = request.GET.get('quickyear') 
    quickmonth = request.GET.get('quickmonth') 
    quicktoday = request.GET.get('quicktoday') 
    quicktomorrow = request.GET.get('quicktomorrow') 
    quickweek = request.GET.get('quickweek') 

    if  title:
        argumentDict['title__icontains'] = title 
    if year:
        argumentDict['event_start_date__year'] = year 
    if month:
        argumentDict['event_start_date__month'] = month 
    if day:
        argumentDict['event_start_date__day'] = day 
    if cost_range:
        argumentDict['cost_range'] =  cost_range
    if parish:
        argumentDict['parish'] = parish 
    if etype:
        argumentDict['event_type'] = etype 
    if quickyear:
        argumentDict['event_start_date__year'] = quickyear
    if quickmonth:
        argumentDict['event_start_date__month'] = quickmonth
    if quicktoday:
        argumentDict['event_start_date__day'] = quicktoday
    if quicktomorrow:
        argumentDict['event_start_date__day'] = quicktomorrow
    if quickweek:
        today = datetime.datetime.now()
        next_date = None

        weekday =  today.weekday()

        if weekday == 0:
            next_date = today + datetime.timedelta(days=5)
        if weekday == 1:
            next_date = today + datetime.timedelta(days=4)
        if weekday == 2:
            next_date = today + datetime.timedelta(days=3)
        if weekday == 3:
            next_date = today + datetime.timedelta(days=2)
        if weekday == 4:
            next_date = today + datetime.timedelta(days=1)
        if weekday == 5:
            next_date = today + datetime.timedelta(days=0)
        if weekday == 6:
            next_date = today + datetime.timedelta(days=8)
        argumentDict['event_start_date__gte'] = today
        argumentDict['event_start_date__lt']  = next_date
      
    #if titleBool: 
        #search_results = Event.objects.filter(**argumentDict) 
    #else:
        #search_results = [] 


    search_results = Event.objects.filter(**argumentDict) 


    paginator = Paginator(search_results,3) 
    try:
        page = int(request.GET.get("page",'1'))
    except ValueError:
        page = 1
    try:
        search_results = paginator.page(page)
    except:
        search_results = paginator.page(paginator.num_pages)

    return render_to_response('fiesta/searchresults.html',dict(media_url=settings.MEDIA_URL,ads_lst=ads_to_display,search_results=search_results,queries=queries_without_page,user=request.user))

@login_required
def attend(request):
    #ad  = get_object_or_404(Ad,pk=ad_id) 
    #select_attend = ad.ad_set.get(pk=request.POST['attendance']) 
    a = request.POST
    if "attendance" in a:
        select_attend = Event.objects.get(pk=request.POST["attendance"])
        if select_attend.creator == request.user:
            return render_to_response('fiesta/event_detail.html',{})
            #return HttpResponseRedirect('fiesta/event_detail.html')
        upcoming_events_lst = get_upcoming_events()
        event_address = select_attend.get_address() 
        ads_to_display = get_ads()
        select_attend.number_attending += 1
        select_attend.save()
    #let it return the number_attending so that it can update the detail page
    #return HttpResponseRedirect('',contex_instance=RequestContext(request))
    return render_to_response('fiesta/event_detail.html',add_csrf(request,event=select_attend,media_url=settings.MEDIA_URL,upcoming_events=upcoming_events_lst,ads_lst=ads_to_display,ev_address=event_address,user=request.user))



def add_csrf(request, ** kwargs):
    """Add CSRF and user to dictionary."""
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d


def filter_event_day(request,year,month,day,v_parish,v_event_type,v_cost):
      
    COST = {'0':'0-0','1':'1-500','2':'501-1000','3':'1001-2500','4':'2501-4500','5':'4501-100000' } 

    date_stamp = time.strptime(year+month+day,"%Y%b%d")
    event_start_date_args = datetime.date(*date_stamp[:3])



    if (v_cost != '' and v_event_type=='' and v_parish== '') :
        cost_range = COST[v_cost].split('-') 
        filter_event_for_day = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month,event_start_date__day=event_start_date_args.day,cost__range=(cost_range[0],cost_range[1]))
    
  
    if (v_cost != '' and v_event_type !='' and v_parish== '') :
        cost_range = COST[v_cost].split('-') 
        #event_match = EVENT_TYPES[v_event_type] 
        filter_event_for_day = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month,event_start_date__day=event_start_date_args.day,cost__range=(cost_range[0],cost_range[1]),event_type=v_event_type)

  
    if (v_cost != '' and v_event_type !='' and v_parish != '') :
        cost_range = COST[v_cost].split('-') 
        #event_match = EVENT_TYPES[v_event_type] 
        
        #filter_event_for_day = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month,event_start_date__day=event_start_date_args.day)
        #filter_event_for_day = Event.objects.filter(cost__range=(cost_range[0],cost_range[1]))

        filter_event_for_day = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month,event_start_date__day=event_start_date_args.day,cost__range=(cost_range[0],cost_range[1]),event_type=v_event_type,parish=v_parish)


    if (v_cost != '' and v_event_type == '' and v_parish != '') :
        cost_range = COST[v_cost].split('-') 
        #event_match = EVENT_TYPES[v_event_type] 
        filter_event_for_day = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month,event_start_date__day=event_start_date_args.day,cost__range=(cost_range[0],cost_range[1]),parish=v_parish)


    if (v_cost == '' and v_event_type != '' and v_parish != '') :
        cost_range = COST[v_cost].split('-') 
        #event_match = EVENT_TYPES[v_event_type] 
        filter_event_for_day = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month,event_start_date__day=event_start_date_args.day,parish=v_parish,event_type=v_event_type)


    if (v_cost == '' and v_event_type !='' and v_parish == ''):
        cost_range = COST[v_cost].split('-') 
        #event_match = EVENT_TYPES[v_event_type] 
        filter_event_for_day = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month,event_start_date__day=event_start_date_args.day, event_type=v_event_type)



    if (v_cost == '' and v_event_type =='' and v_parish != '') :
        cost_range = COST[v_cost].split('-') 
        #event_match = EVENT_TYPES[v_event_type] 
        filter_event_for_day = Event.objects.filter(event_start_date__year=event_start_date_args.year,event_start_date__month=event_start_date_args.month,event_start_date__day=event_start_date_args.day,parish=v_parish)

    
    return render_to_response('fiesta/filter_event_day.html',{'filter_event_day':filter_event_for_day},user=request.user)


