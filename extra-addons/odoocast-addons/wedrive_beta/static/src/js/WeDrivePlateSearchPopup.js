odoo.define('wedrive_beta.WeDrivePlateSearchPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { useState, useEnv } = owl;

    class WeDrivePlateSearchPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.env = useEnv();
            this.changes = useState({ plate: '' });
        }

        captureChange(event) {
            this.changes.plate = event.target.value;
        }

        async consultPlate() {
            const plate = this.changes.plate;
            const cnpj_cpf = this.changes.cnpj_cpf;
            const name = this.changes.name;
            const phone = this.changes.phone;
            const result = await this.env.services.rpc({
                route: '/fleet/vehicle/consult_plate',
                params: {
                    plate: plate,
                    name: name,
                    cnpj_cpf: cnpj_cpf,
                    phone: phone,
                }
            });
            if (result.status === 'success') {
                this.trigger('close-popup', { confirmed: true, payload: result.partner });
            } else {
                alert(result.message);
            }
        }

        async cancel() {
            super.cancel();
        }
    }

    WeDrivePlateSearchPopup.template = 'WeDrivePlateSearchPopup';
    Registries.Component.add(WeDrivePlateSearchPopup);

    return WeDrivePlateSearchPopup;
})
