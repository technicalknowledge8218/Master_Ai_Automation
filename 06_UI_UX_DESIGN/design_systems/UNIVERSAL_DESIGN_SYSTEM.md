# Universal UI/UX Design System Specification

## 1. Overview and Core Philosophy

The **Universal UI/UX Design System (UDS)** provides a cross-platform design specification for web, mobile (Android/iOS via Capacitor or React Native), and desktop applications in the MASTER AI ecosystem.

### Foundational Principles
1. **Accessibility by Default (WCAG 2.2 AAA)**: Every interactive element must be keyboard navigable, screen-reader announced, and meet rigorous contrast and target size ratios.
2. **Predictable State Modeling**: Components operate as finite state machines (`idle`, `hover`, `focus-visible`, `active`, `loading`, `disabled`, `error`). No hidden or intermediate undefined states.
3. **Token-Driven Consistency**: All layout dimensions, colors, typographic hierarchy, shadows, and animation curves are derived from [DESIGN_TOKENS.json](../tokens/DESIGN_TOKENS.json).
4. **Mobile-First & Adaptive**: Interfaces scale progressively from 320px viewport widths to ultra-wide displays without horizontal overflow or clipped touch targets.
5. **Content-First Clarity**: Minimal cognitive load. Layouts prioritize scannability, clear typography, and unambiguous visual hierarchy over decorative styling.

---

## 2. Design Tokens Integration

The design system directly consumes the token taxonomy defined in `06_UI_UX_DESIGN/tokens/DESIGN_TOKENS.json`:

```
┌─────────────────────────────────────────────────────────────┐
│                       DESIGN TOKENS                         │
├──────────────┬──────────────┬───────────────┬───────────────┤
│    Colors    │  Typography  │    Spacing    │    Motion     │
│ Semantic L/D │ Scales xs-5xl│ 4px/8px grid  │ Easing/Timers │
└───────┬──────┴──────┬───────┴───────┬───────┴───────┬───────┘
        │             │               │               │
        ▼             ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│                 UNIVERSAL COMPONENT LAYER                   │
│   Buttons · Forms · Modals · Cards · Nav · Tables · States  │
└─────────────────────────────────────────────────────────────┘
```

- **Baseline Spacing Grid**: 4px micro-grid / 8px macro-grid (`space-1` = 4px, `space-2` = 8px, `space-4` = 16px, etc.).
- **Typography**: System font stacks (`Inter`, `Segoe UI`, `Roboto`, `system-ui`) paired with Monospace (`JetBrains Mono`, `Fira Code`) for technical payloads.
- **Breakpoints**: Mobile (`sm`: 640px), Tablet (`md`: 768px), Desktop (`lg`: 1024px), Wide (`xl`: 1280px), Ultra-Wide (`2xl`: 1536px).

---

## 3. Core Component Specifications

### 3.1 Button Component
Buttons communicate user intent and trigger deterministic actions.

- **Variants**:
  - `Primary`: High-emphasis actions (Submit, Confirm, Create). High-contrast solid fill.
  - `Secondary`: Medium-emphasis actions (Cancel, Filter, Back). Outline or surface fill.
  - `Destructive`: Irreversible or high-risk actions (Delete, Terminate). Crimson/Red palette.
  - `Ghost`: Low-emphasis actions inside toolbars or tables. Transparent background until hover.
- **Sizes**:
  - `sm`: Height 32px, text 12px, padding 8px 12px (Dense interfaces).
  - `md`: Height 40px, text 14px, padding 10px 16px (Standard desktop/tablet).
  - `lg`: Height 48px, text 16px, padding 12px 24px (Mobile primary actions, touch-optimized).
- **Interactive States**:
  - `idle`: Token-defined surface and border.
  - `hover`: Subtle contrast increase (+8% brightness or surface overlay).
  - `focus-visible`: 2px solid ring with 2px offset (`ring-primary-500 ring-offset-2`).
  - `active`: Slight scale depression (transform: `scale(0.98)`).
  - `loading`: Spinner replaces leading icon or text; element receives `aria-busy="true"` and `disabled`.
  - `disabled`: Opacity 45%, `cursor: not-allowed`, `pointer-events: none` on mouse/touch.

### 3.2 Form Controls & Input Fields
Form inputs must provide persistent context, clear boundaries, and explicit validation feedback.

- **Structure**:
  1. `Label`: Always visible above the input (`text-sm font-medium text-neutral-800 dark:text-neutral-200`). Never rely solely on placeholder text.
  2. `Input Box`: 40px height minimum, 1px solid border (`border-neutral-300 dark:border-neutral-700`), 6px border-radius, 12px horizontal padding.
  3. `Helper Text / Error Text`: Displayed below input box. Error text is rendered in `error-500` color accompanied by `role="alert"` and tied to input via `aria-describedby`.
- **States**:
  - `Default`: Subdued border.
  - `Focus`: High-contrast border (`border-primary-500`), focus ring (`ring-2 ring-primary-500/20`).
  - `Error`: Crimson border (`border-red-500`), focus ring in red, error message rendered with exclamation icon.
  - `Success`: Green check indicator (optional on async validation).

### 3.3 Cards and Containers
Cards organize related information into distinct, scannable units.

- **Surface**: `surface-primary` (`#FFFFFF` light, `#1E293B` dark).
- **Border & Shadow**: Subtle 1px border (`neutral-200` light, `neutral-800` dark) paired with `shadow-sm` or `shadow-md`. Avoid heavy drop shadows.
- **Padding**: Uniform `space-4` (16px) or `space-6` (24px).
- **Header, Body, Footer**: Explicit semantic separation. Actions aligned right in footer.

### 3.4 Modal Dialogs and Overlays
Used for focused user input, confirmations, or critical alerts.

- **Overlay / Backdrop**: `rgba(0, 0, 0, 0.5)` with backdrop blur (`backdrop-blur-sm`).
- **Focus Trap**: Focus must be trapped inside modal when open. Pressing `Escape` must close the modal unless `preventDismiss` is true.
- **Accessibility Attributes**:
  - `role="dialog"` or `role="alertdialog"`
  - `aria-modal="true"`
  - `aria-labelledby="dialog-title-id"`
  - `aria-describedby="dialog-description-id"`
- **Closing & Focus Restoration**: Focus must return to the triggering element upon closure.

### 3.5 Feedback and Notifications (Toasts)
Ephemeral messages communicating system state and asynchronous results.

- **Categories**: `Info`, `Success`, `Warning`, `Error`.
- **Positioning**: Bottom-right on desktop (`bottom-4 right-4`), top-center on mobile devices.
- **Accessibility**:
  - Non-critical messages: `role="status"`, `aria-live="polite"`.
  - Critical/Error alerts: `role="alert"`, `aria-live="assertive"`.
- **Persistence**: Auto-dismiss after 4000ms for info/success; persistent or manual dismiss for errors. Always provide a visible close button.

### 3.6 Data Display & Tables
Tabular data must remain readable and accessible across viewports.

- **Desktop**: Compact row height (44px), sticky headers, alternating or border-separated rows, explicit sort icons with `aria-sort`.
- **Mobile/Responsive**: Transform into stacked cards or responsive scroll container with sticky primary column.
- **Empty States**: If zero rows, display a centered illustration or icon with explanatory text and a primary call-to-action (e.g., "No records found — Create new record").

### 3.7 Loading and Skeleton States
Prevent layout shift during asynchronous data fetching.

- **Skeleton Screens**: Mirror the exact dimensions and layout of the incoming content (shimmer animation with `neutral-200` to `neutral-300` gradient).
- **Progressive Disclosure**: Show cached data first where applicable, then update silently.
- **Spinners**: Used only for inline actions (e.g. inside a button during submission), never for full-page layout loading.

---

## 4. Accessibility Standards (WCAG 2.2 Level AA Baseline with AAA Enhancements)

The Universal Design System establishes **WCAG 2.2 Level AA** as the non-negotiable compliance baseline, with selective **Level AAA enhancements** applied where feasible:

| Rule | Compliance Tier | Requirement | Implementation Detail |
|---|---|---|---|
| **Body Text Contrast** | **Level AAA** | Target $\ge 7:1$ (Min 4.5:1) | Primary text achieves **17.85:1** light (`#0F172A`/`#FFFFFF`) and **18.33:1** dark (`#F9FAFB`/`#0B0F19`). |
| **Secondary Text Contrast** | **Level AAA** | Target $\ge 7:1$ (Min 4.5:1) | Secondary text achieves **7.58:1** light (`#475569`/`#FFFFFF`) and **12.90:1** dark (`#CBD5E1`/`#0B0F19`). |
| **Muted Text Restriction** | **Exemption** | Only for disabled UI | Muted text (`#94A3B8`/`#6B7280`) is strictly restricted to disabled elements (exempt under WCAG 1.4.3). Never use for body copy or form hints. |
| **Primary Button Labels** | **Level AA** | Minimum 4.5:1 (Normal) / 3:1 (Large) | Light mode white on `#2563EB` achieves **5.17:1** (AA Pass). Dark mode white on `#3B82F6` achieves **3.68:1** (requires bold/14pt+ large text, or use dark text for small buttons). |
| **UI Component Borders** | **Level AA (1.4.11)** | Minimum 3:1 against background | Inputs must use high-contrast borders (`neutral-400` / `#94A3B8`) or distinct surface fills to maintain boundary visibility. |
| **Touch Target Size** | **Level AAA (2.5.5)** | Minimum 44x44 CSS pixels | Interactive buttons, icon toggles, and form controls padded to $\ge 44\times 44$px (exceeding AA 2.5.8 24px requirement). |
| **Focus Indicator** | **Level AA (2.4.11)** | Visible, $\ge 3:1$ contrast | 2px solid ring with 2px offset (`outline: 2px solid var(--primary-500)`). |
| **Reduced Motion** | **Level AAA (2.3.3)** | Honor motion preferences | `@media (prefers-reduced-motion: reduce) { * { animation-duration: 0.01ms !important; } }` |
| **Non-Color Indicators** | **Level A (1.4.1)** | No color-only status | Error states include both red text AND exclamation icon + text prefix. |

---

## 5. Theme System (Light and Dark Mode)

The design system operates a dual-theme token pipeline:
- **Default Resolution**: Uses `prefers-color-scheme` media query by default, with an override persisted in `localStorage`.
- **CSS Variables Mapping**: All components consume CSS custom properties referencing tokens:
```css
:root {
  --color-surface-bg: #FFFFFF;
  --color-surface-panel: #F8FAFC;
  --color-text-primary: #0F172A;
  --color-text-secondary: #475569;
  --color-border: #E2E8F0;
}

[data-theme="dark"], .dark {
  --color-surface-bg: #0F172A;
  --color-surface-panel: #1E293B;
  --color-text-primary: #F8FAFC;
  --color-text-secondary: #94A3B8;
  --color-border: #334155;
}
```
- **Anti-Flicker Execution**: Theme script runs synchronously before DOM rendering in `<head>` to prevent flash of unstyled content (FOUC).

---

## 6. Good vs Bad UI/UX Design Examples

### Example 1: Form Input with Validation

```tsx
// ❌ BAD: Floating placeholder, no label, red color only, inaccessible
function BadInput({ error, onChange }) {
  return (
    <div>
      <input placeholder="Enter your email" onChange={onChange} style={{ borderColor: error ? 'red' : 'gray' }} />
      {error && <span style={{ color: 'red' }}>Invalid</span>}
    </div>
  );
}

// ✅ GOOD: Visible label, ARIA linking, 44px touch target, icon + text error, focus ring
function GoodInput({ id, label, helperText, error, value, onChange }: InputProps) {
  const errorId = `${id}-error`;
  const helperId = `${id}-helper`;

  return (
    <div className="flex flex-col gap-1.5 w-full">
      <label htmlFor={id} className="text-sm font-medium text-neutral-800 dark:text-neutral-200">
        {label}
      </label>
      <input
        id={id}
        type="email"
        value={value}
        onChange={onChange}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? errorId : helperText ? helperId : undefined}
        className={clsx(
          "h-11 px-3.5 rounded-lg border text-sm transition-colors duration-150",
          "focus:outline-none focus:ring-2 focus:ring-offset-2",
          error
            ? "border-red-500 focus:border-red-600 focus:ring-red-500/30 text-red-900 dark:text-red-100"
            : "border-neutral-300 dark:border-neutral-700 focus:border-primary-500 focus:ring-primary-500/20"
        )}
      />
      {error ? (
        <p id={errorId} role="alert" className="flex items-center gap-1.5 text-xs font-medium text-red-600 dark:text-red-400">
          <AlertCircleIcon className="w-4 h-4 shrink-0" aria-hidden="true" />
          <span>{error}</span>
        </p>
      ) : helperText ? (
        <p id={helperId} className="text-xs text-neutral-500 dark:text-neutral-400">
          {helperText}
        </p>
      ) : null}
    </div>
  );
}
```

### Example 2: Destructive Action Confirmation

```tsx
// ❌ BAD: Sudden alert(), irreversible deletion on click
function BadDeleteButton({ onDelete }) {
  return <button onClick={onDelete}>Delete Account</button>;
}

// ✅ GOOD: Accessible alertdialog, explicit consequences, keyboard trapped, primary safe action
function GoodDeleteModal({ isOpen, onClose, onConfirm, itemName }: ModalProps) {
  return (
    <Dialog open={isOpen} onClose={onClose} role="alertdialog" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
      <DialogOverlay className="fixed inset-0 bg-black/60 backdrop-blur-sm" />
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel className="w-full max-w-md rounded-xl bg-white dark:bg-neutral-900 p-6 shadow-xl border border-neutral-200 dark:border-neutral-800">
          <DialogTitle id="dialog-title" className="text-lg font-semibold text-neutral-900 dark:text-neutral-50">
            Permanently delete {itemName}?
          </DialogTitle>
          <p id="dialog-desc" className="mt-2 text-sm text-neutral-600 dark:text-neutral-400">
            This action cannot be undone. All associated data and backups will be removed immediately.
          </p>
          <div className="mt-6 flex justify-end gap-3">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm font-medium rounded-lg border border-neutral-300 hover:bg-neutral-100 focus:ring-2">
              Cancel
            </button>
            <button type="button" onClick={onConfirm} className="px-4 py-2 text-sm font-medium rounded-lg bg-red-600 text-white hover:bg-red-700 focus:ring-2 focus:ring-red-500">
              Confirm Deletion
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  );
}
```

---

## 7. Machine Validation and Registry

Component specifications and token compliance are machine-auditable via:
- Token Schema: `06_UI_UX_DESIGN/tokens/DESIGN_TOKENS.json`
- Component Registry: `06_UI_UX_DESIGN/design_systems/DESIGN_SYSTEM_REGISTRY.json`
- Automated Test Validator: `06_UI_UX_DESIGN/scripts/validate_design_system.py`
