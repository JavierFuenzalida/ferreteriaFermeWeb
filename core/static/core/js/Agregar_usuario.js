
var $ = jQuery.noConflict();
function abrirModalEdicion(url) {
    $('#edicion').load(url, function () {
        $(this).modal('show');
    });
}



var $ = jQuery.noConflict();
function abrirModalCreacion(url) {
    $('#edicion').load(url, function () {
        $(this).modal('show');
    });
}



function eliminarEmpleado(id) {
    Swal.fire({
        title: '¿Estas Seguro?',
        text: "¿Eliminar Usuario?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#343a40',
        cancelButtonColor: '#dc3545',
        confirmButtonText: 'Si',
        cancelButtonText: 'No'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/eliminar_empleado/' + id + '/'
        }
    })
}



function eliminarProveedor(id) {
    Swal.fire({
        title: '¿Estas Seguro?',
        text: "¿Eliminar Usuario?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#343a40',
        cancelButtonColor: '#dc3545',
        confirmButtonText: 'Si',
        cancelButtonText: 'No'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/eliminar_proveedor/' + id + '/'
        }
    })
}
