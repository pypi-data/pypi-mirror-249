Change log
==========

3.1 (2024-01-03)
----------------

- Add support for Python 3.12.


3.0 (2023-02-02)
----------------

- Drop support for Python 2.7, 3.5, 3.6.


2.0 (2023-01-05)
----------------

- Add support for Python 3.11.


2.0b1 (2022-09-23)
------------------
- Add compatibility with Python 3 and Zope 4 and 5.

- Remove compatibility with Zope 2.

- Clean up package configuration.

- Remove unused or broken features.

- Updated the built-in documentation.


1.14 (2018-11-12)
-----------------
- added missing MANIFEST


1.13 (2018-11-12)
-----------------
- package as Python egg
- convert documentation from Zope Help System to Sphinx


Changes v1.12 - Thimo Kraemer <thimo.kraemer@joonis.de>
-------------------------------------------------------
- Removed management tab "Properties"


Changes v1.11 - Thimo Kraemer <thimo.kraemer@joonis.de>
-------------------------------------------------------
- Complete rewrite of StreamingFile.py
- Data is not longer loaded into memory on object creation
- Added streaming support for images


Changes v1.10 - Thimo Kraemer <thimo.kraemer@joonis.de>
-------------------------------------------------------
- Added builtin PythonScript (.py)
- Removed management options that cannot be used


Changes v1.9 - Thimo Kraemer <thimo.kraemer@joonis.de>
------------------------------------------------------
- Added support for Zope 2.13 (should also work with Zope 2.12)
- Fixed Webdav support (now ExternalEditor can be used again)
- Cleaned up StreamingFile and added range support
- Fixed support of .xml files (useable via ParsedXML)


Changes v1.8
------------
- ???


Changes v1.7-andreas 
--------------------
- Fix for FTP PUT bug on text/plain text/html and unknown files ;Stephen


Changes v1.6.1-andreas 
----------------------
- QUICKHACK fix for FTP PUT bug on text/plain text/html and unknown files


Changes v1.6-andreas 
--------------------
- fixes for FTP support ... thanks to Stephen Kirby


Changes v1.5-andreas 
--------------------
- added FTP support ... thanks to Stephen Kirby for his contribution


Changes v1.4-andreas 
--------------------
- added space separated file_filter option
  If you want LocalFS to display only PDF files and 
  subdirectories file_filter should look like:
  \*.pdf \*.PDF \*/


Changes v1.3-andreas 
--------------------
- added optional Zope2.7.1 filestream_iterator support 
  for better performance on large files (Thanks to Paul Winkler)
  see also at: http://www.slinkp.com/linux/code/zopestuff/blobnotes


Changes v1.2-andreas 
--------------------
- applyed all changes from SmileyChris which are:
    - Changed isPrincipiaFolderish to be always true for overall localFS object
    - Fixed editing Page Templates in the ZMI
    - Changing properties no longer just displays blank page
    - Changed so that anonymous DOES NOT have upload rights by default!
    - Changed property "tree_view" to off by default
    - Fix for [ 610152 ] security settings in fs
    - Fix for [ 742484 ] Cannot add LocalFS programmatically 
- do not show MessageDialog if manahe_upload was called from PloneLocalFS
- added refresh.txt


Changes v1.1-andreas by Andreas Heckel (andreas@easyleading.org)
----------------------------------------------------------------
- changed sorting so that directory comes first


Changes v1.0-andreas by Andreas Heckel (andreas@easyleading.org)
----------------------------------------------------------------
- fixed missing dogstring error when used with Zope2.7b3, UserTrack 
  and Plone
- made changes on __bobo_traverse__
- created version.txt


Changes v1.0
------------
- Fixed regex deprecation warning.
- Fixed possible IOError on module loadup trying to log exceptions.
- Fixed acquisition problems with LocalFile and LocalDirectory 
  objects. DTML rendered from the file system should now work just
  like DTML in the object database.
- Fixed a permissions bug with the manage_upload() method. It was 
  looking for the wrong permission. =(
- Updated management pages to new Zope look and feel.
- Removed redundant edit page and manage_edit() method. All properties
  are now edited through the properties page.
- Added help system documentation.
- Removed automatic text mode translation. All files are now copied
  as binary (with a nice little performance boost!)
- Removed old, crusty win32wnet.pyd.
- Changed manage_upload() to use a new strategy for determining the
  object id from the file path. First we check for Unix path seperators.
  If we find one we grab everything after the last one as the filename.
  Next we check for Windows and then Mac path separators and hope we
  never get a Unix path without a Unix path seperator but with one of 
  these characters ('\' or ':'). Finally, if we never see any kind of 
  path separator we just assume there is no path and use the whole 
  thing as the filename. I think this should work for most browsers. :-/
- Changed object creation protocol. External adapters now receive an
  open file object instead of a blob of text.
- Added get_size() and bobobase_modification_time() methods to
  LocalFile objects.
- Added new manage_createDirectory() method to LocalDirectory objects
  (uses the 'Manage local files' permission).


Changes v0.10.1
---------------
- Fixes for Zope 2.3


Changes v0.9.6
--------------
- Fixed saving large File and Image objects.
- Added ZCatalog support.
- Fixed fileIds, fileItems, fileValues behavior when spec='\*/'.
- Added optional 'propagate' parameter to fileItems and fileValues
  to prevent 'spec' from propagating to the url for child directories.


Changes v0.9.5
--------------
- Fixed bobobase_modification_time.
- Fixed cross-platform bug calculating object id in manage_upload.
- Added optional 'id' parameter to manage_upload to allow the
  caller to specify the new object id.
- Added optional 'action' parameter to manage_upload to allow
  redirecting somewhere other than the default 'manage_workspace'.


Changes v0.9.4
--------------
- Really fixed __getitem__ this time. Really.


Changes v0.9.3
--------------
- Fixed a bug in __getitem__ that broke the mapping protocol, 
  i.e. localfs['subobject'].
- Fixed a problem with tree tag items from separate localfs instances 
  affecting each other's state.
- Prevented exceptions in the localfs tree rendering from crashing the 
  management interface.
- Added 'Display in Tree View' option to disable displaying LocalFS
  objects in the management tree.
- Added LocalFile properties display_size and display_mtime which return 
  formatted properties. The size and mtime attributes now return an integer
  and a DateTime object, respectively. This should make the LocalFile 
  object more useful for creating custom directory views.
      

Changes v0.9.2
--------------
- Fixed a typo error in __ac_permissions__.
- Fixed a bug in manage_upload. The 'file' parameter must be a 
  FileUpload instance. It was accepting a string as input which
  caused an error.


Changes v0.9.1
--------------
- Added Contents view.
- Added support for adding and editing objects in the local file 
  system through the management interface.
- Added rename, cut, copy, paste, and delete support.


Changes v0.8.1
--------------
- Set modified time on File and Image objects so browser caching works
  correctly. This also fixes a bug with Zope versions 2.1.5 and later.
- Eliminated __init__ from factory class. Use __call__(self, id, data).
- Added file uploading.


Changes v0.7.1
--------------
- Fixed Zope permissions on LocalFS and LocalDirectory objects.
- Changed the spec parameter to filter directories as well as files.
  (Use '\*/' to include all directories.)
- Added ability to use LocalFS objects with the tree tag.
- Added object traversal methods: fileIds, fileValues, fileItems.
  Obsoleted objectIds, objectProps.
- Renamed FSProps class to LocalFile and added getObject method
  to get the Zope object from a LocalFile object. This is the object
  returned by the fileValues and fileItems methods.
- Added 'type map' property to allow customizing the content-types 
  and optionally the Zope object class associated with each file 
  extension.
- Added 'icon map' property to specify the icon associated with
  each content-type in directory browse view.
- Added Help tab.
    

Changes v0.6.1
--------------
- Fixed a bug with filtering in directory browse view.
- Fixed bogus text/html content-type on non-HTML files.
- Use a more aggressive search to determine whether files are 
  binary or text. This causes directory browsing to take a bit 
  longer but hopefully prevents file corruption problems.
- Added a Properties tab which allows specifying custom properties.
- Improved the formatting of directory browse view again with tables.
- Convert .xml files to XMLDocument objects if the XMLDocument 
  product is installed.
- Convert .stx files to StructuredDocument objects if the 
  StructuredDocument product is installed.


Changes v0.5.1
--------------
- Fixed lots of problems with local permissions. Many thanks to Greg Ward 
  for his help.


Changes v0.4.1
--------------
- Fixed problems with acquisition.
- Added the ability to connect to network shares using UNC paths on 
  win32 only. This does not affect non-Windows platforms. Many thanks 
  to Jephte CLAIN for submitting this code.
- Improved the formatting of directory browse view.
- Added 'default.html' and 'default.htm' to the default document list.


Changes v0.3.1
--------------
- Converted all dtml to 1.x syntax for backward compatibility.
- Prevented Zope from inserting <base> tag for HTML files.
- Moved icons to misc\_/LocalFS/ to avoid name conflicts.
- Added default document property.
- Added date and time in directory browse view.
- Sort directory contents by filename in browse view.


Changes v0.2.1
--------------
- Fixed url escaping in directory browse view. Now filenames with
  spaces and other 'special characters' work correctly.
- Added filtering by file extension in directory browse view.
