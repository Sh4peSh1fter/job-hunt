# Folder Structure Proposal: [Project/Module Name]

**Author(s):** [Your Name/Team]
**Date Proposed:** [Date]
**Status:** [e.g., Draft, Discussion, Approved for Implementation]

---

## 1. Purpose / Scope

*   _[Briefly describe what this folder structure is for. Is it for a new project, a new major feature module, a refactor of an existing section, etc.? What are the boundaries of this proposal?]_

---

## 2. Guiding Principles / Rationale

*   _[Explain the main reasons for choosing this particular structure. Refer to the general principles in `docs/rules/folder-structure.mdc` (e.g., Clarity, Scalability, Separation of Concerns, Cohesion) and explain how this proposal aligns with them.]_
*   **Key Goals:**
    *   _[Goal 1 for this structure, e.g., "Improve developer onboarding for the payments module."]_
    *   _[Goal 2, e.g., "Isolate payment provider integrations for easier swapping."]_
*   **Decisions Made (and why):**
    *   _[e.g., "Chose feature-based organization for `src/payments/` because each payment method has distinct UI, logic, and API interactions."]_
    *   _[e.g., "Co-locating tests within feature folders (`__tests__/`) to keep them close to the code they test."]_

---

## 3. Proposed Folder Structure

_[Use a tree-like format to illustrate the proposed structure. Include brief comments for clarity where needed.]_

```plaintext
[root_directory_for_this_proposal]/
├── main-folder-1/                  # Purpose of main-folder-1
│   ├── sub-folder-a/             # Purpose of sub-folder-a
│   │   └── file-1.ts             # Description of file-1
│   └── sub-folder-b/
│       └── component-x.tsx
├── main-folder-2/                  # Purpose of main-folder-2
│   ├── sub-folder-c/
│   │   └── utility-script.js
│   └── index.ts                    # Entry point or main export for main-folder-2
├── configuration-file.json
└── README.md                       # Specific README for this module/section (if applicable)
```

---

## 4. Key Directory Explanations

_[For each significant new or modified top-level folder in your proposal, provide a brief explanation of its purpose and what it will contain.]_

*   **`[folder_name_1]/`**: _[Explanation]_
*   **`[folder_name_2]/components/`**: _[Explanation]_
*   **`[folder_name_2]/hooks/`**: _[Explanation]_

---

## 5. Naming Conventions (if specific to this proposal)

_[Outline any specific naming conventions for files or folders within this proposed structure if they deviate from or add detail to the project-wide conventions (defined in `docs/rules/folder-structure.mdc` and `docs/folder-structure.md`).]_

*   **Folders:** _[e.g., `kebab-case`, `PascalCase` for specific types of folders]_
*   **Files:**
    *   **Components:** _[e.g., `ComponentName.tsx`]_
    *   **Services:** _[e.g., `serviceName.service.ts`]_
    *   **Types:** _[e.g., `entityName.types.ts`]_

---

## 6. Impact on Existing Structure (if applicable)

*   _[If this proposal modifies an existing structure, describe which parts of the current project folder structure (see `docs/folder-structure.md`) will be affected, renamed, moved, or deleted.]_
*   _[Outline any migration steps needed.]_

---

## 7. Open Questions / Areas for Discussion

*   _[List any unresolved questions, alternative considerations, or points that require team discussion before finalizing this structure.]_
*   **Question 1:** _[e.g., "Should utility functions specific to `main-folder-1` be in `main-folder-1/utils/` or a global `src/lib/`?"]_
*   **Question 2:** _[e.g., "What is the preferred naming for X type of file within this module?"]_

---

## 8. Next Steps

*   _[e.g., Discuss with team, Get approval, Implement structure, Update `docs/folder-structure.md`.]_ 