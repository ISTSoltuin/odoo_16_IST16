odoo.define("wedrive_beta.WeDrivePlateSearch", function (require) {
    "use strict";

    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const { useListener } = require("@web/core/utils/hooks");
    class WeDrivePlateSearch extends PosComponent {
        setup() {
            super.setup();
            useListener("click", this.onClick);
        }
        async onClick() {
            var self = this;
            const { confirmed, payload } = await this.showPopup("WeDrivePlateSearchPopup", {
                title: this.env._t("Plate Search"),
                body: this.env._t("Enter the plate number"),
            });
            if (confirmed) {
                this.trigger("update-search", payload);
            }
        }
    }
    WeDrivePlateSearch.template = "WeDrivePlateSearch";
    ProductScreen.addControlButton({
        component: WeDrivePlateSearch,
        isVisible: () => true,
        position: ["before", "OrderlineCustomerNoteButton"],
    });
    Registries.Component.add(WeDrivePlateSearch);

    return WeDrivePlateSearch;
})