/** @odoo-module **/

import { WaThreadView } from "@tus_meta_wa_discuss/js/wa_thread_view";
import { patch } from 'web.utils';
import { LeadList } from "@tus_meta_wa_crm_in_discuss/js/LeadList";
import { useEffect } from "@web/core/utils/hooks";

const { ComponentWrapper, WidgetAdapterMixin } = require('web.OwlCompatibility');

patch(WaThreadView.prototype, 'tus_meta_wa_crm_in_discuss/static/src/js/wa_thread_view.js', {
    tabLead(){
        this.state.nav_active = 'lead'
        $('.back_btn').addClass('o_hidden');
        $('.main-button').addClass('o_hidden');
        $('#main-form-view').replaceWith("<div id='main-form-view'></div>")
        const LeadComponent=new ComponentWrapper(this, LeadList, {'WaThreadView': this});
        LeadComponent.mount($('#main-form-view')[0]);
    },
    onClickBack(){
        this._super()
        if(this.state.nav_active == 'lead'){
            this.tabLead();
        }
    }
});