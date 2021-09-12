$().ready(function(){
    llenarGraficoBarras();
    llenarGraficoPie();
    
});

function llenarGraficoBarras() {
    $.ajax({
        url: "/listado-totales-json/",
        type: "get",
        dataType: "json",
        success: function (response) {
            GraficoValoresPorMes(response);
            
        },
            error: function (error) {
                console.log(error);
            }
        });
    }

function llenarGraficoPie() {
    $.ajax({
        url: "/productos-vendidos-mes-json/",
        type: "get",
        dataType: "json",
        success: function (response) {
            GraficoProductosMasVendidos(response)
        },
            error: function (error) {
                console.log(error);
            }
        });
    }

function GraficoValoresPorMes(data){
    var fecha = new Date();
    var anio = fecha.getFullYear();
    Highcharts.chart('graficoColumnas', {
        chart: {type: 'column'},
        title: {text: 'Reporte de Ganancias del año Actual '+anio+''},
        subtitle: {text: 'Ferreteas FERME'},
        xAxis: {
            categories: [
                'Enero',
                'Febrero',
                'Marzo',
                'Abril',
                'Mayo',
                'Junio',
                'Julio',
                'Agosto',
                'Septiembre',
                'Octubre',
                'Noviembre',
                'Deciembre'
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Ganacias Totales por Mes'
            }
        },
        credits: {
            enabled: false
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} $</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: '% de venta',
            showInLegend: false,
            colorByPoint: true,
            data: data

        }]
    });
}

function GraficoProductosMasVendidos(data){
    const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    var fecha = new Date();
    var anio = fecha.getFullYear();
    var mes = monthNames[fecha.getMonth()];
    Highcharts.chart('graficopie', {
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: 'Productos Mas Vendidos en el mes de '+mes+' '+anio+''
        },
        credits: {
            enabled: false
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: true,
                    format: '{point.name}'
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'Porcentaje de Venta',
            data: data
        }],
    });

}