$().ready(function(){

    $.validator.addMethod("soloLetras", function(value, element) 
    {
        return this.optional(element) || /^[a-z ]+$/i.test(value);
    }, "Solo se Permiten Letras y Espacios");

    $.validator.addMethod(
        "validarUsername", 
        function(value, element) {
            var result;
            $.ajax({
                type: "GET",
                url: "/validate-username/"+value+"/",
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
        "El username ya se encuentra en uso"
    );

    $.validator.addMethod(
        "validarEmail", 
        function(value, element) {
            var result;
            $.ajax({
                type: "GET",
                url: "/validate-email/"+value+"/",
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

    $.validator.addMethod(
        "validarRut", 
        function(value, element) {
            var result;
            $.ajax({
                type: "GET",
                url: "/validate-rut-proveedor/"+value+"/",
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

    $("#formulario_proveedor").validate({
        rules: {
            rut_pro: {
                required: true,
                digits: true,
                minlength: 8,
                maxlength: 9,
                validarRut: true
            },
            nombre_pro: {
                required: true,
                soloLetras: true, 
                minlength: 3,
                maxlength: 20
            },
            username_pro: {
                required: true,
                minlength: 2,
                maxlength: 15,
                validarUsername: true
            },
            password_pro: {
                required: true,
                minlength: 3,
                
            },
            password2_pro: {
                required: true,
                minlength: 3,
                equalTo : "#password_pro"
                
            },
            fono_pro:{
                required: true,
                digits: true,
                minlength: 8,
                maxlength: 9
            },
            mail_pro: {
                required: true,
                email: true,
                validarEmail: true
            },
            rubro_pro: {
                required: true, 
            }
        }
    })
})


$("#btnguardar").click(function(){
    if($("#formulario_proveedor").valid() == false){
        return;
    }
    else{
        $("#formulario_proveedor").submit();
    }
})