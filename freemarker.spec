Name:		freemarker
Version:	2.3.35
Release:	1
Summary:	Java template engine
Group:		Development/Java
License:	Apache-2.0
URL:		https://freemarker.apache.org/
# Apache FreeMarker 2.3.35 source release. The FTL parser is not in
# the tarball; JavaCC 7.0.12 generates it during the build.
Source0:	freemarker-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	javacc >= 7.0.12
BuildRequires:	jaxen
BuildRequires:	dom4j
BuildRequires:	slf4j2
BuildRequires:	apache-commons-logging
BuildRequires:	log4j12
BuildRequires:	avalon-logkit

%description
Apache FreeMarker %{version} compiles text templates. Gradle 9.9.1
accepts this release. The jar is the core engine. JDOM, Rhino,
JRebel, and the Xalan XPath adapters are not compiled. SLF4J,
Commons Logging, Log4j 1, and Avalon LogKit are compile-only so the
log factories can be loaded later by Class.forName. They are not
runtime requirements.

%prep
%autosetup -n freemarker-%{version}
find . -depth \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -exec /bin/rm -rf {} +

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
J=%{_javadir}
for jar in jaxen.jar dom4j.jar slf4j-api.jar commons-logging.jar log4j.jar avalon-logkit.jar org.apache.log.jar; do
	test -s "$J/$jar"
done
OUT=gen/freemarker/core
mkdir -p "$OUT"
javacc -OUTPUT_DIRECTORY="$OUT" freemarker-core/src/main/javacc/freemarker/core/FTL.jj
test -f "$OUT/FMParser.java"
test -f "$OUT/ParseException.java"
test -f "$OUT/TokenMgrError.java"
rm -f "$OUT/ParseException.java" "$OUT/TokenMgrError.java"
test -f freemarker-core/src/main/java/freemarker/core/ParseException.java
test -f freemarker-core/src/main/java/freemarker/core/TokenMgrError.java
python - << 'PY'
from pathlib import Path
out = Path("gen/freemarker/core")
def repl(name, old, new, required):
    path = out / name
    text = path.read_bytes().decode("iso-8859-1")
    count = text.count(old)
    print(f"{name} {old!r} {count}")
    if required and count != 1:
        raise SystemExit(f"{name}: expected one {old!r}, found {count}")
    if count:
        path.write_bytes(text.replace(old, new).encode("iso-8859-1"))
repl("FMParser.java", "enum", "ENUM", True)
repl("FMParserConstants.java", "public interface FMParserConstants", "interface FMParserConstants", True)
repl("Token.java", "public class Token", "class Token", True)
repl("SimpleCharStream.java", "public final class SimpleCharStream", "final class SimpleCharStream", False)
PY
find freemarker-core/src/main/java -name '*.java' \
	! -path '*/freemarker/ext/jdom/*' \
	! -path '*/freemarker/ext/rhino/*' \
	! -name 'JRebelClassChangeNotifier.java' \
	! -name '_JdomNavigator.java' \
	! -name 'XalanXPathSupport.java' \
	! -name 'SunInternalXalanXPathSupport.java' > sources.list
find "$OUT" -name '*.java' >> sources.list
test "$(wc -l < sources.list)" -eq 538
mkdir -p classes
CP="$J/jaxen.jar:$J/dom4j.jar:$J/slf4j-api.jar:$J/commons-logging.jar:$J/log4j.jar:$J/avalon-logkit.jar:$J/org.apache.log.jar"
javac --release 8 -encoding UTF-8 -Xlint:-options -proc:none \
	-cp "$CP" -d classes @sources.list
cp -a freemarker-core/src/main/resources/. classes/
mkdir -p classes/freemarker
cp -a freemarker-core/src/main/resource-templates/freemarker/version.properties classes/freemarker/version.properties
jar cf freemarker.jar -C classes .
jar i freemarker.jar
jar tf freemarker.jar | grep -qx 'freemarker/version.properties'

cat > freemarker.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.freemarker</groupId>
  <artifactId>freemarker</artifactId>
  <version>2.3.35</version>
  <name>Apache FreeMarker</name>
  <description>Java template engine 2.3.35.</description>
  <url>https://freemarker.apache.org/</url>
  <licenses>
    <license>
      <name>Apache License, Version 2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
</project>
EOF

%install
set -eo pipefail
sysjar install --buildroot %{buildroot} \
	--artifact freemarker.pom:freemarker.jar \
	--file-name freemarker \
	--filelist .mfiles

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
JAR=%{buildroot}%{_javadir}/freemarker.jar
test -s "$JAR"
mkdir -p check
cat > check/Smoke.java << 'END'
import freemarker.template.Configuration;
import freemarker.template.Template;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.HashMap;
public class Smoke {
	public static void main(String[] args) throws Exception {
		Configuration cfg = new Configuration(Configuration.VERSION_2_3_35);
		Template t = new Template("t", new StringReader("Hello ${name}"), cfg);
		HashMap<String, Object> model = new HashMap<String, Object>();
		model.put("name", "gradle");
		StringWriter out = new StringWriter();
		t.process(model, out);
		System.out.println("freemarker_ok " + out.toString() + " " + Configuration.getVersion());
	}
}
END
javac --release 8 -encoding UTF-8 -Xlint:-options -proc:none -cp "$JAR" -d check check/Smoke.java
java -cp "check:$JAR" Smoke > check/out.txt
cat check/out.txt
grep -F -q "freemarker_ok Hello gradle %{version}" check/out.txt

%files -f .mfiles
%doc LICENSE NOTICE README.md
