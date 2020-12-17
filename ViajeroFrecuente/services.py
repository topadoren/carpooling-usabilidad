'''
Created on 28 jul. 2019

@author: Topadora
'''
from _overlapped import NULL
from django.contrib.auth.models import User
from ViajeroFrecuente.models import Vehicle, Trip, Qualification

class ServiceBase():
    
    def RetrieveAll(self):
        return NULL
    
    def RetrieveById(self, idnum):
        return NULL
    
    def DeleteById(self, idnum):
        return NULL
    
    def Delete(self, entity):
        entity.delete()
        return NULL
    
#     def Create(self, entity):
#         entity.save()     
#         return entity
#     
#     def Update(self, entity):
#         entity.update()      
#         return entity


class ServiceUser(ServiceBase):

    '''USER'''

    def RetrieveAll(self):
        return User.objects.all()
 
    def RetrieveById(self, idnum):
        return User.objects.get(id=idnum)
    
    def DeleteById(self, idnum):
        usr = User.objects.get(id=idnum)
        usr.delete()

    #def ValidateUserPass(self, user, pwd):
    #    usr = User.objects.filter(username=user)
    #    
    #    if (usr.count() == 0):
    #        return False
    #    else:
    #        newPwd = Utils.hashPassword(self, pwd)
    #        if (usr.getUsername() == user) and (usr.getPassword() == newPwd):
    #            return True
    #        else:
    #            return False       

#    def Create(self, entity):
#        usrs = AppUser.objects.filter(username=entity.username)
#       if (usrs.count() > 0):
#            raise Exception('User already exists on DB')
#        else:
#            entity.save()     
#            return entity    

class ServiceVehicle(ServiceBase):

    '''VEHICLE'''

    def RetrieveAll(self):
        return Vehicle.objects.all()
 
    def RetrieveById(self, idnum):
        return Vehicle.objects.get(id=idnum)
    
    def DeleteById(self, idnum):
        usr = Vehicle.objects.get(id=idnum)
        usr.delete()

#     def Create(self, entity):
#         return entity.Create()
        
#        '''vhcs = Vehicle.objects.filter(licenseplate=entity.licenseplate)'''
#        '''if (vhcs.count() > 0):'''
#        '''   raise Exception('Vehicle already exists on DB')'''
#        '''else:'''
#        '''    entity.save()'''     
#        '''    return entity'''

class ServiceTrip(ServiceBase):

    '''TRIP'''

    def RetrieveAll(self):
        return Trip.objects.all()
 
    def RetrieveById(self, idnum):
        return Trip.objects.get(id=idnum)
    
    def DeleteById(self, idnum):
        trip = Trip.objects.get(id=idnum)
        trip.delete()
    
    def Create(self, entity):
        
        qs = Trip.objects.filter(trip_tripstatus=1)         
        qs1 = qs.filter(trip_driver=entity.trip_driver.id)
        qs2 = qs.filter(trip_vehicle=entity.trip_vehicle.id)      
        
        if (qs1.count() > 0):
            raise Exception('Driver is assigned to another trip')

        if (qs2.count() > 0):
            raise Exception('Vehicle is assigned to another trip')
        
        if (entity.trip_passengerqty > entity.trip_vehicle.passengerqty):
            raise Exception('Too many passengers for the selected vehicle')
        else:
            entity.save()     
            return entity
        
class ServiceQualification(ServiceBase):

    '''QUALIFICATION'''

    def RetrieveAll(self):
        return Qualification.objects.all()
 
    def RetrieveById(self, idnum):
        return Qualification.objects.get(id=idnum)
    
    def DeleteById(self, idnum):
        qual = Qualification.objects.get(id=idnum)
        qual.delete()