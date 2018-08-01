# MSFT-Translate-Android-Parser
Microsoft Translate Android app parser for the xml/json data store.

This Phyton script will take the an extracted 'com.microsoft.translator_preferences.xml' file from a Microsoft Translate Android app and parse it for OCR and spoke translation content. Content will be placed in a SQLite database, one table for each content type.

With both the script and the target file in the same directory, execute the script. The database will be created in the same working directory.
