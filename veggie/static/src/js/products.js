odoo.define('veggie.snippet_product', ['web.ajax'], function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function () {
        console.log('Veggie Website ON');
        var container_ingresos = document.getElementById("veggie_ingresos");
        var container_ingresos_2 = document.getElementById("veggie_ingresos_2");

        if (container_ingresos_2) {
            container_ingresos_2.innerHTML = "";
            ajax.jsonRpc('/get_products/ingresos','call', {}).then(function(data) {
                console.log(data);
                container_ingresos_2.innerHTML = "";
                for (var i = 0; i < data.length; i++) {
                    if (i === 0) {
                        container_ingresos_2.innerHTML += '\
                                            <div class="col-14 mb-3 p_ingreso" style="color:#222; padding-top:60px">\
                                                <a href="/shop/product/' + data[i].id +'" class="d-block col-12 col-lg-10 text-center pt-3 pl-3 pr-3 m-auto" style="color:#222;">\
                                                    <img class="img-fluid" src="/web/image/product.template/'+data[i].id+'/image_256" loading="lazy" width="256" height="256" />\
                                                    <h6 class="mt-3 text-center pb-1 mb-1">' + data[i].name + '</h6>\
                                                    <h6 class="text-center pb-1 mb-1">$ ' + Math.round(data[i].combination.price) + '</h6>\
                                                </a>\
                                            </div>';
                    }
                }
            });
        }

        if (container_ingresos) {
            container_ingresos.innerHTML = "";
            ajax.jsonRpc('/get_products/ingresos','call', {}).then(function(data) {
                console.log(data);
                container_ingresos.innerHTML = "";
                for (var i = 0; i < data.length; i++) {
                    if (i !== 0) {
                        container_ingresos.innerHTML += '\
                                            <div class="col-6 col-sm-6 col-md-4 col-lg-4 mb-3 p_ingreso" style="color:#222;">\
                                                <a href="/shop/product/' + data[i].id +'" class="d-block col-12 col-lg-10 text-center pt-3 pl-3 pr-3 m-auto" style="color:#222;">\
                                                    <img class="img-fluid" src="/web/image/product.template/'+data[i].id+'/image_256" loading="lazy" width="256" height="256" />\
                                                    <h6 class="mt-3 text-center pb-1 mb-1">' + data[i].name + '</h6>\
                                                    <h6 class="text-center pb-1 mb-1">$ ' + Math.round(data[i].combination.price) + '</h6>\
                                                </a>\
                                            </div>';
                    }
                }
            });
        }

        var container_liquidacion = document.getElementById("veggie_liquidacion");

        if (container_liquidacion) {
            container_liquidacion.innerHTML = "";
            ajax.jsonRpc('/get_products/liquidacion','call', {}).then(function(data) {
                console.log(data);
                container_liquidacion.innerHTML = "";
                for (var i = 0; i < data.length; i++) {
                    container_liquidacion.innerHTML += '\
                                            <div class="col-6 col-sm-6 col-md-4 col-lg-2 mb-3">\
                                                <a href="/shop/product/' + data[i].id +'" class="d-block col-12 col-lg-10 text-center pt-3 pl-3 pr-3 m-auto">\
                                                    <img class="img-fluid" src="/web/image/product.template/'+data[i].id+'/image_256" loading="lazy" width="256" height="256" />\
                                                    <h6 class="mt-3 text-left pb-1 mb-1">' + data[i].name + '</h6>\
                                                    <h6 class="text-left pb-1 mb-1">$ ' + Math.round(data[i].combination.price) + '</h6>\
                                                    <small class="text-primary text-left float-left">Comprar ahora</small>\
                                                </a>\
                                            </div>';
                }
            });
        }

        var container_destacados = document.getElementById("veggie_destacados");

        if (container_destacados) {
            container_destacados.innerHTML = "";
            ajax.jsonRpc('/get_products/featured','call', {}).then(function(data) {
                console.log(data);
                container_destacados.innerHTML = "";
                for (var i = 0; i < data.length; i++) {
                    container_destacados.innerHTML += '\
                                            <div class="d-none d-sm-block col-sm-6 col-md-8 col-lg-8 mb-3"></div>\
                                            <div class="col-12 col-sm-6 col-md-4 col-lg-4 mb-3 p_featured">\
                                                <a href="/shop/product/' + data[i].id +'" class="d-block col-12 col-lg-10 text-center pt-3 pl-3 pr-3 m-auto">\
                                                    <img class="img-fluid" src="/web/image/product.template/'+data[i].id+'/image_256" loading="lazy" width="256" height="256" />\
                                                    <h6 class="mt-3 text-center pb-1 mb-1">' + data[i].name + '</h6>\
                                                    <h6 class="text-center pb-1 mb-1">$ ' + Math.round(data[i].combination.price) + '</h6>\
                                                </a>\
                                            </div>';
                }
            });
        }
    });
});