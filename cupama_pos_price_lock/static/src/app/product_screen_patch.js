import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

/* #10: the native restrict_price_control only covers the Price mode of the
 * numpad. A line discount changes the paid price just as much, so the "%"
 * button follows the same right: managers only when the restriction is on. */
patch(ProductScreen.prototype, {
    getNumpadButtons() {
        const buttons = super.getNumpadButtons();
        if (!this.pos.cashierHasPriceControlRights()) {
            for (const button of buttons) {
                if (button.value === "discount") {
                    button.disabled = true;
                }
            }
        }
        return buttons;
    },
});
