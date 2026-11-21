# MASTER-AI Full-Stack Standards: Mobile Engineering

> **Domain**: `05_DEVELOPMENT/standards/`  
> **Status**: APPROVED & ACTIVE (Phase 5)  
> **Core Platforms**: Native Android (Kotlin / Jetpack Compose) & Hybrid Cross-Platform (Capacitor)  

---

## 1. Mobile Architectural Paradigms

MASTER-AI mobile development adopts a dual-path architecture based on project requirements:
1. **Cross-Platform Hybrid (Capacitor)**: Recommended default for content, SaaS, and web-adjacent mobile applications. Utilizes a shared modern web frontend (React/Tailwind) packaged inside a native WebView wrapper with typed plugin bridges.
2. **Native Android (Kotlin / Jetpack Compose)**: Mandated for high-performance graphics, real-time background processing, hardware sensor integration, and deeply native platform experiences.

---

## 2. Capacitor Cross-Platform Standards

### Architecture Principles:
- **Offline-First Storage**: Store local application data in **SQLite** via `@capacitor-community/sqlite` or **Preferences** for simple key-value pairs. Never rely on volatile `localStorage` for critical data.
- **Native Plugin Isolation**: Wrap all native Capacitor plugin calls in strongly-typed service abstractions (e.g., `CameraService`, `BiometricAuthService`). Provide automatic fallback implementations when running in a standard web browser.
- **Safe Area Insets**: Respect device safe areas (notches, status bars, navigation bars) using CSS environment variables:
  ```css
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  ```

---

## 3. Native Android Architecture (Jetpack Compose)

```
[UI Layer (Jetpack Compose Screens & Components)]
        │
        ├──> State Flows (StateFlow / SharedFlow)
        ▼
[Presentation / ViewModel Layer (Android Architecture Components)]
        │
        ├──> Coroutines (viewModelScope / Dispatchers.IO)
        ▼
[Domain / Use Case Layer (Business Logic & Repository Interfaces)]
        │
        ├──> Repository Implementations
        ▼
[Data Layer (Room SQLite DB + Retrofit Network Client)]
```

### Core Native Invariants:
1. **Single Source of Truth (SSOT)**: The local database (Room) serves as the single source of truth for the UI. Remote API responses update the database, which automatically emits updated state to the UI via Kotlin `Flow`.
2. **Lifecycle Awareness**: ViewModels must survive configuration changes (device rotation). Never pass Activity contexts into ViewModels to prevent memory leaks.
3. **Jetpack Compose Performance**: Avoid unstable lambdas in Composables. Use `@Immutable` or `@Stable` annotations on data models passed to Compose trees to facilitate intelligent recomposition skipping.

---

## 4. Mobile Security & Secure Storage

1. **Secure Credential Storage**:
   - **Android**: Use `EncryptedSharedPreferences` backed by the hardware-backed **Android Keystore System**. Never store auth tokens or passwords in plain XML files.
   - **iOS / Capacitor**: Store sensitive tokens in the **iOS Keychain**.
2. **Runtime Permissions**:
   - Never request permissions upfront on app launch. Request permissions contextually when the user initiates an action requiring the feature (e.g., requesting camera access only after tapping "Scan QR").
   - Handle permission denials gracefully with explanatory fallback UI.
3. **Network Security Config**:
   - Enforce cleartext traffic blocking (`android:usesCleartextTraffic="false"`).
   - Implement SSL Certificate Pinning for high-security enterprise and financial endpoints.
4. **App Hardening & Obfuscation**:
   - Enable ProGuard / R8 minification and resource shrinking for release builds:
     ```kotlin
     buildTypes {
         release {
             isMinifyEnabled = true
             isShrinkResources = true
             proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
         }
     }
     ```
