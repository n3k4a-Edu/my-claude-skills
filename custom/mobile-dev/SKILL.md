---
name: mobile-dev
description: "Mobile app development for iOS, Android, React Native, Flutter, and cross-platform. Use when the user asks about building mobile apps, React Native, Flutter, Swift/SwiftUI, Kotlin/Jetpack Compose, app store publishing, mobile UI patterns, push notifications, offline-first, or any mobile development question."
metadata:
  version: "1.0.0"
---

# Mobile Development

Build apps that feel native, perform well, and ship fast.

## Framework Selection

| Framework | Best for | Performance | Team skill needed |
|---|---|---|---|
| **React Native** | Teams with React/JS experience, rapid prototyping | Good (90%+ native) | JavaScript/TypeScript |
| **Flutter** | Custom UI, pixel-perfect design, single codebase | Excellent (compiled) | Dart |
| **SwiftUI** | iOS-only, Apple ecosystem deep integration | Native | Swift |
| **Jetpack Compose** | Android-only, Material Design | Native | Kotlin |
| **Kotlin Multiplatform** | Shared business logic, native UI per platform | Native | Kotlin |

Decision tree:
1. iOS only → SwiftUI
2. Android only → Jetpack Compose
3. Both, team knows React → React Native
4. Both, custom UI/animations → Flutter
5. Both, shared logic but native UI → Kotlin Multiplatform

## React Native

### Project Setup (Expo recommended)
```bash
npx create-expo-app@latest my-app
cd my-app && npx expo start
```

### Key Libraries
| Need | Library |
|---|---|
| Navigation | `@react-navigation/native` |
| State | `zustand` or `@tanstack/react-query` |
| UI Components | `tamagui`, `nativewind`, or `react-native-paper` |
| Storage | `@react-native-async-storage/async-storage` |
| HTTP | `axios` or `fetch` with `@tanstack/react-query` |
| Forms | `react-hook-form` + `zod` |
| Animations | `react-native-reanimated` |
| Maps | `react-native-maps` |
| Camera | `expo-camera` |
| Push | `expo-notifications` |

### Performance Rules
- Use `FlatList` (not ScrollView) for lists >20 items
- Memoize with `React.memo`, `useMemo`, `useCallback`
- Avoid inline styles in render (create StyleSheet.create)
- Use Hermes engine (enabled by default in Expo)
- Image optimization: resize before display, use `expo-image`
- Minimize bridge calls (new architecture: JSI eliminates this)

## Flutter

### Project Setup
```bash
flutter create my_app
cd my_app && flutter run
```

### Architecture (Clean Architecture)
```
lib/
  core/          # Shared utilities, constants, themes
  features/
    auth/
      data/      # Repositories, data sources, models
      domain/    # Entities, use cases, repository interfaces
      presentation/ # Screens, widgets, state management
```

### State Management
| Solution | Complexity | Best for |
|---|---|---|
| `Riverpod` | Medium | Most apps (recommended) |
| `Bloc/Cubit` | Medium-High | Large teams, strict patterns |
| `Provider` | Low | Simple apps |
| `GetX` | Low | Rapid prototyping (careful with tech debt) |

## Mobile UI Patterns

### Navigation
- **Tab bar** (bottom): 3-5 primary destinations
- **Drawer**: Secondary navigation, settings
- **Stack**: Detail screens push on top
- **Modal**: Interrupting actions (confirmations, quick inputs)

### Common Screens
- **Onboarding**: 3-4 slides max, skip button, value propositions
- **Auth**: Email/password, social login, biometric
- **Feed/List**: Pull-to-refresh, infinite scroll, skeleton loading
- **Detail**: Hero image, scrollable content, sticky CTA
- **Settings**: Grouped sections, toggles, navigation items
- **Empty states**: Illustration + action button (not just "No data")
- **Error states**: Retry button, helpful message

### Responsive Design
- Use relative units (% or flex) not fixed pixels
- Test on smallest (iPhone SE 375px) and largest (iPad/tablet 1024px+)
- Safe area insets for notches and home indicators
- Dynamic type support for accessibility

## App Store Publishing

### iOS (App Store)
1. Apple Developer account ($99/year)
2. App Store Connect: screenshots, description, keywords
3. Build with Xcode → Archive → Upload
4. Review process: 1-7 days (usually 24-48h)
5. Required: privacy policy URL, app icons (1024x1024)

### Android (Google Play)
1. Google Play Developer account ($25 one-time)
2. Play Console: store listing, screenshots, content rating
3. Build signed APK/AAB → Upload
4. Review: usually hours to 1 day
5. Required: privacy policy, content rating questionnaire

### Both Platforms
- Screenshots: 3-5 showing key features, with marketing text overlay
- Description: first 2 lines are critical (visible before "read more")
- Keywords/ASO: research with App Annie, Sensor Tower
- Ratings: prompt happy users (after positive action, not on launch)

## Push Notifications

Best practices:
- Ask permission at the right time (after value is shown, not on launch)
- Segment users (don't blast everyone the same message)
- Include deep links (tap → go to relevant screen)
- Respect quiet hours
- A/B test notification copy
- Track: open rate, conversion, opt-out rate

## Offline-First Architecture

1. Local database (SQLite/Realm/Hive) as source of truth
2. Sync engine: queue local changes, push when online
3. Conflict resolution: last-write-wins or merge strategy
4. UI shows local data immediately, syncs in background
5. Visual indicator for sync status (online/offline/syncing)
