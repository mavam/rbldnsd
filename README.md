This enhanced version of [rbldnsd](http://www.corpit.ru/mjt/rbldnsd.html)
provides enhanced logging features:

- IP address anonymization (via SHA256 hashing)
- GeoIP lookup of client IP addresses
- Contents of the reply RR

Note that this version rbldnsd uses a tab character (`\t`) to separate the log
fields, since the new GeoIP fields may contain spaces.

Installation
============

The installation procedure is the same as with the stock version of rbldnsd:

    ./configure && make && make install

Additionaly, the configure script supports the options `anonymize` and `geoip`.
Anonymization requires OpenSSL and GeoIP lookups require libGeoIP. If your
system provides these dependencies, these options are automatically enabled.

Usage
=====

The new features require explicit activation on the command line:

- `-z`: enable IP address anonymization
- `-g`: enable GeoIP lookups
- `-L`: enables logging of answer details the logfile
