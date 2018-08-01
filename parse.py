import json
import sqlite3
import xml.etree.ElementTree as ET


tree = ET.parse('com.microsoft.translator_preferences.xml')
root = tree.getroot()

readtext=''
translatedtext=''

#Create database
db = sqlite3.connect('AMSTranslate.db')
cursor = db.cursor()

#Create database fields for ocr
cursor.execute('''
    CREATE TABLE OCR(path TEXT, geo1 TEXT, geo2 TEXT, 
					 timestamp INT, idv TEXT, sourcelang TEXT, translang TEXT,
					 ocrtxt TEXT, translatedtxt TEXT)
''')
db.commit()
#Create database fields for translated phrases

cursor.execute('''
    CREATE TABLE PHRASES(fromlangcode TEXT, fromphrase TEXT, tolangcode TEXT, 
					 tophrase TEXT, idx TEXT, historytimestamp int, pinnedtimestamp TEXT)
''')
db.commit()

for string in root.findall('string'): #Each if gets you to the proper tag in XML for pertinent data
	name = string.get('name')
	if name == 'KEY_PREFS_LANG_TEXT_TRANSLATE_TO':
		keytextto = string.text
	
	if name == 'KEY_DATA_TRANSLATED_PHRASES':
		jsonphrases = string.text 
		data10 = json.loads(jsonphrases)
		#print (isinstance(data10, list))
		for x in range(len(data10)):
			fromLangCode = data10[x]['fromLangCode']
			fromPhrase = data10[x]['fromPhrase']
			toLangCode = data10[x]['toLangCode']
			toPhrase = data10[x]['toPhrase']
			Idx = data10[x]['Id']
			historyTimeStamp = data10[x]['historyTimeStamp']
			try:
				pinnedTimeStamp = data10[x]['pinnedTimeStamp']
				#print(pinnedTimeStamp)
			except KeyError:              #error handling since not all entries are pinned. Dont want issues with sqlite.
				pinnedTimeStamp = '' 
				
			#print(fromLangCode)
			#print(fromPhrase)
			#print(toLangCode)
			#print(toPhrase)
			#print(Idx)
			#print(historyTimeStamp)	
			#print(pinnedTimeStamp)
			
			cursor = db.cursor()
			datainsert2 = (fromLangCode, fromPhrase, toLangCode, toPhrase, Idx, historyTimeStamp, pinnedTimeStamp,)
			#print (datainsert2)
			cursor.execute('INSERT INTO PHRASES (fromlangcode, fromphrase, tolangcode, tophrase, idx, historytimestamp, pinnedtimestamp)  VALUES(?,?,?,?,?,?,?)', datainsert2)
			db.commit()
		
	if name == 'KEY_PREFS_OCR_DATA': #json data inside json data
		jsonocr = string.text
		data = json.loads(jsonocr, encoding="utf-16")
			
		for key, value in data.items():
			data2 = value
			for key, value in data2.items():
				if key == 'imagePath':
					imagepath = value
		
				if key == 'location':
					#print (key, value)
					data6 = json.dumps(value)
					data6 = json.loads(data6)
					for key, value in data6.items():
						if key == 'first':
							geoone = value
						if key == 'second':
							geotwo = value
        
				if key == 'sourceLanguage':
					sourcelang = value	

				if key == 'translatedLanguage':
					translatedlanguage = value
					
				if key == 'Id':
					idv = value
				
				if key == 'historyTimeStamp':
					historytimestamp = value	
					
				if key == 'ocrResult':
					data3 = json.dumps(value)
					data3 = json.loads(data3)
					
					for key, value in data3.items():
						if key == 'regions':
							#data4 = json.dumps(value)
							#data4 = json.loads(data4)
							#print (len(data4))
							#for fields in data4():
								#print (key)
							
							data4 = value
							
							
							for i in range(len(data4)):
								data5 = data4[i]['lines']
								#print (data4[i]['lines'])
								for y in range(len(data5)):
									readtext = readtext + data5[y]['text']
									translatedtext = translatedtext + data5[y]['translation']
								


			else:                    #after values extracted from jason key values and stored lists insert them into ocr table
				#print (imagepath)
				#print (geoone)
				#print (geotwo)
				#print (historytimestamp)
				#print (idv)
				#print (translatedlanguage)
				#print (sourcelang)
				#print (readtext)
				#print (translatedtext)
				#import to sqlite row
				cursor = db.cursor()
				datainsert = (imagepath, geoone, geotwo, historytimestamp, idv, sourcelang, translatedlanguage, readtext, translatedtext)
				#print (datainsert)
				cursor.execute('INSERT INTO OCR (path, geo1, geo2, timestamp, idv, sourcelang, translang, ocrtxt, translatedtxt) VALUES(?,?,?,?,?,?,?,?,?)', datainsert)
				db.commit()
				
				readtext = ''            #these variables aggregate the ocr text and corresponding translation so i clear them after each translation group
				translatedtext = ''		 #that way they don't aggregate all translations into one.
db.close()				

