---
name: mobile-engineering
description: >-
  Builds secure, responsive, and offline-first mobile applications using native Android (Jetpack Compose)
  or cross-platform Capacitor. Governs mobile lifecycle, Keystore secure storage, runtime permissions, and hardware bridging.
---

# Mobile Engineering Skill

> **Status**: APPROVED (Workspace-Local)  
> **Version**: 1.0.0  
> **Domain**: DOM-07 (Software Development), DOM-11 (Mobile Engineering)  
> **Reference Standard**: [mobile_engineering.md](../../05_DEVELOPMENT/standards/mobile_engineering.md)

---

## 1. Purpose & Scope
This skill governs the development and packaging of mobile applications for Android and iOS within the MASTER AI ecosystem. It covers both cross-platform hybrid workflows (Capacitor + React/TypeScript) and native Android implementations (Jetpack Compose + Kotlin coroutines).

## 2. When to Use This Skill
- Packaging a web application into an installable Android APK/AAB or iOS IPA.
- Implementing native device features (Camera, Biometrics, Push Notifications, Geolocation).
- Designing offline-first synchronization with SQLite / WatermelonDB / Room.
- Securing client-side tokens and API keys using Android Keystore / iOS Keychain.
- Handling mobile application lifecycle states (active, paused, background, destroyed).
- Managing Android runtime permission requests and edge-to-edge UI layouts.

## 3. Required Inputs
- Target platforms (Android API 26+, iOS 15+).
- Application architecture choice (Capacitor Hybrid vs Native Android Compose).
- Required hardware permissions and offline data synchronization requirements.

## 4. Execution Workflow

### Step 1: Framework Selection
- **Capacitor Hybrid**: Default choice for 90% of business applications, dashboards, and portals where code sharing with web is paramount.
- **Native Android Compose**: Reserved for high-frequency sensor processing, low-latency audio/video, or platform-native widgets.

### Step 2: Capacitor Project Setup & Bridge Configuration
1. Initialize Capacitor in web project: `npx cap init <AppName> <AppId> --web-dir dist`.
2. Add platform targets: `npx cap add android` and `npx cap add ios`.
3. Configure `capacitor.config.ts` with strict security settings:
   - Disable remote URL loading in production (serve exclusively from bundled web assets).
   - Enforce HTTPS and restrict allowed navigation origins.

### Step 3: Hardware APIs & Security Integration
1. Access hardware via official Capacitor plugins (`@capacitor/camera`, `@capacitor/preferences`).
2. Store sensitive tokens exclusively in hardware-backed storage (Keystore/Keychain via `@capacitor-community/secure-storage`).
3. Request runtime permissions just-in-time with clear contextual user explanation.

### Step 4: Offline-First Synchronization
1. Persist local mutations in SQLite with status `is_dirty = 1`.
2. Listen to network connectivity changes via `@capacitor/network`.
3. Replay local changes to backend when connection is restored, handling conflict resolution via server timestamp comparison.

### Step 5: Native Build & Release Packaging
1. Sync web assets into native shells: `npx cap sync`.
2. Generate signed release bundles using Gradle (`./gradlew bundleRelease`) with R8/ProGuard obfuscation enabled.
3. Validate APK on physical or virtual device via `android` CLI.

## 5. Strict Rules & Constraints
- NEVER store unencrypted auth tokens or passwords in `localStorage` or `SharedPreferences`.
- NEVER request permissions on app launch before explaining why the permission is required.
- NEVER block the UI thread on native or web layers with heavy JSON serialization.
- NEVER leave debug signing keys or developer logging active in release builds.

## 6. Code Pattern Example (Capacitor Hardware & Secure Storage)

```typescript
import { SecureStoragePlugin } from 'capacitor-secure-storage-plugin';
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
import { Network } from '@capacitor/network';

// Secure Token Storage via Android Keystore / iOS Keychain
export async function storeSessionToken(token: string): Promise<void> {
  await SecureStoragePlugin.set({
    key: 'auth_session_token',
    value: token,
  });
}

export async function getSessionToken(): Promise<string | null> {
  try {
    const { value } = await SecureStoragePlugin.get({ key: 'auth_session_token' });
    return value;
  } catch {
    return null; // Key does not exist or device is locked
  }
}

// Camera Capture with graceful error handling
export async function captureDocumentImage(): Promise<string | null> {
  try {
    const photo = await Camera.getPhoto({
      resultType: CameraResultType.Base64,
      source: CameraSource.Camera,
      quality: 85,
      allowEditing: false,
    });
    return photo.base64String || null;
  } catch (error) {
    console.warn("User canceled photo capture or permission denied", error);
    return null;
  }
}
```

## 7. Quality Checklist
- [ ] App launches cleanly in offline airplane mode without crashing.
- [ ] Edge-to-edge system bar insets (`WindowInsetsCompat`) are respected.
- [ ] Sensitive tokens are stored in hardware-backed secure storage.
- [ ] R8 / ProGuard rules verify zero leakage of internal class names in release APK.
- [ ] Memory footprint remains below 120MB on base webview initialization.
