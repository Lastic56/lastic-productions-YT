[app]

# (str) Title of your application
title = Lastic Productions

# (str) Package name
package.name = lastic_productions

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt

# (list) List of exclusions using pattern matching
source.exclude_patterns = license,images/*/*.jpg

# (list) List of exclusions using pattern matching
#source.exclude_dirs = tests, bin, venv

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.1,yt-dlp,ffmpeg-python,certifi,android

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (str) Application version
version = 1.0.0

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) The entry point of your application
#entrypoint = main.py

# (str) Unpack some files inside the private storage/app/ directory
#android.add_packed_files =

# (list) Java classes to add
#android.add_src =

# (list) Java jars to add
#android.add_jars = foo.jar,bar.jar,common/acme.jar

# (list) Java files to add
#android.add_java_src =

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (list) Java classes to exclude from the apk
#android.add_acyclic_classes =

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package (default=False)
android.enable_androidx = True

# (list) Android aidl files
#android.add_aidl =

# (list) Android assets to copy only
#android.add_assets =

# (list) Android assets to exclude
#android.exclude_assets =

# (list) Android resources to copy only
#android.add_resources =

# (list) Android resources to exclude
#android.exclude_resources =

# (list) Android shared libraries to copy only
#android.add_shared_libraries =

# (list) Android shared libraries to exclude
#android.exclude_shared_libraries =

# (list) Android meta-data to set (key=value format)
#android.meta_data =

# (list) Android build tools to use
#android.build_tools_version =

# (str) Android app theme, default is 'Theme.Black.NoTitleBar'
#android.manifest_theme =

# (list) Android manifest intent filters
#android.manifest_intent_filters =

# (list) Android activity launch mode
#android.manifest_launch_mode = standard

# (list) Android activity intent filters
#android.manifest_activity_intent_filters =

# (str) Android activity name
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Android activity parent class name
#android.activity_parent_class_name = org.kivy.android.PythonActivity

# (str) Android service parent class name
#android.service_parent_class_name = org.kivy.android.PythonService

# (list) Android service intent filters
#android.service_intent_filters =

# (list) Android broadcast receiver intent filters
#android.receiver_intent_filters =

# (list) Android provider intent filters
#android.provider_intent_filters =

# (list) Android meta-data to set (key=value format)
#android.meta_data =

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output storage, absolute or relative to spec file
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:name].
#    Each line will be considered as a option to the list.
#    Let's take "source.include_exts" for example:
#
#    [app:source.include_exts]
#    py
#    png
#    jpg
#    kv
#    atlas
#    txt
#
