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
                url: "/validate-rut-empleado/"+value+"/",
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

    $("#formulario_empleado").validate({
        rules: {
            rut_emp: {
                required: true,
                digits: true,
                minlength: 8,
                maxlength: 9,
                validarRut: true
            },
            nombres_emp: {
                required: true,
                soloLetras: true, 
                minlength: 3,
                maxlength: 20
            },
            apellidos_emp: {
                required: true,
                soloLetras: true,
                minlength: 5,
                maxlength: 20
            },
            username_emp: {
                required: true,
                minlength: 2,
                maxlength: 15,
                validarUsername: true
            },
            password_emp: {
                required: true,
                minlength: 3,
                
            },
            password2_emp: {
                required: true,
                minlength: 3,
                equalTo : "#password_emp"
                
            },
            mail_emp: {
                required: true,
                email: true,
                validarEmail: true
            },
            cargo_emp: {
                required: true, 
            }
        }
    })
})


$("#Btnguardar").click(function(){
    if($("#formulario_empleado").valid() == false){
        return;
    }
    $("#formulario_empleado").submit();
            
})
