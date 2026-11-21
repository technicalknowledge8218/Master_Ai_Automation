---
name: frontend-engineering
description: >-
  Builds accessible, high-performance, and responsive frontend applications using modern React,
  TypeScript strict mode, token-driven Tailwind CSS, and robust state management. Use when creating UI
  components, wiring forms with validation, optimizing client performance, or implementing WCAG 2.2 AAA accessibility.
---

# Frontend Engineering Skill

> **Status**: APPROVED (Workspace-Local)  
> **Version**: 1.0.0  
> **Domain**: DOM-07 (Software Development), DOM-08 (Frontend Engineering)  
> **Reference Standard**: [frontend_engineering.md](../../05_DEVELOPMENT/standards/frontend_engineering.md)

---

## 1. Purpose & Scope
This skill guides the construction of enterprise-grade, accessible, and type-safe frontend web applications. It governs component hierarchy, state segregation (server vs global vs local vs URL), form validation pipelines, accessibility invariants, and rendering performance.

## 2. When to Use This Skill
- Creating or refactoring React components and user interfaces.
- Setting up TypeScript strict configuration for frontend projects.
- Integrating design tokens from `06_UI_UX_DESIGN/tokens/DESIGN_TOKENS.json`.
- Implementing complex forms using React Hook Form and Zod schemas.
- Diagnosing and resolving Core Web Vitals (LCP, INP, CLS) or layout shifts.
- Auditing and remediating WCAG 2.2 accessibility violations.

## 3. Required Inputs
- Component or screen requirements (wireframes, specifications, or user stories).
- Data models and API contracts (OpenAPI schema or TypeScript interfaces).
- Target viewport requirements (desktop, tablet, mobile webview).

## 4. Execution Workflow

### Step 1: Component & State Architecture
1. Decompose UI into Presentational (stateless) and Container (stateful) components.
2. Segregate state into four distinct layers:
   - **Server State**: Managed via TanStack Query (cached, deduped, stale-while-revalidate).
   - **URL State**: Route params and query strings for shareable filters and pagination.
   - **Global State**: Minimal client-only session data via Zustand.
   - **Local State**: Component-level ephemeral UI state via `useState` / `useReducer`.

### Step 2: Implementation & Styling
1. Apply TypeScript strict mode: zero `any`, discriminated unions for asynchronous states.
2. Utilize Tailwind CSS utility classes aligned with design tokens (`space-4`, `text-sm`, `bg-surface-primary`).
3. Enforce mobile-first responsive design (`w-full md:w-1/2 lg:w-1/3`).

### Step 3: Accessibility & Form Hardening
1. Link all inputs to persistent labels (`htmlFor`) and helper/error IDs (`aria-describedby`).
2. Ensure interactive elements meet the 44x44px minimum touch target size.
3. Verify visible focus rings (`focus-visible:ring-2 focus-visible:ring-offset-2`).
4. Validate forms using Zod schemas with instant client feedback and server error mapping.

### Step 4: Verification & Performance Audit
1. Verify keyboard navigation: All interactive flows must be operable via Tab/Enter/Space/Escape.
2. Ensure color contrast ratios meet or exceed 4.5:1 for normal text and 3:1 for graphical UI.
3. Test under simulated mobile network throttling to confirm zero CLS and smooth rendering.

## 5. Strict Rules & Constraints
- NEVER use TypeScript `any` or non-null assertion `!` in production components.
- NEVER use inline style objects for dynamic theming; use CSS custom properties or token classes.
- NEVER suppress accessibility warnings or remove outline focus rings without providing custom rings.
- NEVER fetch data directly inside raw `useEffect` hooks without abort controllers or query libraries.

## 6. Code Pattern Example

```tsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import clsx from 'clsx';

const ProfileSchema = z.object({
  displayName: z.string().min(2, "Name must be at least 2 characters").max(50),
  email: z.string().email("Invalid email address"),
});

type ProfileInput = z.infer<typeof ProfileSchema>;

export function ProfileForm({ onSubmit }: { onSubmit: (data: ProfileInput) => Promise<void> }) {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<ProfileInput>({
    resolver: zodResolver(ProfileSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 max-w-md w-full" noValidate>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="displayName" className="text-sm font-medium text-neutral-800 dark:text-neutral-200">
          Display Name
        </label>
        <input
          id="displayName"
          type="text"
          {...register('displayName')}
          aria-invalid={Boolean(errors.displayName)}
          aria-describedby={errors.displayName ? "displayName-error" : undefined}
          className={clsx(
            "h-11 px-3.5 rounded-lg border text-sm transition-colors",
            "focus:outline-none focus:ring-2 focus:ring-primary-500/20",
            errors.displayName ? "border-red-500" : "border-neutral-300 dark:border-neutral-700"
          )}
        />
        {errors.displayName && (
          <p id="displayName-error" role="alert" className="text-xs text-red-600 dark:text-red-400">
            {errors.displayName.message}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="h-11 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg disabled:opacity-50"
      >
        {isSubmitting ? "Saving..." : "Update Profile"}
      </button>
    </form>
  );
}
```

## 7. Quality Checklist
- [ ] TypeScript compiles cleanly with zero diagnostics under `tsc --noEmit`.
- [ ] All inputs have explicit `<label>` tags with matching `htmlFor` attributes.
- [ ] Contrast ratios audited and confirmed >= 4.5:1.
- [ ] Interactive touch targets measure at least 44x44px.
- [ ] No unhandled Promise rejections or layout shifts (CLS < 0.1).
