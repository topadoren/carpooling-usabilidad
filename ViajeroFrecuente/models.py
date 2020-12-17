# Create your models here.
from django.db import models
from _decimal import Decimal
import datetime
from django.conf import settings
from django.utils.timezone import make_aware
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q 

#class Utils():
#    
#    def encrypt(self, message):
#        newS = ''
#        for car in message:
#            newS = newS + chr(ord(car) + 2)
#        return newS
#    
#    def decrypt(self, message):
#        newS = ''
#        for car in message:
#            newS = newS + chr(ord(car) - 2)
#        return newS

    
# Create your models here.
class AppUser(models.Model):
    #user = 
    #fullname = models.CharField(max_length=255)
    #username = models.CharField(max_length=50, unique=True)
    #password = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)
    credits = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    #reputation = Decimal('0.00')
    
    def __str__(self):
        usr = User.objects.get(id = self.user)
        return usr.get_full_name()
    
    def getfullName(self):
        usr = User.objects.get(id = self.user)
        return usr.get_full_name()

    def getUsername(self):
        usr = User.objects.get(id = self.user)
        return usr.get_username()
    
    #def getPassword(self):
    #    usr = User.objects.get(id = self.user)
    #    return self.password
    
    def getCredits(self):
        usr = User.objects.get(id = self.id)
        return self.credits    
    
    #def getReputation(self):
    #    return self.reputation 

    #def setfullName(self, fullname):
    #    self.fullname = fullname

    #def setUsername(self, username):
    #    self.username = username
    
    #def setPassword(self, password):
    #    self.password = Utils.hashPassword(self, password) 
    
    def setCredits(self, creditsToSet):
        self.credits = creditsToSet

    #def setReputation(self, value):
    #    self.reputation = value

    def AddCredits(self, creditsToAdd):
        self.setCredits(self.getCredits() + creditsToAdd)
        self.save()
        return self.getCredits()
    
    def RemoveCredits(self, creditsToRemove):
        self.setCredits(self.getCredits() - creditsToRemove)
        self.save()
        return self.getCredits()
    
    def GetReputation(self):
        '''quals = Qualification.objects.filter(user__id=user.id)'''
        quals = Qualification.objects.filter(user = self.id).all()
        total = 0
        for qual in quals:
            total = total + qual.givenvalue
        return total / quals.count()
        '''user.setReputation(average)'''
        '''return user'''
   
    #def Save(self):
    #    self.password = Utils().encrypt(self.password) 
    #    self.save()
    #    return self
    
class Vehicle(models.Model):
    
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=255)
    licenseplate = models.CharField(max_length=8, unique=True)
    passengerqty = models.IntegerField(default=0)
    drivers = models.ManyToManyField(User)
    
    def getModel(self):
        return self.model    

    def setModel(self, model):
        self.model = model
        
    def getLicensePlate(self):
        return self.licenseplate    

    def setLicensePlate(self, licenseplate):
        self.licenseplate = licenseplate
        
    def getPassengerQty(self):
        return self.passengerqty    

    def setPassengerQty(self, passengerqty):
        self.passengerqty = passengerqty

    def getDrivers(self):
        return self.drivers    

    def setDrivers(self, drivers):
        self.drivers = drivers    
    
    def addDriver(self, driver):
        self.drivers.add(driver)
    
    def removeDriver(self, driver):
        self.drivers.remove(driver)
    
    def __str__(self):
        return self.model + ' - ' + self.licenseplate

    def AddDriversToVehicle(self, drivers):
        self.drivers.set(drivers)
        return self

    def Save(self):
        self.save()
        return self

# Create your models here.
class TripStatus(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)

    def Save(self):
        self.save()
        return self

# Create your models here.
class Trip(models.Model):
    
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.now())
    fromPlace = models.CharField(max_length=255)
    toPlace = models.CharField(max_length=255)
    amount = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    passengerqty = models.IntegerField(default=0)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver')
    passengers = models.ManyToManyField(User, related_name='passengers', blank=True)
    status = models.ForeignKey(TripStatus, on_delete=models.CASCADE, related_name='trip_status')

    def setTripStatus(self, tripstatus):
        self.trip_tripstatus = tripstatus
        
    def getTripStatus(self):
        return self.trip_tripstatus

    def setTripDate(self, tripDate):
        self.date = tripDate
        
    def getTripDate(self):
        return self.date

    def setTripFrom(self, tripFrom):
        self.fromPlace = tripFrom
        
    def getTripFrom(self):
        return self.fromPlace

    def setTripTo(self, tripto):
        self.toPlace = tripto
        
    def getTripTo(self):
        return self.toPlace

    def setAmount(self, amount):
        self.amount = amount
        
    def getAmount(self):
        return self.amount
    
    def getCurrentAmount(self):
        return self.amount / (self.passengers.count() + 1)

    def getNextAmount(self):
        return self.amount / (self.passengers.count() + 2)
    
    def getMinAmount(self):
        return self.amount / (self.passengerqty + 1)
    
    def getMaxAmount(self):
        return self.amount / 2

    def setPassengerQty(self, passengerqty):
        
        ''' AGREGAR VALIDACION AUTO Y CAPACIDAD'''
        self.passengerqty = passengerqty
        
    def getPassengerQty(self):
        return self.passengerqty

    def setVehicle(self, vehicle):
        
        if (self.hasVehicle()):
            self.vehicle.add(vehicle)
        else:
            raise Exception('This trip already has a vehicle')

    def getVehicle(self):
        return self.vehicle
    
    def hasVehicle(self):
        if (self.vehicle.count() == 1):
            return True
        else: 
            return False
        
    def setDriver(self, driver):
        
        if (self.hasDriver()):
            self.driver.add(driver)
        else:
            raise Exception('This trip already has a driver')

    def getDriver(self):
        return self.driver
    
    def hasDriver(self):
        if (self.driver.count() == 1):
            return True
        else: 
            return False
    
    def getPassengers(self):
        return self.passengers
           
    def removePassenger(self, passenger):
        self.passengers.remove(passenger)
                
    def __str__(self):
        return self.fromPlace + ' - ' + self.toPlace

    def hasEmptySpaceLeft(self):
        if (self.getPassengers().count() == self.passengerqty):
            return False
        else:
            return True 
    
    def CloseTrip(self):
        self.trip_tripstatus_id = 2
        self.save()
        return self

    def Save(self):
        
        #NO ESTOY CONVENCIDO DE ESTO
        qs = Trip.objects.filter(Q(status=1) | Q(status=2) | Q(status=3))         
        qs1 = qs.filter(driver=self.driver.id)
        qs2 = qs.filter(vehicle=self.vehicle.id)      
        
        if (qs1.count() > 0):
            raise Exception('Driver is assigned to another trip')

        if (qs2.count() > 0):
            raise Exception('Vehicle is assigned to another trip')
        
        if (self.passengerqty > self.vehicle.passengerqty):
            raise Exception('Too many passengers for the selected vehicle')
        else:
            self.save()     
            return self

    def AddPassengerToTrip(self, passenger):

        #user = User.objects.filter(username=passenger.username).first()
        appuser = AppUser.objects.get(id = passenger.id)

        if (self.getNextAmount() > appuser.getCredits()):
            raise Exception('Not enough credits to pay for this trip')

        if (self.hasEmptySpaceLeft()):
            self.passengers.add(passenger)
            self.save()     
            return self
        else:
            raise Exception('Max Occupancy reached')


class Qualification(models.Model):

    date = models.DateTimeField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userqual')
    givenby = models.ForeignKey(User, on_delete=models.CASCADE, related_name='givenby')
    givenvalue = models.IntegerField(default=0)
    comments = models.CharField(max_length=255, default=None, blank=True, null=True)
    
    #class Meta:
    #    unique_together = ('trip', 'user', 'givenby')

    def setQualificationDate(self, date):
        self.date = date
    
    def getQualificationDate(self):
        return self.date
   
    def setQualificationTrip(self, trip):
        self.trip = trip
    
    def getQualificationTrip(self):
        return self.trip
    
    def setQualificationUser(self, user):
        self.user = user
    
    def getQualificationUser(self):
        return self.user
    
    def setQualificationGivenBy(self, user):
        self.givenby = user
    
    def getQualificationGivenBy(self):
        return self.givenby  
    
    def setQualificationValue(self, value):
        self.givenvalue = value
    
    def getQualificationValue(self):
        return self.givenvalue

    def __str__(self):
        return self.user + ' - ' + self.givenby + ' - ' + self.date

    def Save(self):
        
        date = datetime.now()      
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)

        if (self.getQualificationUser().id == self.getQualificationGivenBy().id):
            raise Exception('User giving and receiving feedback is the same')
           
        if (self.getQualificationTrip().getTripDate() > date_with_timezone):
            raise Exception('Incorrect Trip Date')
        else:
            self.save()     
            return self
