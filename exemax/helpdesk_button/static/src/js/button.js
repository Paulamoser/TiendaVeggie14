odoo.define("helpdesk_button.button", function (require) {
    "use strict";

    var rpc = require("web.rpc");
    var core = require("web.core");

    core.bus.on("web_client_ready", null, function () {
        var ribbon = $('<a href="https://www.exemax.com.ar/helpdesk/" target="_blank" class="btn btn-secondary helpdesk_btn"><span class="fa fa-warning"></span> Reportar Error</a>');
        $("body").append(ribbon);
    });
});
