dtcloud.define('iap.redirect_dtcloud_credit_widget', function(require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');


var IapDTCloudCreditRedirect = AbstractAction.extend({
    template: 'iap.redirect_to_dtcloud_credit',
    events : {
        "click .redirect_confirm" : "dtcloud_redirect",
    },
    init: function (parent, action) {
        this._super(parent, action);
        this.url = action.params.url;
    },

    dtcloud_redirect: function () {
        window.open(this.url, '_blank');
        this.do_action({type: 'ir.actions.act_window_close'});
        // framework.redirect(this.url);
    },

});
core.action_registry.add('iap_dtcloud_credit_redirect', IapDTCloudCreditRedirect);
});
