# CyberArk Defender (PAM-DEF) — Practice Question Bank

**277 practice questions** for the CyberArk Defender – PAM certification, each with the
correct answer, why it is correct, and why the other options are not.

Written from the official Defender-PAM Study Guide objectives and checked against
current CyberArk (Idira) documentation in August 2026. **Not copied from exam dumps** —
where third-party sample questions were consulted, they were used only to find topic
gaps, and every answer here was reasoned from official documentation. That matters:
several widely circulated answer keys turn out to be wrong, and the ones we found are
[documented below](#where-circulating-answer-keys-are-wrong).

## Try it

Open `index.html` in a browser — it is a single self-contained file, no build step, no
server, no dependencies.

Two modes:

- **Practice** — instant feedback and the full explanation after every answer.
- **Exam simulation** — 60 random questions, 90-minute timer, feedback withheld until
  you finish. Matches the real exam format.

Progress is kept in browser storage, so you can close the tab and pick up where you left
off. Filter by domain, drill only the questions you missed, and see a per-domain score
breakdown at the end.

## Coverage

Weighted the way the official objectives are, so the practice reflects the exam.

| # | Domain | Questions |
|---|---|---|
| 1 | Onboard Accounts | 38 |
| 2 | Manage the Application | 33 |
| 3 | Perform Ongoing Maintenance and Troubleshooting | 36 |
| 4 | Configure and Manage Passwords | 61 |
| 5 | Manage Security and Audit Functions | 35 |
| 6 | Configure Session Management | 44 |
| 7 | Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP) | 30 |
| | **Total** | **277** |

Beyond the core domains the bank also covers Vault security and hierarchical encryption,
PTA detections and automatic responses, backup / DR / HA, Distributed and Cluster Vaults,
integrations (LDAP, LDAPS, RADIUS, SAML, SMTP/ENE, SNMP, syslog, NTP), and Privilege
Cloud with SIA and Zero Standing Privileges.

## Repository layout

```
index.html                  the quiz — open this
questions.json              all 277 questions as data
docs/practice-questions.md  the same bank as a readable document
build/part*.json            question sources, split by batch
build/template.html         page template ( __DATA__ is replaced at build time )
build/build.py              regenerates questions.json and index.html
```

To change a question, edit the relevant `build/part*.json` and run:

```bash
python3 build/build.py
```

The build validates as it goes: contiguous ids, 2–4 options per question, answer indices
in range, every explanation present, and multi-answer questions actually saying
"Choose N" in the stem.

## Verification status

Honest accounting of how far each range has been checked:

| Questions | Status |
|---|---|
| 1–125, 193–200 | Adversarially re-checked against docs.cyberark.com; 44 corrections applied |
| 126–192 | Written from a verified knowledge base; the final documentation pass was cut short — confirm parameter defaults in your own lab |
| 201–277 | Answers reasoned from official documentation, not yet through a full adversarial pass |

CyberArk documentation changes. Treat parameter defaults as a starting point for your own
lab rather than as settled fact, and verify anything you intend to memorise.

## Where current docs contradict the v12.6 course material

The widely used v12.6 (2023) course material predates a lot. Know both — if an exam
question clearly wants the older answer, give the older answer — but understand why it
changed:

- **Blueprint** — the five-stage model was replaced by a risk-versus-effort prioritisation
  index, and the first guiding principle was reworded from *prevent credential theft* to
  *prevent identity compromise*. Tier 0/1/2 belongs to the PAM Implementation Program
  Phase 1, not the Blueprint, and there is no Tier 3.
- **Onboarding rule precedence** — the newest rule gets precedence 1 and the first match
  wins. Current docs also state dependencies are onboarded *with* the account.
- **Safe renaming** — Safes *can* be renamed by a user with Add Safes. What cannot change
  after creation is the Encryption tab configuration, and OLAC once enabled.
- **LDAP administration** — gated by *Manage Directory Mapping* plus Audit Users and Vault
  Admins membership, not restricted to the built-in Administrator user.
- **xRay** — current docs say the package comes from your CyberArk representative; older
  material says the Marketplace.
- **Verification parameters** carry a `VF` prefix (`VFPerformPeriodicVerification`,
  `VFVerificationPeriod`), with no documented defaults.
- **`PSM-WebApp` does not exist** as an out-of-the-box connection component. The web ones
  are `PSM-PVWA`, `PSM-MS-Azure` and `PSM-AWSConsoleWithSTS`. Official casing is `PSM-TOAD`.
- **"Time of use restrictions"** and **"split workflow"** are exam-objective wording with
  no matching UI element — see Q40 and Q77 for what they actually map to.
- **Linux paths are case-sensitive** — `/var/opt/CARKpsmp/logs`, `basic_psmpserver.conf`,
  `vaultPermissionsValidation.sh`. Course slides frequently show the wrong casing.

## Where circulating answer keys are wrong

Four cases found while reviewing third-party sample questions. Each is a question in this
bank, answered correctly:

| Topic | Circulating answer | Correct answer |
|---|---|---|
| PSM recording storage sizing (**Q244**) | 250 GB | **~40–50 GB** — compute sessions × minutes × days × bit rate, then add the 20 GB constant |
| PSM-for-SSH recording playback (**Q203**) | Browser is out of date | **A PSMP session produces a text/command recording**, not video — so there is nothing to scrub |
| Permission levels (**Q262**) | Add Safes is Safe-level | **Add Safes is a Vault-level authorization** — you cannot hold a permission inside a Safe that does not exist yet |
| Tracking a shared account (**Q263**) | One-time passwords alone | **Exclusive access** tells you who holds it *now*; OTP gives non-repudiation after the fact. Combine both |

## A note on scope

Roughly half the third-party sample questions reviewed test **PAM-SEN (Sentry)** material
rather than Defender: Vault and PVWA installation sequences, hardening script ordering,
EC2 sizing, load-balancer topology, PVWA and PSM count design, cluster heartbeat
behaviour. Those were deliberately left out — they are not on the Defender exam.

## Licence and disclaimer

Study material only. CyberArk, PAM-DEF, PVWA, CPM, PSM and PTA are trademarks of
CyberArk Software Ltd. This project is not affiliated with or endorsed by CyberArk, and
contains no CyberArk exam content.
