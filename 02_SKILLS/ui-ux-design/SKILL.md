---
name: ui-ux-design
description: >-
  Designs accessible, beautiful, and user-centered design systems, layouts, and interaction patterns.
  Translates design tokens into cohesive interfaces following WCAG 2.2 AAA guidelines and mobile-first principles.
---

# UI/UX Design Skill

> **Status**: APPROVED (Workspace-Local)  
> **Version**: 1.0.0  
> **Domain**: DOM-07 (Software Development), DOM-08 (UI/UX Design)  
> **Reference Standard**: [UNIVERSAL_DESIGN_SYSTEM.md](../../06_UI_UX_DESIGN/design_systems/UNIVERSAL_DESIGN_SYSTEM.md)

---

## 1. Purpose & Scope
This skill governs user experience design, visual aesthetics, component ergonomics, design token governance, and accessibility compliance. It ensures all interfaces created across the MASTER AI ecosystem provide exceptional usability, low cognitive load, and pixel-level consistency.

## 2. When to Use This Skill
- Establishing design systems, component guidelines, and visual tokens.
- Designing responsive layouts across desktop, tablet, and mobile viewports.
- Defining interactive states for complex UI components (Buttons, Modals, Forms, Drawers).
- Auditing user workflows for cognitive load, visual clutter, and accessibility barriers.
- Designing empty states, loading skeletons, and error recovery flows.
- Ensuring seamless dark/light mode transitions without visual jarring.

## 3. Required Inputs
- User persona, target tasks, and device contexts.
- Design tokens defined in `06_UI_UX_DESIGN/tokens/DESIGN_TOKENS.json`.
- Functional specifications of screens and interaction goals.

## 4. Execution Workflow

### Step 1: Token & Hierarchy Alignment
1. Adhere to the 4px/8px baseline grid for all spacing, margins, and padding.
2. Establish typographic scale: H1 (32px/40px), H2 (24px/32px), H3 (20px/28px), Body (14px/20px or 16px/24px), Caption (12px/16px).
3. Ensure color contrast reaches at least 4.5:1 (AA) and targets 7:1 (AAA) against surfaces.

### Step 2: Component State Specification
Every interactive component must define 7 discrete visual states:
- `idle`: Default resting state.
- `hover`: Subtle brightness/surface shift (+8% overlay).
- `focus-visible`: 2px solid primary ring with 2px offset.
- `active`: Slight press scale (`scale(0.98)`).
- `loading`: Replaces icon/label with spinner and sets `aria-busy="true"`.
- `disabled`: Opacity 45%, `cursor: not-allowed`, inert.
- `error`: High-contrast error border and icon + text announcement.

### Step 3: Information Architecture & Scannability
1. Put primary actions top-right (desktop) or sticky bottom (mobile).
2. Group related data using cards with subtle 1px borders rather than heavy drop shadows.
3. Use progressive disclosure: show summaries first with optional drill-downs.

### Step 4: Responsive & Mobile Adaptations
1. Mobile-first design: single-column layout by default, expanding to multi-column at `md` (768px) and `lg` (1024px).
2. Ensure minimum touch targets are 44x44px or 48x48px on mobile devices.
3. Support swipe-to-dismiss and native gestures for mobile dialogs and sheets.

### Step 5: Accessibility & Screen Reader Validation
1. Verify keyboard navigation with Tab, Shift+Tab, and Enter/Space.
2. Ensure modal dialogs trap focus and close upon pressing Escape.
3. Verify that non-color cues (icons, badges, text labels) accompany all status indicators.

## 5. Strict Rules & Constraints
- NEVER rely solely on color to convey information or system state.
- NEVER use low-contrast text (contrast ratio < 4.5:1 is strictly prohibited).
- NEVER hide focus outlines without replacing them with custom accessible focus rings.
- NEVER display full-page blank screens during data fetching; use content skeletons.

## 6. Code Pattern Example (Accessible Card with Theme Support)

```tsx
import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  trend: { direction: 'up' | 'down'; percentage: number };
  description: string;
}

export function MetricCard({ title, value, trend, description }: MetricCardProps) {
  const isPositive = trend.direction === 'up';

  return (
    <article className="rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 p-5 shadow-sm transition-shadow hover:shadow-md">
      <header className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-neutral-600 dark:text-neutral-400">
          {title}
        </h3>
        <span
          className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold ${
            isPositive
              ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300'
              : 'bg-rose-50 text-rose-700 dark:bg-rose-950/50 dark:text-rose-300'
          }`}
          aria-label={`Trend: ${isPositive ? 'Increased' : 'Decreased'} by ${trend.percentage}%`}
        >
          <span aria-hidden="true">{isPositive ? '↑' : '↓'}</span>
          <span>{trend.percentage}%</span>
        </span>
      </header>
      
      <div className="mt-3">
        <p className="text-3xl font-bold tracking-tight text-neutral-900 dark:text-neutral-50">
          {value}
        </p>
        <p className="mt-1 text-xs text-neutral-500 dark:text-neutral-400">
          {description}
        </p>
      </div>
    </article>
  );
}
```

## 7. Quality Checklist
- [ ] Color palettes verified with WebAIM contrast checker (all text >= 4.5:1).
- [ ] Touch targets measure >= 44x44px on all mobile viewports.
- [ ] Focus indicators visible and prominent during keyboard navigation.
- [ ] Skeletons reflect final layout dimensions to prevent Cumulative Layout Shift (CLS).
- [ ] Light and Dark mode appearances verified across all components.
