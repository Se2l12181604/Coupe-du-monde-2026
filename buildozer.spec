[app]

# (str) Title of your application
title = Coupe du Monde 2026

# (str) Package name
package.name = coupedumonde2026

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code directory where the main.py is
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
# SQLITE3 AJOUTÉ ICI POUR S'ASSURER QUE LA BASE DE DONNÉES CROISE BIEN TES RÉSULTATS
requirements = python3==3.11.9,kivy,sqlite3

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

# (bool) Use ccache to speed up compilation
android.meta_data =

# (list) Permissions
android.permissions = INTERNET

# (list) Architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) skip byte compile for .py files
android.skip_byte_compile = False

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
