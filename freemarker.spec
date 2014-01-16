%{?_javapackages_macros:%_javapackages_macros}
# Prevent brp-java-repack-jars from being run.
%global __jar_repack %{nil}

%global checkForbiddenJARFiles F=`find -type f -iname '*.jar'`; [ ! -z "$F" ] && \
echo "ERROR: Sources should not contain JAR files:" && echo "$F" && exit 1

%global fm_compatible_ver 2.3
%global fm_ver %{fm_compatible_ver}.19

Name:           freemarker
Version:        %{fm_ver}
Release:        7.0%{?dist}
Summary:        A template engine


License:        BSD
URL:            http://freemarker.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        http://freemarker.sourceforge.net/maven2/org/%{name}/%{name}/%{version}/%{name}-%{version}.pom

# disabled functionality: ext/jdom, ext/jsp/FreeMarkerPageContext1, ext/xml/JdomNavigator
Patch0:         %{name}-%{version}-build.patch
#
Patch1:         %{name}-2.3.13~PyObject.__class__.patch
# http://netbeans.org/bugzilla/show_bug.cgi?id=156876
Patch2:         %{name}-%{version}-logging.patch
# illegal character in the javadoc comment
Patch3:         %{name}-2.3.13~encoding.patch
# do not depend on tomcat5
Patch4:         %{name}-%{version}-no-tomcat5.patch
# Disable JavaRebelIntegration
Patch5:         %{name}-%{version}-no-javarebel.patch
# enable jdom extension
Patch6:         %{name}-%{version}-enable-jdom.patch
# use system javacc and fix Token.java
Patch7:         %{name}-%{version}-javacc.patch

BuildArch:      noarch

BuildRequires: ant >= 1.6
BuildRequires: apache-commons-logging
BuildRequires: avalon-logkit >= 1.2
BuildRequires: dom4j >= 1.6.1
BuildRequires: dos2unix
BuildRequires: emma >= 2.0
BuildRequires: java-devel >= 1:1.6.0
BuildRequires: javacc >= 4.0
BuildRequires: jaxen >= 1.1
BuildRequires: jdom >= 1.0
BuildRequires: jpackage-utils
BuildRequires: junit >= 3.8.2
BuildRequires: jython >= 2.2.1
BuildRequires: log4j >= 1.2
BuildRequires: rhino >= 1.6
BuildRequires: slf4j
BuildRequires: tomcat-el-2.2-api
BuildRequires: tomcat-lib >= 6.0.16
BuildRequires: tomcat-jsp-2.2-api
BuildRequires: tomcat-servlet-3.0-api >= 6.0
BuildRequires: xalan-j2 >= 2.7.0

Requires: java >= 1:1.6.0
Requires: jpackage-utils

%description
FreeMarker is a Java tool to generate text output based on templates.
It is designed to be practical as a template engine to generate web
pages and particularly for servlet-based page production that follows
the MVC (Model View Controller) pattern. That is, you can separate the
work of Java programmers and website designers - Java programmers
needn't know how to design nice websites, and website designers needn't
know Java programming.

%package javadoc
Summary:        Javadocs for %{name}

Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}

find -type f \( -iname '*.jar' -o -iname '*.class' \)  -exec rm -f '{}' \;

%patch0 -p0
#  % p atch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p0

# %{__rm} -rf src/freemarker/core/ParseException.java
%{__rm} -rf src/freemarker/core/FMParser.java
%{__rm} -rf src/freemarker/core/FMParserConstants.java
%{__rm} -rf src/freemarker/core/FMParserTokenManager.java
%{__rm} -rf src/freemarker/core/SimpleCharStream.java
%{__rm} -rf src/freemarker/core/Token.java
%{__rm} -rf src/freemarker/core/TokenMgrError.java

%{__ln_s} -f %{_javadir}/ant.jar           lib/ant.jar
%{__ln_s} -f %{_javadir}/commons-logging.jar    lib/commons-logging.jar
%{__ln_s} -f %{_javadir}/dom4j.jar         lib/dom4j.jar
%{__ln_s} -f %{_javadir}/emma_ant.jar      lib/emma_ant.jar
%{__ln_s} -f %{_javadir}/emma.jar          lib/emma.jar
#%{__ln_s} -f %{_javadir}/javacc.jar        lib/javacc.jar
%{__ln_s} -f %{_javadir}/jaxen.jar         lib/jaxen.jar
%{__ln_s} -f %{_javadir}/jdom.jar          lib/jdom.jar
# js.jsr provided by rhino package
%{__ln_s} -f %{_javadir}/js.jar            lib/js.jar

# The JavaServer Pages 1.2 technology isn't provided in Fedora 10
#%{__ln_s} -f %{_javadir}/jsp-api-1.2.jar   lib/jsp-api-1.2.jar

%{__ln_s} -f %{_javadir}/tomcat-jsp-api.jar  lib/jsp-api-2.0.jar

%{__ln_s} -f %{_javadir}/tomcat-jsp-api.jar  lib/jsp-api-2.1.jar

%{__ln_s} -f %{_javadir}/junit.jar         lib/junit.jar
%{__ln_s} -f %{_javadir}/jython.jar        lib/jython.jar
%{__ln_s} -f %{_javadir}/log4j.jar         lib/log4j.jar
%{__ln_s} -f %{_javadir}/avalon-logkit.jar lib/logkit.jar
%{__ln_s} -f %{_javadir}/slf4j/api.jar lib/slf4j-api.jar

# It doesn't required due to OpenJDK 6 is used
#%{__ln_s} -f %{_javadir}/rt122.jar         lib/rt122.jar

# SAXPath has been merged into the Jaxen codebase and is
# no longer being maintained separately. See jaxen-1.1.jar
#%{__ln_s} -f %{_javadir}/saxpath.jar       lib/saxpath.jar

# The package javax.el isn't included in:
%{__ln_s} -f %{_javadir}/tomcat-servlet-api.jar lib/servlet.jar
# so, el-api.jar is additionally used.
%{__ln_s} -f %{_javadir}/tomcat-el-api.jar lib/el-api.jar

%{__ln_s} -f %{_javadir}/struts.jar        lib/struts.jar
%{__ln_s} -f %{_javadir}/xalan-j2.jar      lib/xalan.jar

dos2unix -k docs/docs/api/stylesheet.css
dos2unix -k docs/docs/api/package-list

%checkForbiddenJARFiles

%build
%{ant}

%install
# jars
%{__install} -d -m 755 %{buildroot}%{_javadir}
%{__install} -m 644 lib/%{name}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
%{__install} -d -m 755 %{buildroot}%{_javadocdir}/%{name}
%{__cp} -pr docs/docs/api/* %{buildroot}%{_javadocdir}/%{name}

# pom
%{__install} -d -m 755 %{buildroot}%{_mavenpomdir}
%{__install} -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

# depmap
%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%defattr(-,root,root,-)
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*.jar
%doc LICENSE.txt README.txt

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
* Mon Aug 05 2013 Omair Majid <omajid@redhat.com> - 2.3.19-7
- Fix build dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 01 2012 Omair Majid <omajid@redhat.com> - 2.3.19-4
- Build remaining classes with target 6 too.
- Fixes RHBZ#842594

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Omair Majid <omajid@redhat.com> - 2.3.19-2
- Remove obsolete patches

* Tue Jun 05 2012 gil cattaneo <puntogil@libero.it - 2.3.19-2
- update patch for logging

* Thu May 31 2012 Omair Majid <omajid@redhat.com> - 2.3.19-1
- Add dependency on apache-commons-logging

* Wed May 16 2012 gil cattaneo <puntogil@libero.it> - 2.3.19-1
- update to 2.3.19

* Wed Feb 01 2012 Marek Goldmann <mgoldman@redhat.com> - 2.3.13-14
- Added Maven POM, RHBZ#786383

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 16 2011 Omair Majid <omajid@redhat.com> - 2.3.13-12
- Drop build dependency on struts
- Remove buildroot cleaning and definition
- Remove versioned jars
- Remove dependency of javadoc subpackage on main package

* Mon Feb 28 2011 Omair Majid <omajid@redhat.com> - 2.3.13-12
- Remove dependency on tomcat5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep 13 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3.13-10
- Adapt to tomcat6-el jar rename.

* Mon Sep 13 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3.13-9
- Add tomcat6-libs BR.
- Use global instead of define.

* Sat Feb 27 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.3.13-8
- fix build patch for use of the javacc 5.0
- patch for encoding
- disable brp-java-repack-jars

* Sat Feb 27 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.3.13-7
- patch for logging
- remove name from the summary

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 01 2008 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.3.13-4
- Redundant dependency upon xerces-j2 is removed (#456276#c6)
- The dos2unix package is added as the build requirements
- The ant-nodeps build-time requirement is added

* Wed Aug 20 2008 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.3.13-3
- The downloads.sourceforge.net host is used in the source URL
- %%{__install} and %%{__cp} are used everywhere
- %%defattr(-,root,root,-) is used everywhere

* Fri Aug 14 2008 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.3.13-2
- Appropriate values of Group Tags are chosen from the official list
- Versions of java-devel & jpackage-utils are corrected
- Name of dir for javadoc is changed
- Manual is removed due to http://freemarker.org/docs/index.html

* Fri Jun 06 2008 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.3.13-1
- Initial version
