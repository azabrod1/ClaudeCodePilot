---
name: cc-build
description: Implement work with the cc-build agent using focused research and validation helpers.
agent: cc-build
argument-hint: "[task] [constraints] [files or area]"
---

Implement `${input:task,task to build}`.

Requirements:

- explore the current implementation before editing
- delegate only isolated research or validation subtasks
- keep the main synthesis and final decisions in the primary thread
- make the smallest coherent change that solves the request
- run targeted validation and report what was verified versus not verified
