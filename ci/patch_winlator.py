from pathlib import Path
import json

ROOT = Path('winlator')

def replace(path, old, new):
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'Pattern not found in {path}: {old!r}')
    p.write_text(s.replace(old, new), encoding='utf-8')

replace('app/build.gradle', "applicationId 'com.winlator'", "applicationId 'com.pesnicaragua.android'")
replace('app/build.gradle', 'versionCode 33', 'versionCode 1001')
replace('app/build.gradle', 'versionName "11.2"', 'versionName "0.1.0"')
replace('app/src/main/res/values/strings.xml', '<string name="app_name">Winlator</string>', '<string name="app_name">PES Nicaragua</string>')
replace('app/src/main/AndroidManifest.xml', 'android:authorities="com.winlator.FileProvider"', 'android:authorities="com.pesnicaragua.android.FileProvider"')
replace('app/src/main/java/com/winlator/core/FileUtils.java', '"com.winlator.FileProvider"', 'activity.getPackageName()+".FileProvider"')

strings = ROOT / 'app/src/main/res/values/strings.xml'
s = strings.read_text(encoding='utf-8')
translations = {
    'Run':'Jugar', 'Shortcuts':'Juegos', 'Containers':'Entorno', 'Input Controls':'Controles táctiles',
    'New Container':'Nuevo entorno', 'Edit Container':'Editar entorno', 'Settings':'Ajustes',
    'About':'Acerca de', 'Exit':'Salir', 'Starting up...':'Iniciando...',
    'Installing System Files...':'Preparando motor de juego...',
    'Updating System Files...':'Actualizando motor de juego...',
    'Unable to install system files':'No se pudo preparar el motor de juego',
    'Keyboard':'Teclado', 'Toggle Fullscreen':'Pantalla completa'
}
for en, es in translations.items():
    s = s.replace('>'+en+'</string>', '>'+es+'</string>')
strings.write_text(s, encoding='utf-8')

profile = {
  'id': 5,
  'name': 'PES 6 Nicaragua',
  'cursorSpeed': 1,
  'disableMouseInput': True,
  'elements': [
    {'type':'STICK','shape':'CIRCLE','bindings':['GAMEPAD_LEFT_THUMB_UP','GAMEPAD_LEFT_THUMB_RIGHT','GAMEPAD_LEFT_THUMB_DOWN','GAMEPAD_LEFT_THUMB_LEFT'],'scale':1.12,'x':0.13,'y':0.73,'toggleSwitch':False,'text':'','iconId':0,'opacity':0.58},
    {'type':'BUTTON','shape':'CIRCLE','bindings':['GAMEPAD_BUTTON_X','NONE','NONE','NONE'],'scale':0.92,'x':0.82,'y':0.73,'toggleSwitch':False,'text':'TIRO','iconId':0,'opacity':0.62},
    {'type':'BUTTON','shape':'CIRCLE','bindings':['GAMEPAD_BUTTON_Y','NONE','NONE','NONE'],'scale':0.92,'x':0.88,'y':0.59,'toggleSwitch':False,'text':'HUECO','iconId':0,'opacity':0.62},
    {'type':'BUTTON','shape':'CIRCLE','bindings':['GAMEPAD_BUTTON_A','NONE','NONE','NONE'],'scale':0.92,'x':0.88,'y':0.87,'toggleSwitch':False,'text':'PASE','iconId':0,'opacity':0.62},
    {'type':'BUTTON','shape':'CIRCLE','bindings':['GAMEPAD_BUTTON_B','NONE','NONE','NONE'],'scale':0.92,'x':0.94,'y':0.73,'toggleSwitch':False,'text':'CENTRO','iconId':0,'opacity':0.62},
    {'type':'BUTTON','shape':'RECT','bindings':['GAMEPAD_BUTTON_L2','NONE','NONE','NONE'],'scale':0.78,'x':0.08,'y':0.22,'toggleSwitch':False,'text':'L2','iconId':0,'opacity':0.52},
    {'type':'BUTTON','shape':'RECT','bindings':['GAMEPAD_BUTTON_L1','NONE','NONE','NONE'],'scale':0.78,'x':0.08,'y':0.37,'toggleSwitch':False,'text':'L1','iconId':0,'opacity':0.52},
    {'type':'BUTTON','shape':'RECT','bindings':['GAMEPAD_BUTTON_R2','NONE','NONE','NONE'],'scale':0.78,'x':0.92,'y':0.22,'toggleSwitch':False,'text':'R2','iconId':0,'opacity':0.52},
    {'type':'BUTTON','shape':'RECT','bindings':['GAMEPAD_BUTTON_R1','NONE','NONE','NONE'],'scale':0.78,'x':0.92,'y':0.37,'toggleSwitch':False,'text':'R1','iconId':0,'opacity':0.52},
    {'type':'BUTTON','shape':'ROUND_RECT','bindings':['GAMEPAD_BUTTON_SELECT','NONE','NONE','NONE'],'scale':0.7,'x':0.45,'y':0.92,'toggleSwitch':False,'text':'SELECT','iconId':16,'opacity':0.48},
    {'type':'BUTTON','shape':'ROUND_RECT','bindings':['GAMEPAD_BUTTON_START','NONE','NONE','NONE'],'scale':0.7,'x':0.55,'y':0.92,'toggleSwitch':False,'text':'PAUSA','iconId':15,'opacity':0.48}
  ]
}
profile_path = ROOT / 'app/src/main/assets/inputcontrols/profiles/controls-5.icp'
profile_path.parent.mkdir(parents=True, exist_ok=True)
profile_path.write_text(json.dumps(profile, ensure_ascii=False, separators=(',',':')), encoding='utf-8')

marker = ROOT / 'PES_NICARAGUA_BUILD.txt'
marker.write_text('PES Nicaragua Android Runtime v0.1\nBase: Winlator 11.2\nUpstream commit pinned by GitHub Actions.\n', encoding='utf-8')
print('Applied PES Nicaragua Android v0.1 patch')
