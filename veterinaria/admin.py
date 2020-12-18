from django.contrib import admin
from .models import Usuario, Reserva, Animal
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Reserva)
admin.site.register(Animal)