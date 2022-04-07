%global binary          seanatic-gateway
%global service         %{binary}.service
%global modbusconf      control-modbus_seanatic-bench-config.json
%global cloudconf       control-cloud-publication_seanatic-config.json
%global composerconf	control-signal-composer-config.json
%global confdir         %{_sysconfdir}/gateway
%global afmdatadir      /var/local/lib/afm/applications
%global modbusbinding   modbus-binding
%global cloudbinding    cloud-publication-binding
%global composerbinding signal-composer-binding

Name:           seanatic-gateway-config 
Version:        0.0.0
Release:        0%{?dist}
Summary:        This project contains all configs sources and useful tools to run seanatic gateway project on board (tested on raspberry pi and solidrun solidense board).
Group:          tool/binary/configs
License:        APL2.0
URL:            http://git.ovh.iot/seanatic/gateway-on-board-config.git
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  systemd-rpm-macros

Requires:       jq
Requires:       afb-binder
Requires:       redis-tsdb-binding
Requires:       modbus-binding
Requires:       signal-composer-binding
Requires:       signal-composer-plugin-seanatic-gateway
Requires:       cloud-publication-binding

%description
%summary

%prep
%autosetup -p 1

%install
install -Dm755 bin/%{binary} %{buildroot}%{_bindir}/%{binary}
install -Dm644 systemd/%{service} %{buildroot}%{_unitdir}/%{service}
install -Dm644 configs/%{modbusconf} %{buildroot}%{confdir}/%{modbusconf}
install -Dm644 configs/%{cloudconf} %{buildroot}%{confdir}/%{cloudconf}
#install -Dm644 configs/%{composerconf} %{buildroot}%{confdir}/%{composerconf}

%files
%{_bindir}/%{binary}
%{_unitdir}/%{service}
%config(noreplace) %{confdir}/%{modbusconf}
%config(noreplace) %{confdir}/%{cloudconf}
#%config(noreplace) %{confdir}/%{composerconf}

%post
# binding config
if [[ -d %{afmdatadir}/%{modbusbinding} ]]; then
    cp %{confdir}/%{modbusconf} %{afmdatadir}/%{modbusbinding}/etc/%{modbusconf}
    chsmack -a App:modbus-binding:Conf %{afmdatadir}/%{modbusbinding}/etc/%{modbusconf}
fi
if [[ -d %{afmdatadir}/%{cloudbinding} ]]; then
    cp %{confdir}/%{cloudconf} %{afmdatadir}/%{cloudbinding}/etc/%{cloudconf}
    chsmack -a App:cloud-publication-binding:Conf %{afmdatadir}/%{cloudbinding}/etc/%{cloudconf}
fi
#if [[ -d %{afmdatadir}/%{composerbinding} ]]; then
#    cp %{confdir}/%{composerconf} %{afmdatadir}/%{composerbinding}/etc/%{composerconf}
#    chsmack -a App:signal-composer-binding:Conf %{afmdatadir}/%{composerbinding}/etc/%{composerconf}
#fi
systemctl is-enabled --quiet redis || systemctl enable redis
systemctl is-active --quiet redis || systemctl start redis
%systemd_post %{service}

%preun
%systemd_preun %{service}

%changelog
