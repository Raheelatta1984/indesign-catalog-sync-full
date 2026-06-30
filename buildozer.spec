[app]

title = InDesign Catalog Sync MCP
package.name = indesigncatalogsync
package.domain = org.raheelatta

version = 1.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,yaml,csv
source.exclude_dirs = tests,build,dist,.git
source.exclude_patterns = *.pyc,*.pyo,*__pycache__*

requirements = python3,kivy==2.3.0,pandas,pyyaml,watchdog

orientation = portrait

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

fullscreen = 0