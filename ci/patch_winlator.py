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
replace('app/build.gradle', 'versionCode 33', 'versionCode 1100')
replace('app/build.gradle', 'versionName "11.2"', 'versionName "0.3.0-audit"')
replace('app/src/main/res/values/strings.xml', '<string name="app_name">Winlator</string>', '<string name="app_name">PES Nicaragua</string>')
replace('app/src/main/AndroidManifest.xml', 'android:authorities="com.winlator.FileProvider"', 'android:authorities="com.pesnicaragua.android.FileProvider"')
replace('app/src/main/java/com/winlator/core/FileUtils.java', '"com.winlator.FileProvider"', 'activity.getPackageName()+".FileProvider"')

replace('app/src/main/java/com/winlator/core/AppUtils.java',
        'public static final String INTERNAL_STORAGE = "/data/data/com.winlator/storage";',
        'public static final String INTERNAL_STORAGE = "/data/data/com.pesnicaragua.android/storage";')
replace('app/src/main/cpp/winlator/include/winlator.h',
        '#define APP_CACHE_DIR "/data/data/com.winlator/cache"',
        '#define APP_CACHE_DIR "/data/data/com.pesnicaragua.android/cache"')
replace('app/src/main/cpp/vortekrenderer/include/vortek.h',
        '#define VORTEK_SERVER_PATH "/data/data/com.winlator/files/rootfs/tmp/.vortek/V0"',
        '#define VORTEK_SERVER_PATH "/data/data/com.pesnicaragua.android/files/rootfs/tmp/.vortek/V0"')
replace('app/src/main/cpp/gladiorenderer/include/gladio.h',
        '#define X11_SERVER_PATH "/data/data/com.winlator/files/rootfs/tmp/.X11-unix/X0"',
        '#define X11_SERVER_PATH "/data/data/com.pesnicaragua.android/files/rootfs/tmp/.X11-unix/X0"')

gradle_path = ROOT / 'app/build.gradle'
gradle_text = gradle_path.read_text(encoding='utf-8')
gradle_text = gradle_text.replace(
    "    implementation 'androidx.lifecycle:lifecycle-process:2.5.1'\n",
    "    implementation 'androidx.lifecycle:lifecycle-process:2.5.1'\n    testImplementation 'junit:junit:4.13.2'\n"
)
gradle_path.write_text(gradle_text, encoding='utf-8')

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
import android.os.Environment;
import android.os.Handler;
import android.os.StatFs;
import android.provider.OpenableColumns;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
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
import java.io.PrintWriter;
import java.io.StringWriter;
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
    private ActivityResultLauncher<Intent> importLauncher;
    private boolean filePickerOpen = false;
    private boolean importInProgress = false;

    private TextView statusView;
    private TextView gpuView;
    private Button playButton;
    private Button importButton;
    private Button manualImportButton;
    private Button settingsButton;
    private Button technicalButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        AppUtils.setActivityTheme(this);
        super.onCreate(savedInstanceState);
        installCrashLogger();
        registerImportLauncher();
        buildUi();
        showPreviousCrashIfAny();
        refreshUi();

        if (!RootFS.find(this).isValid()) {
            statusView.setText("Preparando motor de juego…");
            setMainButtonsEnabled(false);
            RootFSInstaller.installIfNeeded(this);
            pollRootFs();
        }
        else {
            refreshUi();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (!filePickerOpen && !importInProgress) refreshUi();
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

        TextView version = text("v0.2.5", 13, COLOR_MUTED);
        version.setGravity(Gravity.CENTER_HORIZONTAL);
        LinearLayout.LayoutParams versionParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT);
        versionParams.setMargins(0, 0, 0, dp(18));
        version.setLayoutParams(versionParams);
        root.addView(version);

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

        importButton = button("Buscar juego en Descargas");
        importButton.setOnClickListener(v -> findGameInDownloads());
        root.addView(importButton);

        manualImportButton = button("Elegir archivo manualmente");
        manualImportButton.setOnClickListener(v -> chooseGamePackage());
        root.addView(manualImportButton);

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
                "Primero toca Buscar juego en Descargas. La app localizará automáticamente el ZIP o .7z de PES 6. Si no lo encuentra, usa Elegir archivo manualmente.",
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
        if (manualImportButton != null) manualImportButton.setEnabled(rootReady);
    }

    private void setMainButtonsEnabled(boolean enabled) {
        playButton.setEnabled(enabled);
        importButton.setEnabled(enabled);
        if (manualImportButton != null) manualImportButton.setEnabled(enabled);
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
                }
                else {
                    handler.postDelayed(this, 1200);
                }
            }
        }, 1200);
    }

    private void findGameInDownloads() {
        if (importInProgress) return;
        statusView.setText("Buscando PES 6 en Descargas…");

        executor.execute(() -> {
            try {
                ArrayList<File> roots = new ArrayList<>();
                File publicDownloads = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
                if (publicDownloads != null) roots.add(publicDownloads);
                roots.add(new File("/storage/emulated/0/Download"));
                roots.add(new File("/sdcard/Download"));

                ArrayList<File> candidates = new ArrayList<>();
                for (File root : roots) collectArchives(root, candidates, 2);

                File best = null;
                long bestScore = Long.MIN_VALUE;
                for (File file : candidates) {
                    String n = file.getName().toLowerCase(Locale.ENGLISH);
                    long score = file.length();
                    if (n.contains("pes")) score += 2_000_000_000L;
                    if (n.contains("opti")) score += 1_000_000_000L;
                    if (n.endsWith(".7z")) score += 500_000_000L;
                    if (file.length() < 50L * 1024L * 1024L) score -= 5_000_000_000L;
                    if (best == null || score > bestScore) {
                        best = file;
                        bestScore = score;
                    }
                }

                final File found = best;
                handler.post(() -> {
                    if (found == null || !found.isFile()) {
                        statusView.setText("No encontré un ZIP/7z de PES 6 en Descargas. Usa Elegir archivo manualmente.");
                        return;
                    }

                    long mb = found.length() / (1024L * 1024L);
                    statusView.setText("Encontrado: " + found.getName() + " (" + mb + " MB)\nIniciando importación…");
                    importGamePackage(Uri.fromFile(found));
                });
            }
            catch (Throwable e) {
                writeCrashLog(e);
                handler.post(() -> statusView.setText("No pude leer Descargas: " + e.getClass().getSimpleName() + ". Usa Elegir archivo manualmente."));
            }
        });
    }

    private void collectArchives(File dir, ArrayList<File> out, int depth) {
        if (dir == null || depth < 0 || !dir.isDirectory()) return;
        File[] files = dir.listFiles();
        if (files == null) return;

        for (File file : files) {
            if (file.isDirectory()) {
                collectArchives(file, out, depth - 1);
                continue;
            }
            String name = file.getName().toLowerCase(Locale.ENGLISH);
            if ((name.endsWith(".7z") || name.endsWith(".zip")) && file.canRead()) out.add(file);
        }
    }

    private void registerImportLauncher() {
        importLauncher = registerForActivityResult(
                new ActivityResultContracts.StartActivityForResult(),
                result -> {
                    filePickerOpen = false;
                    Intent data = result.getData();
                    if (result.getResultCode() != Activity.RESULT_OK || data == null || data.getData() == null) {
                        statusView.setText("No se seleccionó ningún archivo.");
                        refreshUi();
                        return;
                    }

                    Uri uri = data.getData();
                    try {
                        int flags = data.getFlags() & Intent.FLAG_GRANT_READ_URI_PERMISSION;
                        if (flags != 0) getContentResolver().takePersistableUriPermission(uri, flags);
                    }
                    catch (Throwable ignored) {}

                    String selectedName = getDisplayName(uri);
                    statusView.setText("Archivo seleccionado: " + selectedName + "\nIniciando importación…");
                    importGamePackage(uri);
                }
        );
    }

    private void chooseGamePackage() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
        intent.setType("*/*");
        intent.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{
                "application/zip",
                "application/x-7z-compressed",
                "application/octet-stream",
                "application/x-compressed"
        });
        filePickerOpen = true;
        statusView.setText("Selecciona el ZIP o .7z del juego…");
        importLauncher.launch(intent);
    }

    private File getCrashLogFile() {
        return new File(getBaseDir(), "pes_nicaragua_crash.log");
    }

    private void installCrashLogger() {
        final Thread.UncaughtExceptionHandler previous = Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread, throwable) -> {
            writeCrashLog(throwable);
            if (previous != null) previous.uncaughtException(thread, throwable);
        });
    }

    private void writeCrashLog(Throwable throwable) {
        try {
            StringWriter sw = new StringWriter();
            throwable.printStackTrace(new PrintWriter(sw));
            try (FileOutputStream out = new FileOutputStream(getCrashLogFile(), false)) {
                out.write(sw.toString().getBytes(java.nio.charset.StandardCharsets.UTF_8));
            }
        }
        catch (Throwable ignored) {}
    }

    private void showPreviousCrashIfAny() {
        File log = getCrashLogFile();
        if (!log.isFile()) return;
        try {
            String txt = new String(java.nio.file.Files.readAllBytes(log.toPath()), java.nio.charset.StandardCharsets.UTF_8);
            String first = txt.split("\\n", 2)[0];
            statusView.setText("La ejecución anterior falló: " + first);
        }
        catch (Throwable ignored) {}
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

    private long getDocumentSize(Uri uri) {
        try (Cursor cursor = getContentResolver().query(uri, null, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                int index = cursor.getColumnIndex(OpenableColumns.SIZE);
                if (index >= 0 && !cursor.isNull(index)) return cursor.getLong(index);
            }
        }
        catch (Exception ignored) {}
        return 0;
    }

    private long directorySize(File file) {
        if (file == null || !file.exists()) return 0;
        if (file.isFile()) return file.length();
        long size = 0;
        File[] children = file.listFiles();
        if (children != null) for (File child : children) size += directorySize(child);
        return size;
    }

    private boolean hasEnoughSpace(Uri uri) {
        try {
            long archiveSize = getDocumentSize(uri);
            long oldGameSize = directorySize(getGameDir());
            long required = Math.max(1500L * 1024L * 1024L, archiveSize * 4L) + oldGameSize;
            long available = new StatFs(getBaseDir().getAbsolutePath()).getAvailableBytes();
            if (available < required) {
                final long needMb = required / (1024L * 1024L);
                final long freeMb = available / (1024L * 1024L);
                handler.post(() -> statusView.setText("Espacio insuficiente. Libre: " + freeMb + " MB; recomendado: " + needMb + " MB."));
                return false;
            }
            return true;
        }
        catch (Throwable ignored) {
            return true;
        }
    }

    private void importGamePackage(Uri uri) {
        importInProgress = true;
        setMainButtonsEnabled(false);
        AppUtils.keepScreenOn(this);
        String selectedName = getDisplayName(uri);
        statusView.setText("Archivo seleccionado: " + selectedName + "\nAnalizando paquete…");

        executor.execute(() -> {
            File temp = new File(getBaseDir(), "PES6_importando");
            File sevenZipTemp = new File(getBaseDir(), "PES6_importando.7z");
            deleteRecursive(temp);
            deleteRecursive(sevenZipTemp);
            temp.mkdirs();

            try {
                if (!hasEnoughSpace(uri)) {
                    deleteRecursive(temp);
                    handler.post(() -> {
                        importInProgress = false;
                        refreshUi();
                    });
                    return;
                }

                String displayName = getDisplayName(uri).toLowerCase(Locale.ENGLISH);
                if (displayName.endsWith(".7z")) {
                    handler.post(() -> statusView.setText("Copiando paquete .7z…"));
                    copyUriToFile(uri, sevenZipTemp);
                    extractSevenZipOnce(sevenZipTemp, temp);
                }
                else {
                    extractZipOnce(uri, temp);
                }

                File gameRoot = findGameRoot(temp);
                if (gameRoot == null) throw new Exception("No encontré pes6.exe junto con la carpeta dat.");

                cleanLocalOnlyFiles(gameRoot);
                if (!isGameValid(gameRoot)) throw new Exception("Faltan archivos esenciales después de extraer.");

                File gameDir = getGameDir();
                File backup = new File(getBaseDir(), "PES6_anterior");
                deleteRecursive(backup);

                if (gameDir.exists() && !gameDir.renameTo(backup)) {
                    throw new Exception("No pude preparar la actualización del juego anterior.");
                }

                boolean moved = gameRoot.renameTo(gameDir);
                if (!moved) copyRecursive(gameRoot, gameDir);

                if (!isGameValid(gameDir)) {
                    deleteRecursive(gameDir);
                    if (backup.exists()) backup.renameTo(gameDir);
                    throw new Exception("La copia final no pasó la validación.");
                }

                deleteRecursive(backup);
                deleteRecursive(temp);
                deleteRecursive(sevenZipTemp);
                getCrashLogFile().delete();

                handler.post(() -> {
                    importInProgress = false;
                    statusView.setText("Juego importado y verificado ✓\nPulsa JUGAR para preparar el entorno.");
                    refreshUi();
                });
            }
            catch (Throwable e) {
                writeCrashLog(e);
                deleteRecursive(temp);
                deleteRecursive(sevenZipTemp);
                handler.post(() -> {
                    importInProgress = false;
                    statusView.setText("Importación detenida: " + e.getClass().getSimpleName() + ": " + String.valueOf(e.getMessage()));
                    refreshUi();
                });
            }
        });
    }

    private void extractZipOnce(Uri uri, File temp) throws Exception {
        try (InputStream raw = getContentResolver().openInputStream(uri);
             ZipInputStream zin = new ZipInputStream(new BufferedInputStream(raw))) {
            ZipEntry entry;
            byte[] buffer = new byte[131072];
            String tempCanonical = temp.getCanonicalPath() + File.separator;
            int done = 0;

            while ((entry = zin.getNextEntry()) != null) {
                String relative = entry.getName().replace('\\', '/');
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
                if (done % 8 == 0) {
                    final int count = done;
                    handler.post(() -> statusView.setText("Extrayendo ZIP… " + count + " archivos"));
                }
            }
        }
    }

    private void extractSevenZipOnce(File archive, File temp) throws Exception {
        try (SevenZFile sevenZ = new SevenZFile(archive)) {
            SevenZArchiveEntry entry;
            byte[] buffer = new byte[131072];
            String tempCanonical = temp.getCanonicalPath() + File.separator;
            int done = 0;

            while ((entry = sevenZ.getNextEntry()) != null) {
                if (entry.getName() == null) continue;
                String relative = entry.getName().replace('\\', '/');
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
                if (done % 4 == 0) {
                    final int count = done;
                    handler.post(() -> statusView.setText("Extrayendo 7z… " + count + " archivos"));
                }
            }
        }
    }

    private File findGameRoot(File root) {
        if (isGameValid(root)) return root;
        File[] children = root.listFiles();
        if (children == null) return null;
        for (File child : children) {
            if (!child.isDirectory()) continue;
            File found = findGameRoot(child);
            if (found != null) return found;
        }
        return null;
    }

    private File checkedOutputFile(File temp, String tempCanonical, String relative) throws Exception {
        File out = new File(temp, relative);
        String outCanonical = out.getCanonicalPath();
        if (!outCanonical.startsWith(tempCanonical)) throw new SecurityException("Ruta del paquete inválida");
        return out;
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
            existing.setCPUList(Container.getFallbackCPUList());
            existing.setCPUListWoW64(Container.getFallbackCPUList());
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
            data.put("cpuList", Container.getFallbackCPUList());
            data.put("cpuListWoW64", Container.getFallbackCPUList());

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


# Pure-Java archive inspector used by the audited importer and CI tests.
inspector = r'''package com.winlator;

import org.apache.commons.compress.archivers.sevenz.SevenZArchiveEntry;
import org.apache.commons.compress.archivers.sevenz.SevenZFile;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

public final class GameArchiveInspector {
    public enum ArchiveType { ZIP, SEVEN_Z }

    public interface ProgressCallback {
        void onProgress(long written, long total);
    }

    public static final class Inspection {
        public final ArchiveType type;
        public final String prefix;
        public final long totalUncompressedBytes;
        public final int fileCount;

        Inspection(ArchiveType type, String prefix, long totalUncompressedBytes, int fileCount) {
            this.type = type;
            this.prefix = prefix;
            this.totalUncompressedBytes = totalUncompressedBytes;
            this.fileCount = fileCount;
        }
    }

    private static final String[] REQUIRED = new String[]{
            "pes6.exe",
            "dat/0_text.afs",
            "dat/e_text.afs",
            "dat/e_sound.afs"
    };

    private GameArchiveInspector() {}

    public static ArchiveType detectType(File archive) throws IOException {
        byte[] head = new byte[6];
        try (InputStream in = new BufferedInputStream(new FileInputStream(archive))) {
            int read = in.read(head);
            if (read >= 4 && head[0] == 0x50 && head[1] == 0x4b &&
                    ((head[2] == 0x03 && head[3] == 0x04) ||
                     (head[2] == 0x05 && head[3] == 0x06) ||
                     (head[2] == 0x07 && head[3] == 0x08))) {
                return ArchiveType.ZIP;
            }
            if (read >= 6 &&
                    (head[0] & 0xff) == 0x37 && (head[1] & 0xff) == 0x7a &&
                    (head[2] & 0xff) == 0xbc && (head[3] & 0xff) == 0xaf &&
                    (head[4] & 0xff) == 0x27 && (head[5] & 0xff) == 0x1c) {
                return ArchiveType.SEVEN_Z;
            }
        }
        throw new IOException("Formato no reconocido: el archivo no es ZIP ni 7z.");
    }

    public static Inspection inspect(File archive) throws IOException {
        ArchiveType type = detectType(archive);
        List<EntryMeta> entries = type == ArchiveType.ZIP ? listZip(archive) : listSevenZ(archive);
        String prefix = findGamePrefix(entries);
        if (prefix == null) {
            throw new IOException("No encontré pes6.exe junto con dat/0_text.afs, dat/e_text.afs y dat/e_sound.afs.");
        }

        long total = 0;
        int count = 0;
        for (EntryMeta meta : entries) {
            if (meta.directory || !meta.name.startsWith(prefix)) continue;
            String relative = meta.name.substring(prefix.length());
            if (relative.isEmpty() || shouldSkip(relative)) continue;
            total += Math.max(0, meta.size);
            count++;
        }
        if (count == 0) throw new IOException("La carpeta gamedata está vacía.");
        return new Inspection(type, prefix, total, count);
    }

    public static void extract(File archive, Inspection inspection, File outputDir, ProgressCallback callback) throws IOException {
        if (outputDir.exists()) deleteRecursive(outputDir);
        if (!outputDir.mkdirs() && !outputDir.isDirectory()) {
            throw new IOException("No pude crear la carpeta temporal del juego.");
        }
        if (inspection.type == ArchiveType.ZIP) extractZip(archive, inspection, outputDir, callback);
        else extractSevenZ(archive, inspection, outputDir, callback);
    }

    static String findGamePrefixForTest(Collection<String> names) {
        List<EntryMeta> entries = new ArrayList<>();
        for (String name : names) entries.add(new EntryMeta(normalize(name), 1, false));
        return findGamePrefix(entries);
    }

    private static String findGamePrefix(List<EntryMeta> entries) {
        Set<String> lower = new HashSet<>();
        for (EntryMeta meta : entries) lower.add(meta.name.toLowerCase(Locale.ENGLISH));

        String best = null;
        for (EntryMeta meta : entries) {
            if (meta.directory) continue;
            String nameLower = meta.name.toLowerCase(Locale.ENGLISH);
            if (!(nameLower.equals("pes6.exe") || nameLower.endsWith("/pes6.exe"))) continue;

            String prefix = meta.name.substring(0, meta.name.length() - "pes6.exe".length());
            String prefixLower = prefix.toLowerCase(Locale.ENGLISH);
            boolean ok = true;
            for (String required : REQUIRED) {
                if (!lower.contains(prefixLower + required)) {
                    ok = false;
                    break;
                }
            }
            if (ok && (best == null || prefix.length() < best.length())) best = prefix;
        }
        return best;
    }

    private static List<EntryMeta> listZip(File archive) throws IOException {
        List<EntryMeta> result = new ArrayList<>();
        try (ZipFile zip = new ZipFile(archive)) {
            Enumeration<? extends ZipEntry> enumeration = zip.entries();
            while (enumeration.hasMoreElements()) {
                ZipEntry entry = enumeration.nextElement();
                result.add(new EntryMeta(normalize(entry.getName()), entry.getSize(), entry.isDirectory()));
            }
        }
        return result;
    }

    private static List<EntryMeta> listSevenZ(File archive) throws IOException {
        List<EntryMeta> result = new ArrayList<>();
        try (SevenZFile sevenZ = new SevenZFile(archive)) {
            SevenZArchiveEntry entry;
            while ((entry = sevenZ.getNextEntry()) != null) {
                result.add(new EntryMeta(normalize(entry.getName()), entry.getSize(), entry.isDirectory()));
            }
        }
        return result;
    }

    private static void extractZip(File archive, Inspection inspection, File outputDir, ProgressCallback callback) throws IOException {
        long written = 0;
        byte[] buffer = new byte[128 * 1024];
        try (ZipFile zip = new ZipFile(archive)) {
            Enumeration<? extends ZipEntry> enumeration = zip.entries();
            while (enumeration.hasMoreElements()) {
                ZipEntry entry = enumeration.nextElement();
                String name = normalize(entry.getName());
                if (!name.startsWith(inspection.prefix)) continue;
                String relative = name.substring(inspection.prefix.length());
                if (relative.isEmpty() || shouldSkip(relative)) continue;

                File out = safeTarget(outputDir, relative);
                if (entry.isDirectory()) {
                    if (!out.mkdirs() && !out.isDirectory()) throw new IOException("No pude crear " + relative);
                    continue;
                }

                File parent = out.getParentFile();
                if (parent != null && !parent.mkdirs() && !parent.isDirectory()) throw new IOException("No pude crear " + parent.getName());

                try (InputStream in = new BufferedInputStream(zip.getInputStream(entry), buffer.length);
                     BufferedOutputStream bout = new BufferedOutputStream(new FileOutputStream(out), buffer.length)) {
                    int read;
                    while ((read = in.read(buffer)) != -1) {
                        bout.write(buffer, 0, read);
                        written += read;
                        if (callback != null) callback.onProgress(written, inspection.totalUncompressedBytes);
                    }
                }
            }
        }
    }

    private static void extractSevenZ(File archive, Inspection inspection, File outputDir, ProgressCallback callback) throws IOException {
        long written = 0;
        byte[] buffer = new byte[128 * 1024];
        try (SevenZFile sevenZ = new SevenZFile(archive)) {
            SevenZArchiveEntry entry;
            while ((entry = sevenZ.getNextEntry()) != null) {
                String name = normalize(entry.getName());
                if (!name.startsWith(inspection.prefix)) continue;
                String relative = name.substring(inspection.prefix.length());
                if (relative.isEmpty() || shouldSkip(relative)) continue;

                File out = safeTarget(outputDir, relative);
                if (entry.isDirectory()) {
                    if (!out.mkdirs() && !out.isDirectory()) throw new IOException("No pude crear " + relative);
                    continue;
                }

                File parent = out.getParentFile();
                if (parent != null && !parent.mkdirs() && !parent.isDirectory()) throw new IOException("No pude crear " + parent.getName());

                try (BufferedOutputStream bout = new BufferedOutputStream(new FileOutputStream(out), buffer.length)) {
                    int read;
                    while ((read = sevenZ.read(buffer)) > 0) {
                        bout.write(buffer, 0, read);
                        written += read;
                        if (callback != null) callback.onProgress(written, inspection.totalUncompressedBytes);
                    }
                }
            }
        }
    }

    private static boolean shouldSkip(String relative) {
        String lower = normalize(relative).toLowerCase(Locale.ENGLISH);
        return lower.startsWith("bonus/") || lower.equals("scripts/optiprojects.asi");
    }

    private static File safeTarget(File root, String relative) throws IOException {
        File target = new File(root, relative);
        String rootPath = root.getCanonicalPath() + File.separator;
        String targetPath = target.getCanonicalPath();
        if (!targetPath.startsWith(rootPath)) throw new IOException("Ruta insegura dentro del archivo: " + relative);
        return target;
    }

    static String normalize(String name) {
        if (name == null) return "";
        String out = name.replace('\\', '/');
        while (out.startsWith("/")) out = out.substring(1);
        while (out.contains("//")) out = out.replace("//", "/");
        return out;
    }

    private static void deleteRecursive(File file) {
        if (file == null || !file.exists()) return;
        if (file.isDirectory()) {
            File[] children = file.listFiles();
            if (children != null) for (File child : children) deleteRecursive(child);
        }
        file.delete();
    }

    private static final class EntryMeta {
        final String name;
        final long size;
        final boolean directory;

        EntryMeta(String name, long size, boolean directory) {
            this.name = name;
            this.size = size;
            this.directory = directory;
        }
    }
}
'''
(ROOT / 'app/src/main/java/com/winlator/GameArchiveInspector.java').write_text(inspector, encoding='utf-8')

test_source = r'''package com.winlator;

import org.junit.Test;

import java.io.File;
import java.io.FileOutputStream;
import java.util.Arrays;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import static org.junit.Assert.*;

public class GameArchiveInspectorTest {
    @Test
    public void findsOriginalPortableLayout() {
        String prefix = GameArchiveInspector.findGamePrefixForTest(Arrays.asList(
                "PES 6 PORTABLE RIP OptiJuegos/Install/gamedata/pes6.exe",
                "PES 6 PORTABLE RIP OptiJuegos/Install/gamedata/settings.exe",
                "PES 6 PORTABLE RIP OptiJuegos/Install/gamedata/dat/0_text.afs",
                "PES 6 PORTABLE RIP OptiJuegos/Install/gamedata/dat/e_text.afs",
                "PES 6 PORTABLE RIP OptiJuegos/Install/gamedata/dat/e_sound.afs"
        ));
        assertEquals("PES 6 PORTABLE RIP OptiJuegos/Install/gamedata/", prefix);
    }

    @Test
    public void rejectsIncompletePackage() {
        assertNull(GameArchiveInspector.findGamePrefixForTest(Arrays.asList(
                "gamedata/pes6.exe",
                "gamedata/dat/0_text.afs",
                "gamedata/dat/e_text.afs"
        )));
    }

    @Test
    public void detectsAndInspectsZipByMagicNotExtension() throws Exception {
        File temp = File.createTempFile("pes6-import-", ".bin");
        try {
            try (ZipOutputStream zip = new ZipOutputStream(new FileOutputStream(temp))) {
                for (String name : Arrays.asList(
                        "root/gamedata/pes6.exe",
                        "root/gamedata/dat/0_text.afs",
                        "root/gamedata/dat/e_text.afs",
                        "root/gamedata/dat/e_sound.afs",
                        "root/gamedata/scripts/6Fixes.asi"
                )) {
                    zip.putNextEntry(new ZipEntry(name));
                    zip.write(new byte[]{1,2,3,4});
                    zip.closeEntry();
                }
            }
            assertEquals(GameArchiveInspector.ArchiveType.ZIP, GameArchiveInspector.detectType(temp));
            GameArchiveInspector.Inspection inspection = GameArchiveInspector.inspect(temp);
            assertEquals("root/gamedata/", inspection.prefix);
            assertTrue(inspection.fileCount >= 4);
        }
        finally {
            temp.delete();
        }
    }

    @Test
    public void detectsSevenZSignature() throws Exception {
        File temp = File.createTempFile("pes6-7z-", ".bin");
        try {
            try (FileOutputStream out = new FileOutputStream(temp)) {
                out.write(new byte[]{0x37,0x7a,(byte)0xbc,(byte)0xaf,0x27,0x1c,0,0});
            }
            assertEquals(GameArchiveInspector.ArchiveType.SEVEN_Z, GameArchiveInspector.detectType(temp));
        }
        finally {
            temp.delete();
        }
    }
}
'''
test_path = ROOT / 'app/src/test/java/com/winlator/GameArchiveInspectorTest.java'
test_path.parent.mkdir(parents=True, exist_ok=True)
test_path.write_text(test_source, encoding='utf-8')

marker = ROOT / 'PES_NICARAGUA_BUILD.txt'
marker.write_text('PES Nicaragua Android Runtime v0.3.0-audit\nBase: Winlator 11.2\nAudited SAF importer + package-path fixes + import tests.\n', encoding='utf-8')
print('Applied PES Nicaragua Android v0.3.0-audit patch')
