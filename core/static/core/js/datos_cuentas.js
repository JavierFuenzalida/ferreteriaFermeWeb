var $ = jQuery.noConflict();
function abrirModalEdicion(url) {
    $('#edicion').load(url, function () {
        $(this).modal('show');
    });
}








