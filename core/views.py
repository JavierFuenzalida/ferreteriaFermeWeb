import json
import cx_Oracle
import re
import hashlib
from datetime import datetime
from django.http.response import Http404, HttpResponse
from django.core import paginator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
from django.contrib import messages
from django.http import JsonResponse, request, Http404
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.db.models import Sum
from io import BytesIO
from xhtml2pdf import pisa
from .models import *
import cloudinary.uploader




# Create your views here.
#validacion de acceso


@login_required(login_url='/login/')
def mostrar_acceso_denegado(request):
    return render(request, 'core/Acceso_denegado.html')

def es_administrador(user):
    return user.groups.filter(name='SuperUsuarioGrupo').exists()

def es_cliente(user):
    return user.groups.filter(name='ClienteGrupo').exists()

def es_proveedor(user):
    return user.groups.filter(name='ProveedorGrupo').exists()
	
def es_administrador_o_empleado(user):
    return user.groups.filter(name__in=['SuperUsuarioGrupo', 'EmpleadoGrupo']).exists()
#end validacion de acceso


#Base
def buscar_producto_json(request, nombreProducto):
    if request.is_ajax():
        if request.method == 'GET':
            lista_productos = []
            for producto in buscar_producto(nombreProducto):
                data_producto = {}
                data_producto['id'] = str(producto[0])
                data_producto['descripcion'] = str(producto[1])
                data_producto['foto'] = str(producto[2])
                lista_productos.append(data_producto)
            data = json.dumps(lista_productos)
            return HttpResponse(data, 'application/json')


def buscar_producto(nombreProducto):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_PRODUCTO", [nombreProducto, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


#end Base

def home(request):
    if Group.objects.filter(name='ClienteGrupo').count() < 1:
        Group.objects.create(name='ClienteGrupo')

    if Group.objects.filter(name='EmpleadoGrupo').count() < 1:
        Group.objects.create(name='EmpleadoGrupo')

    if Group.objects.filter(name='ProveedorGrupo').count() < 1:
        Group.objects.create(name='ProveedorGrupo')

    if Group.objects.filter(name='SuperUsuarioGrupo').count() < 1:
        Group.objects.create(name='SuperUsuarioGrupo')

    data = {
        'pinturas': listado_productos_por_categoria(203),
        'iluminacion': listado_productos_por_categoria(205)
        
    }

    return render(request, 'core/Home.html', data)


def login(request):
    return render(request, 'registration/login.html')


def mostrar_registro_cliente(request):
    return render(request, 'modal/nuevo_cliente.html')


def mostrar_registro_cliente_empresa(request):
    return render(request, 'modal/nuevo_cliente_empresa.html')


def registrar_cliente_natural(request):

    if request.method == 'POST':
        rut = request.POST['rut_cli']
        nombres = request.POST['nombre_cli']
        apellidos = request.POST['apellido_cli']
        fecha = change_date_format(request.POST['naci_cli'])
        fono = request.POST['fono_cli']
        email = request.POST['mail_cli']
        usernamee = request.POST['username_cli']
        password1 = request.POST['password1_cli']
        password2 = request.POST['password2_cli']
        tipo = 1#natural

    try:
        salida = sp_agregar_cliente(
            usernamee, rut, nombres, apellidos, fecha, fono, email, tipo)
        print('=================creado tabla cliente')
        user = User.objects.create_user(
            username=usernamee, email=email, password=password2)
        print('=================creado tabla user django')
        groupCliente = Group.objects.get(name='ClienteGrupo')
        user.groups.add(groupCliente)
        print('=================grupo asignado user django')

        if salida == 1:
            messages.success(request, "Registrado Correctamente")
            
        else:
            messages.error(request, "Error Al registrar al Usuario")
            
    except:
        messages.error(request, "Error Al registrar al Usuario")
    return redirect('login')    

def registrar_cliente_empresa(request):

    if request.method == 'POST':
        rut = request.POST['rut_cli']
        nombres = request.POST['nombre_cli']
        fono = request.POST['fono_cli']
        email = request.POST['mail_cli']
        usernamee = request.POST['username_cli']
        password2 = request.POST['password2_cli']
        tipo = 2#empresa

    try:
        salida = sp_agregar_cliente(
            usernamee, rut, nombres, None, None, fono, email, tipo)
        print('=================creado tabla cliente')
        user = User.objects.create_user(
            username=usernamee, email=email, password=password2)
        print('=================creado tabla user django')
        groupCliente = Group.objects.get(name='ClienteGrupo')
        user.groups.add(groupCliente)
        print('=================grupo asignado user django')

        if salida == 1:
            messages.success(request, "Registrado Correctamente")
            
        else:
            messages.error(request, "Error Al registrar al Usuario")
            
    except:
        messages.error(request, "Error Al registrar al Usuario")
    return redirect('login')

def sp_agregar_cliente(username, rut, nombres, apellidos, macimeinto, fono, email, tipo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_CLIENTE', [
                    username, rut, nombres, apellidos, macimeinto, fono, email, tipo, salida])
    return salida.getvalue()




@login_required(login_url='/login/')
@user_passes_test(es_cliente, login_url='/acceso-denegado/')
def mostrar_datos_cuenta(request):
    print(request.user.username)
    id_usuario = Usuario.objects.get(username=request.user.username)
    cliente = Cliente.objects.get(id_usuario=id_usuario)
    
    data = {
        'id_usuario': id_usuario,
        'cliente': cliente

    }

    return render(request, 'core/Datos_cuenta.html', data)


def mostrar_actualizar_datos_cuenta(request):
    print(request.user.username)
    id_usuario = Usuario.objects.get(username=request.user.username)
    cliente = Cliente.objects.get(id_usuario=id_usuario)
    
    data = {
        'cliente': cliente

    }

    return render(request, 'modal/actualizar_cliente.html', data)



def mostrar_actualizar_datos_cuenta_empresa(request):
    print(request.user.username)
    id_usuario = Usuario.objects.get(username=request.user.username)
    cliente = Cliente.objects.get(id_usuario=id_usuario)
    
    data = {
        'cliente': cliente

    }

    return render(request, 'modal/actualizar_cliente_empresa.html', data)


def actualizar_datos_cuenta(request):

    rut = request.POST['rut_cli']
    nombres = request.POST['nombre_cli']
    ape = request.POST['apellido_cli']
    fecha = request.POST['naci_cli']
    fono = request.POST['fono_cli']
    email = request.POST['mail_cli']

    try:
        User.objects.filter(username=request.user.username).update(email=email)

        UsuarioOra = Usuario.objects.filter(username=request.user.username).first()

        Cliente.objects.filter(id_usuario=UsuarioOra.id_usuario).update(
            rut_cli=rut ,nombres=nombres, apellidos=ape, nacimiento=fecha, fono=fono, email=email)

        messages.success(request, "Actualizado Correctamente")
    except:
        messages.error(request, "No se ha podido Actualizar los datos")
    return redirect('micuenta')

def actualizar_datos_cuenta_empresa(request):

    rut = request.POST['rut_cli']
    nombres = request.POST['nombre_cli']
    fono = request.POST['fono_cli']
    email = request.POST['mail_cli']

    try:
        User.objects.filter(username=request.user.username).update(email=email)

        UsuarioOra = Usuario.objects.filter(username=request.user.username).first()

        Cliente.objects.filter(id_usuario=UsuarioOra.id_usuario).update(
            rut_cli=rut ,nombres=nombres, fono=fono, email=email)

        messages.success(request, "Actualizado Correctamente")
    except:
        messages.error(request, "No se ha podido Actualizar los datos")
    return redirect('micuenta')

    






####################  USUARIOS
def validate_username(request, username):
    if request.is_ajax():
        if request.method == 'GET':
            nro = User.objects.filter(username=username).count()
            
            if nro > 0:
                mensaje = '1'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response

def validate_email(request, email):
    if request.is_ajax():
        if request.method == 'GET':
            nro = User.objects.filter(email=email).count()
            
            if nro > 0:
                mensaje = '1'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response

def validate_update_email(request, id, email):
    if request.is_ajax():
        if request.method == 'GET':
            id_usu = Usuario.objects.get(id_usuario=id)
            nro = User.objects.filter(email=email).exclude(username=id_usu.username).count()
            
            if nro > 0:
                mensaje = '1'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response

def validate_rut_empleado(request, rut):
    if request.is_ajax():
        if request.method == 'GET':
            nro = Empleado.objects.filter(rut_emp=rut).count()
            
            if nro > 0:
                mensaje = '1'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response

def validate_rut_proveedor(request, rut):
    if request.is_ajax():
        if request.method == 'GET':
            nro = Proveedor.objects.filter(rut_provee=rut).count()
            
            if nro > 0:
                mensaje = '1'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
###
def validate_update_rut_empleado(request, id, rut):
    if request.is_ajax():
        if request.method == 'GET':

            nro = Empleado.objects.filter(id_usuario=id, rut_emp=rut).count()
            us = Empleado.objects.filter(rut_emp=rut).exclude(id_usuario=id).count()
            
            if nro > 0:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                if us > 0:
                    mensaje = '1'
                    response = JsonResponse({'mensaje': mensaje})
                    response.status_code = 200
                    return response
                else:
                    mensaje = '0'
                    response = JsonResponse({'mensaje': mensaje})
                    response.status_code = 200
                    return response


def validate_update_username_empleado(request, id, username):
    if request.is_ajax():
        if request.method == 'GET':

            nro = Usuario.objects.filter(id_usuario=id, username=username).count()
            us = User.objects.filter(username=username).count()
            
            if nro > 0:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                if us > 0:
                    mensaje = '1'
                    response = JsonResponse({'mensaje': mensaje})
                    response.status_code = 200
                    return response
                else:
                    mensaje = '0'
                    response = JsonResponse({'mensaje': mensaje})
                    response.status_code = 200
                    return response

def validate_update_rut_proveedor(request, id, rut):
    if request.is_ajax():
        if request.method == 'GET':

            nro = Proveedor.objects.filter(id_usuario=id, rut_provee=rut).count()
            us = Proveedor.objects.filter(rut_provee=rut).exclude(id_usuario=id).count()
            
            if nro > 0:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                if us > 0:
                    mensaje = '1'
                    response = JsonResponse({'mensaje': mensaje})
                    response.status_code = 200
                    return response
                else:
                    mensaje = '0'
                    response = JsonResponse({'mensaje': mensaje})
                    response.status_code = 200
                    return response

def validate_update_rut_cliente(request, id, rut):
    if request.is_ajax():
        if request.method == 'GET':

            nro = Cliente.objects.filter(id_usuario=id, rut_cli=rut).count()
            us = Cliente.objects.filter(rut_cli=rut).exclude(id_usuario=id).count()
            
            if nro > 0:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                if us > 0:
                    mensaje = '1'
                    response = JsonResponse({'mensaje': mensaje})
                    response.status_code = 200
                    return response
                else:
                    mensaje = '0'
                    response = JsonResponse({'mensaje': mensaje})
                    response.status_code = 200
                    return response

def validate_rut_cliente(request, rut):
    if request.is_ajax():
        if request.method == 'GET':

            nro = Cliente.objects.filter(rut_cli=rut).count()
            
            if nro > 0:
                mensaje = '1'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response
            else:
                mensaje = '0'
                response = JsonResponse({'mensaje': mensaje})
                response.status_code = 200
                return response

@login_required(login_url='/login/')
@user_passes_test(es_administrador, login_url='/acceso-denegado/')
def mostrar_agregar_usuario(request):
    empleados = Empleado.objects.all()
    proveedores = Proveedor.objects.all()

    data = {
        'empleados': empleados,
        'proveedores': proveedores
    }

    return render(request, 'core/Agregar_usuario.html', data)


def mostrar_agregar_empledo(request):
    cargo = Cargo.objects.all()
    data = {
        'cargo': cargo

    }

    return render(request, 'modal/nuevo_empleado.html', data)


def mostrar_agregar_proveedor(request):
    rubro = Rubro.objects.all()
    data = {
        'rubro': rubro

    }

    return render(request, 'modal/nuevo_proveedor.html', data)
    


def agregar_proveedor(request):
    if request.method == 'POST':
        rut = request.POST['rut_pro']
        nombre = request.POST['nombre_pro']
        usernamee = request.POST['username_pro']
        password = request.POST['password_pro']
        password2 = request.POST['password2_pro']
        email = request.POST['mail_pro']
        fono = request.POST['fono_pro']
        rubro = request.POST['rubro_pro']

    if password != password2:
        messages.error(
            request, "LA CONTRASEÑA NO ES IGUAL A SU CONFIRMACION")
        return redirect('nuevo-usuario')

    try:
        salida = sp_agregar_proveedor(
            usernamee, rut, nombre, fono, rubro)
        print('=================creado tabla proveedor')
        user = User.objects.create_user(
            username=usernamee, email=email, password=password2)
        print('=================creado tabla user django')
        groupProo = Group.objects.get(name='ProveedorGrupo')
        user.groups.add(groupProo)
        print('=================grupo asignado user django')

        if salida == 1:
            messages.success(request, "Registrado Correctamente")
            return redirect('nuevo-usuario')
        else:
            messages.error(request, "Error Al registrar al Usuario")
            return redirect('nuevo-usuario')
    except:
        messages.error(request, "Error Al registrar al Usuario")
    return redirect('nuevo-usuario')

def agregar_empleado(request):
    if request.method == 'POST':
        rut = request.POST['rut_emp']
        nombres = request.POST['nombres_emp']
        apellidos = request.POST['apellidos_emp']
        usernamee = request.POST['username_emp']
        password = request.POST['password_emp']
        password2 = request.POST['password2_emp']
        email = request.POST['mail_emp']
        cargo = request.POST['cargo_emp']

    try:
        new_pass = encrypt_string(password2)
        print(new_pass)

        salida = sp_agregar_empleado(
            usernamee, new_pass, rut, nombres, apellidos, cargo)
        print('=================creado tabla empleado')
        if cargo != '1':
            user = User.objects.create_user(
                username=usernamee, email=email, password=password2)
            print('=================creado tabla user django')
            if cargo == '3':
                groupAdm = Group.objects.get(name='SuperUsuarioGrupo')
                user.groups.add(groupAdm)
                print('=================grupo asignado user django como SuperUsuarioGrupo')
            else:
                groupEmp = Group.objects.get(name='EmpleadoGrupo')
                user.groups.add(groupEmp)
                print('=================grupo asignado user django')
        else:
            user = User.objects.create_user(
                username=usernamee, email=email, password=password2,  is_active=0)
            print('=================creado tabla user django como vendedor')

        if salida == 1:
            messages.success(request, "Registrado Correctamente")
            return redirect('nuevo-usuario')
        else:
            messages.error(request, "Error Al registrar al Usuario")
            return redirect('nuevo-usuario')
    except:
        messages.error(request, "Error Al registrar al Usuario")
    return redirect('nuevo-usuario')


def actualizar_empleado(request):
    if request.method == 'POST':
        id_usu = request.POST['id_usu']
        rut = request.POST['rut_emp']
        nombres = request.POST['nombres_emp']
        apellidos = request.POST['apellidos_emp']
        cargo = request.POST['cargo_emp']
        usernamee = request.POST['username_emp']
    try:
        Empleado.objects.filter(id_usuario=id_usu).update(
            rut_emp=rut, nombres=nombres, apellidos=apellidos, id_cargo=cargo)
        userOra = Usuario.objects.get(id_usuario=id_usu)
        userDJ = User.objects.get(username=userOra.username)
        userDJ.groups.clear()
        User.objects.filter(username=userOra.username).update(
            username=usernamee)
        Usuario.objects.filter(id_usuario=id_usu).update(username=usernamee)
        
        if cargo == '3':
            groupAdm = Group.objects.get(name='SuperUsuarioGrupo')
            userDJ.groups.add(groupAdm)
            print('=================grupo asignado user django como SuperUsuarioGrupo')
        else:
            groupEmp = Group.objects.get(name='EmpleadoGrupo')
            userDJ.groups.add(groupEmp)
            print('=================grupo asignado user django')

        messages.success(request, "Actualizado Correctamente")
        
    except:
        messages.error(request, "Error Al Actualizar Usuario")
        
    return redirect('nuevo-usuario')


def actualizar_proveedor(request):
    if request.method == 'POST':
        id_usu = request.POST['id_usu']
        rut = request.POST['rut_pro']
        nombre = request.POST['nombre_pro']
        celular = request.POST['fono_pro']
        rubro = request.POST['rubro_pro']
        usernamee = request.POST['username_pro']
    try:
        Proveedor.objects.filter(id_usuario=id_usu).update(
            rut_provee=rut, nombre=nombre, celular=celular, id_rubro=rubro)
        userOra = Usuario.objects.get(id_usuario=id_usu)
        #userDJ = User.objects.get(username=userOra.username)
        # userDJ.groups.clear()
        User.objects.filter(username=userOra.username).update(
            username=usernamee)
        Usuario.objects.filter(id_usuario=id_usu).update(username=usernamee)

        messages.success(request, "Actualizado Correctamente")
        return redirect('nuevo-usuario')
    except:
        messages.error(request, "Error Al Actualizar Usuario")
        return redirect('nuevo-usuario')
    return redirect('nuevo-usuario')


def eliminar_empleado(request, id):

    try:
        Empleado.objects.filter(id_usuario=id).delete()
        UserOra = Usuario.objects.get(id_usuario=id)
        User.objects.filter(username=UserOra.username).delete()
        Usuario.objects.filter(id_usuario=id).delete()

        messages.success(request, 'Usuario Eliminado Correctamente')
    except:
        messages.error(request, 'Error Al Eliminar Usuario')

    return redirect('nuevo-usuario')


def eliminar_proveedor(request, id):

    try:
        Proveedor.objects.filter(id_usuario=id).delete()
        UserOra = Usuario.objects.get(id_usuario=id)
        User.objects.filter(username=UserOra.username).delete()
        Usuario.objects.filter(id_usuario=id).delete()

        messages.success(request, 'Usuario Eliminado Correctamente')
    except:
        messages.error(request, 'Error Al Eliminar Usuario')

    return redirect('nuevo-usuario')


def sp_agregar_proveedor(username, rut, nombre, fono, rubro):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_PROVEEDOR', [
                    username, rut, nombre, fono, rubro, salida])
    return salida.getvalue()


def sp_agregar_empleado(username, password, rut, nombres, apellidos, cargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_EMPLEADO', [
                    username, password, rut, nombres, apellidos, cargo, salida])
    return salida.getvalue()


def mostrar_actualizar_empleado(request, id):

    empleado = Empleado.objects.get(id_usuario=id)
    usuarioOra = Usuario.objects.get(id_usuario=id)
    cargo = Cargo.objects.all()
    data = {
        'empleado': empleado,
        'cargo': cargo,
        'usuarioOra': usuarioOra
    }

    return render(request, 'modal/actualizar_empleado.html', data)


def mostrar_actualizar_proveedor(request, id):

    proveedor = Proveedor.objects.get(id_usuario=id)
    usuarioOra = Usuario.objects.get(id_usuario=id)
    rubro = Rubro.objects.all()
    data = {
        'proveedor': proveedor,
        'rubro': rubro,
        'usuarioOra': usuarioOra
    }

    return render(request, 'modal/actualizar_proveedor.html', data)

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
#################### FIN USUARIOS






#################### Producto
def detalles_producto(request, idProducto):
    
    producto = Producto.objects.get(id_producto=idProducto)
    foto = FotoProd.objects.get(id_producto=idProducto)
    proveedor = Proveedor.objects.get(id_usuario=producto.id_usuario)
    productosHerramientas = listado_productos_por_categoria(201)
    productospinturas = listado_productos_por_categoria(203)
    productosbaldozas = listado_productos_por_categoria(206)

    data = {
        'producto':producto,
        'foto':foto,
        'proveedor': proveedor,
        'productosHerramientas': productosHerramientas,
        'productospinturas': productospinturas,
        'productosbaldozas':productosbaldozas
    }

    return render(request, 'core/Detalle_producto.html', data)

@login_required(login_url='/login/')
@user_passes_test(es_administrador_o_empleado, login_url='/acceso-denegado/')
def mostrar_agregar_producto(request):
    familia = FamiliaProd.objects.all()
    proveedor = Proveedor.objects.all()

    data = {
        'familia': familia,
        'proveedor': proveedor,
        'productos': listado_productos()
    }

    return render(request, 'core/Agregar_producto.html', data)


def tipo_producto_por_familia(request):
    idfamilia = request.GET.get('idfamilia')
    data = {
        'tipoProdcuto': listar_tipo_producto_por_familia(idfamilia)
    }

    return render(request, 'combobox/tipo_x_familia.html', data)


def listar_tipo_producto_por_familia(id_familia):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TIPOPRODUCTO_POR_FAMILIA",
                    [out_cur, id_familia])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def agregar_producto(request):
    if request.method == 'POST':
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        stock = request.POST['stock']
        critico = request.POST['critico']
        vencimiento = change_date_format(request.POST['vencimiento'])
        proveedor = request.POST['proveedor']
        Familia = request.POST['Familia']
        foto_ = request.FILES.get('foto')

    try:
        new_id = int(sp_obtener_id_producto(proveedor, Familia, vencimiento))
        salida = sp_crear_producto(
            new_id, descripcion, vencimiento, precio, stock, critico, proveedor, Familia)
        foto_id = int(sp_obtener_id_foto_prod())
        FotoProd.objects.create(id_foto=foto_id, foto=foto_)
        FotoProd.objects.filter(id_foto=foto_id).update(id_producto=new_id)

        messages.success(request, 'Producto Registrado Correctamente')
    except:
        messages.error(request, 'Error, Al Registrar Prodcuto')

    return redirect('nuevo-producto')


def sp_crear_producto(id_producto, descripcion, vencimiento, precio, stock, stock_critico, id_proveedor, id_familia):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_PRODUCTO', [
                    id_producto, descripcion, vencimiento, precio, stock, stock_critico, id_proveedor, id_familia, salida])
    return salida.getvalue()


def sp_agregar_foto_producto(id_proveedor, foto):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_FOTO_PRODUCTO', [
                    id_proveedor, foto, salida])
    return salida.getvalue()


def sp_obtener_id_producto(id_proveedor, id_familia, vencimiento):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.STRING)
    cursor.callproc('SP_OBTENER_ID_PRODUCTO', [
                    id_proveedor, id_familia, vencimiento, salida])
    return salida.getvalue()


def sp_obtener_id_foto_prod():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_OBTENER_ID_FOTO_PROD', [salida])
    return salida.getvalue()


def mostrar_productos(request):
    productos = listado_productos()
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(productos, 6)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }

    return render(request, 'core/Productos.html', data)

def mostrar_productos_herramientas(request):
    productos = listado_productos_por_categoria(201)
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(productos, 6)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }

    return render(request, 'core/Productos.html', data)

def mostrar_productos_fijaciones(request):
    productos = listado_productos_por_categoria(200)
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(productos, 6)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }

    return render(request, 'core/Productos.html', data)

def mostrar_productos_pinturas(request):
    productos = listado_productos_por_categoria(203)
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(productos, 6)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }

    return render(request, 'core/Productos.html', data)

def mostrar_productos_iluminacion(request):
    productos = listado_productos_por_categoria(205)
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(productos, 6)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }

    return render(request, 'core/Productos.html', data)

def mostrar_productos_baldozas(request):
    productos = listado_productos_por_categoria(206)
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(productos, 6)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }

    return render(request, 'core/Productos.html', data)


def listado_productos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def listado_productos_por_categoria(IdFamilia):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS_POR_CATEGORIA", [IdFamilia, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def mostrar_detalle_producto(request, id):

    producto = Producto.objects.get(id_producto=id)
    foto = FotoProd.objects.get(id_producto=id)

    data = {
        'producto': producto,
        'foto': foto
    }

    return render(request, 'modal/producto_detalle.html', data)


def mostrar_actualizar_producto(request, id):

    producto = Producto.objects.get(id_producto=id)
    foto = FotoProd.objects.get(id_producto=id)
    proveedor = Proveedor.objects.all()
    familia = FamiliaProd.objects.all()

    data = {
        'producto': producto,
        'foto': foto,
        'proveedor': proveedor,
        'familia': familia
        
    }

    return render(request, 'modal/actualizar_producto.html', data)

def actualizar_producto(request):
    if request.method == 'POST':
        id = request.POST['id_produc']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        stock = request.POST['stock']
        critico = request.POST['critico']
        foto_ = request.FILES.get('foto')
        Disponibilidad = request.POST['Disponibilidad']
        check = request.POST['respuestaCheck']

    try:
        Producto.objects.filter(id_producto=id).update(descripcion=descripcion, precio=precio, stock=stock, stock_critico=critico, activo=Disponibilidad)

        if Disponibilidad == 0 or '0':
            Carrito.objects.filter(id_producto=id).delete()

        if check == '0' or None:
            FotoProd.objects.filter(id_producto=id).delete()
            foto_id = int(sp_obtener_id_foto_prod())
            FotoProd.objects.create(id_foto=foto_id, foto=foto_)
            FotoProd.objects.filter(id_foto=foto_id).update(id_producto=id)
        messages.success(request, 'Producto Actualizado Correctamente')
        
    except:
        messages.error(request, 'El producto no pudo ser Actualizado')
    
    return redirect('listado-producto')


def change_date_format(dt):
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)
#################### fin Producto

















# CARRITO

def agregar_a_carrito(request):
    if request.is_ajax():
        if request.method == 'POST':
            id_produc = request.POST['id-producto']
            usuarioOra = Usuario.objects.get(username=request.user.username)
        try:
            salida = sp_add_carrito(usuarioOra.id_usuario, id_produc)

            if salida == 1:
                print('====Agregado al carrito====')
                mensaje = 'Agregado Correctamente al carrito'
                error = 'No hay Error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                print('====Oracle: No Agregado al carrito====')
                mensaje = 'No se ha podido agregar al carrito'
                error = 'Error al Agregar producto al carrito'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response

        except:
            print('==== except: No Agregado al carrito====')
            mensaje = 'No se ha podido agregar al carrito'
            error = 'Error al Agregar producto al carrito'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 400
            return response


def sp_add_carrito(id_usuario, id_producto):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ADD_CARRITO', [
                    id_usuario, id_producto, salida])
    return salida.getvalue()

@login_required(login_url='/login/')
@user_passes_test(es_cliente, login_url='/acceso-denegado/')
def mostrar_carrito(request):
    return render(request, 'core/Carrito.html')


def listado_carrito_json(request):
    if request.is_ajax():
        if request.method == 'GET':
            usuarioOra = Usuario.objects.get(username=request.user.username)
            lista_carrito = []
            for carrito in listado_carrito(usuarioOra.id_usuario):
                data_carrito = {}
                data_carrito['id'] = carrito[0]
                data_carrito['foto'] = str(carrito[1])
                data_carrito['descripcion'] = carrito[2]
                data_carrito['cantidad'] = carrito[5]
                data_carrito['total'] = carrito[6]
                data_carrito['id_carrito'] = carrito[7]
                lista_carrito.append(data_carrito)
            data = json.dumps(lista_carrito)
            return HttpResponse(data, 'application/json')


def listado_carrito(id_usuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_CARRITO", [id_usuario, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def actualizar_cantidad_carrito(request):
    if request.is_ajax():
        if request.method == 'POST':
            cantidad = request.POST['cantidad']
            id_carro = request.POST['id-carrito']
        try:
            salida = sp_update_carrito(id_carro, cantidad)

            if salida == 1:
                print('====Carrito Actualizado Correctamente====')
                mensaje = 'Carrito Actualizado Correctamente'
                error = 'No hay Error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 200
                return response
            else:
                print('====Carrito no actualizado====')
                mensaje = 'No se ha podido Actualizado el carrito'
                error = 'Error al Actualizado producto del carrito'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response

        except:
            print('==== except: Carrito no actualizado====')
            mensaje = 'No se ha podido Actualizado el carrito'
            error = 'Error al Actualizado producto del carrito'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 400
            return response

def eliminar_registro_carrito(request):
    if request.is_ajax():
        if request.method == 'POST':
            id_carro = request.POST['idcarro']
        try:
            Carrito.objects.filter(id_carrito=id_carro).delete()
            print('====Registro de carrito Eliminado Correctamente====')
            mensaje = 'Registro de carrito Eliminado Correctamente'
            error = 'No hay Error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 200
            return response
        except:
            print('====No se Ha podido Eliminar El registro de Carrito====')
            mensaje = 'No se Ha podido Eliminar El registro de Carrito'
            error = 'Error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 400
            return response
            


def sp_update_carrito(id_carrito, cantidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_UPDATE_CARRITO', [
                    id_carrito, cantidad, salida])
    return salida.getvalue()



def mostrar_proceso_compra(request):
    usuarioOra = Usuario.objects.get(username=request.user.username)
    
    data = {
        'totales': sp_cant_sub_total(usuarioOra.id_usuario),
        'metodo' : MetodoPago.objects.all()
    }
    
    return render(request, 'modal/proceso_compra.html', data)

def regitrar_compra(request):
    if request.method == 'POST':
        pago = request.POST['pago']
        direccion = request.POST['direccion']
        usuarioOra = Usuario.objects.get(username=request.user.username)
        try:
            salida = sp_registrar_compra(usuarioOra.id_usuario, pago, direccion)

            if salida == 1:
                print('Compra Registrada')
                messages.success(request, '¡Gracias Por Su Compra!')
                return redirect('carrito')
            else:
                messages.error(request, 'Hubo un Error al procesar la compra')
                print('Compra No Registrada')
                return redirect('carrito')

        except:
            messages.error(request, 'Hubo un Error al procesar la compra')
            print('except: Compra No Registrada')
            return redirect('carrito')

def sp_registrar_compra(id_usuario, id_pago, despacho):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_REGISTRAR_COMPRA', [
                    id_usuario, id_pago, despacho, salida])
    return salida.getvalue()

def sp_cant_sub_total(id_usuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_OBTENER_CANTIDAD_SUBTOTAL_Y_TOTAL", [id_usuario, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

# FIN CARRITO


#Mis Compras
def listado_mis_comprar(request):
    usuarioOra = Usuario.objects.get(username=request.user.username)

    boletas = Boleta.objects.filter(id_usuario=usuarioOra.id_usuario).order_by('-id_boleta')
    facturas = Factura.objects.filter(id_usuario=usuarioOra.id_usuario).order_by('-id_factura')

    data = {
        'boletas':boletas,
        'facturas': facturas
    }
    return render(request, 'core/MisCompras.html', data)


@login_required(login_url='/login/')
@user_passes_test(es_cliente, login_url='/acceso-denegado/')
def mostrar_boleta_pdf(request, id):
    boletas = Boleta.objects.get(id_boleta=id)
    iva = round(boletas.iva, 2)
    detalle = DetalleBoleta.objects.filter(id_boleta=id)

    data = {
        'boletas':boletas,
        'iva': iva,
        'detalle':detalle
    }

    pdf = html_to_pdf('documentos/boleta.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url='/login/')
@user_passes_test(es_cliente, login_url='/acceso-denegado/')
def mostrar_factura_pdf(request, id):
    factura = Factura.objects.get(id_factura=id)
    iva = round(factura.iva, 2)
    detalle = DetalleFactura.objects.filter(id_factura=id)
    cliente = Cliente.objects.get(id_usuario=factura.id_usuario)

    data = {
        'factura':factura,
        'iva': iva,
        'detalle':detalle,
        'cliente':cliente
    }

    pdf = html_to_pdf('documentos/factura.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
#Fin Mis Compras

#orden de compra
@login_required(login_url='/login/')
@user_passes_test(es_administrador_o_empleado, login_url='/acceso-denegado/')
def mostrar_orden_compra(request):
    try:
        usuarioOra = Usuario.objects.get(username=request.user.username)
        Carrito.objects.filter(id_usuario=usuarioOra.id_usuario).delete()
    except:
        print('Error al Vaciar carro empleado')

    data = {
        'proveedores': Proveedor.objects.all()
    }
    return render(request, 'core/Agregar_orden.html', data)

def listado_productos_por_proveedor_json(request, id_usu):
    if request.is_ajax():
        if request.method == 'GET':
            lista_productos = []
            for producto in Producto.objects.filter(id_usuario=id_usu):
                data_producto = {}
                data_producto['id'] = str(producto.id_producto)
                data_producto['descripcion'] = producto.descripcion
                data_producto['stock'] = str(producto.stock)
                data_producto['stock_critico'] = str(producto.stock_critico)
                lista_productos.append(data_producto)
            data = json.dumps(lista_productos)
            return HttpResponse(data, 'application/json')

def limpiarCarrito(request):
    if request.is_ajax():
        if request.method == 'GET':
            usuarioOra = Usuario.objects.get(username=request.user.username)
            try:
                Carrito.objects.filter(id_usuario=usuarioOra.id_usuario).delete()
                print('====Carrito vaciado Correctamente====')
                mensaje = 'Carrito vaciado Correctamente'
                error = 'No hay Error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 200
                return response
            except:
                print('====Error al vaciar el carrito====')
                mensaje = 'Error al vaciar el carrito'
                error = 'Error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response

def regitrar_orden_compra(request):
    if request.method == 'POST':
        idproveedor = request.POST['id-proveedor']
        empleadoOra = Usuario.objects.get(username=request.user.username)
        try:
            proveedor = Proveedor.objects.get(id_usuario=idproveedor)

            salida = sp_registrar_orden_compra(empleadoOra.id_usuario, proveedor.id_proveedor)

            if salida == 1:
                messages.success(request, 'Orden de Compra Enviada Correctamente')
                
            else:
                messages.error(request, 'Hubo un Error al Enviar la Orden de Compra')

        except:
            messages.error(request, 'Hubo un Error al Enviar la Orden de Compra')
        
        return redirect('nueva-orden-compra')

def sp_registrar_orden_compra(id_usuario, id_proveedor):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_REGISTRAR_ORDEN_COMPRA', [
                    id_usuario, id_proveedor, salida])
    return salida.getvalue()

@login_required(login_url='/login/')
@user_passes_test(es_administrador_o_empleado, login_url='/acceso-denegado/')
def mostrar_ordenes_compra(request):

    data = {
        'ordenes': listar_ordenes_de_compra()
    }

    return render(request, 'core/Listado_ordenes.html', data)



def listar_ordenes_de_compra():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_ORDENES_COMPRA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def mostrar_orden_pdf(request, id):
    orden = OrdenCompra.objects.get(id_orden=id)
    detalle = DetalleOrden.objects.filter(id_orden=id)
    empleado = Empleado.objects.get(id_usuario=orden.id_usuario)
    proveedor = Proveedor.objects.get(id_proveedor=orden.id_proveedor)

    data = {
        'orden':orden,
        'detalle': detalle,
        'proveedor':proveedor,
        'empleado': empleado
    }

    pdf = html_to_pdf('documentos/orden.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def cambiar_estado_orden(request, id):
    try:
        OrdenCompra.objects.filter(id_orden=id).update(id_estado=4)
        messages.success(request, 'La Orden de Compra ha sido Cancelada Correctamente')
    except:
        messages.success(request, 'La Orden de Compra No ha podido ser Cancelada')
    return redirect('ordenes-compra')

#fin orden de compra

#Graficos
@login_required(login_url='/login/')
@user_passes_test(es_administrador, login_url='/acceso-denegado/')
def mostrar_graficos(request):
    
    monto = int(sp_obtener_monto_del_dia())
    
    data = {
        'producto': sp_obtener_producto_mas_vendido(),
        'monto': monto
    }
    
    
    return render(request, 'core/Graficos.html', data)

def sp_obtener_producto_mas_vendido():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_OBTENER_PRODUCTO_MAS_VENDIDO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def sp_obtener_monto_del_dia():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_OBTENER_MONTO_DEL_DIA', [salida])
    return salida.getvalue()


def obtener_total_por_mes():

    anioActual = datetime.now().year
    totalesMesesBoleta = []
    totalesMesesFactura = []
    totalesSumados = []
    try:
        for i in range(12):
            valorMes = Boleta.objects.all().filter(fecha_ingreso__year= anioActual,
                                                fecha_ingreso__month=i+1).aggregate(Sum('total'))
            if valorMes['total__sum'] == None:
                totalesMesesBoleta.append(float(0))
            else:
                totalesMesesBoleta.append(float(valorMes['total__sum']))
    except:
        pass

    try:
        for i in range(12):
            valorMes = Factura.objects.all().filter(fecha_ingreso__year= anioActual,
                                                fecha_ingreso__month=i+1).aggregate(Sum('total'))
            if valorMes['total__sum'] == None:
                totalesMesesFactura.append(float(0))
            else:
                totalesMesesFactura.append(float(valorMes['total__sum']))
    except:
        pass

    totalesSumados = [sum(x) for x in zip(totalesMesesBoleta,totalesMesesFactura)]
    return totalesSumados
    
def listado_totales_por_mes_json(request):
    if request.is_ajax():
        if request.method == 'GET':
            data = json.dumps(obtener_total_por_mes())
        return HttpResponse(data, 'application/json')

def productos_mas_vendidos_mes_json(request):
    if request.is_ajax():
        if request.method == 'GET':

            data = json.dumps(sp_obtener_productos_mas_vendidos_mes())
            return HttpResponse(data, 'application/json')

def sp_obtener_productos_mas_vendidos_mes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_OBTENER_PRODUCTOS_MAS_VENDIDOS_MES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista



#fin Graficos



#Proveedores
@login_required(login_url='/login/')
@user_passes_test(es_proveedor, login_url='/acceso-denegado/')
def mostrar_listado_pedidos(request):
    usuarioOra = Usuario.objects.get(username=request.user.username)
    proveedorOra = Proveedor.objects.get(id_usuario=usuarioOra.id_usuario)

    data = {
        'ordenes': listar_ordenes_de_compra_por_proveedor(proveedorOra.id_proveedor)
    }

    return render(request, 'core/Listado_pedidos.html', data)

def listar_ordenes_de_compra_por_proveedor(idproveedor):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_ORDENES_COMPRA_POR_PROVEEDOR", [idproveedor, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def cambiar_estado_orden_compra(request, idorden, idestado):
    try:
        if idestado == '1':
            OrdenCompra.objects.filter(id_orden=idorden).update(id_estado=idestado)
            messages.success(request, 'La Orden de Compra ha sido Finalizada Correctamente')
        elif idestado == '2':
            OrdenCompra.objects.filter(id_orden=idorden).update(id_estado=idestado)
            messages.success(request, 'La Orden de Compra ha sido Enviada Correctamente')
        elif idestado == '3':
            OrdenCompra.objects.filter(id_orden=idorden).update(id_estado=idestado)
            messages.success(request, 'La Orden de Compra ha sido Tomada Correctamente')
        elif idestado == '4':
            OrdenCompra.objects.filter(id_orden=idorden).update(id_estado=idestado)
            messages.success(request, 'La Orden de Compra ha sido Cancelada Correctamente')
        elif idestado == '5':
            OrdenCompra.objects.filter(id_orden=idorden).update(id_estado=idestado)
            messages.success(request, 'La Orden de Compra ha sido Rechazada Correctamente')
        else:
            messages.error(request, 'No se ha Podido Cambiar el estado de la Orden de Compra')

    except:
        messages.error(request, 'No se ha Podido Cambiar el estado de la Orden de Compra')

    usuarioOra = Usuario.objects.get(username=request.user.username)
    nro = Proveedor.objects.filter(id_usuario=usuarioOra.id_usuario).count()
    if nro > 0:
        return redirect('listado-pedidos')
    else:
        return redirect('ordenes-compra')

#fin Proveedores


#como llegar y contacto
def mostrar_como_llegar(request):
    return render(request, 'core/Como_llegar.html')

def mostrar_contacto(request):
    return render(request, 'core/Contacto.html')
#end Como llegar y contacto
