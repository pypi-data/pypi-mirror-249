##########
Abyssinica
##########

Locale library for the countries of Ethiopia and Eritrea.

See also `HornMT <https://github.com/gebre/HornMT/>`_: a machine-learning corpus for the Horn of Africa region.

*************
Functionality
*************

Numerals
========
Convert between Arabic and Ge'ez numerals::

    >>> from abyssinica.numerals import arabic_to_geez
    >>> arabic_to_geez(42)
    '፵፪'

    >>> from abyssinica.numerals import geez_to_arabic
    >>> geez_to_arabic('፵፪')
    42

Calendar
========
Convert between Gregorian and Ethiopic dates::

    >>> from abyssinica.calendar import Date as EthiopicDate
    >>> from datetime import date as GregorianDate
    >>> EthiopicDate.from_gregorian(GregorianDate(year=1996, month=3, day=2))
    abyssinica.calendar.Date(1988, 6, 23)

    >>> EthiopicDate(year=1988, month=6, day=23).to_gregorian()
    datetime.date(1996, 3, 2)

Romanization
============
Transliterate Ge'ez characters::

    >>> from abyssinica.romanization import romanize
    >>> print(f"{romanize('ሰላም እንደምን አለህ?').capitalize()}")
    Salām ʼendamn ʼalah?
