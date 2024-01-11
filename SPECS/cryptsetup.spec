Obsoletes: python2-cryptsetup
Obsoletes: cryptsetup-python
Obsoletes: cryptsetup-python3

Summary: A utility for setting up encrypted disks
Name: cryptsetup
Version: 2.3.7
Release: 7%{?dist}
License: GPLv2+ and LGPLv2+
Group: Applications/System
URL: https://gitlab.com/cryptsetup/cryptsetup
BuildRequires: openssl-devel, popt-devel, device-mapper-devel
BuildRequires: libuuid-devel, gcc, libblkid-devel
BuildRequires: libpwquality-devel, json-c-devel
Provides: cryptsetup-luks = %{version}-%{release}
Obsoletes: cryptsetup-luks < 1.4.0
Requires: cryptsetup-libs = %{version}-%{release}
Requires: libpwquality >= 1.2.0

%global upstream_version %{version}
Source0: https://www.kernel.org/pub/linux/utils/cryptsetup/v2.0/cryptsetup-%{upstream_version}.tar.xz
# binary archive with updated tests/conversion_imgs.tar.xz and tests/luks2_header_requirements.tar.xz
# for testing (can not be patched via rpmbuild)
Source1: tests.tar.xz
# Following patch has to applied last
Patch0:  %{name}-add-system-library-paths.patch
# Remove the patch when (if ever) osci infrastructure gets stable enough
Patch1:  %{name}-disable-verity-compat-test.patch
Patch2:  %{name}-2.4.2-Do-not-try-to-set-compiler-optimization-flag-if-wipe.patch
Patch3:  %{name}-2.4.2-Fix-bogus-memory-allocation-if-LUKS2-header-size-is-.patch
Patch4:  %{name}-2.5.0-Fix-typo-in-repair-prompt.patch
Patch5:  %{name}-2.5.0-Fix-test-passphrase-when-device-in-reencryption.patch
Patch6:  %{name}-2.5.0-Add-more-tests-for-test-passphrase-parameter.patch
Patch7:  %{name}-2.5.0-Remove-LUKS2-encryption-data-size-restriction.patch
Patch8: %{name}-2.6.0-Fix-cipher-convert-routines-naming-confusion.patch
Patch9: %{name}-2.6.0-Move-cipher_dm2c-to-crypto-utilities.patch
Patch10: %{name}-2.6.0-Code-cleanup.patch
Patch11: %{name}-2.6.0-Copy-also-integrity-string-in-legacy-mode.patch
Patch12: %{name}-2.6.0-Fix-internal-crypt-segment-compare-routine.patch
Patch13: %{name}-2.6.0-Delegate-FIPS-mode-detection-to-configured-crypto-ba.patch
Patch14: %{name}-2.6.1-Abort-encryption-when-header-and-data-devices-are-sa.patch
Patch15: %{name}-2.7.0-Disallow-use-of-internal-kenrel-crypto-driver-names-.patch
Patch16: %{name}-2.7.0-Also-disallow-active-devices-with-internal-kernel-na.patch
Patch17: %{name}-2.7.0-Fix-init_by_name-to-allow-unknown-cipher-format-in-d.patch
Patch18: %{name}-2.7.0-Fix-reencryption-to-fail-properly-for-unknown-cipher.patch
Patch19: %{name}-2.7.0-Fix-activation-of-LUKS2-with-capi-format-cipher-and-.patch

%description
The cryptsetup package contains a utility for setting up
disk encryption using dm-crypt kernel module.

%package devel
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Summary: Headers and libraries for using encrypted file systems
Provides: cryptsetup-luks-devel = %{version}-%{release}
Obsoletes: cryptsetup-luks-devel < 1.4.0

%description devel
The cryptsetup-devel package contains libraries and header files
used for writing code that makes use of disk encryption.

%package libs
Group: System Environment/Libraries
Summary: Cryptsetup shared library
Provides: cryptsetup-luks-libs = %{version}-%{release}
Obsoletes: cryptsetup-luks-libs < 1.4.0

%description libs
This package contains the cryptsetup shared library, libcryptsetup.

%package -n veritysetup
Group: Applications/System
Summary: A utility for setting up dm-verity volumes
Requires: cryptsetup-libs = %{version}-%{release}

%description -n veritysetup
The veritysetup package contains a utility for setting up
disk verification using dm-verity kernel module.

%package -n integritysetup
Group: Applications/System
Summary: A utility for setting up dm-integrity volumes
Requires: cryptsetup-libs = %{version}-%{release}

%description -n integritysetup
The integritysetup package contains a utility for setting up
disk integrity protection using dm-integrity kernel module.

%package reencrypt
Group: Applications/System
Summary: A utility for offline reencryption of LUKS encrypted disks.
Requires: cryptsetup-libs = %{version}-%{release}

%description reencrypt
This package contains cryptsetup-reencrypt utility which
can be used for offline reencryption of disk in situ.

%prep
%setup -q -n cryptsetup-%{upstream_version} -a 1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch0 -p1
chmod -x misc/dracut_90reencrypt/*

%build
%configure --enable-fips --enable-pwquality --enable-internal-sse-argon2 --with-crypto_backend=openssl --with-default-luks-format=LUKS2
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{_libdir}/*.la

%find_lang cryptsetup

%post -n cryptsetup-libs -p /sbin/ldconfig

%postun -n cryptsetup-libs -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS FAQ docs/*ReleaseNotes
%{_mandir}/man8/cryptsetup.8.gz
%{_sbindir}/cryptsetup

%files -n veritysetup
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man8/veritysetup.8.gz
%{_sbindir}/veritysetup

%files -n integritysetup
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man8/integritysetup.8.gz
%{_sbindir}/integritysetup

%files reencrypt
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc misc/dracut_90reencrypt
%{_mandir}/man8/cryptsetup-reencrypt.8.gz
%{_sbindir}/cryptsetup-reencrypt

%files devel
%doc docs/examples/*
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files libs -f cryptsetup.lang
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LGPL
%{_libdir}/libcryptsetup.so.*
%{_tmpfilesdir}/cryptsetup.conf
%ghost %attr(700, -, -) %dir /run/cryptsetup

%clean

%changelog
* Tue Jul 11 2023 Ondrej Kozina <okozina@redhat.com> - 2.3.7-7
- Rebuild due to missing CI environment
- Resolves: #2212772 #2193342

* Thu Jun 28 2023 Daniel Zatovic <dzatovic@redhat.com> - 2.3.7-6
- patch: Delegate FIPS mode detection to configured crypto backend
- patch: Disallow use of internal kenrel crypto driver names in "capi"
- patch: Also disallow active devices with internal kernel names
- patch: Fix init_by_name to allow unknown cipher format in dm-crypt
- patch: Fix reencryption to fail properly for unknown cipher
- patch: Fix activation of LUKS2 with capi format cipher and kernel
- Resolves: #2212772 #2193342

* Tue Jan 10 2023 Daniel Zatovic <dzatovic@redhat.com> - 2.3.7-5
- change cryptsetup-devel dependency from cryptsetup to cryptsetup-libs
- Resolves: #2150254

* Wed Dec 21 2022 Daniel Zatovic <dzatovic@redhat.com> - 2.3.7-4
- patch: Remove LUKS2 encryption data size restriction.
- patch: Abort encryption when header and data devices are same.
- Resolves: #2150254

* Fri Nov 4 2022 Daniel Zatovic <dzatovic@redhat.com> - 2.3.7-3
- patch: Fix internal crypt segment compare routine
- Resolves: #2110810

* Thu Feb 24 2022 Ondrej Kozina <okozina@redhat.com> - 2.3.7-2
- patch: Fix cryptsetup --test-passphrase when device in
  reencryption
- Resolves: #2058009

* Thu Jan 20 2022 Ondrej Kozina <okozina@redhat.com> - 2.3.7-1
- update to cryptsetup 2.3.7
- fixes CVE-2021-4122
- patch: Fix suboptimal optimization in bundled argon2.
- patch: Fix bogus memory allocation/device read with
         invalid LUKS2 headers
- patch: Fix typo in luksRepair prompt.
- Resolves: #2021815 #2022301 #2031859

* Wed Feb 17 2021 Ondrej Kozina <okozina@redhat.com> - 2.3.3-4
- patch: Fix reencryption for custom devices with data segments
  set to use cipher_null.
- Resolves: #1927409

* Wed Feb 03 2021 Ondrej Kozina <okozina@redhat.com> - 2.3.3-3
- patch: Fix crypto backend to properly handle ECB mode.
- Resolves: #1859091

* Thu Aug 27 2020 Ondrej Kozina <okozina@redhat.com> - 2.3.3-2
- patch: Fix possible memory corruption in LUKS2 validation
	 code in 32bit library.
- Resolves: #1872294

* Thu May 28 2020 Ondrej Kozina <okozina@redhat.com> - 2.3.3-1
- Update to cryptsetup 2.3.3
- Resolves: #1796826 #1743891 #1785748

* Fri Apr 03 2020 Ondrej Kozina <okozina@redhat.com> - 2.3.1-1
- Update to cryptsetup 2.3.1
- Resolves: #1796826 #1743891 #1785748

* Mon Nov 18 2019 Ondrej Kozina <okozina@redhat.com> - 2.2.2-1
- Update to cryptsetup 2.2.2
- LUKS2 reencryption honors activation flags (one time and persistent).
- LUKS2 reencryption works also without volume keys put in kernel
  keyring service.
- Resolves: #1757783 #1750680 #1753597 #1743399

* Fri Aug 30 2019 Ondrej Kozina <okozina@redhat.com> - 2.2.0-2
- patch: Fix mapped segments overflow on 32bit architectures.
- patch: Take optimal io size in account with LUKS2 reencryption.
- Resolves: #1742815 #1746532

* Thu Aug 15 2019 Ondrej Kozina <okozina@redhat.com> - 2.2.0-1
- Update to cryptsetup 2.2.0 (final)
- Resolves: #1738263 #1740342 #1733391 #1729600 #1733390

* Fri Jun 14 2019 Ondrej Kozina <okozina@redhat.com> - 2.2.0-0.2
- Updates to reencryption feature.
- Resolves: #1676622

* Fri May 03 2019 Ondrej Kozina <okozina@redhat.com> - 2.2.0-0.1
- Update to cryptsetup 2.2.0
- remove python bits from spec file.
- Resolves: #1676622

* Thu Mar 21 2019 Milan Broz <mbroz@redhat.com> - 2.0.6-2
- Add gating tests.
- Resolves: #1682539

* Mon Dec 03 2018 Ondrej Kozina <okozina@redhat.com> - 2.0.6-1
- Update to cryptsetup 2.0.6
- Enables all supported metadata sizes in LUKS2 validation code.
- Resolves: #1653383

* Fri Aug 10 2018 Ondrej Kozina <okozina@redhat.com> - 2.0.4-2
- patch: fix device alignment bug when processing hinted
  value by device topology info.
- Resolves: #1614219

* Wed Aug 08 2018 Ondrej Kozina <okozina@redhat.com> - 2.0.4-1
- Update to cryptsetup 2.0.4.
- patch: Add RHEL system library paths in configure.
- patch: Increase default LUKS2 header size to 8 MiBs.
- patch: update tests to be compatible with larger headers.
- Set default format to LUKS2.
- Cleanup changelog.
- Resolves: #1564540 #1595257 #1595266 #1595881 #1600164

* Fri May 04 2018 Ondrej Kozina <okozina@redhat.com> - 2.0.3-1
- Update to cryptsetup 2.0.3.

* Tue Mar 27 2018 Björn Esser <besser82@fedoraproject.org> - 2.0.2-2
- Rebuilt for libjson-c.so.4 (json-c v0.13.1) on fc28

* Wed Mar 07 2018 Milan Broz <gmazyland@gmail.com> - 2.0.2-1
- Update to cryptsetup 2.0.2.
