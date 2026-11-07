from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil, Pieza

class RegistroClienteForm(UserCreationForm):
    rut = forms.CharField(max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PiezaForm(forms.ModelForm):
    class Meta:
        model = Pieza
        fields = ['codigo', 'nombre', 'categoria', 'descripcion', 'precio', 'stock', 'imagen', 'estado', 'vigente']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'vigente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser un valor negativo.")
        return precio