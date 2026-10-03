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
replace('app/build.gradle', 'versionCode 33', 'versionCode 1007')
replace('app/build.gradle', 'versionName "11.2"', 'versionName "0.2.5"')
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

marker = ROOT / 'PES_NICARAGUA_BUILD.txt'
marker.write_text('PES Nicaragua Android Runtime v0.2.5\nBase: Winlator 11.2\nDedicated launcher + ZIP/7z importer + auto container + touch controls.\n', encoding='utf-8')
print('Applied PES Nicaragua Android v0.2.5 patch')
