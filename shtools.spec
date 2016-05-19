# AltCCRPMS
%global _cc_name %{getenv:COMPILER_NAME}
%global _cc_version %{getenv:COMPILER_VERSION}
%global _cc_name_ver %{_cc_name}-%{_cc_version}
%global _name_suffix -%{_cc_name}
%global _name_ver_suffix -%{_cc_name_ver}
%global _prefix /opt/%{_cc_name_ver}/%{shortname}-%{version}
%global _modulefiledir /opt/modulefiles/Compiler/%{_cc_name}/%{_cc_version}/%{shortname}

%global _defaultdocdir %{_prefix}/share/doc
%global _mandir %{_prefix}/share/man

# Non gcc compilers don't generate build ids
%undefine _missing_build_ids_terminate_build

%global shortname shtools

Name:           shtools-3.1%{_name_ver_suffix}
Version:        3.1
Release:        4%{?dist}
Summary:        Tools for working with spherical harmonics

Group:          System Environment/Libraries
License:        BSD
URL:            http://shtools.ipgp.fr/
Source0:        https://github.com/SHTOOLS/SHTOOLS/archive/v%{version}.tar.gz#/%{shortname}-%{version}.tar.gz
Source1:        shtools.module.in
# https://github.com/SHTOOLS/SHTOOLS/pull/12
Patch0:         shtools-openmp.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  fftw-devel
# Need to compiled numpy with Intel
#BuildRequires:  numpy-f2py%{?_name_suffix}
BuildRequires:  tcsh
Provides:       %{shortname}%{_name_suffix} = %{version}-%{release}
Provides:       %{shortname}%{_name_suffix}%{?_isa} = %{version}-%{release}
Provides:       %{shortname}%{_name_ver_suffix} = %{version}-%{release}
Provides:       %{shortname}%{_name_ver_suffix}%{?_isa} = %{version}-%{release}

%description
SHTOOLS is an archive of fortran 95 based software that can be used to
perform (among others) spherical harmonic transforms and reconstructions,
rotations of spherical harmonic coefficients, and multitaper spectral
analyses on the sphere.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       fftw-devel
Requires:       environment(modules)
Provides:       %{shortname}%{_name_suffix}-devel = %{version}-%{release}
Provides:       %{shortname}%{_name_suffix}-devel%{?_isa} = %{version}-%{release}
Provides:       %{shortname}%{_name_ver_suffix}-devel = %{version}-%{release}
Provides:       %{shortname}%{_name_ver_suffix}-devel%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n SHTOOLS-%{version}
sed -i -e '/^AR *=/d' src/Makefile
mkdir -p openmp
cp -rl Makefile lib modules src openmp/


%build
export F95FLAGS="$FCFLAGS -ipo -free -Tf"
# f2py fails until we have numpy with intel
make F95=$FC %{?_smp_mflags} || true
pushd openmp
export F95FLAGS="-qopenmp $F95FLAGS"
make F95=$FC %{?_smp_mflags} || true
popd
mv man/man1 man/man3
for x in man/man3/*.1
do
  mv $x ${x/.1/.3}
done


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp -p lib/libSHTOOLS.a $RPM_BUILD_ROOT%{_libdir}
cp -p openmp/lib/libSHTOOLS.a $RPM_BUILD_ROOT%{_libdir}/libSHTOOLS_thread.a
cp -p modules/shtools.mod $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
cp -rp man/man3 $RPM_BUILD_ROOT%{_mandir}

# AltCCRPMS
# Make the environment-modules file
mkdir -p %{buildroot}%{_modulefiledir}
# Since we're doing our own substitution here, use our own definitions.
sed -e 's#@PREFIX@#'%{_prefix}'#' -e 's#@LIB@#%{_lib}#' -e 's#@ARCH@#%{_arch}#' -e 's#@CC@#%{_cc_name}#' \
    < %SOURCE1 > %{buildroot}%{_modulefiledir}/%{version}

%{?_licensedir:mkdir -p %{buildroot}%{_licensedir}}
%{!?_licensedir:mkdir -p %{buildroot}%{_defaultdocdir}}


%files devel
%license LICENSE
%{?_licensedir:%{_licensedir}}
%{!?_licensedir:%{_defaultdocdir}}
%{_modulefiledir}
%{_prefix}/


%changelog
* Thu May 19 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1-4
- Build libSHTOOLS_thread.a with openmp

* Wed Jan 20 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1-3
- Use %%license, own directory

* Wed Dec 23 2015 Orion Poplawski <orion@cora.nwra.com> - 3.1-2
- Use rpm-opt-hooks for dependencies
- Intel 2016.1.150

* Thu Oct 22 2015 Orion Poplawski <orion@cora.nwra.com> - 3.1-1
- Update to 3.1
- Intel 2016.0.109

* Mon Jun 8 2015 Orion Poplawski <orion@cora.nwra.com> - 3.0-1
- Update to 3.0
- Intel 2015.3

* Tue Jan 20 2015 Orion Poplawski <orion@cora.nwra.com> - 2.9-1
- Update to 2.9
- Intel 2015u1

* Mon May 19 2014 Orion Poplawski <orion@cora.nwra.com> - 2.8-4
- Rebuild with intel 2013sp1u3

* Wed Feb 19 2014 Orion Poplawski <orion@cora.nwra.com> - 2.8-3
- Rebuild with intel 2013sp1u2

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
