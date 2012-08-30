This version of [rbldnsd](http://www.corpit.ru/mjt/rbldnsd.html) comes with the
following enhancements to the basic logfile:

- IP address anonymization (via SHA256 hashing)
- GeoIP lookup of client IP addresses

Except for this documentation, the master branch is equivalent to the git
repository at http://git.corpit.ru/?p=rbldnsd.git.

Installation
============

First, check out the branch containing the enhancements:

    git checkout enhanced-logging

The installation does not differ from the basic procedure, but there exist new
configure switches to disable features, if desired.

Usage
=====

The new features require explicit actication on the command line with the
following switches:

- `-z`: enable IP address anonymization
- `-g`: enable GeoIP lookups
