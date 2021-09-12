var $ = jQuery.noConflict();
function abrirModalDetalle(url) {
    $('#detalle').load(url, function () {
        $(this).modal('show');
    });
}


function addCarrito(id_) {
    var id_form = 'formulario' + id_;
    $.ajax({
        data: $('#' + id_form).serialize(),
        url: $('#' + id_form).attr('action'),
        type: $('#' + id_form).attr('method'),
        success: function (response) {
            console.log(response)
            $('#agregadoMensaje'+id_).html(" ");
            $('#agregadoMensaje'+id_).css('display', 'Block');
            let mensaje = '<strong class="text-success">Agregado Correctamente al Carrito</strong>';
            mensaje += '<img style="height: 30px;" src="https://res.cloudinary.com/djxgsv3yo/image/upload/v1623722006/FerreteriaFerme/Mensajes/check_owzdkd.gif" alt="ferme">';
            $('#agregadoMensaje'+id_).append(mensaje);
            $('#agregadoMensaje'+id_).fadeOut(2000);
            contarCarrito();
            
            
        },
        error: function (error) {
            console.log(error)
        }
    });

}
