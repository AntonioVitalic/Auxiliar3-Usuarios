from django.db import models

# Create your models here.
from django.utils import timezone

from categorias.models import Categoria

from django.contrib.auth.models import AbstractUser
# Importante! La clase User tiene que ser la primera clase que aparezca en el modelo.
# El pronombre será un CharField pero solo podrá ser alguna de las opciones definidas en 
# la variable pronombres. El primer elemento del par será el valor del atributo, 
# y el segundo elemneto del par será el valor en lenguaje natural. 
# En este caso les llamaremos igual.
class User(AbstractUser):
  pronombres = [('La','La'),('El','El'), ('Le','Le'),('Otro','Otro')]
  pronombre = models.CharField(max_length=5,choices=pronombres)
  apodo = models.CharField(max_length=30)
    

class Tarea(models.Model):  # Todolist able name that inherits models.Model
    titulo = models.CharField(max_length=250)  # un varchar
    contenido = models.TextField(blank=True)  # un text
    fecha_creación = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))  # un date
    categoria = models.ForeignKey(Categoria, default="general", on_delete=models.CASCADE)  # la llave foránea
    owner = models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.titulo  # name to be shown when called

