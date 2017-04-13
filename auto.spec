%{?scl:%scl_package auto}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

Name:          %{?scl_prefix}auto
Version:       1.1
Release:       3.%{baserelease}%{?dist}
Summary:       A collection of source code generators for Java
License:       ASL 2.0
URL:           https://github.com/google/auto
Source0:       https://github.com/google/auto/archive/auto-value-%{version}.tar.gz

BuildRequires: %{?scl_prefix_maven}maven-local
BuildRequires: %{?scl_prefix}mvn(com.google.guava:guava)
BuildRequires: %{?scl_prefix}mvn(com.squareup:javawriter)
BuildRequires: %{?scl_prefix_java_common}mvn(javax.inject:javax.inject)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-invoker-plugin)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.velocity:velocity)
BuildRequires: %{?scl_prefix_java_common}mvn(org.ow2.asm:asm:5)
BuildRequires: %{?scl_prefix_maven}mvn(org.sonatype.oss:oss-parent:pom:)

%if 0
# Test deps
BuildRequires: mvn(com.google.code.findbugs:jsr305:1.3.9)
BuildRequires: %{?scl_prefix_java_common}mvn(junit:junit)
# Unavailable test deps
BuildRequires: mvn(com.google.dagger:dagger:2.0)
BuildRequires: mvn(com.google.dagger:dagger-compiler:2.0)
BuildRequires: mvn(com.google.guava:guava-testlib:18.0)
BuildRequires: mvn(com.google.inject:guice:4.0-beta)
BuildRequires: mvn(com.google.testing.compile:compile-testing:0.6)
BuildRequires: mvn(com.google.truth:truth:0.25)
%endif

BuildArch:     noarch

%description
The Auto sub-projects are a collection of code generators
that automate those types of tasks.

%package common
Summary:       Auto Common Utilities

%description common
Common utilities for creating annotation processors.

%package factory
Summary:       JSR-330-compatible factories

%description factory
A source code generator for JSR-330-compatible factories.

%package service
Summary:       Provider-configuration files for ServiceLoader

%description service
A configuration/meta-data generator for
java.util.ServiceLoader-style service
providers.

%package value
Summary:       Auto Value

%description value
Immutable value-type code generation for Java 1.6+.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n auto-auto-value-%{version}
find -name '*.class' -print -delete
find -name '*.jar' -print -delete

%pom_xpath_inject "pom:project" "
<modules>
  <module>common</module>
  <module>factory</module>
  <module>service</module>
  <module>value</module>
</modules>"

%pom_xpath_set "pom:project/pom:version" %{version}
for p in common factory service value ;do
%pom_xpath_set "pom:parent/pom:version" %{version} ${p}
%pom_xpath_set "pom:project/pom:version" %{version} ${p}
%pom_xpath_remove "pom:dependency[pom:scope = 'test']" ${p}
done

%pom_remove_plugin org.apache.maven.plugins:maven-checkstyle-plugin
%pom_remove_plugin :maven-shade-plugin value
%pom_remove_plugin :maven-invoker-plugin value
%pom_remove_plugin :maven-invoker-plugin factory

%pom_xpath_set "pom:dependency[pom:artifactId = 'auto-service']/pom:version" %{version} factory
%pom_xpath_set "pom:dependency[pom:artifactId = 'auto-common']/pom:version" %{version} factory
%pom_xpath_set "pom:dependency[pom:artifactId = 'auto-common']/pom:version" %{version} service
%pom_xpath_set "pom:dependency[pom:artifactId = 'auto-common']/pom:version" %{version} value
%pom_xpath_set "pom:dependency[pom:artifactId = 'auto-service']/pom:version" %{version} value
%pom_xpath_set "pom:dependency[pom:artifactId = 'asm']/pom:version" 5 value
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x

# Unavailable test deps
%mvn_build -sf
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles-%{pkg_name}-parent
%dir %{_javadir}/%{pkg_name}
%doc README.md
%doc LICENSE.txt

%files common -f .mfiles-%{pkg_name}-common
%doc common/README.md
%doc LICENSE.txt

%files factory -f .mfiles-%{pkg_name}-factory
%doc factory/README.md
%doc LICENSE.txt

%files service -f .mfiles-%{pkg_name}-service
%doc service/README.md
%doc LICENSE.txt

%files value -f .mfiles-%{pkg_name}-value
%doc value/README.md
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Jan 19 2017 Mat Booth <mat.booth@redhat.com> - 1.1-3.2
- Fix dep on asm 5

* Thu Jan 19 2017 Mat Booth <mat.booth@redhat.com> - 1.1-3.1
- Auto SCL-ise package for rh-eclipse46 collection

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 13 2015 gil cattaneo <puntogil@libero.it> 1.1-1
- update to 1.1

* Wed Apr 01 2015 gil cattaneo <puntogil@libero.it> 1.0-2
- enable factory module

* Tue Mar 31 2015 gil cattaneo <puntogil@libero.it> 1.0-1
- initial rpm
