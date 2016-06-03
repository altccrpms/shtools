%global shortname shtools
%global ver 3.1
%{?altcc_init:%altcc_init -n %{shortname} -v %{ver}}

Name:           shtools%{?altcc_pkg_suffix}
Version:        %{ver}
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

%{!?altcc:BuildRequires: gcc-gfortran}
BuildRequires:  fftw-devel
# Need to compiled numpy with Intel
#BuildRequires:  numpy-f2py%{?altcc_dep_suffix}
BuildRequires:  tcsh
%?altcc_provide

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
%{?altcc:%altcc_provide devel}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n SHTOOLS-%{version}
sed -i -e '/^AR *=/d' src/Makefile
mkdir -p openmp
cp -rl Makefile lib modules src openmp/


%build
[ -z "$FC" ] && export FC=gfortran
%if "%{?altcc_cc_name}" == "intel"
export F95FLAGS="$FCFLAGS -ipo -free -Tf"
%endif
# f2py fails until we have numpy with intel
make F95=$FC %{?_smp_mflags} || true
pushd openmp
%if "%{?altcc_cc_name}" == "intel"
export F95FLAGS="-qopenmp $F95FLAGS"
%else
export F95FLAGS="-fopenmp $F95FLAGS"
%endif
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

%{?altcc:%altcc_writemodule %SOURCE1}
%{?altcc:%altcc_license}


%files devel
%{?altcc:%altcc_files -lm %{_libdir} %{_mandir}/man3}
%license LICENSE
%{_libdir}/libSHTOOLS.a
%{_libdir}/libSHTOOLS_thread.a
%{_libdir}/shtools.mod
%{_mandir}/man3/*.3*


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
