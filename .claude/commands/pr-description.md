---
description: Generate a comprehensive PR description based on git diff and commit history
---

Analyze the current branch and generate a comprehensive pull request description.

Follow these steps:

1. Run `git diff main...HEAD` to see all changes in this branch
2. Run `git log main..HEAD --oneline` to see the commit history
3. Run `git status` to check the current branch name

Based on the analysis, generate a PR description with the following structure:

## Description
- Provide 2-4 concise bullet points summarizing the key changes
- Focus on WHAT changed and WHY (not just the technical details)

## Changes
- List the main changes organized by category (e.g., New Features, Bug Fixes, Refactoring, Tests, Documentation)
- Be specific but concise

## Testing
- Describe what testing was done or what tests were added

## Verification steps
- Run the tests using `poetry run pytest <test_file_path>`

Format the output in a markdown code block (triple backticks) so it can be directly copied into a GitHub PR description with all formatting preserved.
All file names, function names, method names, class names, and code elements should be wrapped in backticks for proper code formatting.

IMPORTANT: Wrap the entire PR description in a markdown code block like this:
```markdown
## Description
...
```

This ensures that when the user copies the text, all backticks are preserved.