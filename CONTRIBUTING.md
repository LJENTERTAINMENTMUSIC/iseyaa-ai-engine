# 🛠️ ISEYAA TiarionX — Contributing Guide (20-Person Team)

To maintain a high-quality "State Operating System," all 20+ developers must adhere to these standards.

---

## 🏗️ Git Workflow & Branching
- **Branch Strategy:** GitFlow.
- **Main:** Production-ready code only.
- **Develop:** The primary integration branch.
- **Features:** `feature/squad-name/description` (e.g., `feature/alpha/lga-intelligence`).
- **PR Rules:** 
  - At least 1 approval from a different squad.
  - All CI/CD checks (Lint, Build, Test) must pass.

---

## 🎨 Coding Standards
- **JavaScript/TypeScript:** ESLint (Next-Gen) + Prettier.
- **Python:** Black (formatting) + Flake8 (linting) + Pyright (strict types).
- **Naming:** 
  - Components: PascalCase (`LgaCard.tsx`).
  - Functions: camelCase (`fetchLgaHistory`).
  - Folders: kebab-case (`ui-kit`).

---

## 🧩 Squad Boundaries
- **Ownership:** If you change a file in a different squad's domain (e.g., Squad Beta editing `apps/api`), you **must** tag a member from that squad for review.
- **Shared Packages:** Any changes to `packages/*` require a "Global Architect" review (Lead PM).

---

## 📑 Pull Request (PR) Template
All PRs must include:
1. **Description:** What does this change solve?
2. **Squad:** Which squad owns this feature?
3. **Tests:** How did you verify the fix?
4. **Impact:** Does this change the database schema or AI prompt?

---

## 📦 Dependency Management
- **Tool:** Use `pnpm`.
- **Global Installs:** Avoid `npm install -g`.
- **Workspace:** Install specific deps for your app (`pnpm add axios --filter web`).

**Failure to follow these rules will result in a rejected PR. We are building the future of Ogun State—quality is non-negotiable.**
