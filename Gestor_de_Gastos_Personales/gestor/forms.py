from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CategoriaGasto, Transaccion, Presupuesto, Ingreso

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaGasto
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['categoria', 'monto', 'fecha', 'descripcion']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['categoria', 'limite']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'limite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['monto', 'fecha', 'descripcion']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FiltroFechaForm(forms.Form):
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
