from django import forms

class NewTripForm(forms.Form):
    fromPlace = forms.CharField(label='Desde', max_length=100)
    toPlace = forms.CharField(label='Hasta', max_length=100)
    amount = forms.IntegerField(label='Costo Total')
    passengerqty = forms.IntegerField(label='Cantidad Pasajeros')

class NewVehicleForm(forms.Form):
    model = forms.CharField(label='Modelo', max_length=100)
    licenseplate = forms.CharField(label='Patente', max_length=100)
    passengerqty = forms.IntegerField(label='Pasajeros')

class QualificationForm(forms.Form):
    currentuser = forms.HiddenInput()
    driverid = forms.HiddenInput()
    qualification = forms.IntegerField(label='Calificacion del conductor')