import datetime
from django.test import TestCase
from ViajeroFrecuente.models import AppUser, Qualification, Trip, Vehicle, TripStatus
from ViajeroFrecuente.services import ServiceUser, ServiceVehicle
from _decimal import Decimal
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import timedelta
from django.contrib.auth.models import User

# Create your tests here.
class AppUserModelTests(TestCase):

    def test_create_user(self):

        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'    
        usr = usr.save()
        savedUsr = User.objects.first()
        
        usr2 = AppUser()
        usr2.id = savedUsr.id
        usr2.credits = 1
        usr2.save()

        savedUsr = AppUser.objects.first()
        self.assertIsNotNone(savedUsr)
 
    def test_assign_initial_credits(self):

        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'    
        usr = usr.save()
        savedUsr = User.objects.first()
        
        usr2 = AppUser()
        usr2.id = savedUsr.id
        usr2.credits = 400
        usr2.save()

        savedUsr = AppUser.objects.first()

        self.assertEqual(savedUsr.getCredits(), Decimal('400.00'))
         
    def test_add_credits(self):

        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'    
        usr = usr.save()
        savedUsr = User.objects.first()
        
        usr2 = AppUser()
        usr2.id = savedUsr.id
        usr2.credits = 400
        usr2.save()

        savedUsr = AppUser.objects.first()
        newCredits = savedUsr.AddCredits(100)  
        self.assertEqual(newCredits, Decimal('500.00'))
 
    def test_remove_credits(self):

        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'    
        usr = usr.save()
        savedUsr = User.objects.first()
        
        usr2 = AppUser()
        usr2.id = savedUsr.id
        usr2.credits = 400
        usr2.save()

        savedUsr = AppUser.objects.first()
        newCredits = savedUsr.RemoveCredits(100)  
        self.assertEqual(newCredits, Decimal('300.00'))
 
#    def test_validate_user_and_pass(self):
#
#        usr = AppUser()
#        originalPwd = 'pwd1'
#        usr.fullname = 'TEST NOMBRE COMPLETO'
#        usr.username = 'TEST1'
#        usr.password = originalPwd
#        usr.credits = 400
#         
#        usr.Save()
#         
#        savedUsr = ServiceUser().RetrieveAll().first()
#
#        self.assertEqual(savedUsr.getUsername(), usr.username)         
#        self.assertEqual(savedUsr.getPassword(), Utils().encrypt(originalPwd))
         
    def test_get_reputation(self):

        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'    
        usr = usr.save()
        savedUsr = User.objects.get(id = 1)
        
        usrCol = [savedUsr]
        
        usr1 = AppUser()
        usr1.id = savedUsr.id
        usr1.credits = 2000
        usr1.save()

        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST2'
        usr.password = 'pwd1'    
        usr = usr.save()
        savedUsr = User.objects.get(id = 2)
        
        usr2 = AppUser()
        usr2.id = savedUsr.id
        usr2.credits = 2000
        usr2.save()

        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST3'
        usr.password = 'pwd1'    
        usr = usr.save()
        savedUsr = User.objects.get(id = 3)
        
        usr3 = AppUser()
        usr3.id = savedUsr.id
        usr3.credits = 2000
        usr3.save()
          
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
         
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVE"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.date = date_with_timezone
        trip.amount = 1000
        trip.driver = User.objects.get(id = 1)
        trip.fromPlace = 'ORIGEN'
        trip.toPlace = 'DESTINO'
        trip.passengerqty = 5
        trip.vehicle = vehicle
        trip.status = tripStatus
         
        trip = trip.Save()

        trip.AddPassengerToTrip(User.objects.get(id = 2))
        trip.AddPassengerToTrip(User.objects.get(id = 3))
        
        tripStatus = TripStatus()
        tripStatus.description = "CLOSED"
        tripStatus = tripStatus.Save()
        trip.CloseTrip()
         
        qual = Qualification()
        qual.date = date_with_timezone
        qual.givenby = User.objects.get(id = 2)
        qual.user = User.objects.get(id = 1)
        qual.trip = trip
        qual.givenvalue = 5
         
        qual = qual.save()
         
        qual = Qualification()
        qual.date = date_with_timezone
        qual.givenby = User.objects.get(id = 3)
        qual.user = User.objects.get(id = 1)
        qual.trip = trip
        qual.givenvalue = 4
         
        qual = qual.save()
        
        reputation = AppUser.objects.get(id = 1).GetReputation()
        
        '''qualUser = ServiceUser.GetReputationByUser(self, savedUsr)'''
         
        self.assertEqual(reputation, Decimal('4.5'))

    def test_create_two_users_with_same_login(self):
        
        usr = User()
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr = usr.save()
        
        usr2 = User()
        usr2.username = 'TEST1'
        usr2.password = 'pwd1'
        usr2.credits = 400
         
        with self.assertRaises(Exception) as context:
            usr2.save()

        self.assertEqual('UNIQUE constraint failed: auth_user.username', context.exception.args[0]) 

class VehicleModelTests(TestCase):

    def test_create(self):

        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        savedVehicle = ServiceVehicle().RetrieveById(vehicle.id)

        self.assertIsNotNone(savedVehicle)
        
    def test_add_driver_to_vehicle(self):

        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        savedVehicle = Vehicle.objects.get(id = 1)
        
        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO1'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        #usr.credits = 400
         
        usr = usr.save()
        savedUsr1 = User.objects.get(id = 1)
        
        usrCol = [savedUsr1]

        savedVehicle.AddDriversToVehicle(usrCol)

        self.assertEqual(vehicle.drivers.count(), 1)  

    def test_create_two_vehicles_with_same_licenseplate(self):
        
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        vehicle2 = Vehicle()
        vehicle2.model = 'FORD FOCUS'
        vehicle2.licenseplate = 'ABC123'
        vehicle2.passengerqty = 5
         
        with self.assertRaises(Exception) as context:
            vehicle2 = vehicle2.Save()

        self.assertEqual('UNIQUE constraint failed: ViajeroFrecuente_vehicle.licenseplate', context.exception.args[0]) 

class TripModelTests(TestCase):

    def test_create(self):

        usr = User()
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr.save()
        savedUsr = User.objects.get(id = 1)
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
         
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVO"
        tripStatus = tripStatus.Save() 
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.date = date_with_timezone
        trip.amount = 1000
        trip.driver = savedUsr
        trip.fromPlace = 'ORIGEN'
        trip.toPlace = 'DESTINO'
        trip.passengerqty = 5
        trip.vehicle = vehicle
        trip.status = tripStatus
              
        savedTrip = trip.Save()

        self.assertIsNotNone(savedTrip)

    def test_trip_has_more_passengers_than_vehicle(self):
        
        usr = User()
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr.save()
        savedUsr = User.objects.get(id = 1)
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVO"
        tripStatus = tripStatus.Save()  
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.date = date_with_timezone
        trip.amount = 100
        trip.driver = savedUsr
        trip.fromPlace = 'ORIGEN'
        trip.toPlace = 'DESTINO'
        trip.passengerqty = 6
        trip.vehicle = vehicle
        trip.status = tripStatus
         
        with self.assertRaises(Exception) as context:
            trip.Save()
            
        self.assertEqual('Too many passengers for the selected vehicle', context.exception.args[0]) 

    def test_trip_has_no_available_space(self):
        
        usr = User()
        #usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr.save()
        savedUsr = User.objects.get(id = 1)
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.date = date_with_timezone
        trip.amount = 200
        trip.driver = savedUsr
        trip.fromPlace = 'ORIGEN'
        trip.toPlace = 'DESTINO'
        trip.passengerqty = 2
        trip.vehicle = vehicle
        trip.status = tripStatus
        
        savedTrip = trip.Save()

        usr = User()
        #usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr1 = usr.save()
        
        appuser1 = AppUser()
        appuser1.id = User.objects.get(id = 2).id
        appuser1.credits = 1000
        appuser1.save()

        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO2'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr2 = usr.save()
        
        appuser2 = AppUser()
        appuser2.id = User.objects.get(id = 3).id
        appuser2.credits = 1000
        appuser2.save()

        usr = User()
        #usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO3'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr3 = usr.save()

        appuser3 = AppUser()
        appuser3.id = User.objects.get(id = 4).id
        appuser3.credits = 1000
        appuser3.save()

        savedTrip.AddPassengerToTrip(User.objects.get(id = 2))
        savedTrip.AddPassengerToTrip(User.objects.get(id = 3))

        with self.assertRaises(Exception) as context:
            savedTrip.AddPassengerToTrip(User.objects.get(id = 4))
            
        self.assertEqual('Max Occupancy reached', context.exception.args[0]) 

    def test_passenger_has_no_enough_credits_to_pay_trip(self):

        usr1 = User()
        usr1.username = 'PASAJERO1'
        usr1.password = 'pwd1'   
        usr1.save()
        
        appuser1 = AppUser()
        appuser1.id = User.objects.get(id = 1).id
        appuser1.credits = 1000
        appuser1.save()
        
        savedUsr = User.objects.get(id = 1)
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.date = date_with_timezone
        trip.amount = 400
        trip.driver = savedUsr
        trip.fromPlace = 'ORIGEN'
        trip.toPlace = 'DESTINO'
        trip.passengerqty = 5
        trip.vehicle = vehicle
        trip.status = tripStatus
        
        savedTrip = trip.Save()

        usr2 = User()
        usr2.username = 'PASAJERO2'
        usr2.password = 'pwd1'   
        usr2.save()
        
        appuser2 = AppUser()
        appuser2.id = User.objects.get(id = 2).id
        appuser2.credits = 100
        appuser2.save()

        with self.assertRaises(Exception) as context:
            savedTrip.AddPassengerToTrip(usr2)
            
        self.assertEqual('Not enough credits to pay for this trip', context.exception.args[0]) 

    def test_driver_has_another_active_trip(self):

        usr1 = User()
        usr1.username = 'DRIVER1'
        usr1.password = 'pwd1'   
        usr1.save()
        
        appuser1 = AppUser()
        appuser1.id = User.objects.get(id = 1).id
        appuser1.credits = 1000
        appuser1.save()
        
        savedUsr = User.objects.get(id = 1)
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        vehicle2 = Vehicle()
        vehicle2.model = 'FORD FOCUS'
        vehicle2.licenseplate = 'ABC124'
        vehicle2.passengerqty = 5
        
        vehicle2 = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
         
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVO"
        tripStatus = tripStatus.Save() 
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.date = date_with_timezone
        trip.amount = 1000
        trip.driver = savedUsr
        trip.fromPlace = 'ORIGEN'
        trip.toPlace = 'DESTINO'
        trip.passengerqty = 5
        trip.vehicle = vehicle
        trip.status = tripStatus
         
        trip.Save()

        '''CREATE TRIP'''
        trip2 = Trip()
        trip2.date = date_with_timezone
        trip2.amount = 1000
        trip2.driver = savedUsr
        trip2.fromPlace = 'ORIGEN'
        trip2.toPlace = 'DESTINO'
        trip2.passengerqty = 5
        trip2.vehicle = vehicle2
        trip2.status = tripStatus         

        with self.assertRaises(Exception) as context:
            trip2.Save()
            
        self.assertEqual('Driver is assigned to another trip', context.exception.args[0]) 

    def test_vehicle_has_another_active_trip(self):

        '''USUARIO 1'''
        usr1 = User()
        usr1.username = 'DRIVER1'
        usr1.password = 'pwd1'   
        usr1.save()
        
        appuser1 = AppUser()
        appuser1.id = User.objects.get(id = 1).id
        appuser1.credits = 1000
        appuser1.save()
        
        '''USUARIO 2'''
        usr2 = User()
        usr2.username = 'DRIVER2'
        usr2.password = 'pwd1'   
        usr2.save()
        
        appuser2 = AppUser()
        appuser2.id = User.objects.get(id = 2).id
        appuser2.credits = 1000
        appuser2.save()
         
        '''CREATE 1 VEHICLE'''   
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        vehicle.drivers.set([usr1])
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
         
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVO"
        tripStatus = tripStatus.Save() 
         
        '''CREATE TRIP 1'''
        trip1 = Trip()
        trip1.date = date_with_timezone
        trip1.amount = 1000
        trip1.driver = usr1
        trip1.fromPlace = 'ORIGEN'
        trip1.toPlace = 'DESTINO'
        trip1.passengerqty = 5
        trip1.vehicle = vehicle
        trip1.status = tripStatus
         
        trip1 = trip1.Save()

        '''CREATE TRIP 2'''
        trip2 = Trip()
        trip2.date = date_with_timezone
        trip2.amount = 1000
        trip2.driver = usr2
        trip2.fromPlace = 'ORIGEN'
        trip2.toPlace = 'DESTINO'
        trip2.passengerqty = 5
        trip2.vehicle = vehicle
        trip2.status = tripStatus         

        with self.assertRaises(Exception) as context:
            trip2 = trip2.Save()
            
        self.assertEqual('Vehicle is assigned to another trip', context.exception.args[0]) 

class QualificationModelTests(TestCase):

    def test_create(self):
        
        usr1 = User()
        usr1.username = 'DRIVER1'
        usr1.password = 'pwd1'   
        usr1.save()
        
        appuser1 = AppUser()
        appuser1.id = User.objects.get(id = 1).id
        appuser1.credits = 1000
        appuser1.save()
        
        savedUsr = User.objects.get(id = 1)
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.date = date_with_timezone
        trip.amount = 200
        trip.driver = savedUsr
        trip.fromPlace = 'ORIGEN'
        trip.toPlace = 'DESTINO'
        trip.passengerqty = 5
        trip.vehicle = vehicle
        trip.status = tripStatus
        
        savedTrip = trip.Save()

        usr1 = User()
        usr1.username = 'DRIVER2'
        usr1.password = 'pwd1'   
        usr1.save()
        
        appuser2 = AppUser()
        appuser2.id = User.objects.get(id = 2).id
        appuser2.credits = 1000
        appuser2.save()

        savedTrip = savedTrip.AddPassengerToTrip(User.objects.get(id = 2))

        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)

        qual = Qualification()
        qual.setQualificationDate(date_with_timezone)
        qual.setQualificationTrip(savedTrip)
        qual.setQualificationUser(savedUsr)
        qual.setQualificationGivenBy(User.objects.get(id = 2))
        qual.setQualificationValue(5)
        
        savedQual = qual.Save()

        self.assertIsNotNone(savedQual)

    def test_qualification_has_a_future_date(self):
        
        usr1 = User()
        usr1.username = 'DRIVER1'
        usr1.password = 'pwd1'   
        usr1.save()
        
        appuser1 = AppUser()
        appuser1.id = User.objects.get(id = 1).id
        appuser1.credits = 1000
        appuser1.save()
        
        savedUsr = User.objects.get(id = 1)
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now() + timedelta(days=1)       
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.date = date_with_timezone
        trip.amount = 200
        trip.driver = savedUsr
        trip.fromPlace = 'ORIGEN'
        trip.toPlace = 'DESTINO'
        trip.passengerqty = 5
        trip.vehicle = vehicle
        trip.status = tripStatus
        
        savedTrip = trip.Save()

        usr = User()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO2'
        usr.password = 'pwd1'
        #usr.credits = 400

        psngr = usr.save()
        
        appuser1 = AppUser()
        appuser1.id = User.objects.get(id = 2).id
        appuser1.credits = 1000
        appuser1.save()
        
        savedTrip = savedTrip.AddPassengerToTrip(User.objects.get(id = 2))

        date = datetime.datetime.now()       
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)

        qual = Qualification()
        qual.setQualificationDate(date_with_timezone)
        qual.setQualificationTrip(savedTrip)
        qual.setQualificationUser(savedUsr)
        qual.setQualificationGivenBy(User.objects.get(id = 2))
        qual.setQualificationValue(5)
        
        with self.assertRaises(Exception) as context:
            qual.Save()
            
        self.assertEqual('Incorrect Trip Date', context.exception.args[0])       

    def test_qualification_is_given_by_same_user(self):
        
        usr1 = User()
        usr1.username = 'DRIVER1'
        usr1.password = 'pwd1'   
        usr1.save()
        
        appuser1 = AppUser()
        appuser1.id = User.objects.get(id = 1).id
        appuser1.credits = 1000
        appuser1.save()
        
        savedUsr = User.objects.get(id = 1)
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now() + timedelta(days=1)       
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.date = date_with_timezone
        trip.amount = 200
        trip.driver = savedUsr
        trip.fromPlace = 'ORIGEN'
        trip.toPlace = 'DESTINO'
        trip.passengerqty = 5
        trip.vehicle = vehicle
        trip.status = tripStatus
        
        savedTrip = trip.Save()
        
        usr2 = User()
        usr2.username = 'DRIVER2'
        usr2.password = 'pwd1'   
        usr2.save()
        
        appuser2 = AppUser()
        appuser2.id = User.objects.get(id = 2).id
        appuser2.credits = 1000
        appuser2.save()
        
        savedUsr = User.objects.get(id = 2)
         
        usrCol = [savedUsr]
                
        savedTrip = savedTrip.AddPassengerToTrip(User.objects.get(id = 2))

        date = datetime.datetime.now()       
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)

        qual = Qualification()
        qual.setQualificationDate(date_with_timezone)
        qual.setQualificationTrip(savedTrip)
        qual.setQualificationUser(savedUsr)
        qual.setQualificationGivenBy(savedUsr)
        qual.setQualificationValue(5)
        
        with self.assertRaises(Exception) as context:
            qual.Save()
            
        self.assertEqual('User giving and receiving feedback is the same', context.exception.args[0])                       

#class UtilsTests(TestCase):
#    
#        def test_is_encryption_working(self):
#            
#            text = "AHI VIENE LA PRUEBA!"
#            cryptText = Utils.encrypt(self, text)
#            self.assertEqual(text, Utils.decrypt(self, cryptText))
