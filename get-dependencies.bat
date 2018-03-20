rd /s /q "C:\Users\6\Desktop\maven-imports\jersey\m2\"

xcopy /d/y /s C:\Users\6\Desktop\maven-imports\base-maven-libs\* C:\Users\6\Desktop\maven-imports\jersey\m2\
mvn dependency:go-offline -s "C:\Users\6\Desktop\maven-imports\jersey\settings.xml"

echo "hey"
cmd /k python "C:\Users\6\Desktop\Maven-imports\jersey\copy-only-new-files.py"