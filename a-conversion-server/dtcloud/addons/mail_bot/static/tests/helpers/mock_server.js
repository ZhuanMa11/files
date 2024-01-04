dtcloud.define('mail_bot/static/tests/helpers/mock_server.js', function (require) {
"use strict";

const MockServer = require('web.MockServer');

MockServer.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    async _performRpc(route, args) {
        if (args.model === 'mail.channel' && args.method === 'init_dtcloudbot') {
            return this._mockMailChannelInitDTCloudBot();
        }
        return this._super(...arguments);
    },

    //--------------------------------------------------------------------------
    // Private Mocked Methods
    //--------------------------------------------------------------------------

    /**
     * Simulates `init_dtcloudbot` on `mail.channel`.
     *
     * @private
     */
    _mockMailChannelInitDTCloudBot() {
        // TODO implement this mock task-2300480
        // and improve test "DTCloudBot initialized after 2 minutes"
    },
});

});
