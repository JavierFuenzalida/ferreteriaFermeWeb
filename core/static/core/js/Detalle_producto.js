var $ = jQuery.noConflict();
function abrirModalDetalle(url) {
    $('#detalle').load(url, function () {
        $(this).modal('show');
    });
}

function agregarCarrito() {
    $.ajax({
        data: $('#formulario-agregar-carrito').serialize(),
        url: $('#formulario-agregar-carrito').attr('action'),
        type: $('#formulario-agregar-carrito').attr('method'),
        success: function (response) {
            console.log(response)
            $('#msj-agregado').html(" ");
            $('#msj-agregado').css('display', 'Block');
            let mensaje = '<strong class="text-success">Agregado Correctamente al Carrito</strong>';
            mensaje += '<img style="height: 40px;" src="https://res.cloudinary.com/djxgsv3yo/image/upload/v1623722006/FerreteriaFerme/Mensajes/check_owzdkd.gif" alt="ferme">';
            $('#msj-agregado').append(mensaje);
            $('#msj-agregado').fadeOut(3000);
            contarCarrito();
             
        },
        error: function (error) {
            console.log(error)
        }
    });

}