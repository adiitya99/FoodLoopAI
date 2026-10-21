# Rollback Plan

1. Stop API/UI with `Ctrl+C`.
2. Inspect `git diff` before accepting code changes.
3. Back up `foodloop.db` before schema changes.
4. Revert the smallest change that caused a regression.
5. Reinstall pinned dependencies from `requirements.txt` if environment drift is suspected.
6. Rerun relevant checks and record evidence.
7. Never delete the database or overwrite user data as a first troubleshooting step.
