from django.shortcuts import render, redirect, render_to_response
from .forms import RegistrationForm, EditProfileForm
from django.contrib.auth.decorators import login_required
import random
import sys, os, django
from django.http import *
from django.views.generic import  ListView, TemplateView, CreateView, DetailView, DeleteView
from .models import *
from main.forms import SearchBox
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
import datetime
from django.db.models import Max
import smtplib
from django.template import loader , context
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.http import JsonResponse
sys.path.append("C:/Users/Vaio/Desktop/auction1")
os.environ["DJANGO_SETTINGS_MODULE"]="auction.settings"
django.setup() 
secs=10

def home(request):
    # notifications = Notification.objects.filter(
    #     created__gte=datetime.datetime.now() + timedelta(seconds=secs))
    notifications=Notification.objects.all()[:]
    args = {'notifications': notifications}
    return render(request, 'profile/home.html',args)

def about(request):
    return render(request , 'profile/About.html')
def contact(request):
    return render(request , 'profile/Contact.html')
@login_required
def chat(request):

    rooms = Room.objects.order_by("title")

    return render(request, "index.html", {
        "rooms": rooms,
    })

def save_bid(request):
    context = dict()
    context['product_list'] = Product.objects.get(id=request.POST.get('product_id'))
    context['seller'] = Seller.objects.get(product_id_id=request.POST.get('product_id'))
    try:
        last_bid=Bidder.objects.filter(product_id=request.POST.get('product_id')).last()
        last_bid_amount=last_bid.bid_amount
    except:
        last_bid = Product.objects.get(id=request.POST.get('product_id'))
        last_bid_amount=last_bid.minimum_price
    if request.method == 'POST':
        if int(request.POST.get('minimum_price')) > int(request.POST.get('bid_amount')):
            context['error'] = "bid price should be more than minimum price"
            return render(request, 'main/product_detail.html', context)
        elif int(last_bid_amount) >= int(request.POST.get('bid_amount')):
            context['error'] = "bid price should be higher than last bid amount"
            return render(request, 'main/product_detail.html', context)
        else:
            x = Bidder.objects.filter(product_id=Product.objects.get(id=request.POST.get('product_id'))).values('user_name')
            a = 0
            for item in x:
                if item['user_name'] == request.user.id:
                    y = Bidder.objects.get(user_name=request.user.id, product_id=Product.objects.get(id=request.POST.get('product_id')))
                    y.bid_amount = int(request.POST.get('bid_amount'))
                    y.save()
                    a = 1
                    notif = Notification.objects.create(notif="amount of "+str(y.bid_amount) + " has been claimed for "+ str(y.product_id))

            if not a:
                obj = Bidder(user_name=request.user, product_id=Product.objects.get(id=request.POST.get('product_id')), bid_amount=int(request.POST.get('bid_amount')))
                obj.save()

            return HttpResponseRedirect(reverse('view_product'))
    return render(request, 'main/product_detail.html', context)

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegistrationForm()
    args = {'form': form}
    return render(request, 'profile/reg_form.html/', args)


class homepage(TemplateView):
    template_name= 'profile/homepage.html'

    def get(self, request):
        form = SearchBox()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = SearchBox(request.POST)
        if form.is_valid():
            text = form.cleaned_data['search']
            form = SearchBox()
        notifications = Notification.objects.filter(
            created__gte=datetime.datetime.now() + timedelta(seconds=secs))
        args = {'form':form ,'text':text ,'notifications':notifications}
        return render(request, self.template_name, args)


@login_required
def profile(request):#LoginRequiredMixin,request):
    bidded_products=Bidder.objects.filter(user_name=request.user)
    print(str(request.user))
    my_products=Seller.objects.filter(user_name=request.user)

    bidder_stat = Notif_for_win.objects.filter(sold_to=request.user)
    seller_stat = Notif_for_seller.objects.filter(seller=request.user)


    args={
        'bidded_products':bidded_products,
        'my_products':my_products,
        'bidder_stat':bidder_stat,
        'seller_stat':seller_stat,
    }
    print(len(bidder_stat))
    print(len(bidder_stat))
    print(len(bidder_stat))
    print(len(bidder_stat))
    return render(request,'profile/profile.html',args)
def edit_profile(request):
    login_url = '/login/'
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'profile/edit_profile.html', args)


class ProductView(ListView):
    model=Product
    login_url = '/login/'

    def get_context_data(self , **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context ["notifications"] = Notification.objects.filter(created__gte=datetime.datetime.now() + timedelta(seconds=secs))
        return context


class AddProductView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Product
    fields = ["product_name", "category", "minimum_price", "bid_end_date", "image", "description"]

    def form_valid(self, form):
        obj = Seller(user_name = self.request.user, product_id = form.save())
        obj.save()
        return super(AddProductView, self).form_valid(form)

    def get_success_url(self):
        return reverse('view_product')

class ProductDetailView(LoginRequiredMixin,DetailView):
    model = Product
    context_object_name = 'product_list'
    login_url = '/login/'
 
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        x = Seller.objects.all()
        context["seller"] = Seller.objects.get(product_id_id=self.kwargs['pk'])

        context ["notifications"] = Notification.objects.filter(created__gte=datetime.datetime.now() + timedelta(seconds=secs))
        return context


class BidderListView(LoginRequiredMixin,ListView):
    model = Bidder
    login_url = '/login/'
    def get_queryset(self):
        return Bidder.objects.filter(product_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(BidderListView, self).get_context_data(**kwargs)
        context["product_id"] = self.kwargs['pk']
        context["room"] = Product.objects.get(id= self.kwargs['pk']).product_name
        context["sold"] = Product.objects.get(id=self.kwargs['pk']).sold
        # context ["notifications"] = Notification.objects.filter(created__gte=datetime.datetime.now() + timedelta(seconds=secs))
        Notification.objects.filter().last().notif
        return context

class ProductDelete(DeleteView,LoginRequiredMixin):
    model = Product
    login_url = '/login/'
    def get_context_data(self, **kwargs):
        context = super(ProductDelete, self).get_context_data(**kwargs)
        context["product_id"] = self.kwargs['pk']
        return context
    def get_success_url(self):
        return reverse('view_product')


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")


    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })

@login_required
def index1(request,pk):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")
    print(pk)
    rooms = Room.objects.filter(ID_product=pk)


    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })

def last_notification(request):
    # try:
        username = request.GET.get('username' , None)
        # username=User.module.request.get('request.user')
        print(username)
        print("hello from last_notification")
        p_username = str("+" + username)
        A = Notification.objects.exclude(sent_to__icontains=p_username).filter().first()
        print(A.notif)
        if A:
            A_id = A.id
            B = Notification.objects.get(id=A_id)
            C = Notification.objects.get(id=A_id).sent_to

            AA = Notification.objects.exclude(sent_to__icontains=p_username).filter().first()
            B.sent_to = C + p_username
            B.save()
            note=AA.notif
            print(note)
            notifi = {
                'note': note
            }
    # except:
    #         notifi = {
    #              'note': ""
    #           }
            return JsonResponse(notifi)


def notif_winner(request):
    username = request.GET.get('username' , None)
    # username=User.module.request.get('request.user')
    print(username)
    print("hello from Notif_winner")
    A1 = Notif_for_win.objects.filter(sold_to=username).exclude(sent=True).first()
    print(A1.sold_to)

    note1=A1.notif

    notifi1 ={
        'note1':note1
    }
    A1.sent = True
    A1.save()
    return  JsonResponse(notifi1)

def notif_seller(request):
    username = request.GET.get('username' , None)
    # username=User.module.request.get('request.user')
    print(username)
    print("hello from Notif_seller")
    A2 = Notif_for_seller.objects.filter(seller=username).filter().exclude(sent=True).first()
    print(A2.seller)
    note2 = A2.notif

    A2.sent = True
    A2.save()
    notifi2 = {
        'note2': note2
    }

    return JsonResponse(notifi2)





