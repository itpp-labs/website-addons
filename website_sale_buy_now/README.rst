.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

'Buy Now' button in web shop
============================

Add a settings to Product, that allows to sale:

* via usual "Add to cart" button only
* via "Buy Now" button only
* both buttons

After clicking on "buy now" at web shop:

* cart is cleared and the product is added
* user is redirected to /shop/checkout page
* page /shop/cart is still availabe, but
  * it doesn't have "continue shopping button"

Tested on `Odoo 8.0 <https://github.com/odoo/odoo/commit/f89220a51313e1bf46ec82175f2449c2e1a0455c>`_
