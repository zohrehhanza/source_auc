from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from time import time
from django.core.validators import *
from django.template.context_processors import request
from django.utils.six import python_2_unicode_compatible
from .settings import MSG_TYPE_MESSAGE
from channels import Group
import json
from django.db.models.signals import pre_save
from django.utils.text import slugify
import datetime

class UserProfile(models.Model):
	user        = models.OneToOneField(User)
	description = models.CharField(max_length=100, default='')
	city        = models.CharField(max_length=100, default='')
	website     = models.URLField(default='')
	phone       = models.IntegerField(default=0)
	image       = models.ImageField(upload_to='profile_image', blank=True,default='\static\person-placeholder.jpg')

	def __str__(self):
		return self.user.username

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

class SearchItem(models.Model):
	search = models.CharField(max_length=50)
	user   = models.ForeignKey(User)


def getImage(instance, filename):
    return "media/image".format(str(time()),filename)
    #return "media/image_{0}_{1}".format(str(time()),filename)


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=getImage)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    minimum_price = models.IntegerField(null=True)
    bid_end_date = models.DateTimeField(default=datetime.datetime.now()+ datetime.timedelta(minutes = 10))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sold = models.BooleanField(default=False)
    sold_to= models.CharField(max_length=50 , blank=True,null=True)
    sold_amount=models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.product_name

def create_room(sender, **kwargs):
    if kwargs['created']:
        room = Room.objects.create(title=kwargs['instance'])

post_save.connect(create_room, sender=Product)


def create_notif_for_product(sender, **kwargs):
    if kwargs['created']:
        notif = Notification.objects.create(notif="product "+ str(kwargs['instance'])+" has been added")

post_save.connect(create_notif_for_product, sender=Product)

class Seller(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_name = models.ForeignKey(User)
    product_id = models.ForeignKey(Product)

    def __unicode__(self):
        return unicodeself(self.user_name)

class Bidder(models.Model):
    numeric = RegexValidator(r'^[0-9]*$', 'Only numerics are allowed.')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_name = models.ForeignKey(User)
    product_id = models.ForeignKey(Product)
    bid_amount = models.CharField(max_length=255, validators=[numeric])



def create_notif_for_bidder(sender, **kwargs):
    if kwargs['created']:
        A=Bidder.objects.filter().last()
        # notif = Notification.objects.create(notif="I bidder")
post_save.connect(create_notif_for_bidder, sender=Bidder)

@python_2_unicode_compatible
class Room(models.Model):
    """
    A room for people to chat in.
    """
    # Room title
    title = models.CharField(max_length=255)
    # If only "staff" users are allowed (is_staff on django's User)

    staff_only = models.BooleanField(default=False)
    slug =models.SlugField(unique=True,null=True)
    ID_product = models.CharField(max_length=10 , null=True)
    def __str__(self):
        return self.title


    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )
def create_slug(instance, new_slug=None):
    slug =slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Room.objects.filter(slug=slug).order_by("-id")
    exists =qs.exists()
    if exists:
        new_slug ="%s-%s"%(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug
def pre_save_room(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug =create_slug(instance)
        instance.title=instance.slug
        instance.ID_product = Product.objects.filter().last().id

pre_save.connect(pre_save_room,sender=Room)

class Notification(models.Model):
    notif = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    sent_to= models.CharField(max_length=300,default="a")

class Notif_for_win(models.Model):
    product =models.CharField(max_length=100,default="")
    notif = models.CharField(max_length=250)
    sold_to= models.CharField(max_length=300,default="a")
    sent= models.BooleanField(default=False)

class Notif_for_seller(models.Model):
    product = models.CharField(max_length=100,default="")
    notif = models.CharField(max_length=250)
    seller= models.CharField(max_length=300,default="a")
    sent= models.BooleanField(default=False)
