Summary: OVH Check Out
Name: oco
Version: 1.15
Release: 2%{?dist}
# The sources don't contain any info, but the official website states :
# "OCO is under the GPL licence."
License: GPL+
Group: System Environment/Daemons
URL: http://help.ovh.co.uk/Oco
Source0: ftp://ftp.ovh.net/made-in-ovh/oco/oco-ded.tar.gz
Source1: oco.init
Patch0: oco-ded-1.15-pidfile.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# For the /etc/cron.d parent directory
Requires: vixie-cron
BuildArch: noarch

%description
OCO is the software used by OVH on their infrastructure to know the status of
servers. Each server running in a cluster should check and tell others if it
is ok or not. OCO is compatible with load balancing cards of the Cisco SLB
type / ACE (SMTP probe).


%prep
%setup -q -n oco-ded-%{version}
%patch0 -p1 -b .pidfile
# Move this default script to be with the examples
mv bin/60sec/http bin/examples/
# Remove executable bit from the examples to not create package deps for them
chmod -x bin/examples/*


%build


%install
rm -rf %{buildroot}
# Yeah, it's gr8... but the install.sh is UGLY
# We should try to move files to FHS compliant locations, but they're hardcoded
# everywhere, so it's not that easy.

# Prepare empty directories
mkdir -p %{buildroot}%{_prefix}/local/oco/{bin,lock,result,result_debug}
mkdir -p %{buildroot}%{_prefix}/local/oco/bin/{60sec,120sec,300sec}
mkdir -p %{buildroot}%{_var}/log/oco

# Copy the common where a perl file is located
cp -a bin/common %{buildroot}%{_prefix}/local/oco/bin/

# Create our own clean cron file where we execute the 1, 2 and 5min scripts
mkdir -p %{buildroot}%{_sysconfdir}/cron.d
cat > %{buildroot}%{_sysconfdir}/cron.d/oco << EOF
# Run the OVH Check Out scripts
*/1 * * * * root run-parts %{_prefix}/local/oco/bin/60sec &>/dev/null
*/2 * * * * root run-parts %{_prefix}/local/oco/bin/120sec &>/dev/null
*/5 * * * * root run-parts %{_prefix}/local/oco/bin/300sec &>/dev/null
EOF

# The main daemon, easy to take out of the ugly tree
install -D -m 0755 -p bin/oco-tcpresponder.pl \
    %{buildroot}%{_sbindir}/oco-tcpresponder

# Our custom clean init script
install -D -m 0755 -p %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/init.d/oco


%clean
rm -rf %{buildroot}


%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add oco
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service oco stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del oco
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service oco condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc errorcodes.txt bin/examples
%{_sysconfdir}/cron.d/oco
%{_sysconfdir}/init.d/oco
%{_prefix}/local/oco/
%{_sbindir}/oco-tcpresponder
%dir %{_var}/log/oco/


%changelog
* Wed Mar  7 2012 Matthias Saou <matthias@saou.eu> 1.15-3
- Spec file cleanup, release to the world.

* Wed Mar 10 2010 Matthias Saou <matthias@saou.eu> 1.15-2
- Initial RPM release.

