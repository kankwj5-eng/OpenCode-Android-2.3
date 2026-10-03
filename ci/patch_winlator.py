from pathlib import Path
import json

ROOT = Path('winlator')

def replace(path, old, new):
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'Pattern not found in {path}: {old!r}')
    p.write_text(s.replace(old, new), encoding='utf-8')

# App identity
replace('app/build.gradle', "applicationId 'com.winlator'", "applicationId 'com.pesnicaragua.android'")
replace('app/build.gradle', 'versionCode 33', 'versionCode 1004')
replace('app/build.gradle', 'versionName "11.2"', 'versionName "0.2.2"')
replace('app/src/main/res/values/strings.xml', '<string name="app_name">Winlator</string>', '<string name="app_name">PES Nicaragua</string>')
replace('app/src/main/AndroidManifest.xml', 'android:authorities="com.winlator.FileProvider"', 'android:authorities="com.pesnicaragua.android.FileProvider"')
replace('app/src/main/java/com/winlator/core/FileUtils.java', '"com.winlator.FileProvider"', 'activity.getPackageName()+".FileProvider"')

# RootFS installer usable by the dedicated launcher.
replace('app/src/main/java/com/winlator/xenvironment/RootFSInstaller.java',
        'public static void install(final MainActivity activity)',
        'public static void install(final AppCompatActivity activity)')
replace('app/src/main/java/com/winlator/xenvironment/RootFSInstaller.java',
        'public static void installIfNeeded(final MainActivity activity)',
        'public static void installIfNeeded(final AppCompatActivity activity)')

# Dedicated launcher becomes the Android launcher. MainActivity remains available as technical mode.
old_activity = '''        <activity android:name="com.winlator.MainActivity"
            android:theme="@style/AppThemeDark"
            android:exported="true"
            android:screenOrientation="sensor"
            android:configChanges="keyboard|keyboardHidden|orientation|screenSize|screenLayout|smallestScreenSize|density|navigation">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
'''
new_activity = '''        <activity android:name="com.winlator.PesLauncherActivity"
            android:theme="@style/AppThemeDark"
            android:exported="true"
            android:screenOrientation="portrait"
            android:configChanges="keyboard|keyboardHidden|orientation|screenSize|screenLayout|smallestScreenSize|density|navigation">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

        <activity android:name="com.winlator.MainActivity"
            android:theme="@style/AppThemeDark"
            android:exported="false"
            android:screenOrientation="sensor"
            android:configChanges="keyboard|keyboardHidden|orientation|screenSize|screenLayout|smallestScreenSize|density|navigation" />
'''
replace('app/src/main/AndroidManifest.xml', old_activity, new_activity)

# Spanish strings still used by the technical mode / engine dialogs.
strings = ROOT / 'app/src/main/res/values/strings.xml'
s = strings.read_text(encoding='utf-8')
translations = {
    'Run':'Jugar', 'Shortcuts':'Juegos', 'Containers':'Entorno', 'Input Controls':'Controles táctiles',
    'New Container':'Nuevo entorno', 'Edit Container':'Editar entorno', 'Settings':'Ajustes',
    'About':'Acerca de', 'Exit':'Salir', 'Starting up...':'Iniciando...',
    'Installing System Files...':'Preparando motor de juego...',
    'Updating System Files...':'Actualizando motor de juego...',
    'Unable to install system files':'No se pudo preparar el motor de juego',
    'Keyboard':'Teclado', 'Toggle Fullscreen':'Pantalla completa',
    'No items to display':'No hay elementos'
}
for en, es in translations.items():
    s = s.replace('>'+en+'</string>', '>'+es+'</string>')
strings.write_text(s, encoding='utf-8')

# PES 6 touch profile.
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

# Make the PES profile automatic when launching from the dedicated launcher.
xserver = ROOT / 'app/src/main/java/com/winlator/XServerDisplayActivity.java'
xs = xserver.read_text(encoding='utf-8')
old_force = 'renderer.setForceWindowsFullscreen(shortcut != null && shortcut.getExtra("forceFullscreen", "0").equals("1"));'
new_force = 'renderer.setForceWindowsFullscreen((shortcut != null && shortcut.getExtra("forceFullscreen", "0").equals("1")) || getIntent().getBooleanExtra("pes_nicaragua", false));'
if old_force not in xs:
    raise SystemExit('fullscreen hook not found')
xs = xs.replace(old_force, new_force)
old_controls = '''        if (shortcut != null) {
            String controlsProfile = shortcut.getExtra("controlsProfile");
            if (!controlsProfile.isEmpty()) {
                ControlsProfile profile = inputControlsManager.getProfile(Integer.parseInt(controlsProfile));
                if (profile != null) showInputControls(profile);
            }
        }
'''
new_controls = '''        if (shortcut != null) {
            String controlsProfile = shortcut.getExtra("controlsProfile");
            if (!controlsProfile.isEmpty()) {
                ControlsProfile profile = inputControlsManager.getProfile(Integer.parseInt(controlsProfile));
                if (profile != null) showInputControls(profile);
            }
        }
        else if (getIntent().getBooleanExtra("pes_nicaragua", false)) {
            ControlsProfile profile = inputControlsManager.getProfile(5);
            if (profile != null) showInputControls(profile);
        }
'''
if old_controls not in xs:
    raise SystemExit('controls hook not found')
xs = xs.replace(old_controls, new_controls, 1)
xserver.write_text(xs, encoding='utf-8')

launcher = r'''package com.winlator;

import android.app.Activity;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.provider.OpenableColumns;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.winlator.box64.Box64Preset;
import com.winlator.container.Container;
import com.winlator.container.ContainerManager;
import com.winlator.container.DXWrappers;
import com.winlator.container.GraphicsDrivers;
import com.winlator.core.AppUtils;
import com.winlator.core.GPUHelper;
import com.winlator.xenvironment.RootFS;
import com.winlator.xenvironment.RootFSInstaller;

import org.json.JSONObject;
import org.apache.commons.compress.archivers.sevenz.SevenZArchiveEntry;
import org.apache.commons.compress.archivers.sevenz.SevenZFile;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class PesLauncherActivity extends AppCompatActivity {
    private static final int REQUEST_IMPORT = 9101;
    private static final String CONTAINER_NAME = "PES Nicaragua";
    private static final int COLOR_BG = 0xff11161c;
    private static final int COLOR_PANEL = 0xff1b222b;
    private static final int COLOR_TEXT = 0xfff4f7fb;
    private static final int COLOR_MUTED = 0xffaab5c1;
    private static final int COLOR_ACCENT = 0xffd51e2b;

    private final Handler handler = new Handler();
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    private TextView statusView;
    private TextView gpuView;
    private Button playButton;
    private Button importButton;
    private Button settingsButton;
    private Button technicalButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        AppUtils.setActivityTheme(this);
        super.onCreate(savedInstanceState);
        buildUi();
        refreshUi();

        if (!RootFS.find(this).isValid()) {
            statusView.setText("Preparando motor de juego…");
            setMainButtonsEnabled(false);
            RootFSInstaller.installIfNeeded(this);
            pollRootFs();
        }
        else {
            ensurePesContainer(null);
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        refreshUi();
        if (RootFS.find(this).isValid()) ensurePesContainer(null);
    }

    @Override
    protected void onDestroy() {
        executor.shutdownNow();
        super.onDestroy();
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private TextView text(String value, float size, int color) {
        TextView v = new TextView(this);
        v.setText(value);
        v.setTextSize(size);
        v.setTextColor(color);
        return v;
    }

    private Button button(String value) {
        Button b = new Button(this);
        b.setText(value);
        b.setAllCaps(false);
        b.setTextSize(17);
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(58));
        p.setMargins(0, dp(8), 0, dp(8));
        b.setLayoutParams(p);
        return b;
    }

    private void buildUi() {
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(COLOR_BG);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(24), dp(28), dp(24), dp(28));
        scroll.addView(root, new ScrollView.LayoutParams(
                ScrollView.LayoutParams.MATCH_PARENT,
                ScrollView.LayoutParams.WRAP_CONTENT));

        TextView title = text("PES NICARAGUA", 31, COLOR_TEXT);
        title.setGravity(Gravity.CENTER_HORIZONTAL);
        title.setTypeface(title.getTypeface(), android.graphics.Typeface.BOLD);
        root.addView(title);

        TextView subtitle = text("Liga Primera • Android", 16, COLOR_MUTED);
        subtitle.setGravity(Gravity.CENTER_HORIZONTAL);
        LinearLayout.LayoutParams subtitleParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT);
        subtitleParams.setMargins(0, dp(4), 0, dp(28));
        subtitle.setLayoutParams(subtitleParams);
        root.addView(subtitle);

        LinearLayout panel = new LinearLayout(this);
        panel.setOrientation(LinearLayout.VERTICAL);
        panel.setPadding(dp(18), dp(18), dp(18), dp(18));
        panel.setBackgroundColor(COLOR_PANEL);
        root.addView(panel, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT));

        statusView = text("Comprobando…", 17, COLOR_TEXT);
        statusView.setPadding(0, 0, 0, dp(8));
        panel.addView(statusView);

        gpuView = text("", 14, COLOR_MUTED);
        panel.addView(gpuView);

        importButton = button("Importar / actualizar juego");
        importButton.setOnClickListener(v -> chooseGamePackage());
        root.addView(importButton);

        playButton = button("JUGAR");
        playButton.setTextSize(21);
        playButton.setTextColor(Color.WHITE);
        playButton.setBackgroundColor(COLOR_ACCENT);
        playButton.setOnClickListener(v -> launchGame());
        root.addView(playButton);

        settingsButton = button("Configurar PES 6");
        settingsButton.setOnClickListener(v -> launchSettings());
        root.addView(settingsButton);

        TextView help = text(
                "Importa el ZIP de datos o el .7z original de PES 6. La app buscará pes6.exe automáticamente, preparará el entorno y después podrás entrar con JUGAR.",
                14, COLOR_MUTED);
        help.setPadding(0, dp(16), 0, dp(16));
        root.addView(help);

        technicalButton = button("Modo técnico");
        technicalButton.setOnClickListener(v -> startActivity(new Intent(this, MainActivity.class)));
        root.addView(technicalButton);

        setContentView(scroll);
    }

    private File getBaseDir() {
        File base = getExternalFilesDir(null);
        if (base == null) base = getFilesDir();
        return base;
    }

    private File getGameDir() {
        return new File(getBaseDir(), "PES6");
    }

    private boolean isGameValid(File dir) {
        return new File(dir, "pes6.exe").isFile()
                && new File(dir, "dat/0_text.afs").isFile()
                && new File(dir, "dat/e_text.afs").isFile()
                && new File(dir, "dat/e_sound.afs").isFile();
    }

    private void refreshUi() {
        boolean rootReady = RootFS.find(this).isValid();
        boolean gameReady = isGameValid(getGameDir());

        String renderer;
        try {
            renderer = GPUHelper.glGetRenderer(this);
        }
        catch (Throwable t) {
            renderer = "GPU Android";
        }

        boolean adreno = renderer.toLowerCase(Locale.ENGLISH).contains("adreno");
        gpuView.setText("GPU: " + renderer + "\nPerfil: " + (adreno ? "Adreno / Turnip + D8VK" : "Mali-Xclipse / compatibilidad"));

        if (!rootReady) {
            statusView.setText("Motor: preparando…");
        }
        else if (!gameReady) {
            statusView.setText("Motor listo ✓\nFalta importar el juego.");
        }
        else {
            statusView.setText("Motor listo ✓\nJuego listo ✓");
        }

        playButton.setEnabled(rootReady && gameReady);
        settingsButton.setEnabled(rootReady && gameReady);
        importButton.setEnabled(rootReady);
    }

    private void setMainButtonsEnabled(boolean enabled) {
        playButton.setEnabled(enabled);
        importButton.setEnabled(enabled);
        settingsButton.setEnabled(enabled);
    }

    private void pollRootFs() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                if (isFinishing()) return;
                if (RootFS.find(PesLauncherActivity.this).isValid()) {
                    statusView.setText("Motor listo ✓");
                    refreshUi();
                    ensurePesContainer(null);
                }
                else {
                    handler.postDelayed(this, 1200);
                }
            }
        }, 1200);
    }

    private void chooseGamePackage() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("*/*");
        intent.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{
                "application/zip",
                "application/x-7z-compressed",
                "application/octet-stream"
        });
        startActivityForResult(intent, REQUEST_IMPORT);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_IMPORT && resultCode == Activity.RESULT_OK && data != null && data.getData() != null) {
            importGamePackage(data.getData());
        }
    }

    private String getDisplayName(Uri uri) {
        String result = null;
        try (Cursor cursor = getContentResolver().query(uri, null, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                int index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                if (index >= 0) result = cursor.getString(index);
            }
        }
        catch (Exception ignored) {}
        if (result == null || result.isEmpty()) result = uri.getLastPathSegment();
        return result != null ? result : "paquete";
    }

    private void importGamePackage(Uri uri) {
        setMainButtonsEnabled(false);
        statusView.setText("Analizando paquete del juego…");

        executor.execute(() -> {
            File temp = new File(getBaseDir(), "PES6_importando");
            File sevenZipTemp = new File(getBaseDir(), "PES6_importando.7z");
            deleteRecursive(temp);
            deleteRecursive(sevenZipTemp);
            temp.mkdirs();

            try {
                String displayName = getDisplayName(uri).toLowerCase(Locale.ENGLISH);
                if (displayName.endsWith(".7z")) {
                    handler.post(() -> statusView.setText("Copiando paquete .7z…"));
                    copyUriToFile(uri, sevenZipTemp);
                    importSevenZip(sevenZipTemp, temp);
                }
                else {
                    importZip(uri, temp);
                }

                cleanLocalOnlyFiles(temp);

                if (!isGameValid(temp)) throw new Exception("El paquete se extrajo, pero faltan archivos esenciales.");

                File gameDir = getGameDir();
                File backup = new File(getBaseDir(), "PES6_anterior");
                deleteRecursive(backup);
                if (gameDir.exists() && !gameDir.renameTo(backup)) deleteRecursive(gameDir);

                if (!temp.renameTo(gameDir)) {
                    copyRecursive(temp, gameDir);
                    deleteRecursive(temp);
                }
                deleteRecursive(backup);
                deleteRecursive(sevenZipTemp);

                handler.post(() -> {
                    statusView.setText("Juego importado correctamente ✓");
                    ensurePesContainer(() -> {
                        refreshUi();
                        playButton.setEnabled(true);
                    });
                });
            }
            catch (Exception e) {
                deleteRecursive(temp);
                deleteRecursive(sevenZipTemp);
                handler.post(() -> {
                    statusView.setText("No se pudo importar: " + e.getMessage());
                    refreshUi();
                });
            }
        });
    }

    private void importZip(Uri uri, File temp) throws Exception {
        ArrayList<String> names = new ArrayList<>();
        try (InputStream raw = getContentResolver().openInputStream(uri);
             ZipInputStream zin = new ZipInputStream(new BufferedInputStream(raw))) {
            ZipEntry entry;
            while ((entry = zin.getNextEntry()) != null) {
                String name = entry.getName().replace('\\', '/');
                if (!entry.isDirectory()) names.add(name);
            }
        }

        String prefix = findGamePrefix(names);
        if (prefix == null) throw new Exception("El ZIP no contiene pes6.exe y dat/0_text.afs.");

        int total = 0;
        for (String name : names) if (name.startsWith(prefix)) total++;
        final int totalFiles = Math.max(1, total);
        int done = 0;

        try (InputStream raw = getContentResolver().openInputStream(uri);
             ZipInputStream zin = new ZipInputStream(new BufferedInputStream(raw))) {
            ZipEntry entry;
            byte[] buffer = new byte[131072];
            String tempCanonical = temp.getCanonicalPath() + File.separator;

            while ((entry = zin.getNextEntry()) != null) {
                String name = entry.getName().replace('\\', '/');
                if (!name.startsWith(prefix)) continue;
                String relative = name.substring(prefix.length());
                if (relative.isEmpty()) continue;

                File out = checkedOutputFile(temp, tempCanonical, relative);
                if (entry.isDirectory()) {
                    out.mkdirs();
                    continue;
                }

                File parent = out.getParentFile();
                if (parent != null) parent.mkdirs();
                try (BufferedOutputStream bout = new BufferedOutputStream(new FileOutputStream(out), 131072)) {
                    int read;
                    while ((read = zin.read(buffer)) != -1) bout.write(buffer, 0, read);
                }

                done++;
                postImportProgress(done, totalFiles);
            }
        }
    }

    private void importSevenZip(File archive, File temp) throws Exception {
        ArrayList<String> names = new ArrayList<>();
        try (SevenZFile sevenZ = new SevenZFile(archive)) {
            SevenZArchiveEntry entry;
            while ((entry = sevenZ.getNextEntry()) != null) {
                if (!entry.isDirectory() && entry.getName() != null) {
                    names.add(entry.getName().replace('\\', '/'));
                }
            }
        }

        String prefix = findGamePrefix(names);
        if (prefix == null) throw new Exception("El .7z no contiene la carpeta gamedata de PES 6.");

        int total = 0;
        for (String name : names) if (name.startsWith(prefix)) total++;
        final int totalFiles = Math.max(1, total);
        int done = 0;

        try (SevenZFile sevenZ = new SevenZFile(archive)) {
            SevenZArchiveEntry entry;
            byte[] buffer = new byte[131072];
            String tempCanonical = temp.getCanonicalPath() + File.separator;

            while ((entry = sevenZ.getNextEntry()) != null) {
                if (entry.getName() == null) continue;
                String name = entry.getName().replace('\\', '/');
                if (!name.startsWith(prefix)) continue;
                String relative = name.substring(prefix.length());
                if (relative.isEmpty()) continue;

                File out = checkedOutputFile(temp, tempCanonical, relative);
                if (entry.isDirectory()) {
                    out.mkdirs();
                    continue;
                }

                File parent = out.getParentFile();
                if (parent != null) parent.mkdirs();
                try (BufferedOutputStream bout = new BufferedOutputStream(new FileOutputStream(out), 131072)) {
                    int read;
                    while ((read = sevenZ.read(buffer)) > 0) bout.write(buffer, 0, read);
                }

                done++;
                postImportProgress(done, totalFiles);
            }
        }
    }

    private File checkedOutputFile(File temp, String tempCanonical, String relative) throws Exception {
        File out = new File(temp, relative);
        String outCanonical = out.getCanonicalPath();
        if (!outCanonical.startsWith(tempCanonical)) throw new SecurityException("Ruta del paquete inválida");
        return out;
    }

    private void postImportProgress(int done, int total) {
        if (done % 8 == 0 || done == total) {
            final int progress = Math.min(100, (done * 100) / Math.max(1, total));
            handler.post(() -> statusView.setText("Importando juego… " + progress + "%"));
        }
    }

    private void copyUriToFile(Uri uri, File out) throws Exception {
        try (InputStream in = new BufferedInputStream(getContentResolver().openInputStream(uri), 131072);
             BufferedOutputStream bout = new BufferedOutputStream(new FileOutputStream(out), 131072)) {
            byte[] buffer = new byte[131072];
            int read;
            while ((read = in.read(buffer)) != -1) bout.write(buffer, 0, read);
        }
    }

    private void cleanLocalOnlyFiles(File root) {
        deleteRecursive(new File(root, "bonus"));
        deleteRecursive(new File(root, "scripts/6Fixes.asi"));
        deleteRecursive(new File(root, "scripts/6Fixes.ini"));
        deleteRecursive(new File(root, "scripts/optiprojects.asi"));
    }

    private String findGamePrefix(ArrayList<String> names) {
        ArrayList<String> candidates = new ArrayList<>();
        for (String name : names) {
            String lower = name.toLowerCase(Locale.ENGLISH);
            if (lower.endsWith("pes6.exe")) {
                candidates.add(name.substring(0, name.length() - "pes6.exe".length()));
            }
        }

        String best = null;
        for (String prefix : candidates) {
            boolean text = false;
            boolean sound = false;
            for (String name : names) {
                String lower = name.toLowerCase(Locale.ENGLISH);
                String p = prefix.toLowerCase(Locale.ENGLISH);
                if (lower.equals(p + "dat/0_text.afs")) text = true;
                if (lower.equals(p + "dat/e_sound.afs")) sound = true;
            }
            if (text && sound && (best == null || prefix.length() < best.length())) best = prefix;
        }
        return best;
    }

    private Container getPesContainer() {
        if (!RootFS.find(this).isValid()) return null;
        ContainerManager manager = new ContainerManager(this);
        for (Container c : manager.getContainers()) {
            if (CONTAINER_NAME.equals(c.getName())) return c;
        }
        return null;
    }

    private void ensurePesContainer(@Nullable Runnable callback) {
        if (!RootFS.find(this).isValid()) return;

        ContainerManager manager = new ContainerManager(this);
        Container existing = null;
        for (Container c : manager.getContainers()) {
            if (CONTAINER_NAME.equals(c.getName())) {
                existing = c;
                break;
            }
        }

        boolean adreno;
        try {
            adreno = GPUHelper.getAdrenoModelId(this) > 0;
        }
        catch (Throwable t) {
            adreno = false;
        }

        String graphicsDriver = adreno
                ? GraphicsDrivers.TURNIP + "," + GraphicsDrivers.GLADIO
                : GraphicsDrivers.VORTEK + "," + GraphicsDrivers.GLADIO;
        String dxwrapper = adreno ? DXWrappers.DXVK : DXWrappers.WINED3D;

        if (existing != null) {
            existing.setScreenSize("960x540");
            existing.setGraphicsDriver(graphicsDriver);
            existing.setDXWrapper(dxwrapper);
            existing.setAudioDriver(Container.DEFAULT_AUDIO_DRIVER);
            existing.setWinComponents(Container.DEFAULT_WINCOMPONENTS);
            existing.setDrives("D:" + getGameDir().getAbsolutePath());
            existing.setStartupSelection(Container.STARTUP_SELECTION_ESSENTIAL);
            existing.setBox64Preset(Box64Preset.PERFORMANCE);
            existing.saveData();
            if (callback != null) callback.run();
            return;
        }

        try {
            JSONObject data = new JSONObject();
            data.put("name", CONTAINER_NAME);
            data.put("screenSize", "960x540");
            data.put("envVars", Container.DEFAULT_ENV_VARS);
            data.put("graphicsDriver", graphicsDriver);
            data.put("dxwrapper", dxwrapper);
            data.put("audioDriver", Container.DEFAULT_AUDIO_DRIVER);
            data.put("wincomponents", Container.DEFAULT_WINCOMPONENTS);
            data.put("drives", "D:" + getGameDir().getAbsolutePath());
            data.put("hudMode", 0);
            data.put("startupSelection", Container.STARTUP_SELECTION_ESSENTIAL);
            data.put("box64Preset", Box64Preset.PERFORMANCE);

            statusView.setText("Creando entorno PES Nicaragua…");
            manager.createContainerAsync(data, container -> {
                if (container == null) {
                    statusView.setText("No se pudo crear el entorno.");
                }
                else {
                    statusView.setText("Entorno PES Nicaragua listo ✓");
                }
                refreshUi();
                if (callback != null && container != null) callback.run();
            });
        }
        catch (Exception e) {
            statusView.setText("Error creando entorno: " + e.getMessage());
        }
    }

    private void launchGame() {
        if (!isGameValid(getGameDir())) {
            statusView.setText("Primero importa el juego.");
            return;
        }
        launchExecutable(new File(getGameDir(), "pes6.exe"), true);
    }

    private void launchSettings() {
        File exe = new File(getGameDir(), "settings.exe");
        if (!exe.isFile()) {
            statusView.setText("No se encontró settings.exe");
            return;
        }
        launchExecutable(exe, false);
    }

    private void launchExecutable(File exe, boolean pesControls) {
        Container c = getPesContainer();
        if (c == null) {
            ensurePesContainer(() -> launchExecutable(exe, pesControls));
            return;
        }

        Intent intent = new Intent(this, XServerDisplayActivity.class);
        intent.putExtra("container_id", c.id);
        intent.putExtra("exec_path", exe.getAbsolutePath());
        if (pesControls) intent.putExtra("pes_nicaragua", true);
        startActivity(intent);
    }

    private void deleteRecursive(File file) {
        if (file == null || !file.exists()) return;
        if (file.isDirectory()) {
            File[] children = file.listFiles();
            if (children != null) for (File child : children) deleteRecursive(child);
        }
        file.delete();
    }

    private void copyRecursive(File src, File dst) throws Exception {
        if (src.isDirectory()) {
            dst.mkdirs();
            File[] children = src.listFiles();
            if (children != null) {
                for (File child : children) copyRecursive(child, new File(dst, child.getName()));
            }
            return;
        }

        File parent = dst.getParentFile();
        if (parent != null) parent.mkdirs();
        try (InputStream in = new BufferedInputStream(new java.io.FileInputStream(src), 131072);
             BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(dst), 131072)) {
            byte[] buffer = new byte[131072];
            int read;
            while ((read = in.read(buffer)) != -1) out.write(buffer, 0, read);
        }
    }
}
'''

launcher_path = ROOT / 'app/src/main/java/com/winlator/PesLauncherActivity.java'
launcher_path.write_text(launcher, encoding='utf-8')

marker = ROOT / 'PES_NICARAGUA_BUILD.txt'
marker.write_text('PES Nicaragua Android Runtime v0.2.2\nBase: Winlator 11.2\nDedicated launcher + ZIP/7z importer + auto container + touch controls.\n', encoding='utf-8')
print('Applied PES Nicaragua Android v0.2.2 patch')
