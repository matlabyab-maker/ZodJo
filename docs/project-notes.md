# ZodJo project notes

The project generator owns the following source files:
- README.md
- project.json
- buildozer.spec
- app/build.gradle
- app/src/main/AndroidManifest.xml
- app/src/main/python/main.py
- app/src/main/assets/index.html
- .github/workflows/android.yml
- docs/project-notes.md

Do not store GitHub access tokens in source files.

The current workflow validates source files. It does not build an APK.
The current Python prototype opens pages externally and is not yet a
full embedded browser.
