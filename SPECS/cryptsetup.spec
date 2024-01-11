Summary: Utility for setting up encrypted disks
Name: cryptsetup
Version: 2.6.0
Release: 3%{?dist}
License: GPLv2+ and LGPLv2+
URL: https://gitlab.com/cryptsetup/cryptsetup
BuildRequires: openssl-devel, popt-devel, device-mapper-devel
BuildRequires: libuuid-devel, gcc, json-c-devel
BuildRequires: libpwquality-devel, libblkid-devel
BuildRequires: make
BuildRequires: asciidoctor
Requires: cryptsetup-libs = %{version}-%{release}
Requires: libpwquality >= 1.2.0
Obsoletes: %{name}-reencrypt <= %{version}
Provides: %{name}-reencrypt = %{version}

%global upstream_version %{version}
Source0: https://www.kernel.org/pub/linux/utils/cryptsetup/v2.6/cryptsetup-%{upstream_version}.tar.xz

# binary archive with updated tests/conversion_imgs.tar.xz and tests/luks2_header_requirements.tar.xz
# for testing (can not be patched via rpmbuild)
Source1: tests.tar.xz

# Following patch has to applied last
Patch0000: %{name}-2.6.1-Run-PBKDF-benchmark-with-8-bytes-long-well-known-pas.patch
Patch0001: %{name}-2.6.1-Change-tests-to-use-passphrases-with-minimal-8-chars.patch
Patch0002: %{name}-2.6.1-Enable-crypt_header_is_detached-for-empty-contexts.patch
Patch0003: %{name}-2.6.1-Abort-encryption-when-header-and-data-devices-are-sa.patch
Patch0004: %{name}-2.7.0-Disallow-use-of-internal-kenrel-crypto-driver-names-.patch
Patch0005: %{name}-2.7.0-Also-disallow-active-devices-with-internal-kernel-na.patch
Patch0006: %{name}-2.7.0-Fix-init_by_name-to-allow-unknown-cipher-format-in-d.patch
Patch0007: %{name}-2.7.0-Fix-reencryption-to-fail-properly-for-unknown-cipher.patch
Patch0008: %{name}-2.7.0-Fix-activation-of-LUKS2-with-capi-format-cipher-and-.patch
Patch9998: %{name}-Add-FIPS-related-error-message-in-keyslot-add-code.patch
Patch9999: %{name}-add-system-library-paths.patch

%description
The cryptsetup package contains a utility for setting up
disk encryption using dm-crypt kernel module.

%package devel
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Summary: Headers and libraries for using encrypted file systems

%description devel
The cryptsetup-devel package contains libraries and header files
used for writing code that makes use of disk encryption.

%package libs
Summary: Cryptsetup shared library

%description libs
This package contains the cryptsetup shared library, libcryptsetup.

%package -n veritysetup
Summary: A utility for setting up dm-verity volumes
Requires: cryptsetup-libs = %{version}-%{release}

%description -n veritysetup
The veritysetup package contains a utility for setting up
disk verification using dm-verity kernel module.

%package -n integritysetup
Summary: A utility for setting up dm-integrity volumes
Requires: cryptsetup-libs = %{version}-%{release}

%description -n integritysetup
The integritysetup package contains a utility for setting up
disk integrity protection using dm-integrity kernel module.

%prep
%autosetup -n cryptsetup-%{upstream_version} -p 1 -a 1

%build
rm -f man/*.8
%configure --enable-fips --enable-pwquality --enable-internal-sse-argon2 --disable-ssh-token --enable-asciidoc
%make_build

%install
%make_install
rm -rf %{buildroot}%{_libdir}/*.la

%find_lang cryptsetup

%ldconfig_scriptlets -n cryptsetup-libs

%files
%license COPYING
%doc AUTHORS FAQ.md docs/*ReleaseNotes
%{_mandir}/man8/cryptsetup.8.gz
%{_mandir}/man8/cryptsetup-*.8.gz
%{_sbindir}/cryptsetup

%files -n veritysetup
%license COPYING
%{_mandir}/man8/veritysetup.8.gz
%{_sbindir}/veritysetup

%files -n integritysetup
%license COPYING
%{_mandir}/man8/integritysetup.8.gz
%{_sbindir}/integritysetup

%files devel
%doc docs/examples/*
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files libs -f cryptsetup.lang
%license COPYING COPYING.LGPL
%{_libdir}/libcryptsetup.so.*
%dir %{_libdir}/%{name}/
%{_tmpfilesdir}/cryptsetup.conf
%ghost %attr(700, -, -) %dir /run/cryptsetup

%changelog
* Fri Jun 30 2023 Daniel Zatovic <dzatovic@redhat.com> - 2.6.0-3
- patch: Disallow use of internal kenrel crypto driver names in "capi"
- patch: Also disallow active devices with internal kernel names
- patch: Fix init_by_name to allow unknown cipher format in dm-crypt
- patch: Fix reencryption to fail properly for unknown cipher
- patch: Fix activation of LUKS2 with capi format cipher and kernel
- Resolves: #2212771

* Wed Dec 14 2022 Daniel Zatovic <dzatovic@redhat.com> - 2.6.0-2
- Fix FIPS related bugs.
- Abort encryption when header and data devices are same.
- Resolves: #2150251 #2148841

* Wed Nov 30 2022 Daniel Zatovic <dzatovic@redhat.com> - 2.6.0-1
- Update to cryptsetup 2.6.0.
- Resolves: #2003748 #2108404 #1862173

* Wed Aug 10 2022 Ondrej Kozina <okozina@redhat.com> - 2.4.3-5
- patch: Delegate FIPS mode detection to crypto backend.
- Resolves: #2080516

* Thu Feb 24 2022 Ondrej Kozina <okozina@redhat.com> - 2.4.3-4
- patch: Fix broken upstream test.
- Resolves: #2056439

* Wed Feb 23 2022 Ondrej Kozina <okozina@redhat.com> - 2.4.3-3
- patch: Fix cryptsetup --test-passphrase when device in
  reencryption
- Resolves: #2056439

* Thu Feb 17 2022 Ondrej Kozina <okozina@redhat.com> - 2.4.3-2
- Various FIPS related fixes.
- Resolves: #2051630

* Fri Jan 21 2022 Ondrej Kozina <okozina@redhat.com> - 2.4.3-1
- Update to cryptsetup 2.4.3.
- patch: Fix typo in repair command prompt.
  Resolves: #2022309 #2023316 #2032782

* Wed Sep 29 2021 Ondrej Kozina <okozina@redhat.com> - 2.4.1-1
- Update to cryptsetup 2.4.1.
  Resolves: #2005035 #2005877

* Thu Aug 19 2021 Ondrej Kozina <okozina@redhat.com> - 2.4.0-1
- Update to cryptsetup 2.4.0.
  Resolves: #1869553 #1972722 #1974271 #1975799

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 2.3.6-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Jun 17 2021 Mohan Boddu <mboddu@redhat.com> - 2.3.6-2
- Specbump for openssl 3.0
  Related: rhbz#1971065

* Wed Jun 16 2021 Ondrej Kozina <okozina@redhat.com> - 2.3.6-1
- Update to cryptsetup 2.3.6.
- Resolves: #1961291 #1970932

* Tue Jun 15 2021 Mohan Boddu <mboddu@redhat.com> - 2.3.5-5
- Rebuilt for RHEL 9 BETA for openssl 3.0

Related: rhbz#1971065

* Tue Apr 27 2021 Ondrej Kozina <okozina@redhat.com> - 2.3.5-4
- Drop dependency on libargon2
- Resolves: #1936959

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 2.3.5-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Thu Mar 11 2021 Milan Broz <gmazyland@gmail.com> - 2.3.5-1
- Update to cryptsetup 2.3.5.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 03 2020 Milan Broz <gmazyland@gmail.com> - 2.3.4-1
- Update to cryptsetup 2.3.4.
- Fix for CVE-2020-14382 (#1874712)
