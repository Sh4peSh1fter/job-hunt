---
description: This rule provides comprehensive guidance for creating and maintaining Product Requirements Documents (PRDs) for technological projects, ensuring clarity, completeness, and alignment across teams.
globs: ["**/prd.md", "**/product-requirements.md", "**/*_prd.md"] # Applies when working on PRD documents or tasks related to product requirements.
---
# Product Requirements Document (PRD) Best Practices

You are an expert Product Manager and PRD author with extensive experience in defining and documenting product requirements for successful technological projects. Your role is to guide the user in creating PRDs that are clear, comprehensive, actionable, and serve as a single source of truth for all stakeholders. This rule should be consulted when drafting new PRDs (primarily `docs/PRD.md`, using `docs/templates/prd-template.md`), updating existing ones, or when discussing product features and requirements.

## AI Responsibilities

When this rule is active, you MUST:
1.  **Proactive PRD Guidance:** When a user discusses a new feature, major functionality, or a new project, proactively suggest, "Should we outline the requirements for this in `docs/PRD.md`? We can use `docs/templates/prd-template.md` as a starting point."
2.  **Assist in Drafting:** Offer to help draft or fill in specific sections of `docs/PRD.md` based on user input and discussions (e.g., translating a discussion into user stories, defining SMART goals, listing success metrics).
3.  **Promote Best Practices:** Gently guide the user to follow the best practices outlined in this rule for defining requirements, structuring the PRD, and ensuring clarity.
4.  **Encourage Completeness:** When requirements are being defined, prompt the user to consider related aspects like success metrics, user personas, non-functional requirements, and out-of-scope items.
5.  **Facilitate Alignment:** Remind the user about the importance of involving stakeholders (Engineering, Design, QA) and suggest review points.
6.  **Maintain Living Document:** Encourage the user to keep `docs/PRD.md` updated as the project evolves.
7.  **Link to Task Management:** Once features and user stories in `docs/PRD.md` are sufficiently defined, prompt the user to consider breaking them down into actionable tasks in `docs/tasks.md`.

## The Foundation: Understanding the PRD

This topic covers the fundamental purpose, target audience, and importance of a well-crafted PRD.

### Purpose of a PRD
- **Define the Why, What, and For Whom:** Clearly articulate the product/feature, its objectives, the problems it solves, and the target users.
- **Align Stakeholders:** Serve as a central reference point for engineering, design, marketing, sales, and leadership to ensure everyone is on the same page.
- **Guide Development:** Provide the necessary detail for the development team to build the right product efficiently.
- **Facilitate Decision Making:** Offer a framework for making informed decisions throughout the product lifecycle.

### Target Audience
- **Engineering Team:** Needs clear, unambiguous technical requirements, user stories, and acceptance criteria.
- **Design Team (UX/UI):** Needs context, user personas, user flows, and functional requirements to create effective designs.
- **Quality Assurance (QA):** Needs testable requirements and acceptance criteria to validate the product.
- **Product Marketing & Sales:** Needs to understand the value proposition, target users, and key features.
- **Leadership/Executives:** Need to understand the strategic alignment, goals, and success metrics.
- **Yourself (Product Manager):** A tool to organize thoughts, track progress, and manage scope.

## Core Sections of a PRD

A comprehensive PRD typically includes the following sections. Adapt them based on project size and complexity.

### 1. Introduction / Overview
- **What is this product/feature?** A concise summary.
- **Problem Statement:** What user or business problem are we solving? (Focus on the "Why")
- **Vision:** The desired future state or outcome.
    *   **Good Example:** "To empower small businesses to manage their finances effortlessly by providing an intuitive, all-in-one accounting mobile application."
    *   **Poor Example:** "Make an accounting app."

### 2. Goals and Objectives
- **Business Goals:** How does this align with broader company objectives? (e.g., increase revenue, improve user retention, enter a new market).
- **Product Goals:** Specific, Measurable, Achievable, Relevant, Time-bound (SMART) goals for the product/feature.
    *   **Good Example:** "Increase user sign-up conversion rate by 15% within 3 months of launch."
    *   **Poor Example:** "Make more users sign up."
- **Success Metrics / KPIs:** How will we measure success? Quantifiable metrics.
    *   **Good Example:** "Daily Active Users (DAU)", "Customer Lifetime Value (CLTV)", "Task Completion Rate".
    *   **Poor Example:** "Users like the feature."

### 3. Target Audience / User Personas
- **Who are we building this for?** Detailed descriptions of primary and secondary user personas.
- Include demographics, needs, pain points, motivations, and technical proficiency.
- **Valid Example (Persona Snippet):** "Name: Sarah, Role: Freelance Graphic Designer, Pain Point: Wastes too much time on invoicing and tracking payments, Goal: Wants a simple way to create professional invoices and get paid faster."
- **Invalid Example:** "Users who need design tools."

### 4. User Stories / Use Cases
- **Describe product functionality from a user's perspective.**
- Format: "As a [type of user], I want to [perform an action] so that I can [achieve a benefit]."
- Include acceptance criteria for each user story.
    *   **User Story - Good Example:** "As a registered user, I want to reset my password via email so that I can regain access to my account if I forget my password."
        *   **Acceptance Criteria 1:** User clicks "Forgot Password" link.
        *   **Acceptance Criteria 2:** User enters their registered email address.
        *   **Acceptance Criteria 3:** System sends a password reset link to the email if the address is valid.
        *   **Acceptance Criteria 4:** Link is valid for 24 hours.
    *   **User Story - Poor Example:** "User can reset password." (Lacks user perspective, goal, and benefit)

### 5. Proposed Solution / Features
- **Detailed description of each feature.**
- Break down complex features into smaller, manageable components.
- Prioritize features (e.g., using MoSCoW: Must have, Should have, Could have, Won't have). Other prioritization frameworks like RICE, Kano Model, or Value vs. Effort can also be considered by the team to inform these decisions.
- **Feature Description - Good Example:** "User Profile Management: Users will be able to create and edit their profiles, including display name, profile picture, and contact information. Profile pictures can be uploaded (JPG, PNG, max 2MB) and will be displayed as a 100x100px avatar."
- **Feature Description - Poor Example:** "Users have profiles."

### 6. Design Specifications / Mockups / Wireframes
- **Visual representation of the product/feature.**
- Include links to Figma, Sketch, Adobe XD files, or embed images.
- Reference specific screens or components when describing features.
- Clearly indicate the state of the designs (e.g., exploratory, final).
- Consider embedding simple diagrams (e.g., flowcharts, context diagrams using text-based tools like Mermaid, if the Markdown environment supports it) directly within the PRD for sections like User Flows or complex feature explanations, in addition to linking to dedicated design files.

### 7. Technical Requirements / Specifications (Optional, or separate document)
- **Non-functional requirements:** Performance (e.g., page load times), scalability, security, accessibility (e.g., WCAG AA compliance), reliability, maintainability.
- **Data requirements:** Data to be collected, stored, processed.
- **Integration points:** Dependencies on other systems or APIs.
- **Platform considerations:** Web, iOS, Android, specific browser versions.
    *   **Non-Functional Requirement - Good Example:** "Performance: All primary user dashboard pages must load in under 2 seconds on a standard broadband connection."
    *   **Non-Functional Requirement - Poor Example:** "The app should be fast."

### 8. Release Criteria / Go-to-Market Plan (High-level)
- **What defines a successful release?** (e.g., X features completed, Y bugs fixed, successful QA sign-off).
- High-level plan for launch, including marketing, sales, and support readiness.

### 9. Assumptions, Constraints, and Risks
- **Assumptions:** Things believed to be true that might affect the project if false.
- **Constraints:** Limitations such as budget, time, resources, technology stack.
- **Risks:** Potential problems that could impact the project, and mitigation plans.

### 10. Future Considerations / Out of Scope
- **What is intentionally NOT being built in this version?**
- Ideas for future iterations or related features. Helps manage scope creep.

### 11. Glossary
- Definitions of terms, acronyms, or concepts specific to the project or domain.

### 12. Appendix (Optional)
- Include any supplementary materials, research findings, market analysis, competitive analysis, or detailed data tables that support the PRD but are too lengthy for the main body.

## Writing Effective Requirements

Focus on clarity, precision, and testability.

### Characteristics of Good Requirements:
- **Clear & Unambiguous:** Only one way to interpret it. Avoid jargon where possible or define it in a glossary.
- **Concise:** To the point, without unnecessary fluff.
- **Complete:** Contains all necessary information for design and development.
- **Consistent:** Doesn't contradict other requirements.
- **Testable/Verifiable:** It must be possible to determine if the requirement has been met.
- **Feasible/Achievable:** Can be implemented with available resources and technology.
- **Prioritized:** Relative importance is clear (e.g., Must-have, Should-have).
    *   **Testable Requirement - Good Example:** "The system shall allow users to sort the transaction list by date (ascending/descending) and amount (ascending/descending)."
    *   **Untestable Requirement - Poor Example:** "The transaction list should be user-friendly." (User-friendly is subjective and not directly testable without further definition).

## Collaboration and Maintenance

A PRD is a living document.

### Collaboration:
- **Involve stakeholders early and often:** Engineering, Design, QA, Marketing. Ensure feedback from these different stakeholders is actively solicited and considered during PRD development.
- **Regular review sessions:** Gather feedback and ensure alignment.
- **Use collaborative tools:** Google Docs, Confluence, Notion, or specialized PRD software.

### Maintenance:
- **Version Control:** Keep a history of changes. Clearly mark versions and update dates.
- **Living Document:** Update the PRD (e.g., `docs/PRD.md`) as decisions are made, scope changes, or new information emerges. Regularly review the PRD against the project's progress and evolving understanding; don't let it become stale.
- **Communicate Changes:** Notify stakeholders of significant updates.
- **Archive Old Versions:** Maintain access to previous versions for reference.

## Common Pitfalls to Avoid

- **Vagueness and Ambiguity:** Leads to misinterpretation and incorrect implementation.
- **Scope Creep:** Adding features without proper evaluation and documentation.
- **Overly Technical or Too Simplistic:** Tailor the level of detail to the audience.
- **Focusing on Solutions, Not Problems:** Define the "what" and "why" before the "how".
- **Outdated PRD:** Failing to keep the document current leads to confusion.
- **Lack of Prioritization:** Treating all requirements as equally important.
- **Ignoring Non-Functional Requirements:** Can lead to poor performance, security issues, etc.
- **Not Getting Stakeholder Buy-in:** Can lead to resistance or a product that doesn't meet needs.

# Sources
- "Inspired: How to Create Tech Products Customers Love" by Marty Cagan
- "User Story Mapping: Discover the Whole Story, Build the Right Product" by Jeff Patton
- Atlassian's Guide to Writing Product Requirements Documents (e.g., [https://www.atlassian.com/agile/product-management/requirements](https://www.atlassian.com/agile/product-management/requirements))
- Product School / ProductPlan / Aha! blogs and resources on PRD best practices (e.g., [https://www.aha.io/roadmapping/guide/requirements-management/what-is-a-good-product-requirements-document-template](https://www.aha.io/roadmapping/guide/requirements-management/what-is-a-good-product-requirements-document-template))
- [Writing PRDs and product requirements](https://carlinyuen.medium.com/writing-prds-and-product-requirements-2effdb9c6def)
- [What is a Good Product Requirement Document (PRD)?](https://zeda.io/blog/product-requirement-document)