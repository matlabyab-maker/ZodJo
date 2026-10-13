[app]
title = ZodJo
package.name = zodjo
package.domain = org.zodjo
source.dir = app/src/main/python
source.include_exts = py,html,css,js,json,png,jpg,kv,txt
version = 0.1.0
requirements = python3,kivy
orientation = all
fullscreen = 0

# Internet permission is required by the browser prototype.
android.permissions = INTERNET

# Keep SDK/NDK selection to the build environment defaults.
# Do not add the obsolete package command: sdkmanager tools.

[buildozer]
log_level = 2
warn_on_root = 1
