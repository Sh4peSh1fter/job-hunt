# Technology Stack Proposal: [Project/Module Name or Proposal Title]

**Author(s):** [Your Name/Team]
**Date Proposed:** [Date]
**Status:** [e.g., Draft, Discussion, Approved for Implementation]

---

## 1. Purpose / Scope

*   _[Briefly describe the purpose of this document. Is it for initial tech stack definition for a new project? A proposal to add/change a specific part of the stack? What are the boundaries of this proposal/document?]_

---

## 2. Guiding Principles for this Proposal (if applicable)

*   _[If this is a proposal for a change, briefly state the main principles from `docs/rules/tech-stack.mdc` that guided these choices (e.g., improving performance, reducing costs, leveraging team skills).]_ 

---

## 3. Core Stack Overview (Proposed/Actual)

*   _[Provide a brief, high-level summary of the main architectural choices. e.g., "This project will be a Next.js application using TypeScript for the frontend and backend (API routes), with PostgreSQL as the primary database. Deployed on Vercel."]_

---

## 4. Proposed/Documented Technologies

### Frontend Technologies

-   **Technology Name:** _[e.g., Next.js]_
    -   **Current/Proposed Version(s):** _[e.g., ^14.0.0]_
    -   **Purpose/Role in Project:** _[e.g., Full-stack React framework... ]_
    -   **Rationale/Decision Date (and by whom, if proposal):** _[e.g., Chosen for its comprehensive feature set... (Decision: [Date] by [Team/Person])]_
    -   **Key Libraries/Plugins Used (if any):** _[e.g., React, Webpack (managed by Next.js)]_

-   **Technology Name:** _[e.g., React]_
    -   **Current/Proposed Version(s):** _[e.g., ^18.2.0]_
    -   **Purpose/Role in Project:** _[e.g., Core UI library...]_
    -   **Rationale/Decision Date:** _[e.g., Industry standard... (Implicit with Next.js)]_

-   **Technology Name:** _[e.g., TypeScript]_
    -   **Current/Proposed Version(s):** _[e.g., ^5.0.0]_
    -   **Purpose/Role in Project:** _[e.g., Static typing for code quality...]_
    -   **Rationale/Decision Date:** _[e.g., Enhances code reliability... (Decision: [Date])]_

-   **Technology Name:** _[e.g., Tailwind CSS]_
    -   **Current/Proposed Version(s):** _[e.g., ^3.3.0]_
    -   **Purpose/Role in Project:** _[e.g., Utility-first CSS framework...]_
    -   **Rationale/Decision Date:** _[e.g., Allows for rapid UI development... (Decision: [Date])]_

-   **Technology Name:** _[e.g., State Management Library - Zustand, Redux Toolkit, etc.]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[...]_
    -   **Rationale/Decision Date:** _[...]_

### Backend Technologies

-   **Technology Name:** _[e.g., Node.js (if using Next.js API routes or dedicated backend)]_
    -   **Current/Proposed Version(s):** _[e.g., ^18.x LTS]_
    -   **Purpose/Role in Project:** _[e.g., Runtime for Next.js backend...]_
    -   **Rationale/Decision Date:** _[e.g., Native environment for JS/TS... (Implicit with Next.js)]_

-   **Technology Name:** _[e.g., Dedicated Backend Framework - Express.js, NestJS, Python/Django, etc.]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[...]_
    -   **Rationale/Decision Date:** _[...]_

### Database

-   **Technology Name:** _[e.g., PostgreSQL, MySQL, MongoDB, Supabase, Firebase Firestore]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[e.g., Primary data storage]_
    -   **Rationale/Decision Date:** _[e.g., Chosen for its relational capabilities and scalability... (Decision: [Date])]_
    -   **Key Libraries/Plugins Used (ORM, drivers):** _[e.g., Prisma, Drizzle ORM, TypeORM, node-postgres]_

### DevOps / Infrastructure

-   **Technology Name:** _[e.g., Vercel, AWS, Azure, Google Cloud]_
    -   **Current/Proposed Version(s):** _[N/A for managed services, or specific SDK versions]_
    -   **Purpose/Role in Project:** _[e.g., Hosting, deployment, CI/CD]_
    -   **Rationale/Decision Date:** _[e.g., Optimized for Next.js, existing team expertise... (Decision: [Date])]_

-   **Technology Name:** _[e.g., Docker]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[e.g., Containerization for development/production]_
    -   **Rationale/Decision Date:** _[...]_

-   **Technology Name:** _[e.g., GitHub Actions, Jenkins, GitLab CI]_
    -   **Current/Proposed Version(s):** _[N/A or specific runner versions]_
    -   **Purpose/Role in Project:** _[e.g., CI/CD automation]_
    -   **Rationale/Decision Date:** _[...]_

### Testing

-   **Technology Name:** _[e.g., Jest, Vitest]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[e.g., Unit/Integration testing framework]_
    -   **Rationale/Decision Date:** _[...]_

-   **Technology Name:** _[e.g., React Testing Library, Vue Test Utils]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[e.g., Component testing utility]_
    -   **Rationale/Decision Date:** _[...]_

-   **Technology Name:** _[e.g., Playwright, Cypress]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[e.g., End-to-end testing]_
    -   **Rationale/Decision Date:** _[...]_

### Linters & Formatters

-   **Technology Name:** _[e.g., ESLint]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[e.g., Code linting]_
    -   **Rationale/Decision Date:** _[...]_

-   **Technology Name:** _[e.g., Prettier]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[e.g., Code formatting]_
    -   **Rationale/Decision Date:** _[...]_

### Other Key Libraries / Utilities

-   **Technology Name:** _[e.g., Axios, Zod, date-fns]_
    -   **Current/Proposed Version(s):** _[...]_
    -   **Purpose/Role in Project:** _[...]_
    -   **Rationale/Decision Date:** _[...]_

---

## 5. Dependency Versioning Strategy

*   **Proposed Default:** _[e.g., Use `^` (caret) for minor updates for most dependencies in `package.json`.]_
*   **Critical Dependencies to Pin (if any):** _[List any dependencies that should be pinned to exact versions and why.]_

---

## 6. Alternatives Considered (if proposal for change/new tech)

*   **Alternative 1:** _[Technology Name]_
    *   **Pros:** _[...]_
    *   **Cons:** _[...]_
    *   **Reason for not choosing:** _[...]_
*   **Alternative 2:** _[Technology Name]_
    *   **Pros:** _[...]_
    *   **Cons:** _[...]_
    *   **Reason for not choosing:** _[...]_

---

## 7. Risks & Mitigation (if proposal for change/new tech)

*   **Risk 1:** _[e.g., Learning curve for the team.]_ **Mitigation:** _[e.g., Allocate time for training, pair programming.]_
*   **Risk 2:** _[e.g., Integration challenges with existing system X.]_ **Mitigation:** _[e.g., Develop a PoC for integration, allocate buffer time.]_

---

## 8. Open Questions / Areas for Discussion

*   _[List any unresolved questions or points requiring team input.]_
*   **Question 1:** _[e.g., "What is the team's preference for library X vs. library Y for this specific task?"]_

---

## 9. Next Steps (if proposal)

*   _[e.g., Team discussion on [Date], PoC development, Final decision, Update `docs/tech-stack.md`.]_ 