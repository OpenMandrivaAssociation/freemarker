Name:           freemarker
Version:        2.3.10
Release:        8
Summary:        FreeMarker template engine - a generic tool to generate text output
License:        BSD
Group:          Development/Java
Url:            http://freemarker.org/
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.gz
Patch0:         build.patch
BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  java-devel >= 1.6
BuildRequires:  java >= 1.6
Requires:       java >= 1.6

%description
FreeMarker is a "template engine"; a generic tool to generate text output 
(anything from HTML to autogenerated source code) based on templates. 
It's a Java package, a class library for Java programmers. 
It's not an application for end-users in itself, but something that 
programmers can embed into their products.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:        %{name} = %{version}-%{release}
%description    javadoc
FreeMarker is a "template engine"; a generic tool to generate text output 
(anything from HTML to autogenerated source code) based on templates. 
It's a Java package, a class library for Java programmers. 
It's not an application for end-users in itself, but something that 
programmers can embed into their products.

%prep
%setup -q
%remove_java_binaries
%patch0 -p0 -b .sav

#
# XXX: This package contains just core of freemarker. This is enough for
# NetBeans integration, that is why it removes certain extensions. In case
# of need, feel free to modify this script to compile these extensions correctly.
#
%{__rm} -rf src/freemarker/ext/jython/
%{__rm} -rf src/freemarker/ext/xml/
%{__rm} -rf src/freemarker/ext/jsp/
%{__rm} -rf src/freemarker/ext/servlet/
%{__rm} src/freemarker/cache/WebappTemplateLoader.java

%build
ant -f build.xml jar javadoc

%install
install -m644 lib/%{name}.jar -D %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

install -d %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -r build/api %{buildroot}%{_javadocdir}/%{name}-%{version}

%create_jar_links

%post

%postun

%defattr(644,root,root,755)
%{_javadir}/%{name}.jar
%ghost %{_javadir}/%{name}-%{version}.jar

%files
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.10-7mdv2011.0
+ Revision: 618341
- the mass rebuild of 2010.0 packages

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 2.3.10-6mdv2010.0
+ Revision: 437591
- rebuild

* Sun Mar 29 2009 Pascal Terjan <pterjan@mandriva.org> 2.3.10-5mdv2009.1
+ Revision: 362179
- Fix summary of -javadoc subpackage

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 2.3.10-2mdv2008.1
+ Revision: 120880
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Dec 02 2007 Jaroslav Tulach <jtulach@mandriva.org> 2.3.10-1mdv2008.1
+ Revision: 114454
- Yet another try: Just using %%{ant} defines JAVA_HOME to non-existant gcj directory. Trying plain ant
- Make sure Java is available also during compile time
- Is there a better way to enforce compilation with real javac than to require java-devel >= 1.6?
- The core of freemarker builds. Extensions (JSP, Jython, XML) are not included.
- create freemarker

