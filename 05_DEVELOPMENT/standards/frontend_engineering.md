# MASTER-AI Full-Stack Standards: Frontend Engineering

> **Domain**: `05_DEVELOPMENT/standards/`  
> **Status**: APPROVED & ACTIVE (Phase 5)  
> **Primary Framework**: React 19 + TypeScript Strict  

---

## 1. Modern Frontend Architecture

MASTER-AI web applications follow a modular, component-driven architecture built with **React 19**, **TypeScript (Strict Mode)**, and **Tailwind CSS**.

### Directory Structure Standard:
```text
src/
├── app/              # Application entry, providers, global layout, routing
├── components/       # Reusable design system primitives (Button, Input, Card)
├── features/         # Domain-specific feature slices (auth, billing, dashboard)
│   └── [feature]/
│       ├── api/          # Query/mutation hooks (TanStack Query / fetch wrappers)
│       ├── components/   # Feature-specific components
│       ├── types/        # TypeScript interfaces and Zod schemas
│       └── utils/        # Feature-specific helper functions
├── hooks/            # Global reusable React hooks
├── lib/              # Client instances (API client, analytics, storage)
├── stores/           # Global state slices (Zustand)
└── types/            # Ambient and shared TypeScript definitions
```

---

## 2. Component Design & State Management

### Component Invariants:
1. **Single Responsibility**: Components must do one thing well. Separate container/data-fetching components from pure visual presentational components.
2. **Prop Interface Contracts**: Every component must declare explicit, strongly-typed TypeScript props. Never pass untyped `any` props.
3. **Composition Over Inheritance**: Utilize slots, render props, and `children` composition rather than rigid configuration prop trees.

### State Management Hierarchy:
- **Server State**: Managed via **TanStack Query** (React Query) or SWR for caching, background revalidation, and optimistic updates.
- **Global Client State**: Managed via **Zustand** for lightweight, decoupled state outside the React render tree. Avoid excessive React Context providers which trigger widespread re-renders.
- **Local UI State**: Managed via `useState` / `useReducer` for ephemeral component-local state (e.g., dropdown open/closed, active tab).
- **URL State**: Query parameters (`useSearchParams`) must be the source of truth for shareable filters, sorting, search queries, and pagination.

---

## 3. Forms & Runtime Schema Validation

All forms must combine **React Hook Form** with **Zod** for schema validation:
- **Client-Side Validation**: Validate on blur or change to provide instant user feedback.
- **Server-Side Reuse**: Share the exact same Zod schema across frontend forms and backend API route validators to eliminate validation drift.
- **Zero Raw Form State**: Avoid manual `onChange` handlers with uncontrolled inputs; rely on `register` and standard form state.

---

## 4. Accessibility (A11y) & WCAG 2.2 Standards

All web and mobile interfaces must meet **WCAG 2.2 AA (Targeting AAA)** compliance:
1. **Semantic HTML**: Use native semantic elements (`<nav>`, `<main>`, `<article>`, `<button>`, `<header>`) rather than `div` tags with click handlers.
2. **Keyboard Navigation**: All interactive elements must be focusable via `Tab`, visually indicate focus with a high-contrast focus ring, and respond to `Enter` and `Space`. Modals and drawers must trap focus and close on `Escape`.
3. **ARIA Attributes**: Use ARIA attributes (`aria-label`, `aria-expanded`, `aria-live`, `aria-describedby`) only when native HTML semantics are insufficient.
4. **Color Contrast**: Enforce a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text against background colors in both light and dark themes.

---

## 5. Performance Optimization & Responsive Design

1. **Code Splitting**: Route-level code splitting via `React.lazy()` and dynamic `import()` to ensure initial bundle size stays under 150 KB gzipped.
2. **Asset Optimization**: Serve modern image formats (WebP/AVIF) with explicit `width`, `height`, and `loading="lazy"`.
3. **List Virtualization**: Render long lists (> 100 items) using virtualization libraries (`@tanstack/react-virtual`).
4. **Mobile-First Layouts**: Design for the smallest screen viewport first (320px–375px) and scale up using standard responsive breakpoints (`sm: 640px`, `md: 768px`, `lg: 1024px`, `xl: 1280px`).
5. **Error Boundaries**: Wrap major routes and independent widgets in React Error Boundaries to prevent full-screen crashes from isolated component errors.
