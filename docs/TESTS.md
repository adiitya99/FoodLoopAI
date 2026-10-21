# Test Checklist

Mark only after executing and recording the actual result.

- [ ] Install dependencies from `requirements.txt`.
- [ ] Start API and confirm `GET /`, `/health`, `/docs`.
- [ ] Valid donation is saved.
- [ ] Zero/negative quantity is rejected.
- [ ] Deadline at/before preparation time is rejected.
- [ ] Donation starts in `pending_review` with review flag enabled.
- [ ] Valid recipient can be registered.
- [ ] Category mismatch is excluded.
- [ ] Capacity below donation quantity is excluded.
- [ ] Match response requires human review.
- [ ] Agent run stores action, rationale and tool log.
- [ ] Streamlit can create donations, register recipients, run matching and show logs.

Evidence: record date, command and observed result in `HANDOVER.md`. Do not claim unchecked tests passed.
