$().ready(function(){
    
    $("#formulario_producto").validate({
        rules: {
            file: {
                required: false,
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
                maxlength: 10
            },
            stock: {
                required: true,
                digits: true,
                minlength: 1,
                maxlength: 10
            },
            critico: {
                required: true,
                digits: true,
                minlength: 1,
                maxlength: 10
            },
            vencimiento: {
                required: false
            },
            validar: {
                required: false
            },
            proveedor: {
                required: true
                
            },
            Familia: {
                required: true
                
            }
        }
    })
})


$("#btnguardar").click(function(){
    if($("#formulario_producto").valid() == false){
        return;
    }
    $("#vencimiento").prop('disabled', false);
    $("#formulario_producto").submit();
            
})
/*-------------*/
    
    
    
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
        dvQuitar.innerHTML = '';
        div = document.createElement('div');
        div.className = 'text-center pt-4'
        div.innerHTML = '<i class="fas fa-3x fa-upload"></i>'
        div.innerHTML += '<p>Seleccione una imagen</p>'
        preview.innerHTML = ''
        inputf.value = ''
        preview.append(div);
    }



    var checkbox = document.getElementById('validar');
    checkbox.addEventListener("change", validaCheckbox, false);
    function validaCheckbox() {
        var checked = checkbox.checked;
        if (checked) {

            var fecha = document.getElementById('vencimiento')
            fecha.disabled = true;
            vencimiento.value = '';
        }
        if (!checked) {

            var fecha = document.getElementById('vencimiento')
            fecha.disabled = false;
        }
    }




