/** @odoo-module **/

import {useService} from "@web/core/utils/hooks"
import {uid} from "web.session"

const {Component, useState, onWillStart} = owl

class CallDetail extends Component {
    static template = 'asterisk_plus_phone.call_detail'

    constructor() {
        super(...arguments)
        this.phone_configs = this.props.phone_configs
        this.state = useState({
            call: this.props.call,
        })
    }

    setup() {
        super.setup()
        this.orm = useService('orm')
        this.action = useService('action')

        onWillStart(async () => {
            this.getCall(this.state.call.id)
        })
    }

    async getCall(id) {
        const fields = [
            "id",
            "duration_human",
            "called_number",
            "calling_number",
            "answered_user",
            "calling_user",
            "partner",
            "direction",
            "started"
        ]
        const [call] = await this.orm.searchRead( "asterisk_plus.call", [["id", "=", id]], fields)
        this.state.call = call
    }

    async _createOpenPartner() {
        await this.getCall(this.state.call.id)
        if (this.state.call.partner) {
            this.action.doAction({
                res_id: this.state.call.partner[0],
                res_model: "res.partner",
                target: 'new',
                type: 'ir.actions.act_window',
                views: [[false, 'form']],
            })
        } else {
            const phone = this.state.call.called_number === this.phone_configs.sip_user ?
                    this.state.call.calling_number : this.state.call.called_number
            let context = {
                call_id: this.state.call.id,
                default_phone: phone,
                default_name: `Partner ${phone}`
            }
            this.action.doAction({
                context,
                res_model: 'res.partner',
                target: 'new',
                type: 'ir.actions.act_window',
                views: [[false, 'form']],
            })
        }
    }

    _OpenInCallHistory() {
        this.action.doAction({
            res_id: this.state.call.id,
            res_model: 'asterisk_plus.call',
            target: 'new',
            type: 'ir.actions.act_window',
            views: [[false, 'form']],
        })
    }
}

export class Calls extends Component {
    static template = 'asterisk_plus_phone.calls'
    static components = {CallDetail}

    constructor() {
        super(...arguments)
        this.phone_configs = this.props.phone_configs
        this.bus = this.props.bus
    }

    setup() {
        super.setup()
        this.orm = useService('orm')
        this.action = useService('action')
        this.notification = useService('notification')
        this.user = uid
        this.favorites = []
        this.state = useState({
            calls: [],
            call: null,
        })

        onWillStart(async () => {
            this.bus.on('busCallsGetCalls', this, this._getCalls)
            this.bus.on('busCallsGetFavorites', this, this._getFavorites)
            this._getFavorites()
        })
    }

    _getCalls() {
        this.state.calls = []
        const fields = [
            "id",
            "called_number",
            "calling_number",
            "answered_user",
            "calling_user",
            "partner",
            "direction",
            "started"
        ]
        this.orm.searchRead(
                "asterisk_plus.call",
                ["|", ["calling_user", "=", this.user], ["called_users", "=", this.user]],
                fields,
                {order: "id desc", limit: 20}
        ).then((records) => {
            records.forEach(item => {
                const call_number = item.called_number === this.phone_configs.sip_user ? item.calling_number : item.called_number
                item.favorite = this.favorites.includes(call_number)
                const local_time = new Date(`${item.started} UTC`).toLocaleTimeString("en-GB")
                item.started = `${item.started.split(' ')[0]} ${local_time}`
            })
            this.state.calls = records
        })
    }

    async _getFavorites() {
        this.favorites = []
        const favorites = await this.orm.searchRead('asterisk_plus_phone.favorite', [], ['phone_number'])
        favorites.forEach((el) => this.favorites.push(el.phone_number))
        this.state.calls.forEach(item => {
            const call_number = item.called_number === this.phone_configs.sip_user ? item.calling_number : item.called_number
            item.favorite = this.favorites.includes(call_number)
        })
    }

    _onClickContactCall(phoneNumber) {
        this.bus.trigger('busPhoneMakeCall', {phone: phoneNumber})
    }

    async _onClickFavorite(call) {
        const kwargs = {}
        const isCalled = call.called_number === this.phone_configs.sip_user
        kwargs.phone_number = isCalled ? call.calling_number : call.called_number
        if (call.partner) {
            kwargs.partner = call.partner[0]
        } else if (call.calling_user && call.answered_user) {
            kwargs.user = isCalled ? call.calling_user[0] : call.answered_user[0]
        } else {
            kwargs.name = kwargs.phone_number
        }

        const domain = [["phone_number", "=", kwargs.phone_number]]
        const getFavorite = await this.orm.search('asterisk_plus_phone.favorite', domain)

        if (getFavorite.length === 0) {
            await this.orm.create('asterisk_plus_phone.favorite', [kwargs])
            this.notification.add('Added to Favorite!', {title: 'Phone', type: 'info'})
            this._getFavorites()
        } else {
            await this.orm.unlink("asterisk_plus_phone.favorite", getFavorite, {})
            await this._getFavorites()
            this.notification.add('Removed to Favorite!', {title: 'Phone', type: 'info'})
        }
    }

    _open_detail(call) {
        this.state.call = call
    }

    _close_call_detail() {
        this.state.call = null
        this._getCalls()
    }
}
