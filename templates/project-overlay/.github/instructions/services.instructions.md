---
name: project-service-conventions
description: Apply to service, API, or backend implementation files in this repository.
applyTo: "**/src/services/**"
---

# Project Service Conventions

- Preserve public API behavior unless the task explicitly changes it.
- Validate input and error handling consistently with the existing service layer.
- Reuse existing client, logging, and configuration helpers before adding new infrastructure.
- Add or update targeted tests when changing service behavior.
