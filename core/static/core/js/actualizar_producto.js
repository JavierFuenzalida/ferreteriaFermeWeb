$().ready(function(){

    $("#formulario_actualizar_producto").validate({
        rules: {
            file: {
                required: false
            },
            descripcion: {
                required: true,
                minlength: 3,
                maxlength: 30
            },
            precio: {
                required: true,
                digits: true,
                minlength: 1,
                maxlength: 20
            },
            stock: {
                required: true,
                digits: true,
                minlength: 1,
                maxlength: 20
            },
            critico: {
                required: true,
                digits: true,
                minlength: 1,
                maxlength: 20
            },
            respuestaCheck: {
                required: false
            },
            eliminarFoto: {
                required: false
            },
            Disponibilidad: {
                required: true
            }
        }
    })
})


$("#btn-guardar").click(function(){
    if($("#formulario_actualizar_producto").valid() == false){
        return;
    }
    if( $('#eliminarFoto').prop('checked') ) {
        $('#respuestaCheck').val('1');
    }
    else{
        $('#respuestaCheck').val('0');
    }
    $("#formulario_actualizar_producto").submit();
            
})


/*-------------------------------------*/

    document.getElementById('file').onchange = function (e) {
        let reader = new FileReader();
        reader.readAsDataURL(e.target.files[0]);
        reader.onload = function () {
            let preview = document.getElementById('preview');
            let dvQuitar = document.getElementById('dvQuitar');
            dvQuitar.innerHTML = ''
            dvQuitar.innerHTML += '<a type="button" class="text-danger" onclick="quitarFoto()"><i class="fas fa-trash-alt"></i></a>'
            image = document.createElement('img');
            image.src = reader.result;
            image.className = 'card-img-top img-fluid';
            image.style.width = '100%';
            preview.innerHTML = '';
            preview.append(image);

        }
    }



    function quitarFoto() {
        let preview = document.getElementById('preview');
        let dvQuitar = document.getElementById('dvQuitar');
        let inputf = document.getElementById('file');
        let ch = document.getElementById('ch');
        ch.style.display = 'none';
        dvQuitar.innerHTML = '';
        div = document.createElement('div');
        div.className = 'text-center pt-4'
        div.innerHTML = '<i class="fas fa-3x fa-upload"></i>'
        div.innerHTML += '<p>Seleccione una imagen</p>'
        preview.innerHTML = ''
        inputf.value = ''
        preview.append(div);
    }
