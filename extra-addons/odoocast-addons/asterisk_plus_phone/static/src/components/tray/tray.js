/** @odoo-module **/
"use strict"
import {useService} from "@web/core/utils/hooks"
import {browser} from "@asterisk_plus_phone/js/utils"

const {Component, useState, onMounted, onWillStart, markup} = owl

export class PhoneSysTray extends Component {
    static template = 'asterisk_plus_phone.menu'

    constructor() {
        super(...arguments)
        this.bus = this.props.bus
        this.state = useState({
            isDisplay: false,
            inCall: false
        })
        this.sound = false
        this.microphone = false
        this.message = 'For better user experience grant permission for: '
        this.browser = navigator.userAgent.includes("Firefox") ? browser.firefox : browser.chrome
    }

    setup() {
        super.setup()
        this.notification = useService("notification")
        this.permissionsChecked = localStorage.getItem('asterisk_plus_phone_permissions_checked')

        onMounted(() => {
            this.bus.on('busTraySetState', this, function ({isDisplay, inCall}) {
                this.state.isDisplay = isDisplay
                this.state.inCall = inCall
            })
            if (this.permissionsChecked) return
            // Check sound permission
            this.testPlayer.play().then(() => {
                this.sound = true
                this.checkPermissions()
            }).catch((e) => {
                this.checkPermissions()
            })
        })

        onWillStart(async () => {
            if (this.permissionsChecked) return
            this.testPlayer = new Audio()
            this.testPlayer.src = "/asterisk_plus_phone/static/src/sounds/mute.mp3"
            this.testPlayer.volume = 0.5
            const self = this
            // Check microphone permission for Chrome
            if (this.browser === browser.chrome) {
                const permissionStatus = await navigator.permissions.query({name: 'microphone'})
                if (permissionStatus.state === "granted") {
                    this.microphone = true
                }
                // Check microphone permission for Firefox
            } else if (this.browser === browser.firefox) {
                navigator.mediaDevices
                        .getUserMedia({video: false, audio: true})
                        .then((stream) => {
                            stream.getTracks().forEach(function (track) {
                                track.stop()
                                self.microphone = true
                            })
                        })
                        .catch((err) => {
                            console.error(`you got an error: ${err}`)
                        })
            }
        })
    }

    checkPermissions() {
        if (!this.microphone || !this.sound) {
            this.notify()
        }
        localStorage.setItem('asterisk_plus_phone_permissions_checked', 'true')
    }

    notify() {
        this.message += this.sound ? '' : '<br/>&emsp; - Sound'
        this.message += this.microphone ? '' : '<br/>&emsp; - Microphone'
        this.message += '<br/><a href="https://help.odoopbx.com/en/articles/8945386-browser-configuration-for-asterisk-plus-phone" target="_blank" style="text-decoration: underline;">See documentation how do this!</a>'
        this.notification.add(markup(this.message), {title: 'Phone', sticky: true, type: 'warning'})
    }

    _onClick() {
        this.bus.trigger('busPhoneToggleDisplay')
    }

    _onClickHangUp() {
        this.bus.trigger('busPhoneHangUp')
        this.state.isDisplay = false
        this.state.inCall = false
    }
}