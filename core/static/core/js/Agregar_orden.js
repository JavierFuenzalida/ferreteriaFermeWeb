/* $().ready(function(){

    function listarProductos(id_usu){
        $.ajax({
            url: "/productos_por_proveedor/"+id_usu+"/",
            type: "get",
            dataType: "json",
            success: function(response){

                if (response.length <= 0) {
                    $('#msj-tabla-vacia').html("");
                    $('#tabla-productos').attr('hidden', true);
                    let mensaje = '<div class="text-center">';
                    mensaje += '<div class="d-flex justify-content-center">';
                    mensaje += '<i class="fas fa-arrow-up text-danger pr-3"></i>';
                    mensaje += '<strong>Por Favor Seleccione un proveedor.</strong>';
                    mensaje += '</div>';
                    mensaje += '</div>';
                    $('#msj-tabla-vacia').append(mensaje);
                    $('#msj-tabla-vacia').removeAttr('hidden');
                }



                $('#listado-productos tbody').html("");

                for (let i = 0; i < response.length; i++) {
                    
                    let fila = '<tr>';
                    fila += '<th scope="row">'+(i+1)+'</th>';
                    fila += '<td>'+response[i].descripcion + '</td>';
                    fila += '<td>'+response[i].stock + '</td>';
                    fila += '<td>'+response[i].stock_critico + '</td>';
                    fila += '<td><form method="POST" id="formulario'+i+'">';
                    fila += '<input hidden Name="id-producto" value ="'+response[i].id+'"/>';
                    fila += '<a href="#" type="button" onclick="addCarrito_emp('+i+')" class="btn btn-sm btn-warning">Agregar</a></form></td>';
                    $('#listado-productos tbody').append(fila);
                    $('#tabla-productos').removeAttr('hidden');
                    $('#msj-tabla-vacia').attr('hidden', true);
                }
            },
            error: function(error){
                console.log(error);
            }
        })
    }
    
    
    
    $('#proveedores').change(function(){
        let id_pro = $('#proveedores').val()
        if (id_pro == 0){
            $('#nameProveedor').html("");
            listarProductos(id_pro);
        }
        else{
            let nombre_Pro = $('#proveedores option:selected').text();
            $('#nameProveedor').html("");
            $('#nameProveedor').append("Nombre de Proveedor: "+nombre_Pro);
            listarProductos(id_pro);
        }





    })

});

function addCarrito_emp(nro) {
    var form = 'formulario' + nro;
    console.log(form)
    $.ajax({
        data: $('#'+form).serialize(),
        url: '/agregar_a_carrito/',
        type: $('#'+form).attr('method'),
        success: function (response) {
            console.log(response)
            
        },
        error: function (error) {
            console.log(error)
        }
    });

} */