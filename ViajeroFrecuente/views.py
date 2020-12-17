from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from ViajeroFrecuente.models import Trip, Vehicle, AppUser, TripStatus, Qualification
from ViajeroFrecuente.forms import NewTripForm, QualificationForm, NewVehicleForm
from django.template.context_processors import request
from django.template import loader
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import ListView
import datetime

# Create your views here.

@login_required
def triplist(request):
    
    '''TIENE ALGUN VIAJE ACTIVO EL USER'''
    myActiveTrips = Trip.objects.filter(Q(driver = request.user.id) | Q(passengers__id = request.user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 1) | Q(status = 2) | Q(status = 3))
    if (myActiveTrips.count() > 0):
        return HttpResponseRedirect("/ViajeroFrecuente/currenttrip")
    
    template = loader.get_template('triplist.html')

    currentTrips = Trip.objects.filter(Q(status = 1) | Q(status = 2))

    context = {
        'trip_list': currentTrips,
    }
    
    return HttpResponse(template.render(context, request))
@login_required
def main(request):
    current_user = request.user
    if (current_user.username == 'admin'):
            return HttpResponseRedirect("/admin")
    
    '''VIAJES DISPONIBLES'''
    hasActiveTrips = False;

    tripActiveList = Trip.objects.filter(status = 1)
    tripActiveListCount = tripActiveList.count()
    if (tripActiveListCount > 0):
        hasActiveTrips = True;
    
    '''TIENE ALGUN VIAJE ACTIVO EL USER'''
    myActiveTrips = Trip.objects.filter(Q(driver = current_user.id) | Q(passengers__id = current_user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 1) | Q(status = 2) | Q(status = 3))
    if (myActiveTrips.count() > 0):
            return HttpResponseRedirect("/ViajeroFrecuente/currenttrip")
    myActiveTrips = Trip.objects.filter(Q(driver = current_user.id) | Q(passengers__id = current_user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 4))
    if (myActiveTrips.count() > 0):
        trip = myActiveTrips.first()
        quals = Qualification.objects.filter(Q(trip = trip.id) & Q(givenby = request.user.id))    
        if (quals.count() == 0):
            return HttpResponseRedirect("/ViajeroFrecuente/currenttrip")
    
    '''TIENE UN VEHICULO ASOCIADO'''
    vehicleList = Vehicle.objects.filter(drivers__id = current_user.id)
    vehicleListCount = vehicleList.count()
    hasNoVehicle = False
    
    if (vehicleListCount == 0):
        hasNoVehicle = True;
    
    userCredits = AppUser.objects.filter(id = current_user.id).first().credits
    
    quals = Qualification.objects.filter(Q(user = request.user.id))
    
    userrating = NULL
    
    if (quals.count() > 0):
        total = 0
        for qual in quals:
            total = total + qual.givenvalue
        
        userrating = total / quals.count()
    

    template = loader.get_template('home.html')
    context = {
        'has_active_trips': hasActiveTrips,
        'has_no_vehicle': hasNoVehicle,
        'user_credits': userCredits,
        'user_rating' : userrating
    }
    
    return HttpResponse(template.render(context, request))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            authUser = User.objects.filter(username=username)
            usr = AppUser()
            usr.id = authUser.first().id
            usr.credits = 1000
            usr.save()
            
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def newtrip(request):
    
    '''TIENE ALGUN VIAJE ACTIVO EL USER'''
    myActiveTrips = Trip.objects.filter(Q(driver = request.user.id) | Q(passengers__id = request.user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 1) | Q(status = 2) | Q(status = 3))
    if (myActiveTrips.count() > 0):
        return HttpResponseRedirect("/ViajeroFrecuente/currenttrip")
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTripForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            authUser = User.objects.filter(username=request.user.username)
            user_id = authUser.first().id
            
            vehicle = Vehicle.objects.filter(drivers__id = user_id)
            vehicle_id = vehicle.first().id
            
            trip = Trip()
            trip.fromPlace = form.cleaned_data['fromPlace']
            trip.toPlace = form.cleaned_data['toPlace']
            trip.amount = form.cleaned_data['amount']
            trip.passengerqty = form.cleaned_data['passengerqty']
            trip.vehicle = Vehicle.objects.get(id = vehicle_id) 
            trip.driver = User.objects.get(id = user_id)
            trip.status = TripStatus.objects.get(id = 1) 
            
            trip.Save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('main')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTripForm()

    return render(request, 'newtrip.html', {'form': form})

@login_required
def currenttrip(request):
    
    myActiveTrips = Trip.objects.filter(Q(driver = request.user.id) | Q(passengers__id = request.user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 1) | Q(status = 2) | Q(status = 3) | Q(status = 4))
    trip = myActiveTrips.first()
    
    print(trip.status)
    
    if (trip.status.id == 4):
        #print("entre " + request.user.id)
        return HttpResponseRedirect("/ViajeroFrecuente/qualification/" + str(trip.id))
    
    
    drivermode = False
    if (request.user.id == trip.getDriver().id):
        drivermode = True
    
    template = loader.get_template('currenttrip.html')
    context = {
        'trip': trip,
        'currentamount': trip.getCurrentAmount(),
        'passengerqty' : trip.getPassengers().count(),
        'drivermode' : drivermode
    }
    
    return HttpResponse(template.render(context, request))

@login_required
def tripjoin(request, id):
    
    '''TIENE ALGUN VIAJE ACTIVO EL USER'''
    myActiveTrips = Trip.objects.filter(Q(driver = request.user.id) | Q(passengers__id = request.user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 1) | Q(status = 2) | Q(status = 3))
    if (myActiveTrips.count() > 0):
        return HttpResponseRedirect("/ViajeroFrecuente/currenttrip")
    
    authUser = User.objects.get(id=request.user.id)
    trip = Trip.objects.get(id = id)
    trip.AddPassengerToTrip(authUser)
    
    
    # SET NO MORE SPACE    
    if (trip.passengerqty == trip.getPassengers().count()):
        tripstatus = TripStatus.objects.get(id = 3)
        trip.status = tripstatus
        trip.save()
    
    return redirect('currenttrip')

@login_required
def tripclose(request, id):

    # CLOSE    
    trip = Trip.objects.get(id = id)

    tripstatus = TripStatus.objects.get(id = 4)
    trip.status = tripstatus
    trip.save()
    
    for psgr in trip.getPassengers().all():
        appUser = AppUser.objects.get(id = psgr.id)
        appUser.RemoveCredits(trip.getCurrentAmount())
        appUser = AppUser.objects.get(id = request.user.id)
        appUser.AddCredits(trip.getCurrentAmount())
        
    return redirect('/ViajeroFrecuente/qualification/' + id)

@login_required
def tripdetail(request, id):
    
    '''TIENE ALGUN VIAJE ACTIVO EL USER'''
    myActiveTrips = Trip.objects.filter(Q(driver = request.user.id) | Q(passengers__id = request.user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 1) | Q(status = 2) | Q(status = 3))
    if (myActiveTrips.count() > 0):
        return HttpResponseRedirect("/ViajeroFrecuente/currenttrip")
    
    trip = Trip.objects.get(id = id)
    print (trip.status.id)
    if ((trip.status.id == 3) | (trip.status.id == 4) | (trip.status.id == 5)):
        return HttpResponseRedirect("/ViajeroFrecuente/main")
    
    quals = Qualification.objects.filter(Q(user = trip.driver.id))
    
    driverrating = NULL
    
    if (quals.count() > 0):
        total = 0
        for qual in quals:
            total = total + qual.givenvalue
        
        driverrating = total / quals.count()
    
    template = loader.get_template('tripdetail.html')
    context = {
        'trip': trip,
        'minamount': trip.getMinAmount(),
        'maxamount': trip.getMaxAmount(),
        'nextamount': trip.getNextAmount(),
        'driverrating': driverrating
    }
    
    return HttpResponse(template.render(context, request))

@login_required
def qualification(request, id):
    
    '''TIENE ALGUN VIAJE ACTIVO EL USER'''
    myActiveTrips = Trip.objects.filter(Q(driver = request.user.id) | Q(passengers__id = request.user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 1) | Q(status = 2) | Q(status = 3))
    if (myActiveTrips.count() > 0):
        return HttpResponseRedirect("/ViajeroFrecuente/currenttrip")
    
    #qualifications = Qualification.objects.filter(Q(trip = id) & Q(givenby=request.user.id))
    qualifactionTrips = Trip.objects.filter(Q(driver = request.user.id) | Q(passengers__id = request.user.id))
    qualifactionTrips = qualifactionTrips.filter(Q(status = 4))
    if (qualifactionTrips.count() > 0):
        qualifactionTrip = qualifactionTrips.first()
    
    EnableField = [False, False, False, False, False, False, False, False]
    UserName = ['', '', '', '', '', '', '', '']
    
    trip = Trip.objects.filter(id = id).first()
    
    if (request.user.id == trip.getDriver().id):
        users = trip.getPassengers().all()
        for i in range(0, users.count()):
            EnableField[i] = True
            UserName[i] = users[i].username
    else:
        EnableField[0] = True
        UserName[0] = trip.getDriver().username
    
        #drivermode = False
        #if (request.user.id == qualifactionTrip.getDriver().id):
        #    drivermode = True
        #
        #if (drivermode == False):
        #    
        #    form = QualificationForm()
        #    if (qualifications.count() > 0):
        #        return HttpResponseRedirect("/ViajeroFrecuente/main")
        #    
        #else:
        #    
        #    # CAMBIAR ESTO
        #    form = QualificationForm()
        #    
        #    if (qualifications.count() == qualifactionTrip.passengers.count()):
        #        tripstatus = TripStatus.objects.get(id = 5)
        #       qualifactionTrip.status = tripstatus
        #        qualifactionTrip.save()
        #        return HttpResponseRedirect("/ViajeroFrecuente/main")

    template = loader.get_template('qualification.html')
    context = {
        'trip': qualifactionTrip.id,
        #'drivermode' : drivermode,
        #'qualifications': qualifications,
        'enablefield1': EnableField[0],
        'enablefield2': EnableField[1],
        'enablefield3': EnableField[2],
        'enablefield4': EnableField[3],
        'enablefield5': EnableField[4],
        'enablefield6': EnableField[5],
        'enablefield7': EnableField[6],
        'enablefield8': EnableField[7],
        'username1': UserName[0],
        'username2': UserName[1],
        'username3': UserName[2],
        'username4': UserName[3],
        'username5': UserName[4],
        'username6': UserName[5],
        'username7': UserName[6],
        'username8': UserName[7],
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponseRedirect("/ViajeroFrecuente/main")

@login_required
def newvehicle(request):
    
    '''TIENE ALGUN VIAJE ACTIVO EL USER'''
    myActiveTrips = Trip.objects.filter(Q(driver = request.user.id) | Q(passengers__id = request.user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 1) | Q(status = 2) | Q(status = 3))
    if (myActiveTrips.count() > 0):
        return HttpResponseRedirect("/ViajeroFrecuente/currenttrip")
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewVehicleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            authUser = User.objects.filter(username=request.user.username)
            user_id = authUser.first().id
            
            vehicle = Vehicle()
            vehicle.model = form.cleaned_data['model']
            vehicle.licenseplate = form.cleaned_data['licenseplate']
            vehicle.passengerqty = form.cleaned_data['passengerqty']

            vehicle.Save()
            vehicle.addDriver(User.objects.get(id = user_id))
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('main')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewVehicleForm()

    return render(request, 'newvehicle.html', {'form': form})

@login_required
def setqualification(request):
    
    '''TIENE ALGUN VIAJE ACTIVO EL USER'''
    myActiveTrips = Trip.objects.filter(Q(driver = request.user.id) | Q(passengers__id = request.user.id))
    myActiveTrips = myActiveTrips.filter(Q(status = 1) | Q(status = 2) | Q(status = 3))
    if (myActiveTrips.count() > 0):
        return HttpResponseRedirect("/ViajeroFrecuente/currenttrip")
    

    if request.method == 'POST':
        x = 1
        values = []
        
        for param in request.POST.dict():
            text = 'input' + str(x)
            if (text in param):
                values.append(request.POST[param]) 
                x = x + 1
        
        tripid = request.POST['tripid']
        trip = Trip.objects.get(id = tripid)
        
        drivermode = False
        if (trip.getDriver().id == request.user.id):
            drivermode = True    

        if (drivermode):
            x = 0
            for pgr in trip.getPassengers().all():
                    
                    qual = Qualification()
                    qual.date = datetime.datetime.now()
                    qual.givenby = User.objects.get(id = request.user.id)
                    qual.givenvalue = values[x]
                    qual.user = User.objects.get(id = pgr.id)
                    qual.trip = trip
                    x = x + 1
                    qual.save()

                    closedstatus = TripStatus.objects.get(id = 5)
                    trip.status = closedstatus
                    trip.save()
        else:
            qual = Qualification()
            qual.date = datetime.datetime.now()
            qual.givenby = User.objects.get(id = request.user.id)
            qual.givenvalue = request.POST['input1']
            qual.user = User.objects.get(id = trip.getDriver().id)
            qual.trip = trip
            qual.save()

        return HttpResponseRedirect("/ViajeroFrecuente/main")