from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.contrib.messages import error


# Create your views here.

def index(request):
    return render(request,'travel/index.html')


def create(request):
    errors= User.objects.validate_registration(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user = User.objects.valid_user(request.POST)
        request.session['user_id'] = user.id
        #keeps track of the current user_id that is "logged in", 
        # you can directly use it as argument, no need to pass into parameters: def example(x,y):
        messages.success(request, "registered")
        return redirect ('/success')






def login(request):
    errors= User.objects.validate_login(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user = User.objects.valid_login(request.POST)
        request.session['user_id'] = user.id
        messages.success(request, "Logged in")
        return redirect('/success')



def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'travel/success.html', context)




def logout(request):
    context = {
        'logout': request.session.pop('user_id')
    }
    return render(request,'travel/index.html', context)


################  END END LOGIN END END  ################################################################################


#solo_user = many to many
#primaryuser = Fkey

def home(request):
    user = User.objects.get(id=request.session['user_id'])
    user_trips = Trip.objects.filter(user_solo=request.session['user_id'])
    other_trips = Trip.objects.all().exclude(user_solo=user)

    context = {
        'user': user,
        'user_trips': user_trips,
        'other_trips': other_trips,
    }
    return render(request, 'travel/home.html', context)



def destination(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    trip_user = trip.user_solo.all()

    context = {
        'trip': trip,
        'trip_users': trip_user,
        'current_user': user,
    }
    return render(request, 'travel/destination.html', context)


def add(request):
    print 'add poop'
    return render(request, 'travel/add.html')


def create_trip(request):
    print "+++++++++++++++============++++++"
    errors = Trip.objects.valid_trip(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/add')

    else:
        user = User.objects.get(id=request.session['user_id'])

        trip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], date_start=request.POST['date_start'], date_end=request.POST['date_end'], primaryuser_id=request.session['user_id'])
        trip.user_solo.add(user)
        trip.save()
        return redirect('/home')




def join(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])
    trip.user_solo.add(user)
    trip.save()
    return redirect('/home')

#solo_user = many to many
#primaryuser = Fkey