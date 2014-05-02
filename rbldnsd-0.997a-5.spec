# RPM spec file for rbldnsd

%define   gitsnap  300daa0
%define _home /var/lib/rbldnsd

%define _rbldnsuid 6490
%define _rbldnsusr rbldns
%define _rbldnsgid 6490
%define _rbldnsgrp rbldns
%define  name rbldnsd
%define  version 0.997a


Summary: Small fast daemon to serve DNSBLs
Name: %{name}
Version: %{version}
Release: 5.git_300daa0
License: GPL
Group: System Environment/Daemons
BuildRoot: %_tmppath/%name-%version
Source: http://www.corpit.ru/mjt/%name/%{name}-%{gitsnap}.tar.gz
Source1: %{name}.suburl.org.cron

BuildRequires:  zlib-devel
BuildRequires:  glibc-devel
BuildRequires:  linux-glibc-devel
BuildRequires:  libnet-devel

Requires:  util-linux
Requires:  aaa_base
Requires:  coreutils
Requires:  zlib
Requires:  glibc
Requires:  shadow
Requires:  pam



%description
Rbldnsd is a small authoritate-only DNS nameserver
designed to serve DNS-based blocklists (DNSBLs).
It may handle IP-based and name-based blocklists.

%prep
%setup -q -n %name-%gitsnap

%build
test "%{buildroot}" != "/" && %__rm -rf "%{buildroot}"
mkdir -p %{buildroot}

CFLAGS="$RPM_OPT_FLAGS" CC="${CC:-%__cc}" ./configure  \
        --enable-asserts  \
        --enable-stats \
        --enable-master-dump \
        --enable-ipv6
make

%install

mkdir -p $RPM_BUILD_ROOT{%_sbindir,%_datadir,%_mandir/man8,/etc/init.d,/etc/sysconfig}
mkdir -p $RPM_BUILD_ROOT/%_libdir/%{name}
mkdir -p $RPM_BUILD_ROOT/%_includedir/%{name}
mkdir -p $RPM_BUILD_ROOT/var/lib/%{name}/bin

install -m 0755 rbldnsd $RPM_BUILD_ROOT%_sbindir/
install -m 0644 -p rbldnsd.8 $RPM_BUILD_ROOT%_mandir/man8/
install -m 0644  debian/rbldnsd.default $RPM_BUILD_ROOT/etc/sysconfig/rbldnsd
install -m 0755 debian/rbldnsd.init $RPM_BUILD_ROOT/etc/init.d/rbldnsd

install -m 0644 librbldnsd.a $RPM_BUILD_ROOT/%_libdir/%{name}/librbldnsd.a
for i in `ls *.h`
do
install -m 0644 $i $RPM_BUILD_ROOT/%_includedir/%{name}/$i
done

test -d $RPM_BUILD_ROOT/var/lib/%{name} || mkdir -p $RPM_BUILD_ROOT/var/lib/%{name}/bin
install -m 755 %{S:1} $RPM_BUILD_ROOT/var/lib/%{name}/bin/suburl.org.cron


%clean
test "%{buildroot}" != "/" && %__rm -rf "%{buildroot}"

%pre

set -x

rbldnsuid=%{_rbldnsuid}
rbldnsgid=%{_rbldnsgid}
rbldnsusr=%{_rbldnsusr}
rbldnsgrp=%{_rbldnsgrp}
rbldnshome=%{_home}

echo $rbldnshome

if ! getent group $rbldnsgrp; then
      /usr/sbin/groupadd -g $rbldnsgid $rbldnsgrp > /dev/null 2>&1
        echo " required"  $rbldnsgrp "group not exist -  added rbldns group  - gid"  $rbldnsgid
fi


if ! getent passwd $rbldnsusr ; then
   useradd -g $rbldnsgid -u $rbldnsuid -m -d $rbldnshome -c "rbldns Daemon" -s /sbin/nologin $rbldnsusr > /dev/null 2>&1
        echo " required" $rbldnsusr "user  has not exist -  added rbldns user - uid"  $rbldnsuid
fi

test -d $rbldnshome && chown -R $rbldnsuid:$rbldnsgid $rbldnshome

# remove  skelton user dirs if exist
test -d $rbldnshome/public_html && cd  $rbldnshome ; rm -rf ./public_html
test -d $rbldnshome/.emacs && cd  $rbldnshome ; rm -rf .emacs
test -d $rbldnshome/.fonts && cd  $rbldnshome ; rm -rf .fonts
test -d $rbldnshome/.local && cd  $rbldnshome ; rm -rf .local
test -d $rbldnshome/.config && cd  $rbldnshome ; rm -rf .config
test -f $rbldnshome/.xinitrc.template && cd  $rbldnshome ; rm -f .xinitrc.template


%post

rbldnsuid=%{_rbldnsuid}
rbldnsgid=%{_rbldnsgid}
rbldnsusr=%{_rbldnsusr}
rbldnsgrp=%{_rbldnsgrp}
rbldnshome=%{_home}


test -d $rbldnshome && mkdir -p $rbldnshome/dsbl; chown rbldns:rbldns $rbldnshome/dsbl
test -f /etc/sysconfig/rbldnsd && cp -p /etc/sysconfig/rbldnsd /etc/sysconfig/rbldnsd.orig;  cat > /etc/sysconfig/rbldnsd.new << EOF
#
# default config
#  list.dsbl.org on local 127.0.0.2 port 753
RBLDNSD="dsbl -r/var/lib/rbldnsd/dsbl -b127.2/753 list.dsbl.org:ip4set:list -u rbldns -4 "
#
EOF
#
test -f /etc/sysconfig/rbldnsd.new && cat /etc/sysconfig/rbldnsd.orig /etc/sysconfig/rbldnsd.new >/etc/sysconfig/rbldnsd ;chmod 644 /etc/sysconfig/rbldnsd; rm -f /etc/sysconfig/rbldnsd.orig /etc/sysconfig/rbldnsd.new

#
/sbin/chkconfig --add rbldnsd
/etc/init.d/rbldnsd restart

%preun
if [ $1 -eq 0 ]; then
   /etc/init.d/rbldnsd stop || :
   /sbin/chkconfig --del rbldnsd
fi

%postun
rbldnsuid=%{_rbldnsuid}
rbldnsgid=%{_rbldnsgid}
rbldnsusr=%{_rbldnsusr}
rbldnsgrp=%{_rbldnsgrp}
rbldnshome=%{_home}

echo removing user $rbldnsusr with group $rbldnsgrp
echo $rbldnshome left due not empty
userdel $rbldnsusr
groupdel $rbldnsgrp

echo removing /var/spool/mail/$rbldnsusr
test -f /var/spool/mail/rbldns && rm -f /var/spool/mail/rbldns

%files
%defattr (-,root,root)
%_sbindir/rbldnsd
%config(noreplace) /etc/sysconfig/rbldnsd
/etc/init.d/rbldnsd

%package devel
Summary: rbldnsd - devel
Group: Applications/System
Requires: %{name}

%description devel
Rbldnsd is a small authoritate-only DNS nameserver


%files devel
%_libdir/%{name}/librbldnsd.a
%_includedir/%{name}/*.h


%package doc
Summary: rbldnsd - Documents
Group: Applications/System
Requires: %{name}
Requires: man

%description doc
rbldnsd - Documents

%files doc
%defattr(-,root,root)
%doc README.user NEWS TODO debian/changelog CHANGES-0.81
%_mandir/man8/rbldnsd.8*


%package cron
Summary: rbldnsd - RBL cron jobs
Group: Applications/System
Requires: %{name}
Requires: rsync
Requires: cron

%description cron
rbldnsd - cron mirrot jobs
see http://www.surbl.org/setup-local-rbl-mirror

 (Note: there is a dot between "rbldnsd" and ">" to denote the current directory,
  and you'll replace some_rsync_server in the rbldnsd.cron script with the
 _ actual rsync server_   name provided when you are _granted RYSNC access_ from surbl.org - needs register with valididated email.

[Editor: Also note that multi.surbl.org.rbldnsd is the only zone that should be used.]

%files cron
%defattr(0750,root,root,0750)
/var/lib/rbldnsd/bin/suburl.org.cron

%post cron
cat <(crontab -l -u rbldns) <(echo "10,40 * * * * /var/lib/rbldnsd/bin/suburl.org.cron") | crontab -

# listening local on port 754
test -d /etc/rbldnsd && echo "# listening local on port 754" >/etc/rbldnsd/rbldnsd-multi.surbl.conf; echo "multi.surbl -r/var/lib/named/surbl -t21600 -c60 -b127.0.0.1/754 " >>/etc/rbldnsd/rbldnsd-multi.surbl.conf; echo "multi.surbl.org:dnset:multi.surbl.org.rbldnsd" >>/etc/rbldnsd/rbldnsd-multi.surbl.conf

test -d /etc/rbldnsd && cat > /etc/rbldnsd/rbldnsd-multi.named.zone << EOF
;
; bind9 zone config
zone "multi.surbl.org" IN {
        type forward;
        forward first;
        forwarders {
        127.0.0.1 port 754;
        };
};
;
EOF


%postun cron
( crontab -l -u rbldns | egrep -v "suburl.org.cron" ) | crontab -u rbldns -


%changelog
* Wed Apr 30  2014 support@remsnet.de -r5
update to 0.997a - -300daa0 GIT http://www.corpit.ru/mjt/rbldnsd.html
- added %doc , %devel sub packages
- updated %cleanup - test "%{buildroot}" != "/" && %__rm -rf "%{buildroot}"
- added --enable-asserts --enable-stats --enable-master-dump --enable-ipv6
- updated user creation , user /gid now at 6490
- added %cron package - http://www.surbl.org/setup-local-rbl-mirror

* Wed Jul 7 2004 Horst Venzke <hv@remsnet.de>
- First Suse9 Package
