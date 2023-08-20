#Estos son los imports que van al inicio de views.py
from todoapp.models import User       

# Create your views here.
from django.shortcuts import render, redirect

# Create your views here.
from todoapp.models import Tarea
from categorias.models import Categoria


def tareas(request):  # the index view
    mis_tareas = Tarea.objects.all()  # quering all todos with the object manager
    categorias = Categoria.objects.all()  # getting all categories with object manager
    
    if request.user.is_authenticated:
        mis_tareas = Tarea.objects.filter(owner=request.user)# quering all todos with the object manager
    else:
        mis_tareas = Tarea.objects.filter(owner=None)

    if request.method == "GET":
        return render(request, "todoapp/index.html", {"tareas": mis_tareas, "categorias": categorias})

    if request.method == "POST":  # revisar si el método de la request es POST
        if "taskAdd" in request.POST:  # verificar si la request es para agregar una tarea (esto está definido en el button)
            titulo = request.POST["titulo"]  # titulo de la tarea
            nombre_categoria = request.POST["selector_categoria"]  # nombre de la categoria
            categoria = Categoria.objects.get(nombre=nombre_categoria)  # buscar la categoría en la base de datos
            contenido = request.POST["contenido"]  # contenido de la tarea

            #Verificar si el usuario inició sesión o no!!
            if request.user.is_authenticated:
                nueva_tarea = Tarea(titulo=titulo, contenido=contenido, categoria=categoria,owner=request.user)  # Crear la tarea
            else:
                nueva_tarea = Tarea(titulo=titulo, contenido=contenido, categoria=categoria)
            nueva_tarea.save()  # guardar la tarea en la base de datos.
            return redirect("/tareas")  # recargar la página.

from django.http import HttpResponseRedirect
from django.contrib import messages
def register_user(request):
    if request.method == 'GET': #Si estamos cargando la página
     return render(request, "todoapp/register_user.html") #Mostrar el template

    elif request.method == 'POST': #Si estamos recibiendo el form de registro
     #Tomar los elementos del formulario que vienen en request.POST
     nombre = request.POST['nombre']
     contraseña = request.POST['contraseña']
     apodo = request.POST['apodo']
     pronombre = request.POST['pronombre']
     mail = request.POST['mail']

     #Crear el nuevo usuario
     user = User.objects.create_user(username=nombre, password=contraseña, email=mail, apodo=apodo, pronombre=pronombre)
     messages.success(request, 'Se creó el usuario para ' + user.apodo)
     
     #Redireccionar la página /tareas
     return HttpResponseRedirect('/tareas')
    
# En el código anterior, cuando el método es POST estamos haciendo lo siguiente:

# - recuperamos los datos que vienen del formulario.
# - creamos un User con estos datos.
# - redirigimos a la página de inicio.
# Atención: En el formulario de registro le pusimos un name a cada <input> y con ese
#  name podemos acceder a los datos en request.POST.


# A continuación está el código que nos permitirá autenticar y loguear al usuario. Este código hace lo siguiente:

# Cuando se recibe el formulario, se guarda en variables el nombre y la contraseña que ingresó el usuario.
# Luego usaremos el método authenticate(user, password) que nos permitirá buscar el usuario con esas credenciales.
# Si authenticate no entrega None, significa que el usuario si existe y podemos hacer login().
# Si el usuario fuera None, significa que no existe un usuario con esas credenciales y se redirige a la vista de registro.
from django.contrib.auth import authenticate, login,logout
def login_user(request):
    if request.method == 'GET':
        return render(request,"todoapp/login.html")
    
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        usuario = authenticate(username=username,password=contraseña)
        if usuario is not None:
            login(request,usuario)
            return HttpResponseRedirect('/tareas')
        else:
            return HttpResponseRedirect('/register')
        
 
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/tareas')