# TypeScript & Python Quality Rules Reference

> **Reference**: `02_SKILLS/coding-standards/references/`  

---

## 1. TypeScript Rules
1. **Strict Types**: Always enable `"strict": true` in `tsconfig.json`. The use of `any` is strictly prohibited; use `unknown` with type guards instead.
2. **Explicit Return Types**: All exported functions must declare an explicit return type.
3. **Immutability First**: Prefer `readonly` arrays and properties where state should not mutate.
4. **Zod Validation**: Validate all incoming external request payloads with Zod schemas before passing them to domain logic.

## 2. Python Rules
1. **Type Hints**: Annotate all function parameters and return types using `typing` (`Optional`, `Union`, `List`, `Dict`, `Callable`).
2. **Explicit Exceptions**: Never use bare `except:`. Always catch specific exceptions (`except FileNotFoundError:`, `except ValueError:`) and log the full traceback.
3. **Ruff / Black Compliance**: Code must be formatted with Black and linted with Ruff. Line length max 100 characters.
4. **Context Managers**: Always use `with` blocks when handling files, sockets, and database connections.
