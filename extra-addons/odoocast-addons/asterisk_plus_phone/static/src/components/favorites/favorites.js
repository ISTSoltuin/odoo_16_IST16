/** @odoo-module **/

import {useService} from "@web/core/utils/hooks"
import {uid} from "web.session"

const {Component, useState, onWillStart} = owl

export class Favorites extends Component {
    static template = 'asterisk_plus_phone.favorites'

    constructor() {
        super(...arguments)
        this.phone_configs = this.props.phone_configs
        this.bus = this.props.bus
    }

    setup() {
        super.setup()
        this.orm = useService('orm')
        this.action = useService('action')
        this.user = uid
        this.state = useState({
            favorites: [],
        })

        onWillStart(async () => {
            this.getFavorites()
        })
    }

    getFavorites() {
        const fields = [
            "id",
            "name",
            "partner",
            "user",
            "phone_number",
        ]

        this.orm.searchRead("asterisk_plus_phone.favorite", [], fields, {limit: 30}).then((records) => {
            this.state.favorites = records
        })
    }

    _onClickContactCall(phone_number) {
        this.bus.trigger('busPhoneMakeCall', {phone: phone_number})
    }

    _onClickRemoveFavorite(ev, id) {
        ev.stopPropagation()
        this.orm.unlink("asterisk_plus_phone.favorite", [id], {}).then(() => {
            this.getFavorites()
            this.bus.trigger('busCallsGetFavorites')
        })

    }
}
