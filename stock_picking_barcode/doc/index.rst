===========================================
 Barcode scanner support for Stock Picking
===========================================

Usage
=====

* Open barcode scanning page

  * either click barcode icon at ``Inventory / Dashboard`` menu
  * or select some Stock Picking and click barcode icon there

* Scan product barcode;

* Quantity of scanned product is increased;


Prevents creating extra move
----------------------------

* Open ``[[Inventory]] >> Configuration >> Settings`` menu
* Activate ``Prevents creating extra move`` option
* Go to barcode scanning page
* Set ``Scanned`` qty greater than ``ToDo`` qty
* Click ``Create backorder``
RESULT: extra move for excessed qty is not created
