from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path("/storage/emulated/0/Fkksf")
BACKUP = ROOT / "backups"

FILES = {
    "settings.gradle": """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(
        RepositoriesMode.FAIL_ON_PROJECT_REPOS
    )
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "Fkksf"
include(":app")
""",

    "build.gradle": """plugins {
    id 'com.android.application' version '8.7.3' apply false
}
""",

    "gradle.properties": """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
""",

    ".gitignore": """.gradle/
build/
local.properties
.idea/
*.iml
""",

    "app/build.gradle": """plugins {
    id 'com.android.application'
}

android {
    namespace 'com.fkksf.keyboard'
    compileSdk 35

    defaultConfig {
        applicationId 'com.fkksf.keyboard'
        minSdk 23
        targetSdk 28
        versionCode 1
        versionName '1.0'
    }
}
""",
}

def write_file(name, content):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        BACKUP.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = BACKUP / (
            name.replace("/", "__") + "." + stamp + ".bak"
        )
        shutil.copy2(path, backup)
        print("Backup:", backup)

    path.write_text(content, encoding="utf-8")
    print("Created:", path)

def main():
    ROOT.mkdir(parents=True, exist_ok=True)

    for name, content in FILES.items():
        write_file(name, content)

    print()
    print("Fkksf: مرحله اول تمام شد.")
    print("Project:", ROOT)

if __name__ == "__main__":
    main()
    # Fkksf - Stage 2
# Android Manifest and Main Activity

STAGE2_FILES = {
    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:label="Fkksf"
        android:theme="@style/AppTheme">

        <activity
            android:name=".MainActivity"
            android:exported="true">

            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>

        </activity>

        <service
            android:name=".FkksfInputMethodService"
            android:label="Fkksf Keyboard"
            android:permission="android.permission.BIND_INPUT_METHOD"
            android:exported="true">

            <intent-filter>
                <action android:name="android.view.InputMethod"/>
            </intent-filter>

            <meta-data
                android:name="android.view.im"
                android:resource="@xml/method"/>

        </service>

    </application>
</manifest>
""",

    "app/src/main/res/xml/method.xml": """<?xml version="1.0" encoding="utf-8"?>
<input-method xmlns:android="http://schemas.android.com/apk/res/android">

    <subtype
        android:label="English"
        android:imeSubtypeLocale="en_US"
        android:imeSubtypeMode="keyboard"/>

    <subtype
        android:label="فارسی"
        android:imeSubtypeLocale="fa_IR"
        android:imeSubtypeMode="keyboard"/>

</input-method>
""",

    "app/src/main/res/values/styles.xml": """<resources>
    <style
        name="AppTheme"
        parent="@android:style/Theme.Material.Light.NoActionBar">

        <item name="android:fontFamily">sans</item>
        <item name="android:colorAccent">#356AC3</item>

    </style>
</resources>
""",

    "app/src/main/java/com/fkksf/keyboard/MainActivity.java": r'''package com.fkksf.keyboard;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(24, 32, 24, 24);

        TextView title = new TextView(this);
        title.setText("Fkksf Keyboard");
        title.setTextSize(24);
        root.addView(title);

        TextView info = new TextView(this);
        info.setText(
            "Android Keyboard Fkksf\\n\\n" +
            "Paste, Copy, ReDo, UnDo\\n" +
            "Four cursor arrows\\n" +
            "Persian and English layout"
        );
        info.setTextSize(16);

        LinearLayout.LayoutParams lp =
            new LinearLayout.LayoutParams(-1, -2);

        lp.topMargin = 20;
        root.addView(info, lp);

        Button settings = new Button(this);
        settings.setText("Keyboard Settings");

        settings.setOnClickListener(v ->
            startActivity(
                new Intent(Settings.ACTION_INPUT_METHOD_SETTINGS)
            )
        );

        root.addView(settings);

        Button picker = new Button(this);
        picker.setText("Choose Fkksf Keyboard");

        picker.setOnClickListener(v -> {
            InputMethodManager imm =
                (InputMethodManager)
                getSystemService(Context.INPUT_METHOD_SERVICE);

            if (imm != null) {
                imm.showInputMethodPicker();
            }
        });

        root.addView(picker);
        setContentView(root);
    }
}
'''
}


def write_stage2():
    ROOT.mkdir(parents=True, exist_ok=True)

    for name, content in STAGE2_FILES.items():
        write_file(name, content)

    print()
    print("Fkksf Stage 2 completed.")
    print("Files:", len(STAGE2_FILES))


write_stage2()