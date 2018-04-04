from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
from PIL import Image as PImage
from settings import MEDIA_ROOT
from string import join
from django.core.files import File
from os.path import join as pjoin
from tempfile import *

PARISH = (
('KNG','Kingston'),
('STAND','St. Andrew'),
('STCAT','St. Catherine'),
('STHOM','St. Thomas'),
('STMA','St. Mary'),
('PLND','Portland'),
('STNN','St. Ann'),
('MAN','Manchester'),
('CLAR','Clarendon'),
('TREL','Trelawny'),
('STJ','St. James'),
('WES','Westmoreland'),
('HAN','Hanover'),
('STE','St. Elizabeth'),
)

EVENT_TYPES = (
('PTY','Party'),
('DHLL','Dancehall'),
('GOS','Gospel'),
('FES','Festival'),
('CLU','Club'),
('CON','Concert'),
('SP','Sport'),
('OTH','Other Events'),
)

AD_HOW_OFTEN=(
(1,1),        
(2,2),        
(3,3),        
(4,4),        
(5,5),        
)

EVENT_COST_RANGE=(
(0,'0-0'),        
(1,'1-500'),        
(2,'501-1000'),        
(3,'1001-2500'),        
(4,'2501-4500'),        
(5,'4501-100000'),        
)

EVENT_TIME=(
        ("12:00am","12:00am"),
        ('12:30 am','12:30 am'),
        ('1:00 am','1:00 am'),
        ('1:30 am','1:30 am'),
        ('2:00 am','2:00 am'),
        ('2:30 am','2:30 am'),
        ('3:00 am','3:00 am'),
        ('3:00 am','3:00 am'),
        ('3:30 am','3:30 am'),
        ('4:00 am','4:00 am'),
        ('4:30 am','4:30 am'),
        ('5:00 am','5:00 am'),
        ('5:30 am','5:30 am'),
        ('6:00 am','6:00 am'),
        ('6:30 am','6:30 am'),
        ('7:00 am','7:00 am'),
        ('7:30 am','7:30 am'),
        ('8:00 am','8:00 am'),
        ('8:30 am','8:30 am'),
        ('9:00 am','9:00 am'),
        ('10:00 am','10:00 am'),
        ('10:30 am','10:30 am'),
        ('11:00 am','11:00 am'),
        ('11:30 am','11:30 am'),
        ('12:00 pm','12:00 pm'),
        ('12:30 pm','12:30 pm'),
        ('1:00 pm','1:00 pm'),
        ('1:30 pm','1:30 pm'),
        ('2:00 pm','2:00 pm'),
        ('2:30 pm','2:30 pm'),
        ('3:00 pm','3:00 pm'),
        ('3:30 pm','3:30 pm'),
        ('4:00 pm','4:00 pm'),
        ('4:30 pm','4:30 pm'),
        ('5:00 pm','5:00 pm'),
        ('5:30 pm','5:30 pm'),
        ('6:00 pm','6:00 pm'),
        ('6:30 pm','6:30 pm'),
        ('7:00pm','7:00pm'),
        ('7:30 pm','7:30 pm'),
        ('8:00 pm','8:00 pm'),
        ('8:30 pm','8:30 pm'),
        ('9:00 pm','9:00 pm'),
        ('9:30 pm','9:30 pm'),
        ('10:00 pm','10:00 pm'),
        ('10:30 pm','10:30 pm'),
        ('11:00 pm','11:00 pm'),
        ('11:30 pm','11:30 pm'),
)

#FIXME: WILL NOT RETURN PROPER RESULT WHEN RANGE IS 0-0
def range_bool(num_to_check,start_range,end_range):
    """docstring for range_bool"""
    if ((num_to_check >= start_range) and (num_to_check <= end_range)):
        return True
    else:
        return False

def get_parish_dict(parish_abbrev):
    parish_dict = dict() 
    for p_abbrev, p_name in PARISH:
        parish_dict[p_abbrev]= p_name 
    return parish_dict[parish_abbrev]

def get_parishes():
    #parish_dict = dict() 
    #for p_abbrev, p_name in PARISH:
        #parish_dict[p_abbrev]= p_name 
    #return parish_dict
    return PARISH

def get_times():
    #time_dict = dict()
    #for t_abbrev, t_name in EVENT_TIME:
        #time_dict[t_abbrev]=t_name
    return EVENT_TIME
    #return time_dict

def get_costs():
    #cost_dict = dict() 
    #for c_abbrev, c_range in EVENT_COST_RANGE:
        #cost_dict[c_abbrev]= c_range 
    #return cost_dict
    return EVENT_COST_RANGE 

def get_types():
    #type_dict = dict() 
    #for t_abbrev, t_name in EVENT_TYPES:
        #type_dict[t_abbrev]= t_name 
    #return type_dict
    return EVENT_TYPES 


class Event(models.Model):
    title = models.CharField(max_length=250,help_text='You must enter a title')
    description =  models.TextField() 
    event_start_date = models.DateTimeField() 
    event_end_date = models.DateTimeField(blank=True,null=True) 
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    cost_range = models.IntegerField(null=True, blank=True, choices=EVENT_COST_RANGE)
    venue = models.CharField(max_length=250) 
    event_type = models.CharField(max_length=5,choices=EVENT_TYPES)
    city_or_town = models.CharField(max_length=100)
    parish =  models.CharField(max_length=5,choices=PARISH)
    flyer = models.ImageField(upload_to="images/")
    width = models.IntegerField(blank=True, null=True) 
    height = models.IntegerField(blank=True, null=True) 
    thumbnail = models.ImageField(upload_to="images/",blank=True, null=True)
    thumbnail2 = models.ImageField(upload_to="images/",blank=True, null=True)
    number_attending = models.IntegerField(blank=True, null=True,default=0,help_text='Leave Blank, will be populated when users select')
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
   
    def __unicode__(self):
        return self.title

    def get_address(self):
        return "%s %s %s %s" % (self.venue,self.city_or_town,get_parish_dict(self.parish),"Jamaica") 


    def save(self, *args, **kwargs):
        super(Event,self).save(*args, **kwargs)
        im = PImage.open(os.path.join(MEDIA_ROOT, self.flyer.name))
        self.width, self.height = im.size

        #large thumbnail
        fn, ext = os.path.splitext(self.flyer.name)
        im.thumbnail((128,128), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb2" + ext
        tf2 = NamedTemporaryFile()
        im.save(tf2.name, "JPEG")
        self.thumbnail2.save(thumb_fn,File(open(tf2.name)), save=False)
        tf2.close()

        #small thumbnail
        im.thumbnail((40,40), PImage.ANTIALIAS)
        thumb_fn = fn +"-thumb" + ext
        tf = NamedTemporaryFile()
        im.save(tf.name, "JPEG")
        self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)
        tf.close()

        event_cost_length = len(EVENT_COST_RANGE)
        cost_range_selected=None
        for eachcost in range(0,event_cost_length):
            elem = EVENT_COST_RANGE[eachcost]
            elem_range = (EVENT_COST_RANGE[eachcost][1]).split('-')
            if range_bool(self.cost,int(elem_range[0]),int(elem_range[1])) :
                cost_range_selected = eachcost
                break
        if not cost_range_selected:
            if cost_range_selected == 0:
                cost_range_selected = 0
            else:
                cost_range_selected = event_cost_length - 1
        self.cost_range = cost_range_selected 

        super(Event, self).save(*args, **kwargs)

    def size(self):
        return "%s x %s" % (self.width, self.height)

    def thumbnail_(self):
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="40" /></a> """ % (( self.flyer.name,self.thumbnail.name))

    thumbnail_.allow_tags = True



class Ad(models.Model):
    title = models.CharField(max_length=20,help_text='Ad must have a title')
    url = models.URLField(help_text='Enter the web address of the organization associated with this Ad',null=True, blank=True)
    body = models.TextField()
    pic = models.ImageField(upload_to='imagesAds')
    pic_height = models.IntegerField(help_text='You must enter a picture height',blank=True,null=True)
    pic_width =  models.IntegerField(help_text='You must enter a picture width',blank=True,null=True)
    ad_start_date = models.DateField()
    ad_end_date = models.DateField()
    how_often = models.IntegerField(choices=AD_HOW_OFTEN,help_text='These numbers will dictate how often the ad will appear. 5 will appear the most often')
    thumbnail = models.ImageField(upload_to="images/",blank=True, null=True)
    thumbnail2 = models.ImageField(upload_to="images/",blank=True, null=True)
    active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super(Ad, self).save(*args, **kwargs)
        im = PImage.open(os.path.join(MEDIA_ROOT, self.pic.name))
        #self.pic_width, self.pic_height = im.size

 
        #large thumbnail
        fn, ext = os.path.splitext(self.pic.name)
        im.thumbnail((80,80), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb2" + ext
        tf2 = NamedTemporaryFile()
        im.save(tf2.name, "JPEG")
        self.thumbnail2.save(thumb_fn,File(open(tf2.name)), save=False)
        tf2.close()
        self.pic_width, self.pic_height = im.size
        
        #small thumbnail
        im.thumbnail((40,40), PImage.ANTIALIAS)
        thumb_fn = fn +"-thumb" + ext
        tf = NamedTemporaryFile()
        im.save(tf.name, "JPEG")
        self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)
        tf.close()

        super(Ad, self).save(*args, **kwargs)
                 


    def size(self):
        return "%s x %s" % (self.pic_width, self.pic_height)

    def adthumbnail_(self):
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="40" /></a> """ % (( self.thumbnail2.name,self.thumbnail.name))

    adthumbnail_.allow_tags = True


    def __unicode__(self):
        return self.title


class Contact(models.Model):
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=200)
    sender = models.EmailField()

    def __unicode__(self):
        return self.subject


