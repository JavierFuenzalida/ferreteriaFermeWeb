var $ = jQuery.noConflict();
function abrirModalCreacion(url) {
  $('#creacion').load(url, function () {
      $(this).modal('show');
  });
}


function tipoEntidad(){
  Swal.fire({
title: '¿Como Deseo Registrarte?',
showDenyButton: true,
confirmButtonText: `Persona Natural`,
confirmButtonColor: '#343a40',
denyButtonText: `Persona Empresa`,
denyButtonColor: '#343a40',
icon: 'question',
}).then((result) => {
/* Read more about isConfirmed, isDenied below */
if (result.isConfirmed) {
  abrirModalCreacion("/registro-persona-natural/")
} else if (result.isDenied) {
  abrirModalCreacion("/registro-persona-empresa/")
}
})
}