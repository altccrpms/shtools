# AltCCRPMS
%global _prefix /opt/%{name}/%{version}
%global _sysconfdir %{_prefix}/etc
%global _defaultdocdir %{_prefix}/share/doc
%global _infodir %{_prefix}/share/info
%global _mandir %{_prefix}/share/man

%global _cc_name intel
%global _cc_name_suffix -%{_cc_name}

#We don't want to be beholden to the proprietary libraries
%global    _use_internal_dependency_generator 0
%global    __find_requires %{nil}

# Non gcc compilers don't generate build ids
%undefine _missing_build_ids_terminate_build

%global shortname shtools

Name:           shtools%{?_cc_name_suffix}
Version:        2.8
Release:        2%{?dist}
Summary:        Tools for working with spherical harmonics

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.ipgp.fr/~wieczor/SHTOOLS/SHTOOLS.html
Source0:        http://www.ipgp.fr/~wieczor/SHTOOLS%{version}.tar.Z
Source1:        shtools.module.in
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       fftw-devel
Requires:       environment-modules
Provides:       %{shortname}%{?_cc_name_suffix} = %{version}-%{release}
Provides:       %{shortname}%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}

%description
SHTOOLS is an archive of fortran 95 based software that can be used to
perform (among others) spherical harmonic transforms and reconstructions,
rotations of spherical harmonic coefficients, and multitaper spectral
analyses on the sphere.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Provides:       %{shortname}%{?_cc_name_suffix}-devel = %{version}-%{release}
Provides:       %{shortname}%{?_cc_name_suffix}-devel%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n SHTOOLS
#ifort needs .f90
find -name \*.f95 | while read x 
do
  mv $x ${x/.f95/.f90}
done
sed -i -e 's/\.f95/.f90/g' src/Makefile


%build
export F95FLAGS="-O3 -axSSE3,SSSE3,SSE4.1,SSE4.2 -ipo"
make F95=ifort AR=xiar %{?_smp_mflags}
mv man/man1 man/man3
for x in man/man3/*.1
do
  mv $x ${x/.1/.3}
done


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp -p lib/* $RPM_BUILD_ROOT%{_libdir}
cp -p modules/* $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
cp -rp man/man3 $RPM_BUILD_ROOT%{_mandir}

# AltCCRPMS
# Make the environment-modules file
mkdir -p %{buildroot}/etc/modulefiles/%{shortname}/%{_cc_name}/%{version}
# Since we're doing our own substitution here, use our own definitions.
sed -e 's#@PREFIX@#'%{_prefix}'#' -e 's#@LIB@#%{_lib}#' -e 's#@ARCH@#%{_arch}#' -e 's#@CC@#%{_cc_name}#' \
    < %SOURCE1 > %{buildroot}/etc/modulefiles/%{shortname}/%{_cc_name}/%{version}/%{_arch}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files devel
%doc LICENSE
/etc/modulefiles/%{shortname}/
%{_prefix}/


%changelog
* Wed Oct 16 2013 Orion Poplawski <orion@cora.nwra.com> - 2.8-2
- Rebuild with intel 2013sp1

* Tue Apr 9 2013 Orion Poplawski <orion@cora.nwra.com> - 2.8-1
- Update to 2.8
- intel 2013

* Mon Sep 10 2012 Orion Poplawski <orion@cora.nwra.com> - 2.7-1
- Update to 2.7
- intel 2012
- AltCCRPMs

* Fri Oct 28 2011 Orion Poplawski <orion@cora.nwra.com> - 2.5-4
- ifort 12.1.1.256 Build 20111011

* Mon Oct 3 2011 Orion Poplawski <orion@cora.nwra.com> - 2.5-3
- ifort 12.1.0.233 Build 20110811

* Wed Aug 24 2011 Orion Poplawski <orion@cora.nwra.com> - 2.5-2
- ifort 2011.5.220
