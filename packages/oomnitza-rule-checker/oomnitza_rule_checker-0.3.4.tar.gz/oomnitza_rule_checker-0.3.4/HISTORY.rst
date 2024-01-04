=======
History
=======

0.1.0 (2021-06-01)
------------------

* Initial release

0.3.4 (2023-12-21)
------------------
Fix HAS_CHANGED comparsion for numerics in str and float formats.
For example, no change will be detected if the contents of the datatypes are unchanged.
    str("1.0") == float(1.0)
