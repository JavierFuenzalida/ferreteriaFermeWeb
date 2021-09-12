$().ready(function(){

    $.validator.addMethod("soloLetras", function(value, element) 
    {
        return this.optional(element) || /^[a-z ]+$/i.test(value);
    }, "Solo se Permiten Letras y Espacios");

    $.validator.addMethod(
        "validarRut", 
        function(value, element) {
            var result;
            $.ajax({
                type: "GET",
                url: "/validate-update-rut-cliente/"+$("#id_usu").val()+"/"+value+"/",
                dataType:"json",
                async:false,
                success: function(response)
                {
                    
                    result = response.mensaje;
                    
                }
             });
             if (result == '0'){
                return true;
            }
        },
        "El Rut que intenta registrar ya le pertenece a otra cuenta"
    );

    $.validator.addMethod(
        "validarEmail", 
        function(value, element) {
            var result;
            $.ajax({
                type: "GET",
                url: "/validate-update-email/"+$("#id_usu").val()+"/"+value+"/",
                dataType:"json",
                async:false,
                success: function(response)
                {
                    
                    result = response.mensaje;
                    
                }
             });
             if (result == '0'){
                return true;
            }
        },
        "El correo electronico ya se encuentra en uso"
    );

    $("#formulario_cliente").validate({
        rules: {
            rut_cli: {
                required: true,
                digits: true,
                minlength: 8,
                maxlength: 9,
                validarRut: true
            },
            nombre_cli: {
                required: true,
                soloLetras: true, 
                minlength: 3,
                maxlength: 20
            },
            apellido_cli: {
                required: true,
                soloLetras: true,
                minlength: 5,
                maxlength: 20
            },
            naci_cli: {
                required: true
            },
            fono_cli: {
                required: true,
                digits: true,
                minlength: 8,
                maxlength: 9
            },
            mail_cli: {
                required: true,
                email: true,
                validarEmail: true
            }
        }
    })
})


$("#btnActualizar").click(function(){
    if($("#formulario_cliente").valid() == false){
        return;
    }
    $("#formulario_cliente").submit();
            
})
