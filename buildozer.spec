[app]

# (str) Title of your application
title = Coupe du Monde 2026

# (str) Package name
package.name = worldcup2026

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code directory where the main.py is
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db,json

# (str) Application version
version = "1.0"

# (list) Application requirements
requirements = python3==3.11.9,kivy==2.3.0,sqlite3

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# ==========================================
# Android specific profiles
# ==========================================

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use private storage for data
android.private_storage = 1

# (bool) Accept SDK license
android.accept_sdk_license = True

# (list) Architectures to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
