from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('buscar-producto/<nombreProducto>/', buscar_producto_json, name='buscar-producto'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='core/Home.html'), name='logout'),
    path('registro-persona-natural/', mostrar_registro_cliente, name='registro-persona-natural'),
    path('registro-persona-empresa/', mostrar_registro_cliente_empresa, name='registro-persona-empresa'),
    path('registro_cliente/', registrar_cliente_natural, name='registro_cliente'),
    path('registro_cliente_empresa/', registrar_cliente_empresa, name='registro_cliente_empresa'),
    path('micuenta/', mostrar_datos_cuenta, name='micuenta'),
    path('mostrar-actualizar-datos-cuenta/', mostrar_actualizar_datos_cuenta, name='mostrar-actualizar-datos-cuenta'),
    path('mostrar-actualizar-datos-cuenta-empresa/', mostrar_actualizar_datos_cuenta_empresa, name='mostrar-actualizar-datos-cuenta-empresa'),


    path('actualizar-datos/', actualizar_datos_cuenta, name='actualizar-datos'),
    path('actualizar-datos-empresa/', actualizar_datos_cuenta_empresa, name='actualizar-datos-empresa'),
    
    path('nuevo-producto/', mostrar_agregar_producto, name='nuevo-producto'),
    path('nuevo-usuario/', mostrar_agregar_usuario, name='nuevo-usuario'),
    path('mostrar-nuevo-proveedor/', mostrar_agregar_proveedor, name='mostrar-nuevo-proveedor'),
    path('nuevo-proveedor/', agregar_proveedor, name='nuevo-proveedor'),
    path('mostrar-nuevo-empleado/', mostrar_agregar_empledo, name='mostrar-nuevo-empleado'),
    path('nuevo-empleado/', agregar_empleado, name='nuevo-empleado'),
    
    path('actualizar-empleado/<id>/', mostrar_actualizar_empleado, name='actualizar-empleado'), 
    path('edit_empleado/', actualizar_empleado, name='edit_empleado'),
    path('actualizar-proveedor/<id>/', mostrar_actualizar_proveedor, name='actualizar-proveedor'),
    path('edit_proveedor/', actualizar_proveedor, name='edit_proveedor'),
    path('eliminar_empleado/<id>/', eliminar_empleado, name='eliminar_empleado'),
    path('eliminar_proveedor/<id>/', eliminar_proveedor, name='eliminar_proveedor'),
    path('tipoProducto_por_familia/', tipo_producto_por_familia, name='tipoProducto_por_familia'),


    path('agregar-producto/', agregar_producto, name='agregar-producto'),
    path('listado-producto/', mostrar_productos, name='listado-producto'),
    path('listado-producto/herramientas/', mostrar_productos_herramientas, name='listado-producto-herramientas'),
    path('listado-producto/fijaciones/', mostrar_productos_fijaciones, name='listado-producto-fijaciones'),
    path('listado-producto/pinturas/', mostrar_productos_pinturas, name='listado-producto-pinturas'),
    path('listado-producto/iluminacion/', mostrar_productos_iluminacion, name='listado-producto-iluminacion'),
    path('listado-producto/baldozas/', mostrar_productos_baldozas, name='listado-producto-baldozas'),
    path('detalles-producto/<idProducto>/', detalles_producto, name='detalles-producto'),




    path('detalle-producto/<id>/', mostrar_detalle_producto, name='detalle-producto'),
    path('actualizar-producto/<id>/', mostrar_actualizar_producto, name='actualizar-producto'),
    path('editar-producto/', actualizar_producto, name='editar-producto'),


    path('agregar_a_carrito/', agregar_a_carrito, name='agregar_a_carrito'),
    path('carrito/', mostrar_carrito, name='carrito'),
    path('listado-carrito/', listado_carrito_json, name='listado-carrito'),
    path('actualizar-cantidad/', actualizar_cantidad_carrito, name='actualizar-cantidad'),
    path('eliminar-registro-carrito/', eliminar_registro_carrito, name='eliminar-registro-carrito'),
    path('mostrar-proceso-compra/', mostrar_proceso_compra, name='mostrar-proceso-compra'),
    path('regitrar-compra/', regitrar_compra, name='regitrar-compra'),
    path('mis-compras/', listado_mis_comprar, name='mis-compras'),
    path('boleta-pdf/<id>/', mostrar_boleta_pdf, name='boleta-pdf'),
    path('factura-pdf/<id>/', mostrar_factura_pdf, name='factura-pdf'),

    path('validate-username/<username>/', validate_username, name='validate-username'),
    path('validate-email/<email>/', validate_email, name='validate-email'),
    path('validate-update-email/<id>/<email>/', validate_update_email, name='validate-update-email'),
    path('validate-rut-empleado/<rut>/', validate_rut_empleado, name='validate-rut-empleado'),
    path('validate-rut-proveedor/<rut>/', validate_rut_proveedor, name='validate-rut-proveedor'),
    path('validate-update-username-empleado/<id>/<username>/', validate_update_username_empleado, name='validate-update-username-empleado'),
    path('validate-update-rut-empleado/<id>/<rut>/', validate_update_rut_empleado, name='validate-update-username-empleado'),
    path('validate-update-rut-proveedor/<id>/<rut>/', validate_update_rut_proveedor, name='validate-update-rut-proveedor'),
    path('validate-update-rut-cliente/<id>/<rut>/', validate_update_rut_cliente, name='validate-update-rut-cliente'),
    path('validate-rut-cliente/<rut>/', validate_rut_cliente, name='validate-rut-cliente'),

    path('nueva-orden-compra/', mostrar_orden_compra, name='nueva-orden-compra'),
    path('productos_por_proveedor/<id_usu>/', listado_productos_por_proveedor_json, name='productos_por_proveedor'),
    path('limpiar-Carrito/', limpiarCarrito, name='limpiar-Carrito'),
    path('regitrar-orden-compra/', regitrar_orden_compra, name='regitrar-orden-compra'),
    path('ordenes-compra/', mostrar_ordenes_compra, name='ordenes-compra'),
    path('orden-compra/<id>/', mostrar_orden_pdf, name='orden-compra'),


    path('listado-pedidos/', mostrar_listado_pedidos, name='listado-pedidos'),
    path('cambiar-estado-orden-compra/<idorden>/<idestado>/', cambiar_estado_orden_compra, name='cambiar-estado-orden-compra'),

    path('graficos/', mostrar_graficos, name='graficos'),
    path('listado-totales-json/', listado_totales_por_mes_json, name='listado-totales-json'),
    path('productos-vendidos-mes-json/', productos_mas_vendidos_mes_json, name='productos-vendidos-mes-json'),

    path('como-llegar/', mostrar_como_llegar, name='como-llegar'),
    path('contacto/', mostrar_contacto, name='contacto'),
    path('acceso-denegado/', mostrar_acceso_denegado, name='acceso-denegado'),
    
    ]


    