/** @odoo-module **/

import {useService} from "@web/core/utils/hooks"
import {uid} from "web.session"
import {setFocus} from "@asterisk_plus_phone/js/utils"

const {Component, useState, useRef, onWillStart, onWillUnmount, onMounted} = owl

const searching = {
    all: 'all',
    extensions: 'extensions',
    partners: 'partners',
}

export class ContactList extends Component {
    static template = 'asterisk_plus_phone.contact_list'

    constructor() {
        super(...arguments)
        const {
            bus,
            isTransfer = false,
            isForward = false,
            isContact = false,
            contactSearch = searching.all,
            searchQuery = ''
        } = this.props
        this.bus = bus
        this.isTransfer = isTransfer
        this.isForward = isForward
        this.isContact = isContact
        this.contactSearch = contactSearch
        this.searchQuery = searchQuery
    }

    setup(props) {
        super.setup()
        this.user = uid
        this.state = useState({
            partners: [],
            users: [],
        })
        this.rpc = useService('rpc')
        this.orm = useService('orm')
        this.action = useService('action')

        onWillStart(async () => {
            this.bus.on('busContactListSetState', this, this._busContactListSetState)
            this.bus.on('busContactSearchQuery', this, this._busContactSearchQuery)
            this.bus.on('busContactCall', this, this._busContactCall)
        })

        onWillUnmount(() => {
            this.bus.off('busContactListSetState', this, this._busContactListSetState)
            this.bus.off('busContactSearchQuery', this, this._busContactSearchQuery)
            this.bus.off('busContactCall', this, this._busContactCall)
        })
    }

    _busContactListSetState({isTransfer = false, isForward = false, isContact = false}) {
        this.isTransfer = isTransfer
        this.isContact = isContact
        this.isForward = isForward
        this.state.partners = []
        this.state.users = []
        this.searchQuery = ''
    }

    _busContactSearchQuery({searchQuery = ''}) {
        this.searchQuery = searchQuery
        this.searchUser()
        this.searchPartner()
    }

    _busContactCall() {
        let phoneNumber
        if (this.state.partners.length + this.state.users.length === 1) {
            if (this.state.partners.length) {
                const contact = this.state.partners[0]
                phoneNumber = contact.phone ? contact.phone : contact.mobile
            } else {
                phoneNumber = this.state.users[0].exten
            }
        } else {
            phoneNumber = this.searchQuery
        }

        if (this.isTransfer) {
            this._onClickMakeTransfer(phoneNumber)
        } else if (this.isContact) {
            this._onClickMakeCall(phoneNumber)
        } else if (this.isForward) {
            this._onClickMakeForward(phoneNumber)
        }
    }

    searchPartner() {
        if (this.contactSearch !== searching.all && this.contactSearch !== searching.partners) return
        const self = this
        if (self.searchQuery) {
            self.rpc("/web/dataset/search_read", {
                model: "res.partner",
                domain: [
                    '|', ['phone_normalized', '=ilike', `%${self.searchQuery}%`],
                    '|', ['mobile_normalized', '=ilike', `%${self.searchQuery}%`],
                    ['name', '=ilike', `%${self.searchQuery}%`],
                    '|', ['phone', '!=', null],
                    ['mobile', '!=', null]
                ],
                sort: 'name',
                fields: ['id', 'name', 'email', 'phone_normalized', 'mobile_normalized'],
                limit: 10,
            }).then(({records}) => {
                self.state.partners = records
            })
        } else {
            self.state.partners = []
        }
    }

    searchUser() {
        if (this.contactSearch !== searching.all && this.contactSearch !== searching.extensions) return
        const self = this
        if (self.searchQuery) {
            self.orm.call('asterisk_plus.user', 'search_pbx_users', [self.searchQuery]).then((records) => {
                self.state.users = records
            })
        } else {
            self.state.users = []
        }
    }

    _onClickMakeCall(phoneNumber) {
        this.bus.trigger('busPhoneMakeCall', {phone: phoneNumber})
    }

    _onClickMakeTransfer(phoneNumber) {
        this.bus.trigger('busPhoneMakeTransfer', phoneNumber)
    }

    _onClickMakeForward(phoneNumber) {
        this.bus.trigger('busPhoneMakeForward', phoneNumber.replace('+', ''))
    }

    _openPartner(id) {
        this.action.doAction({
            res_id: id,
            res_model: "res.partner",
            target: 'new',
            type: 'ir.actions.act_window',
            views: [[false, 'form']],
        })
    }
}


export class Contacts extends Component {
    static template = 'asterisk_plus_phone.contacts'
    static components = {ContactList}

    constructor() {
        super(...arguments)
        const {bus, isTransfer = false, isForward = false, isContact = false, contactSearch = 'all'} = this.props
        this.bus = bus
        this.isTransfer = isTransfer
        this.isForward = isForward
        this.isContact = isContact
        this.contactSearch = contactSearch
    }

    setup(props) {
        super.setup()
        this.user = uid
        this.contactInput = useRef('contact-input')
        this.rpc = useService('rpc')
        this.action = useService('action')

        onWillStart(async () => {
            this.bus.on('busContactSetState', this, this._busContactState)
        })

        onMounted(() => {
            setFocus(this.contactInput.el)
        })

        onWillUnmount(() => {
            this.bus.off('busContactSetState', this, this._busContactState)
        })
    }

    _busContactState({isTransfer = false, isForward = false, isContact = false}) {
        this.bus.trigger('busContactListSetState', {isForward, isTransfer, isContact})
        if (this.contactInput.el) {
            this.contactInput.el.value = ''
            setFocus(this.contactInput.el)
        }
    }

    _onSearchContact(ev) {
        if (ev.key === "Enter") {
            this.bus.trigger('busContactCall')
        } else {
            this.bus.trigger('busContactSearchQuery', {searchQuery: ev.target.value})
        }
    }

    _onClickClearSearchContact(ev) {
        this.bus.trigger('busContactSearchQuery', {searchQuery: ''})
        this.contactInput.el.value = ''
        setFocus(this.contactInput.el)
    }
}
