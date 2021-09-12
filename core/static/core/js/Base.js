$(document).ready(function () {
    contarCarrito();

    $('#btnBuscar').click(function () {
        /* $('#divBuscar').slideToggle(); */
        if ($('#divBuscar').css('display') == 'none') {
            $('#divBuscar').show(1000);
            $('#fondoNegro').css('background', 'rgba(0,0,0,0.7)');
            $('#fondoNegro').css('display', 'Block');
            $('#inputBuscar').focus();

        }
        else {
            $('#divBuscar').hide(1000);
            $('#fondoNegro').css('background', '');
            $('#fondoNegro').css('display', 'None');
            $('#resultadoBusqueda').html('');
            $('#inputBuscar').val('');
        }
    });

    $('#contenidoCuerpo').click(function () {
        $('#divBuscar').fadeOut('slow');
        $('#blockContenido').css('background', '');
        $('#fondoNegro').css('display', 'None');
        
    });

    $('#fondoNegro').click(function () {
        $('#divBuscar').fadeOut('slow');
        $('#blockContenido').css('background', '');
        $('#fondoNegro').css('display', 'None');

        $('#resultadoBusqueda').html('');
        $('#inputBuscar').val('');
    });

    $('#navferme').click(function (event) {
        event.stopPropagation();
    });

    $('#divBuscar').click(function (event) {
        event.stopPropagation();
    });

    $('#inputBuscar').keypress(function () {
      if ($('#inputBuscar').val().length < 2){
        $('#resultadoBusqueda').html("");
      }
      
      let result = $('#inputBuscar').val();
      listarBusquedaProducto(result);
    });

    $('#inputBuscar').keydown(function () {
      if ($('#inputBuscar').val().length < 2){
        $('#resultadoBusqueda').html("");
        console.log($('#inputBuscar').val().length);
      }
      
      let result = $('#inputBuscar').val();
      listarBusquedaProducto(result);
    });

  });




  function contarCarrito() {
    $.ajax({
        url: "/listado-carrito/",
        type: "get",
        dataType: "json",
        success: function (response){
          var contador = response.reduce((sum, value) => (typeof value.cantidad == "number" ? sum + value.cantidad : sum), 0);
          console.log(contador);

          if (contador != 0){
            $('#contadiv').html("");
            let conta = '<div class="bg-danger text-center text-white rounded-circle" style="width: 30px; height: 30px;">';
            conta += ''+contador+'';
            conta += '</div>';
            $('#contadiv').append(conta);
            $('#contadiv').removeAttr('hidden');
          }
          else{
            $('#contadiv').attr('hidden', true);
          }

          
        }});
      }

      function listarBusquedaProducto(nombreProducto) {
        $.ajax({
            url: '/buscar-producto/'+nombreProducto+'/',
            type: "get",
            dataType: "json",
            success: function (response) {
                console.log(response);

                $('#resultadoBusqueda').html('');
                for (let i = 0; i < response.length; i++) {
                  let fila = '<div class="row"';
                  fila += '<div class="col-12 col-sm-8 col-lg-5" style="min-width: 100%;">';
                  fila += '<ul class="list-group pl-3 pr-3" style="min-width: 100%;">';
                  fila += '<a href="/detalles-producto/'+(response[i].id)+'/">';
                  fila += '<li class="list-group-item d-flex justify-content-between align-items-center">';
                  fila += ''+response[i].descripcion+'';
                  fila += '<div class="image-parent">';
                  fila += '<img src="https://res.cloudinary.com/djxgsv3yo/image/upload/'+response[i].foto+'"style="max-height: 50px;" class="img-fluid" alt="ferme">';
                  fila += '</div></li></a></ul></div></div></div>';

                  $('#resultadoBusqueda').append(fila);
                }
                $('#resultadoBusqueda').css('display', 'Block');
              }
            });
          }