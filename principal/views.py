from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.validators import validate_integer
import re
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def inicio(request):
    usuario=request.user     

    if usuario.is_authenticated():
        return render_to_response('base.html', context_instance=RequestContext(request))
    else:
        return render_to_response('base.html', context_instance=RequestContext(request))
    
def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario,password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                #No existe el usuario o la contrasena no es correcta.
                validacion=1
                return render_to_response('ingresar.html',{'validacion':validacion, 'formulario':formulario}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/noFormularioValido')
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))


def registro(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password1']
        clave2 = request.POST['password2']
        if not usuario or not clave or not clave2:
            return HttpResponseRedirect('/rellenarcampos')
        else:
            try:              
                existe = User.objects.get(username=usuario)
                #El usuario ya existe.
                validacion=1
                return render_to_response('registro.html',{'validacion':validacion, 'formulario':formulario}, context_instance=RequestContext(request))
            except:
                try:                        
                    u = formulario.save(commit=False)
                    u.is_superuser = 1
                    u.save()
                except:
                    #contrasenas diferentes
                    validacion=2
                    return render_to_response('registro.html',{'validacion':validacion, 'formulario':formulario}, context_instance=RequestContext(request))
                             
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
    return render_to_response('registro.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')