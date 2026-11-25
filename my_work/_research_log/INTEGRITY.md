# Integrity report

Generated 2026-11-25 from the files in `my_work/_research_log/`. This report states the gaps it can see. It does not say the log is complete.

Week numbers: WK-01 is Monday 24 August 2026 through Sunday 30 August 2026. Later weeks are the next Monday–Sunday blocks. The first session file is 26 August, inside WK-01.

## Counts

- Session files: 27
- Exchange records: 170
- Decision files: 23 (DEC-001–DEC-023)
- Correction records: 5
- Records with `reconstructed: true`, or the `reconstructed` flag: 0
- none found

## Exchanges with no disposition

15 of 170 exchanges (9%). The spec asks for a flag above 20%. This rate is under that line.

The missing turns are listed in the weekly files. Several are the last turn of a session, which cannot have a disposition until a later turn. They stay pending. Silence is not treated as acceptance.

## Decision turns

No decision file points at a turn number that is absent from every session file.

These decision files do not name a session, and the same turn number exists in more than one session whose times overlap the decision. The link is not unique:

- DEC-001 turn 12 → 2026-11-15_1639, 2026-11-15_1848
- DEC-002 turn 14 → 2026-11-15_1639, 2026-11-15_1848
- DEC-003 turn 2 → 2026-11-17_0045, 2026-11-17_1348, 2026-11-17_1500, 2026-11-17_1545, 2026-11-17_1631
- DEC-004 turn 11 → 2026-11-15_1639, 2026-11-15_1848
- DEC-005 turn 13 → 2026-11-15_1639, 2026-11-15_1848
- DEC-011 turn 2 → 2026-11-17_1348, 2026-11-17_1500, 2026-11-17_1545, 2026-11-17_1631
- DEC-012 turn 3 → 2026-11-17_1348, 2026-11-17_1500, 2026-11-17_1545, 2026-11-17_1631
- DEC-013 turn 1 → 2026-11-17_1500, 2026-11-17_1631, 2026-11-17_2030
- DEC-018 turn 2 → 2026-11-17_1500, 2026-11-17_2030, 2026-11-18_0017
- DEC-021 turn 1 → 2026-11-17_1500, 2026-11-18_0928

## Gaps of more than seven days

No session file exists for:

- WK-02 2026-08-31 – 2026-09-06
- WK-03 2026-09-07 – 2026-09-13
- WK-04 2026-09-14 – 2026-09-20
- WK-05 2026-09-21 – 2026-09-27
- WK-06 2026-09-28 – 2026-10-04
- WK-09 2026-10-19 – 2026-10-25
- WK-10 2026-10-26 – 2026-11-01
- WK-11 2026-11-02 – 2026-11-08

Two of those gaps contain a commit and no session file:

- `a822f9c` 2026-09-14 Session 4: Nake Nr. 6 design system. No `[log:…]` tag. WK-04 has no session file.
- `2e02904` 2026-10-20 Record idea evaluation, venues, readings, and 3D object work. No `[log:…]` tag. WK-09 has no session file.

WK-02 through WK-06 is 31 August–4 October. WK-09 through WK-11 is 19 October–8 November.

## Sessions and commits

Counted on the student's own commits. A session is tagged only when one of those commit messages contains `[log:<that session>]`. Commits that update the shared course files are not student sessions.

Tagged:

- 2026-08-26_1255: c35d75d (committed 2026-09-02, after the session week)
- 2026-11-10_1326: edcf25c
- 2026-11-11_0018: eb5ae5f, 2a3fe75, 032f420, f345e6d
- 2026-11-25_0024: db05a00, 21b37e3, 8d0aac1
- 2026-11-25_1037: b87e7c4, ae84217

Session files with no commit tagged for that session (22):

- 2026-10-07_1222
- 2026-10-11_2303
- 2026-10-13_0212
- 2026-10-13_2200
- 2026-11-15_1639
- 2026-11-15_1848
- 2026-11-16_0014
- 2026-11-16_1322
- 2026-11-16_1333
- 2026-11-17_0045
- 2026-11-17_1348
- 2026-11-17_1500
- 2026-11-17_1545
- 2026-11-17_1631
- 2026-11-17_2030
- 2026-11-18_0017
- 2026-11-18_0928
- 2026-11-18_2042
- 2026-11-21_1507
- 2026-11-22_2224
- 2026-11-23_1834
- 2026-11-24_1400

The commit that adds these files uses `[log:2026-11-25_1037]`. That tag does not rewrite the earlier sessions. The mismatch stays visible.

Student commits with no session tag:

- `a822f9c` 2026-09-14 Session 4: Nake Nr. 6 design system, declarations scaffold, artist talk.
- `2e02904` 2026-10-20 Record idea evaluation, venues, readings, and 3D object work.

Three further student commits are merges of the course remote (`c2c71bf`, `5903169`, `a2481d0`). They are not session logs.

## Moves outside the spec list

advise 1

## Weekly summaries

Written for weeks that have session files: WK-01, WK-07, WK-08, WK-12, WK-13, WK-14.

Not written for the empty weeks above. An empty summary would invent a week of work.

Every summary leaves both review boxes unticked. The student has not signed them.
