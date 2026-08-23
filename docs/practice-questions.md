# 25 — PAM-DEF Practice Question Bank, Set 2

**277 original practice questions**, written from the official Defender-PAM Study Guide objectives and verified against current CyberArk (Idira) documentation in August 2026. No overlap with `20-practice-questions.md` — use both for 377 questions total.

> Not real exam items, and deliberately not copied from exam dumps. Where sample-question screenshots or dump pages were supplied, they were used only for **topic gap analysis** — the questions here are written from scratch and the answers reasoned from official documentation. That matters: several circulating answer keys turned out to be wrong (see the corrections list at the end).

**Interactive version:** https://claude.ai/code/artifact/fcff2cd5-2de8-4c9b-ae8f-58d2d153beb1

### Verification status

| Questions | Status |
|---|---|
| 1–125, 193–200 | Adversarially re-checked against docs.cyberark.com; 44 corrections applied |
| 126–192 | Written from the verified project knowledge base (docs 01–19). Final documentation pass cut short by an API spend limit — confirm parameter defaults in your own lab |
| 201–277 | Written from a gap analysis of third-party sample questions; answers reasoned from official docs, but not yet through a full adversarial pass |

## Weighting

| Domain | Questions |
|---|---|
| 1. Onboard Accounts | 38 |
| 2. Manage the Application | 33 |
| 3. Perform Ongoing Maintenance & Troubleshooting | 36 |
| 4. Configure and Manage Passwords | 61 |
| 5. Manage Security and Audit Functions | 35 |
| 6. Configure Session Management | 44 |
| 7. Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP) | 30 |
| **Total** | **277** |

---

## Domain 1 — Onboard Accounts

### Q1. Your organisation is starting a PAM programme with roughly 40,000 privileged accounts. Following CyberArk's recommended discovery-and-initiation approach, which accounts should be secured first?

- **A.** Workstation local administrator accounts, because there are the most of them
- **B.** Tier 0 accounts — Domain and Forest Admins, the Vault / Privilege Cloud administrators, and the hypervisor platform hosting them
- **C.** Application and service accounts embedded in scripts
- **D.** Third-party vendor accounts

**Answer: B**

*Why:* Tier 0 is the set of accounts that control the identity infrastructure itself. If a Domain Admin, a Vault admin or the hypervisor running the Domain Controllers is compromised, every other control in the environment is bypassable — so these are secured in Phase 1 (Discovery and initiation). Domain Controllers are always classified as critical.

*Why not the others:* A = Tier 2 (workstation admins), addressed in later phases. C and D matter a great deal, but neither hands an attacker the whole directory the way Tier 0 does. The tiering model is Tier 0 / 1 / 2 only — there is no Tier 3.

<sub>Source area: PAM Implementation Program Phase 1 — Discovery and initiation</sub>

---

### Q2. You are configuring a UNIX Accounts Discovery. Besides the CSV list of machines, you must supply a UNIX user name and password. What is that credential used for?

- **A.** It becomes the reconcile account for every account that is discovered
- **B.** It is the credential the CPM Scanner uses to log on to each machine in the CSV list and enumerate local accounts and SSH keys
- **C.** It is the password that will be set on all discovered accounts when they are onboarded
- **D.** It authenticates the scanner to the Vault

**Answer: B**

*Why:* UNIX discovery has no directory to read, so CyberArk needs a way in to each host. The CSV supplies the targets and the supplied UNIX account supplies the login used to enumerate `/etc/passwd`, local accounts and SSH keys on each one.

*Why not the others:* A — the reconcile account is defined on the platform or per account, not by the scan. C — discovery never changes passwords; that is the CPM's job after onboarding. D — the scanner authenticates to the Vault with its own component credential file, not this account.

<sub>Source area: Accounts Discovery — UNIX</sub>

---

### Q3. Three onboarding rules already exist. You create a fourth. A newly discovered account matches both your new rule and rule #2. Which rule is applied?

- **A.** Rule #2 — older rules take priority because they were established first
- **B.** The new rule — it is created with precedence 1, and an account is onboarded by the first rule it matches
- **C.** Both rules run, and the account is onboarded into both Safes
- **D.** Neither; the conflict sends the account to the Pending Accounts list

**Answer: B**

*Why:* Precedence is based on creation time and runs newest-first: the most recently created rule gets precedence 1, the next most recent gets 2, and so on. A discovered account is compared against precedence 1 first, and the first rule it matches wins. This is counter-intuitive and a favourite exam trap.

*Why not the others:* A inverts the real order. C — an account is onboarded once, by one rule. D — accounts only land in Pending when *no* rule matches.

<sub>Source area: Manage onboarding rules</sub>

---

### Q4. An onboarding rule targets a Safe called WIN-SRV-ADMINS, which does not exist in the Vault. What happens when a matching account is discovered?

- **A.** The Safe is created automatically with default properties
- **B.** Nothing is onboarded — the target Safe (and the reconcile account, if the rule references one) must exist before the rule can run
- **C.** The accounts go to PasswordManager_Pending and the Safe is created on first onboarding
- **D.** The CPM creates the Safe but leaves it unmanaged

**Answer: B**

*Why:* Onboarding rules place accounts into existing containers; they do not provision them. The documented prerequisites are to create the Safe and the reconcile account according to the rule's definition first, and the rule's author must be a member of the target Safe with Add Account permission.

*Why not the others:* A and C both assume auto-creation, which does not happen. D invents behaviour the CPM does not have.

<sub>Source area: Add onboarding rule — prerequisites</sub>

---

### Q5. Which two statements about "Add multiple accounts from a file" (bulk upload) are correct? (Choose two)

- **A.** Each file can contain a maximum of 10,000 accounts
- **B.** Safes and account groups referenced in the file are created automatically if they are missing
- **C.** All accounts must be uploaded into Safes and groups that already exist
- **D.** Only XLSX files are supported

**Answer: A, C**

*Why:* The documented ceiling is 10,000 accounts per file, and the upload writes only into Safes and account groups that already exist — it is a loading mechanism, not a provisioning mechanism.

*Why not the others:* B is the opposite of the documented behaviour. D is wrong: only CSV is supported, and the first row must be a header row of property names. A sample CSV template can be downloaded from the Add accounts from file window.

<sub>Source area: Add multiple accounts from a file</sub>

---

### Q6. A bulk upload of 4,000 accounts finishes with 63 failures. How do you find out which rows failed and why?

- **A.** Read pm_error.log on the CPM
- **B.** Download the failed-accounts CSV that the PVWA produces — it returns the failed rows with two extra columns, Errors and uploadIndex
- **C.** Check ITALog.log on the Vault
- **D.** Re-run the upload; only the failed rows are retried automatically

**Answer: B**

*Why:* The PVWA gives you back a CSV containing only the failed rows, annotated with `Errors` (the reason) and `uploadIndex` (the row's position in the original file). You fix that file and re-upload it.

*Why not the others:* A and C are component logs — the failures here are data validation, not a component fault. D — nothing is retried automatically; the re-upload is a manual action.

<sub>Source area: Add multiple accounts from a file / Create bulk upload of accounts (REST)</sub>

---

### Q7. A content administrator adds an account for srv-app01\svc_backup in the PVWA. What has happened on the target server?

- **A.** A new local account named svc_backup has been created on srv-app01
- **B.** Nothing — adding an account registers information about an account that already exists; it does not provision anything on the target
- **C.** The account's password has already been rotated
- **D.** The account has been added to the local Administrators group

**Answer: B**

*Why:* "Add account" is a Vault-side registration: it records the address, username, platform and current password so CyberArk can start managing an account that is already there. This is one of the most commonly misunderstood points on the exam.

*Why not the others:* A — CyberArk never creates target accounts as part of onboarding. C — a change only happens if the platform or the operator triggers one afterwards. D — group membership is never altered by onboarding.

<sub>Source area: Add accounts</sub>

---

### Q8. Which statement correctly describes the relationship between an account, a Safe and a platform?

- **A.** An account can live in several Safes but is associated with only one platform
- **B.** Every account is stored in exactly one Safe and associated with exactly one target account platform
- **C.** An account can be linked to several target platforms so that different CPMs can manage it
- **D.** The platform determines which Safe the account is stored in

**Answer: B**

*Why:* One Safe, one target account platform — always. The Safe controls who can reach the account and which CPM manages it; the platform controls how it is managed. Both are mandatory and singular.

*Why not the others:* A and C break the one-to-one rule. D reverses the relationship: the Safe is chosen at onboarding, and it is the Safe (not the platform) that carries the CPM assignment.

<sub>Source area: Accounts, Safes and platforms</sub>

---

### Q9. A Windows Accounts Discovery has finished. On what basis does it mark a discovered local account as Privileged?

- **A.** The account name begins with "admin"
- **B.** The account is a member of a local Administrators group on at least one scanned machine
- **C.** The account has a non-expiring password
- **D.** The account has logged on within the last 30 days

**Answer: B**

*Why:* Categorisation is by group membership. Membership of any local Administrators group on any scanned machine makes the account privileged, and it stays privileged until it has been removed from that group on every machine it was discovered on.

*Why not the others:* A — naming is a keyword filter you can use in an onboarding rule, not the categorisation basis. C and D are account attributes discovery records but does not categorise on.

<sub>Source area: Discovered accounts — categorisation</sub>

---

### Q10. Which of the following can a Windows Accounts Discovery detect as a dependency? (Choose three)

- **A.** Windows Services
- **B.** Scheduled Tasks
- **C.** IIS Application Pools
- **D.** A connection string inside a web.config file

**Answer: A, B, C**

*Why:* Discovery finds dependencies that are registered in a machine's own configuration surface: Windows services, scheduled tasks, IIS application pools, IIS anonymous access and COM+ applications. It can read those programmatically.

*Why not the others:* D — credentials sitting inside arbitrary text, XML, INI or web configuration files, database connection strings, registry keys and private SSH keys cannot be discovered. The CPM can *manage* them once you add them by hand, but it cannot find them.

<sub>Source area: Dependent accounts / supported usages</sub>

---

### Q11. A Windows discovery completes but returns only machine names — no local accounts. The scan account is a domain user with read access to Active Directory. What is missing?

- **A.** The scan account needs Domain Admin
- **B.** The scan account needs local administrative rights on the scanned servers and workstations
- **C.** The CPM needs the Backup All Safes authorization
- **D.** Discovery must be run from the PVWA server rather than the CPM

**Answer: B**

*Why:* Windows discovery runs in two phases. Phase 1 reads the directory to build the list of machines in the specified OU — AD read access is enough for that, which is why you got machine names. Phase 2 connects to each machine and enumerates its local accounts and dependencies, and that requires local administrative rights on the target.

*Why not the others:* A — Domain Admin is over-privileged and is not required. C — that is a Vault backup authorization, unrelated. D — the scan is always executed by the CPM Scanner.

<sub>Source area: Accounts Discovery — Windows, scan account permissions</sub>

---

### Q12. Which statement about running an Accounts Discovery is correct?

- **A.** The PVWA runs the scan and writes results directly into the Vault
- **B.** The CPM Scanner runs the scan; it is configured in the PVWA, and the CPM must be able to reach the PVWA on TCP 443
- **C.** PTA runs the scan by analysing network traffic
- **D.** The PrivateArk Client runs the scan

**Answer: B**

*Why:* Discovery is defined in the PVWA but executed by the CPM Scanner service on the CPM machine. Because the scanner pulls its configuration from and reports back through the PVWA's web services, CPM → PVWA on 443 is a hard prerequisite — a missing firewall rule here is the classic "discovery never starts" cause.

*Why not the others:* A — the PVWA only holds the definition. C — PTA does continuous *detection* of newly privileged accounts from AD/network telemetry, which is a different mechanism. D — the PrivateArk Client is an administration interface, not a scanner.

<sub>Source area: Accounts Discovery / component ports</sub>

---

### Q13. A UNIX discovery has finished. Which of these can it bring back in addition to local accounts?

- **A.** SSH keys found on the scanned machines, including authorized and trusted keys
- **B.** Oracle database accounts on those machines
- **C.** cron jobs that use the discovered accounts
- **D.** sudoers entries

**Answer: A**

*Why:* UNIX discovery enumerates local accounts *and* SSH keys, including the authorized/trusted key relationships between machines — which is often the more valuable half of the result, because key-based trust paths are how attackers move laterally across a UNIX estate.

*Why not the others:* B — database accounts live inside the database, not the OS account store, and need their own onboarding. C and D — cron and sudoers are not discoverable dependency types.

<sub>Source area: Accounts Discovery — UNIX / onboard SSH keys</sub>

---

### Q14. You are onboarding an account from the Pending Accounts list onto a platform that requires a reconcile account. What must be true?

- **A.** The reconcile account must already be stored in a Safe and be referenced by the platform (or specified on the account)
- **B.** The CPM creates the reconcile account automatically during onboarding
- **C.** Reconcile accounts are only required for UNIX accounts
- **D.** The reconcile account must be stored in the same Safe as the account being onboarded

**Answer: A**

*Why:* A reconcile account is just another vaulted account. It has to exist and be reachable before the platform can use it — which is why "create the Safe and the reconcile account first" is a documented prerequisite for onboarding rules as well.

*Why not the others:* B — nothing is auto-created. C — reconciliation applies to Windows, UNIX, databases and appliances alike. D — the reconcile account can sit in a dedicated Safe; the platform's ReconcileAccountSafe setting exists precisely so it does not have to share the Safe.

<sub>Source area: Onboard accounts from the pending accounts list</sub>

---

### Q15. You have limited onboarding capacity this quarter. Which of these should be onboarded first?

- **A.** A shared read-only monitoring account present on 200 Linux hosts
- **B.** The break-glass local Administrator account on every Domain Controller
- **C.** A developer's personal named account on a test server
- **D.** An FTP service account used by a nightly reporting job

**Answer: B**

*Why:* Prioritisation is risk-based, not volume-based. The local Administrator on a Domain Controller is Tier 0: it grants control of the machine that holds the directory, and it is the classic persistence and escalation target.

*Why not the others:* A is high-volume but low-privilege — impressive onboarding statistics, minimal risk reduction. C is a named low-privilege account on a non-production box. D matters but is a Tier 1/2 service account. Volume and ease are the wrong prioritisation criteria.

<sub>Source area: Prioritise onboarding projects</sub>

---

## Domain 2 — Manage the Application

### Q16. A colleague copies user.ini from CPM-01 to a new CPM-02 to save time. CPM-02 cannot authenticate to the Vault. Why?

- **A.** The credential file is bound to the machine that created it — CreateCredFile.exe hardens it with machine-specific data such as /IpAddress, /Hostname and /EntropyFile
- **B.** Credential files expire after 24 hours
- **C.** The Vault rejects any credential file that is not listed in Vault.ini
- **D.** The file has to be renamed to cpm.cred on a second CPM

**Answer: A**

*Why:* A credential file is not a portable secret. When it is generated you bind it to the host with parameters such as `/IpAddress`, `/Hostname` and `/EntropyFile`, so the Vault will only accept it when presented from that machine. A new component gets its own Vault user and its own freshly generated credential file.

*Why not the others:* B is true of the Privilege Cloud `installeruser` password, not of credential files. C — Vault.ini holds the Vault's address and port, nothing about credential files. D — file naming is irrelevant to the failure.

<sub>Source area: CreateCredFile / component authentication</sub>

---

### Q17. Which of these does NOT open its own session to the Vault over port 1858?

- **A.** CPM
- **B.** PVWA
- **C.** The PSM HTML5 Gateway
- **D.** PTA

**Answer: C**

*Why:* The HTML5 Gateway sits between the user's browser and the PSM. The browser reaches it over a secure WebSocket on 443, and it connects onward to the PSM server over RDP. It never authenticates to the Vault and holds no Vault credential of its own.

*Why not the others:* The CPM, PVWA, PSM and PTA all authenticate to the Vault with their own component users over the CyberArk proprietary protocol on 1858 (which can be moved to 443).

<sub>Source area: PSM HTML5 Gateway architecture / component ports</sub>

---

### Q18. Which is the correct 2nd-generation REST logon endpoint for LDAP authentication?

- **A.** https://<PVWA>/PasswordVault/API/auth/LDAP/Logon/
- **B.** https://<PVWA>/PasswordVault/WebServices/auth/LDAP/Logon
- **C.** https://<PVWA>/API/LDAP/Authenticate
- **D.** https://<Vault>:1858/API/auth/LDAP/Logon

**Answer: A**

*Why:* The 2nd-generation API base path is `https://<PVWA_Server_address>/PasswordVault/API/`, and the logon endpoints follow the pattern `auth/<method>/Logon/` for Cyberark, LDAP, Windows and RADIUS.

*Why not the others:* B is the 1st-generation (legacy) path under /WebServices/ — still documented, but not the recommended one. C is not a CyberArk path. D is wrong on two counts: the REST API is served by the PVWA over HTTPS, not by the Vault on 1858.

<sub>Source area: CyberArk, LDAP, RADIUS, Windows — Logon (REST)</sub>

---

### Q19. Your identity team wants new joiners' Safe memberships created automatically by their joiner/mover/leaver workflow. What is the appropriate mechanism?

- **A.** A scheduled PARestore job
- **B.** The PAM REST API — it exposes the operations normally performed by hand in the PVWA so they can be scripted and embedded in provisioning automation
- **C.** The Remote Control Client
- **D.** A nightly EVD export

**Answer: B**

*Why:* That is exactly the stated purpose of the REST API: to automate tasks that are usually performed manually through the interface, so they can be driven from provisioning scripts, ITSM tools and CI/CD pipelines.

*Why not the others:* A is a Vault restore utility. C administers Vault services remotely on 9022. D exports audit data outward — none of them write configuration into the Vault.

<sub>Source area: Purpose of the REST API</sub>

---

### Q20. By default, how long does a PAM REST API authentication token remain valid?

- **A.** 5 minutes
- **B.** 20 minutes
- **C.** 1 hour
- **D.** It never expires until an explicit Logoff call is made

**Answer: B**

*Why:* A REST session token is valid for 20 minutes by default. Long-running automation must either finish inside that window or re-authenticate; well-behaved scripts also call Logoff so the session is released rather than left to time out.

*Why not the others:* D is a common wrong assumption — Logoff is good practice, but the token expires on its own regardless.

<sub>Source area: REST API session management</sub>

---

### Q21. A firewall team asks which single port must be open from the CPM, PVWA and PSM servers to the Vault. What do you tell them?

- **A.** TCP 443
- **B.** TCP 1858 — the CyberArk proprietary Vault protocol
- **C.** TCP 9022
- **D.** TCP 3389

**Answer: B**

*Why:* Every component talks to the Vault over the CyberArk proprietary protocol on TCP 1858 (it can be reconfigured to 443). DR replication, PAReplicate backups, EVD and PTA all use the same channel.

*Why not the others:* 443 is what *users* use to reach the PVWA, and what the CPM needs to reach the PVWA for Accounts Discovery — but it is not the component-to-Vault port by default. 9022 is Remote Control Client → PARAgent. 3389 is RDP.

<sub>Source area: Component communication / ports</sub>

---

### Q22. Which dbparm.ini setting pair controls how long a component may be silent before the Vault treats it as inactive and raises a notification?

- **A.** ComponentMonitoringInterval together with ComponentNotificationThreshold
- **B.** MonitorFWRulesInterval
- **C.** AutoSyncExternalObjects
- **D.** UserLockoutPeriodInMinutes

**Answer: A**

*Why:* `ComponentMonitoringInterval` sets how often the Vault checks component activity; `ComponentNotificationThreshold` takes the form `CPM, Yes, 720, 1440` — component, notify or not, minutes before the first notification, minutes between subsequent ones. The resulting message uses notification template 206, "Component is inactive".

*Why not the others:* B governs the periodic ITATS319W firewall-rules message. C controls LDAP object synchronisation. D auto-unsuspends locked-out users.

<sub>Source area: dbparm.ini parameters / component monitoring</sub>

---

### Q23. An administrator cannot find anywhere in the PVWA to grant the "Audit Users" authorization. Why not?

- **A.** It was removed in version 12
- **B.** Vault-level authorizations are managed only in the PrivateArk Client; the PVWA manages Safe-level permissions
- **C.** Only the Master user can see it
- **D.** It is a Master Policy rule, not an authorization

**Answer: B**

*Why:* There are two distinct permission planes. Vault-level authorizations (Add Safes, Audit Users, Manage Users, Backup All Safes, Restore All Safes…) are assigned to individual users in the PrivateArk Client and are not inherited through groups. Safe-level permissions are granted to users or groups, and are inherited — those are what the PVWA exposes.

*Why not the others:* A is false. C — Administrator and other privileged users can set them too. D confuses authorizations with policy rules.

<sub>Source area: Vault vs Safe authorizations</sub>

---

### Q24. Where is the CyberArk licence stored, and how is it updated?

- **A.** In dbparm.ini; a Vault restart is required
- **B.** As License.xml in the System Safe — a new file can be copied in without restarting the Vault
- **C.** In the PVWAConfig Safe; IIS must be restarted afterwards
- **D.** On the CyberArk Marketplace; the Vault fetches it hourly

**Answer: B**

*Why:* The licence lives as `License.xml` inside the `System` Safe. Copying in a replacement file updates the licence in place, which is why licence renewals do not require a maintenance window.

*Why not the others:* A — dbparm.ini holds Vault configuration, and any change there *does* need a restart, which is part of why this distractor is tempting. C is the PVWA's configuration Safe. D is invented.

<sub>Source area: Vault licence management</sub>

---

### Q25. You need to check and restart the PrivateArk Server service from a remote administration station. Which mechanism, and over which port?

- **A.** The Remote Control Client talking to the Remote Control Agent (PARAgent) over TCP 9022
- **B.** RDP on 3389
- **C.** PACLI on 1858
- **D.** SSH on 22

**Answer: A**

*Why:* The Vault Remote Control feature is a pair: the PARAgent service on the Vault and the Remote Control Client on the administration station, communicating on TCP 9022. From the client you run commands such as `status vault`, `stop vault`, `start vault`, `status ene`.

*Why not the others:* B — a hardened Vault should not accept RDP. C — PACLI is a command-line interface for Vault *data*, not for service control. D — the Windows Vault does not run SSH.

<sub>Source area: Vault Remote Control / paragent.ini</sub>

---

## Domain 3 — Perform Ongoing Maintenance & Troubleshooting

### Q26. pm.log on the CPM repeatedly shows ITATS004E Password authentication failed, and System Health shows the CPM as Disconnected. What is the correct fix?

- **A.** Restart the PrivateArk Server service on the Vault
- **B.** Stop the CPM services, reset the PasswordManager user's password in the PrivateArk Client, activate (unsuspend) the user, regenerate the credential file with CreateCredFile.exe using the same password, then start the services
- **C.** Re-run the PSM hardening script
- **D.** Raise CPMDebugLevels to 6 and wait

**Answer: B**

*Why:* This is the classic out-of-sync component user. The credential file rotates the component's password on every successful logon, so if the file and the Vault ever diverge — a restored VM snapshot, a copied file, a failed rotation — authentication fails and repeated failures suspend the user. The fix must do all four things in order: stop, reset, unsuspend, rebuild the credential file, start.

*Why not the others:* A — if the Vault service were down, *every* component would be disconnected, not just the CPM. C is unrelated to Vault authentication. D increases logging but fixes nothing.

<sub>Source area: Troubleshooting — component authentication</sub>

---

### Q27. A single Oracle account fails to change while every other account on the same CPM is fine. Which log will tell you why?

- **A.** pm_error.log
- **B.** The per-plugin log under Logs\ThirdParty\, named <type>-<Safe>-<folder>-<object>.log
- **C.** PMConsole.log
- **D.** ITALog.log

**Answer: B**

*Why:* The CPM writes a separate log per managed object under `Logs\ThirdParty\`, named after the plugin type, Safe, folder and object. When one account misbehaves and the rest are healthy, that per-object log is where the plugin's actual conversation with the target is recorded. Uploaded copies are kept under `Logs\History\`.

*Why not the others:* A gives you warnings and errors across the whole CPM — useful for spotting the failure, not for diagnosing it. C is console output. D is the Vault's log and knows nothing about an Oracle plugin.

<sub>Source area: CPM log files</sub>

---

### Q28. Where do the PVWA application logs live by default?

- **A.** %windir%\temp — the location is set by LogFolder in web.config
- **B.** C:\Program Files\CyberArk\PVWA\Logs
- **C.** Inside the PVWAReports Safe
- **D.** /var/opt/CARKpvwa/logs

**Answer: A**

*Why:* By default the PVWA writes CyberArk.WebApplication.log, CyberArk.WebConsole.log and per-session CyberArk.WebSession.<id>.log into `%windir%\temp`, controlled by the `LogFolder` setting in web.config. Many sites move this, so always check web.config before hunting.

*Why not the others:* B looks plausible but is not the default. C holds generated reports, not logs. D is a Linux path — the PVWA is an IIS application on Windows.

<sub>Source area: PVWA log files / web.config</sub>

---

### Q29. PSM for SSH connections are failing. Which logs do you check, and where?

- **A.** PSMConsole.log in C:\Program Files\CyberArk\PSM\Logs
- **B.** PSMPConsole.log and PSMPTrace.log in /var/opt/CARKPSMP/logs/
- **C.** pm.log and pm_error.log on the CPM
- **D.** ITALog.log and Trace.d0 on the Vault

**Answer: B**

*Why:* PSM for SSH (PSMP) is a Linux component with its own log set: `PSMPConsole.log` and `PSMPTrace.log` under `/var/opt/CARKPSMP/logs/`. Its configuration lives in `/etc/opt/CARKPSMP/conf/basic_PSMPserver.conf`, and the service is controlled with `/etc/init.d/psmpsrv`.

*Why not the others:* A is the Windows PSM, a different component. C is the CPM. D is the Vault.

<sub>Source area: PSM for SSH log files</sub>

---

### Q30. Which of the following is a services engagement rather than a break/fix support case?

- **A.** A PSM session fails to launch after a Windows update
- **B.** Designing and building a custom CPM plugin for an unsupported in-house application
- **C.** A component user is suspended after repeated failed logons
- **D.** The DR Vault has stopped replicating

**Answer: B**

*Why:* Break/fix is restoring documented, expected behaviour of a supported product. Building something that does not exist yet — a custom plugin, a new Safe model, an architecture design — is professional services work, because there is no "working state" to restore.

*Why not the others:* A, C and D are all documented failure modes of supported functionality with documented remediation procedures, which makes them support cases.

<sub>Source area: Break/fix vs services engagement</sub>

---

### Q31. You edit DebugLevel in dbparm.ini on the Vault. When does the change take effect?

- **A.** Immediately — the Vault re-reads dbparm.ini every minute
- **B.** After the PrivateArk Server service is restarted; dbparm.ini changes always require a Vault restart
- **C.** After 20 minutes, on the next configuration refresh
- **D.** Only after the next full backup

**Answer: B**

*Why:* `dbparm.ini` is read at service start. Any change to it — DebugLevel, Syslog, firewall rules, thresholds — needs a restart of the PrivateArk Server service. Two supporting files help here: `dbparm.sample.ini` lists every available option, and `dbparm.ini.good` is written automatically after a successful start so you have a known-good copy to fall back to.

*Why not the others:* A and C describe the PVWA's periodic configuration refresh, not the Vault. D is unrelated. Note that the Vault Server Central Administration Station can change the debug level without a restart — which is exactly why that tool exists.

<sub>Source area: dbparm.ini</sub>

---

### Q32. CyberArk Support asks for a log bundle. Which statement is correct?

- **A.** Run CAVaultManager CollectLogs on the Vault; xRay is the broader tool that collects encrypted logs and configuration from PAM components and is downloaded from the CyberArk Marketplace
- **B.** Run PARestore.exe /CollectLogs
- **C.** Export the data with EVD and send the CSV
- **D.** Copy ITALog.log — Support only needs the Vault's main log

**Answer: A**

*Why:* `CAVaultManager CollectLogs` gathers the Vault's own logs. xRay is the general-purpose diagnostic collector across PAM components — it packages logs and configuration files in encrypted form for Support, and you get it from the CyberArk Marketplace, not from the installation media.

*Why not the others:* B — PARestore restores Safes from backup. C — EVD exports audit *data* for reporting, not diagnostics. D is almost never sufficient; Support needs configuration alongside logs.

<sub>Source area: xRay / CAVaultManager</sub>

---

### Q33. After a new database client is installed on a PSM server, sessions that use it fail immediately. What is the most likely cause and fix?

- **A.** The recording Safe is full — raise MaxSafeSize
- **B.** AppLocker has no rule for the new executable — add it to PSMConfigureAppLocker.xml and re-run PSMConfigureApplocker.ps1
- **C.** Network Level Authentication must be disabled on the PSM
- **D.** The connection component must be deleted and recreated

**Answer: B**

*Why:* PSM hardening puts AppLocker in place so only explicitly permitted binaries can run in a PSM session. Any new client application is blocked until it is whitelisted — you add it to `PSMConfigureAppLocker.xml` and re-run `PSMConfigureApplocker.ps1`. "It worked in testing before hardening" is the tell.

*Why not the others:* A would show as an upload failure after the session, not an instant launch failure. C and D do not produce an immediate application-launch block.

<sub>Source area: PSM AppLocker configuration</sub>

---

### Q34. PSM sessions fail with a logon-rights error for the shadow user PSM-jdoe. What should you check?

- **A.** That the PSMShadowUsers local group still holds the "Allow log on locally" right — hardening or a domain GPO can strip it
- **B.** That jdoe has been added to the Auditors group
- **C.** That PSMConnect has been converted to a domain account
- **D.** That the Vault firewall permits 3389

**Answer: A**

*Why:* For non-RDP-file connections the PSM auto-creates a local shadow user `PSM-<userid>` per Vault user, with credentials reset on every connection. Those users sit in the local `PSMShadowUsers` group, which must retain the "Allow log on locally" user right. A tightening GPO applied after PSM hardening is the usual culprit.

*Why not the others:* B is about auditing, not session logon. C is not a supported change. D would break the connection before any logon error appeared.

<sub>Source area: PSM shadow users / hardening</sub>

---

### Q35. The CPM cannot change a local Windows account's password; the target rejects the new value. The platform generates 12-character passwords. What do you check first?

- **A.** Whether the target's local or group password policy — complexity, minimum length, password history, minimum password age — conflicts with the platform's password policy
- **B.** Whether the Vault has spare licence capacity
- **C.** Whether the account has been added to the Auditors group
- **D.** Whether SearchForUsages is enabled on the platform

**Answer: A**

*Why:* When the target itself rejects the password, the mismatch is almost always between the platform's generated password policy and what the operating system will accept. Minimum password *age* is the sneakiest of these: it silently blocks a second change within the same day, which looks like an intermittent failure.

*Why not the others:* B would prevent onboarding, not changing. C is unrelated. D controls dependency scanning after a successful change.

<sub>Source area: CPM troubleshooting — password change failures</sub>

---

### Q36. You see ITATS310E in a log. What can you infer before looking it up?

- **A.** It came from the PVWA and is informational
- **B.** It originated on the Vault server (the ITA prefix) and the trailing E marks it as an Error
- **C.** It came from the CPM and is a System message
- **D.** It is a PSM warning

**Answer: B**

*Why:* CyberArk message codes are readable at a glance. The leading letters identify the originating component and module — `ITA…` means the Vault server — and the trailing letter is the category: I = Informational, W = Warning, E = Error, S = System.

*Why not the others:* The other options mis-read either the prefix or the suffix. Practise this: ITADB367S is a Vault database System message; ITATS319W is a Vault warning.

<sub>Source area: Message code anatomy</sub>

---

### Q37. A Vault user is suspended after five failed logon attempts. Which two are valid ways to restore access? (Choose two)

- **A.** Activate the user in the PrivateArk Client under Users and Groups
- **B.** Wait for the period set by UserLockoutPeriodInMinutes in dbparm.ini to elapse, where it is configured
- **C.** Restart the PrivateArk Server service
- **D.** Delete the user in the PVWA and recreate them

**Answer: A, B**

*Why:* Suspension is cleared either manually — an administrator activates the user in the PrivateArk Client — or automatically, if `UserLockoutPeriodInMinutes` is set in dbparm.ini, after which the Vault unsuspends the user itself.

*Why not the others:* C does not clear a suspension. D is destructive: deleting a user loses their individually-assigned Safe permissions, which is one of the strongest arguments for granting permissions to groups rather than to people.

<sub>Source area: User suspension / dbparm.ini</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q38. In the Safe properties you can retain account versions by number of days or by number of versions. Which statement is correct?

- **A.** Both can be set at once, for belt-and-braces retention
- **B.** They are mutually exclusive — setting one disables the other, and by default the last five versions are kept
- **C.** Only the "number of days" option exists in current versions
- **D.** Retention is fixed at Safe creation and can never be changed

**Answer: B**

*Why:* The Add/Edit Safe screen offers two Version management options — "Save account versions for a period of N days" and "Save the latest N account versions" — and you may select only one. The default is the last five versions. The REST API mirrors this: setting numberOfVersionsRetention disables numberOfDaysRetention and vice versa.

*Why not the others:* D is a persistent myth. Retention is an editable Safe property (Manage Safe permission required). The things that genuinely cannot be changed after Safe creation are the Safe *name*, the Encryption tab properties, and OLAC once it has been enabled.

<sub>Source area: Add a Safe / Update Safe (REST)</sub>

---

### Q39. Which Safe property determines how many days objects must be retained before they can be deleted, and what is its default?

- **A.** SafeObjectsRetentionPeriod — default 30 days
- **B.** SafeLogRetentionPeriod — default 30 days
- **C.** RequestRetentionPeriod — default 90 days
- **D.** MaxSafeSize — default 50 days

**Answer: A**

*Why:* `SafeObjectsRetentionPeriod` sets the number of days objects are held in the Safe before deletion is permitted; its default is 30. These defaults live in SafeTemplate.xml in the PVWAConfig Safe.

*Why not the others:* The other names are real but the values are swapped: SafeLogRetentionPeriod defaults to 90 days, RequestRetentionPeriod to 30 days, and MaxSafeSize is 50 **MB**, not days.

<sub>Source area: Safe default properties / SafeTemplate.xml</sub>

---

### Q40. You must ensure a Safe can only be opened between 08:00 and 18:00. Where is that configured?

- **A.** Master Policy → Access workflows
- **B.** PrivateArk Client → Safe Properties → Restrictions tab (All Hours, or From/To) — the same tab also sets a delay between opening the Safe and being able to access it
- **C.** Platform → Automatic Password Management → FromHour / ToHour
- **D.** PVWA → Safe → Edit → Time of use restrictions

**Answer: B**

*Why:* Safe access hours are a PrivateArk Client Safe property, on the Restrictions tab. Outside the window the Vault refuses with ITATS100E, "Safe cannot be opened due to preset time restrictions". The parallel control for *users* is the Time Limitations tab on the user's properties, which produces ITATS102E.

*Why not the others:* C is a real setting but it restricts when the **CPM** may perform password operations, not when a human may open the Safe. D does not exist — "time of use restrictions" is legacy exam-objective wording, not a current UI element, and there is no hour-of-day restriction at Safe-member level (only membershipExpirationDate).

<sub>Source area: Safe properties — Restrictions tab</sub>

---

### Q41. How do you change which CPM manages the accounts in a Safe?

- **A.** Platform Management → edit the platform → assign the CPM there
- **B.** PVWA → Safes → select the Safe → Edit → "Assigned to CPM". Underneath, the assignment is CPM-user ownership of the Safe, and only one active CPM user should own a Safe
- **C.** Move the accounts to a different Safe
- **D.** Edit AllowedSafes on the CPM

**Answer: B**

*Why:* CPM assignment is a **Safe** property, chosen at Safe creation and editable afterwards with the Manage Safe authorization. Mechanically it is implemented as Safe ownership by that CPM's Vault user — which is why having two active CPM users owning the same Safe causes contention and must be cleaned up (an inactive DR CPM as a second owner is the one valid exception).

*Why not the others:* A — there is no CPM assignment on a platform. D — AllowedSafes is a platform-level regex that scopes where a platform may be used; it does not assign a CPM. C is unnecessary. Note also that Reports Safes and PSM Recording Safes cannot be CPM-managed at all.

<sub>Source area: Add a Safe / Manage Safes</sub>

---

### Q42. What does AllowedSafes = ^LIN-.* on a platform achieve?

- **A.** It assigns every LIN- Safe to a specific CPM
- **B.** It restricts the platform to Safes whose names match the regular expression, so the CPM only searches those Safes for accounts using this platform
- **C.** It hides the other Safes from users
- **D.** It creates the matching Safes if they do not exist

**Answer: B**

*Why:* `AllowedSafes` (Automatic Password Management → General) limits a platform to Safes matching a regex. Default is `.*` — all Safes. Narrowing it is a real performance tuning measure: it stops the CPM scanning every Safe in the Vault on every loop looking for accounts using that platform.

*Why not the others:* A confuses platform scoping with CPM assignment (which is a Safe property). C — it has no effect on user visibility, which is governed by Safe membership. D — it creates nothing.

<sub>Source area: Automatic Password Management — General</sub>

---

### Q43. You want the CPM to update a Windows Service that runs under a domain account whenever that account's password changes. Which two are required? (Choose two)

- **A.** The dependent (service) platform must be linked to the target platform under UI & Workflows → Usages
- **B.** SearchForUsages must be set to Yes on the target platform
- **C.** The service must be onboarded into a Safe of its own
- **D.** The target platform must be converted to a Group platform

**Answer: A, B**

*Why:* Two documented prerequisites before dependent accounts can be attached to a target account: the dependent platform must be linked to the target platform (target platform → Edit → UI & Workflows → **Usages**), and **SearchForUsages** must be enabled on the target platform so the CPM looks for copies of the credential after a successful change.

*Why not the others:* C — dependents belong to the target account, not to a separate Safe. D — Group platforms coordinate simultaneous changes across several *accounts*; they are unrelated to dependencies.

<sub>Source area: Manage dependent accounts / UI and Workflows — Usages</sub>

---

### Q44. You deactivate a target platform. What happens to the dependent platforms associated with it?

- **A.** They stay active and keep running independently
- **B.** They are deactivated too — dependent platforms are activated and deactivated according to the target platform they are associated with
- **C.** They are deleted
- **D.** They fall back to the default platform

**Answer: B**

*Why:* Dependent platforms have no independent lifecycle; their state follows the target platform they are linked to. This is worth remembering because deactivating a target platform to "tidy up" silently stops the dependency handling that went with it.

*Why not the others:* A is the intuitive but wrong answer. C — deactivation never deletes. D — there is no fallback platform.

<sub>Source area: Manage platforms — Targets, Dependents, Groups, Rotational Groups</sub>

---

### Q45. Three accounts on a clustered application must always be changed at the same time. Which platform type do you use?

- **A.** A dependent platform
- **B.** A group platform — the accounts stay associated with their target platform for the change mechanics, while the group platform governs when the change happens so all members change together
- **C.** A rotational group
- **D.** A duplicated target platform

**Answer: B**

*Why:* Accounts in a group platform are associated with **both** a target platform (whose CPM plugin performs the actual change) and a group platform (which determines when and under what policy the change occurs). That is what guarantees the cluster members change in lockstep.

*Why not the others:* A is for usages of the same credential (services, tasks, app pools). C is a genuine but different construct — rotational groups rotate through several accounts serving the same purpose so a fresh credential is always available. D changes policy, not synchronisation.

<sub>Source area: Manage platforms — group platforms</sub>

---

### Q46. Why must you duplicate a built-in platform before customising it?

- **A.** Built-in platforms are not meant to be edited directly and can be overwritten on upgrade; duplicating gives you an editable copy that survives upgrades and lets different populations of the same system type get different policies
- **B.** Duplicating is the only way to assign a CPM
- **C.** Duplicated platforms consume less licence capacity
- **D.** Only duplicated platforms can be deactivated

**Answer: A**

*Why:* Two reasons, and the exam cares about both. Practical: your customisations survive upgrades. Design: accounts of the same system type frequently need different policies — a 30-day rotation for one environment and 90-day for another — and each policy set needs its own platform, e.g. duplicating "Unix via SSH" into "LIN SSH 30" and "LIN SSH 90".

*Why not the others:* B — CPM assignment is a Safe property. C — licensing counts managed accounts, not platforms. D — any platform can be deactivated, and deactivating unused ones is recommended for both administration and CPM performance.

<sub>Source area: Duplicate a platform</sub>

---

### Q47. A vendor appliance has no matching out-of-the-box platform. What is the correct first step?

- **A.** Write a custom CPM plugin from scratch
- **B.** Search the CyberArk Marketplace for a published platform package and import it through Platform Management → Import
- **C.** Use the PSMSecureConnect platform permanently
- **D.** Store the account without a platform

**Answer: B**

*Why:* The Marketplace is the catalogue of CyberArk-published and partner-published platform packages and plugins. Importing a ready-made package is faster, supported and maintained — always check there before commissioning custom development.

*Why not the others:* A is the correct answer only after the Marketplace has been exhausted, and it is a services engagement rather than break/fix. C leaves the credential unmanaged and unvaulted. D is not possible — every account requires a platform.

<sub>Source area: Import a platform from the Marketplace</sub>

---

### Q48. MinValidityPeriod is set to 60 on a platform that uses one-time passwords. What does that mean?

- **A.** The password is valid for 60 days
- **B.** After the account is retrieved, the CPM waits 60 minutes before replacing the password
- **C.** The user must check the account back in within 60 minutes or lose access
- **D.** The CPM retries a failed change after 60 minutes

**Answer: B**

*Why:* `MinValidityPeriod` (Automatic Password Management → Privileged Account Management, default 60) is the number of **minutes** to wait from the last retrieval until the password is replaced. It exists so a user actually has time to finish the work before the credential is invalidated underneath them.

*Why not the others:* A misreads the unit. C describes exclusive access check-in, a different control. D is not what this parameter does. Related: `ResetOveridesMinValidity` (default Yes) lets an immediate reset ignore this wait, and `ResetOveridesTimeFrame` (default Yes) lets it ignore the FromHour/ToHour window.

<sub>Source area: Automatic Password Management — Privileged Account Management</sub>

---

### Q49. A user clicks Change Now on an account. The platform has ImmediateInterval = 5 and Interval = 1440. When does the change actually run?

- **A.** Within about 5 minutes — ImmediateInterval governs user-initiated operations, while Interval is the periodic CPM processing loop
- **B.** In 1440 minutes, at the next scheduled loop
- **C.** Instantly; both parameters are ignored for manual operations
- **D.** At the next FromHour boundary

**Answer: A**

*Why:* `ImmediateInterval` (default 5) is the number of minutes between a user initiating an operation and the CPM performing it. `Interval` (default 1440, i.e. 24 hours) is how long the CPM waits between loops when processing accounts on that platform. Users who report "Change Now did nothing" have usually just not waited five minutes.

*Why not the others:* B confuses the two parameters — the exact trap this question tests. C — there is always a short queueing delay. D applies to scheduled operations within a time window.

<sub>Source area: Automatic Password Management — General</sub>

---

### Q50. What does HeadStartInterval = 5 do on a platform?

- **A.** The CPM begins the change process 5 days before the password is due to expire according to the Master Policy
- **B.** The CPM waits 5 minutes before starting any change
- **C.** 5 password versions are retained
- **D.** 5 concurrent connections to the target are permitted

**Answer: A**

*Why:* `HeadStartInterval` (Automatic Password Management → Password Change, default 0) is the number of **days** before expiry that the CPM starts the change. Giving the CPM a head start means a target that is temporarily unreachable still has several days of retries before the credential actually expires.

*Why not the others:* B is ImmediateInterval. C is EnforcePasswordVersionsHistory (default 7). D is MaxConcurrentConnections (default 3). Avoid setting HeadStartInterval to -1.

<sub>Source area: Automatic Password Management — Password Change</sub>

---

### Q51. What does MaxConcurrentConnections control, and what is its default?

- **A.** The maximum number of PSM sessions allowed per account; default 3
- **B.** The maximum number of connections the CPM opens simultaneously to the remote machine where passwords are replaced; default 3
- **C.** The maximum number of users in a Safe; default 3
- **D.** The maximum number of concurrent REST sessions; default 3

**Answer: B**

*Why:* `MaxConcurrentConnections` (Automatic Password Management → General, default 3) caps how many simultaneous connections the CPM opens to a single remote machine during password replacement. It is a throttle to protect the target, not a user-facing limit.

*Why not the others:* A is governed by the platform's session settings and PSM capacity. C is Safe membership. D is the REST `concurrentSession` parameter, which supports up to 300.

<sub>Source area: Automatic Password Management — General</sub>

---

### Q52. Which parameters drive automatic password verification on a platform?

- **A.** VFPerformPeriodicVerification and VFVerificationPeriod
- **B.** PerformPeriodicChange and HeadStartInterval
- **C.** RCAutomaticReconcileWhenUnsynched
- **D.** SearchForUsages and Interval

**Answer: A**

*Why:* The verification parameters carry a **VF** prefix in the platform reference: `VFPerformPeriodicVerification` (whether automatic verification runs) and `VFVerificationPeriod` (the number of days between verification runs). The prefixes map to the three CPM actions — VF for verify, CH for change, RC for reconcile.

*Why not the others:* B are the change parameters, C is the reconciliation trigger, D relate to dependency scanning and the processing loop. Note the unprefixed names "PerformPeriodicVerification" and "VerificationPeriod" do not appear in current documentation.

<sub>Source area: Automatic Password Management — Password Verification</sub>

---

### Q53. Verification reports an account as unsynchronised. With RCAutomaticReconcileWhenUnsynched = Yes, what happens next?

- **A.** The account is disabled until an administrator intervenes
- **B.** The CPM uses the linked reconcile account to set a brand-new password on the target and store that same value in the Vault, bringing the two back into sync
- **C.** The account is removed from the Safe
- **D.** The current password is read off the target and copied into the Vault

**Answer: B**

*Why:* Reconciliation is a *write*, not a read. The reconcile account has enough privilege to reset the managed account's password, so the CPM generates a new password, forces it onto the target, and stores it in the Vault — both sides now hold the same known value.

*Why not the others:* D is the single most common misconception about reconciliation. CyberArk cannot read an existing password off a target: they are stored as one-way hashes. A and C are not behaviours the CPM has.

<sub>Source area: Reconcile passwords</sub>

---

### Q54. Which statement correctly distinguishes a logon account from a reconcile account?

- **A.** A logon account has a known password, is typically non-privileged and is used to establish the initial session before elevating — and it is also used when connecting through the PSM. A reconcile account is privileged and is used to reset a password that is unknown or out of sync
- **B.** Both must be domain administrators
- **C.** The reconcile account establishes the initial session and the logon account resets passwords
- **D.** Logon accounts are only ever used by the PSM, never by the CPM

**Answer: A**

*Why:* The two solve different problems. A logon account solves "I cannot log in directly as this account" — the classic case being a Linux host with PermitRootLogin no, where you log on as a normal user and then elevate. A reconcile account solves "I do not know the current password" — it has the rights to overwrite it. A detail that is regularly examined: the logon account is used by the PSM too, not just the CPM.

*Why not the others:* B over-privileges the logon account, which should be as low-privilege as possible. C swaps the two roles. D is the trap that the correct answer's final clause addresses.

<sub>Source area: Linked accounts — logon and reconcile</sub>

---

### Q55. Where can the reconcile account used by a platform be stored?

- **A.** Only in the same Safe as the account it reconciles
- **B.** In a dedicated Safe referenced by the platform (ReconcileAccountSafe), or specified per account — it does not have to share the Safe
- **C.** In the System Safe
- **D.** As a credential file on the CPM server

**Answer: B**

*Why:* Reconcile accounts are usually held in a small, tightly restricted Safe of their own, precisely because they are highly privileged and should not be reachable by everyone who can see the accounts they reconcile. The platform points at that Safe; individual accounts can override it.

*Why not the others:* A would force a very privileged credential into every operational Safe. C is a Vault system Safe, not for managed accounts. D confuses reconcile accounts with component authentication.

<sub>Source area: Configure a reconcile account</sub>

---

### Q56. You must ensure that nobody can retrieve a production Windows credential without a second person's approval. What do you configure?

- **A.** Enable "Require dual control password access approval" — in the Master Policy or as a Safe-level exception — and grant "Authorize account requests" to the approver group on that Safe
- **B.** Enable one-time passwords on the platform
- **C.** Enable exclusive access on the platform
- **D.** Remove Retrieve Accounts from everyone

**Answer: A**

*Why:* Dual control is a two-part configuration and both parts are needed. The Master Policy rule (or its Safe-level exception) makes the request happen; the Safe-level "Authorize account requests" permission decides who can approve it. Configuring only one of the two is the usual mistake.

*Why not the others:* B and C reduce credential-theft risk in other ways but neither introduces an approver. D blocks legitimate access entirely rather than governing it.

<sub>Source area: Dual control</sub>

---

### Q57. A break-glass group must be able to retrieve credentials during an incident without waiting for approval, while dual control remains in force for everyone else. What do you grant them on that Safe?

- **A.** Access Safe without confirmation
- **B.** Authorize account requests
- **C.** Manage Safe
- **D.** Membership of the Auditors group

**Answer: A**

*Why:* "Access Safe without confirmation" is the documented bypass: members holding it retrieve credentials from that Safe without the request-and-approval step, while the Master Policy rule stays active for everyone else. Their access is still fully audited.

*Why not the others:* B is the classic trap — it makes them **approvers** for other people's requests; it does not exempt them from needing approval themselves. C governs Safe properties. D grants audit visibility, not retrieval rights.

<sub>Source area: Safe member permissions / dual control</sub>

---

### Q58. Which combination best supports non-repudiation — being able to prove which individual performed a privileged action?

- **A.** A shared account that anyone with Retrieve Accounts can pull
- **B.** Exclusive access (check-out/check-in) plus one-time passwords, plus "Require users to specify reason for access" — so each use is tied to one named Vault user, with a password value used only once
- **C.** Dual control on its own
- **D.** Session recording on its own

**Answer: B**

*Why:* Non-repudiation needs a one-to-one binding between a human and an action. Exclusive access guarantees only one user holds the account at a time; one-time passwords guarantee the value that appeared in the target's logs can only correspond to that one checkout; the reason-for-access prompt records intent. Together they close the "it could have been anyone with the shared password" defence.

*Why not the others:* A is exactly what destroys non-repudiation. C proves someone approved, not who used it. D is strong evidence but does not by itself prevent two people using the same credential concurrently.

<sub>Source area: Privileged access workflows — exclusive access, one-time passwords, reason for access</sub>

---

### Q59. An account uses exclusive access with one-time passwords. A user checks it out and then goes on leave without checking it back in. What happens?

- **A.** The account stays locked indefinitely until an administrator forcibly releases it
- **B.** Once the MinValidityPeriod elapses the CPM changes the password, which releases the account automatically
- **C.** The CPM permanently skips the account
- **D.** The whole Safe is locked to other users

**Answer: B**

*Why:* The combination is self-healing by design. The one-time-password rule means the credential must be changed after use; MinValidityPeriod defines how long the CPM waits before doing it; and completing that change releases the exclusive lock. No administrator intervention is needed.

*Why not the others:* A is the intuitive answer and the reason this combination is examined — the automatic release is the whole point. C and D do not happen.

<sub>Source area: Exclusive access and one-time passwords</sub>

---

### Q60. Which scenario is the Loosely Connected Devices capability designed for?

- **A.** Database accounts on always-on production servers
- **B.** Local administrator accounts on laptops that are frequently off the corporate network, where a CPM cannot reliably reach the endpoint on schedule
- **C.** Domain administrator accounts in a hardened data centre
- **D.** Service accounts running IIS application pools

**Answer: B**

*Why:* The defining characteristic is intermittent reachability. A standard CPM rotation assumes the target answers when the CPM calls; a roaming laptop does not. Loosely Connected Devices handles endpoints that are only occasionally on the network, so their local admin credentials can still be rotated and made unique without a permanent connection.

*Why not the others:* A, C and D are all continuously reachable and are handled perfectly well by normal CPM management.

<sub>Source area: Loosely Connected Devices</sub>

---

### Q61. Which is the best Safe-naming practice?

- **A.** Name the Safe after the account it holds so it is easy to find
- **B.** Use a short, consistent, meaningful convention — platform / environment / owner — within the 28-character limit, because the Safe name cannot be changed after creation
- **C.** Use GUIDs to guarantee uniqueness
- **D.** Name Safes after the CPM that manages them

**Answer: B**

*Why:* Three constraints shape this. The name is capped at 28 characters, it cannot be changed once the Safe exists, and Safes are the unit of access control — so the name has to convey what is inside and who owns it at a glance. A convention such as `WIN-PRD-DBA` scales; ad hoc names do not.

*Why not the others:* A produces one Safe per account, which is unmanageable — aim for 3,000–5,000 objects per Safe (20,000 is the hard ceiling including versions). C is unreadable to the humans who must administer membership. D breaks as soon as the Safe is reassigned to another CPM.

<sub>Source area: Safe naming conventions</sub>

---

### Q62. Which two are required in order to provision a Safe in the PVWA? (Choose two)

- **A.** Membership of a group holding the Add Safes Vault authorization, such as Safe Managers
- **B.** Choosing the CPM that will manage the accounts in the Safe
- **C.** Membership of the Auditors group
- **D.** The Backup All Safes authorization

**Answer: A, B**

*Why:* Creating a Safe requires the **Add Safes** Vault-level authorization — conventionally granted through the Safe Managers group — and the creation dialog requires you to pick the CPM that will manage the Safe's contents, alongside the retention settings and members.

*Why not the others:* C grants read-and-audit visibility across the Vault, not the right to create Safes. D is a backup authorization held by the Backup and DR users.

<sub>Source area: Add a Safe / Vault authorizations</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q63. The CyberArk Blueprint is built on three guiding principles. Which set is correct?

- **A.** Discover, Onboard, Rotate
- **B.** Prevent identity compromise; stop lateral and vertical movement; limit privilege escalation and abuse
- **C.** Collect, Detect, Alert, Respond
- **D.** Isolate, Monitor, Record

**Answer: B**

*Why:* Those three principles are the spine of the Blueprint: stop the attacker getting an identity in the first place (SSO, adaptive MFA, vaulting, credential rotation), stop them moving once they have one (RBAC, just-in-time access, session isolation, analytics), and stop them gaining or abusing more privilege (least privilege, privilege analysis, audit, continuous authentication).

*Why not the others:* C is PTA's operating model. D describes what the PSM does. Note two currency points: the first principle was reworded from "prevent credential theft" to "prevent identity compromise" in 2024, and the old five-stage model has been retired in favour of a risk-versus-effort prioritisation index — older course material still shows the stages.

<sub>Source area: CyberArk Blueprint — guiding principles</sub>

---

### Q64. Where does CyberArk publish the Blueprint, and who can access it?

- **A.** Only in the System Safe of a licensed Vault
- **B.** Publicly, at cyberark.com/blueprint, with the full guidance in the Blueprint documentation — it is free to anyone
- **C.** Only to certified implementation partners under NDA
- **D.** In the PVWA Reports tab

**Answer: B**

*Why:* The Blueprint is deliberately public: a vendor-neutral, prescriptive, risk-based roadmap that anyone can use to assess their identity security posture and build a prioritised programme. The exam objective explicitly includes "understand how to find out more about the CyberArk Blueprint".

*Why not the others:* A, C and D all imply gated access; none is true.

<sub>Source area: cyberark.com/blueprint</sub>

---

### Q65. What does the CyberArk Telemetry Tool actually do?

- **A.** Detects credential theft and anomalous privileged behaviour in real time
- **B.** Reports component utilisation, credential compliance and licence utilisation, drawing on the licence, the Vault database and configuration files
- **C.** Collects encrypted logs and configuration for a Support case
- **D.** Exports Vault audit data to CSV for a third-party analytics tool

**Answer: B**

*Why:* Telemetry answers "how well are we actually using what we bought?" — component and licence utilisation, compliance status of managed credentials, and business metrics such as managed account counts, platforms in use and logged-on users. It is an adoption and maturity tool, not a security detection tool.

*Why not the others:* A is PTA. C is xRay. D is EVD. Distinguishing these four is a recurring exam theme, so learn them as a set.

<sub>Source area: Telemetry tool — introduction</sub>

---

### Q66. Where do you view Telemetry results, and what does installing the tool create?

- **A.** In the PVWA Reports tab; it creates a scheduled report
- **B.** In the Telemetry dashboard in the CyberArk Technical Community; installation creates a Windows scheduled task and a TelemetryUser Vault account with Auditor permissions
- **C.** On the System Health page; it creates no new objects
- **D.** In PTA; it creates a PTA integration user

**Answer: B**

*Why:* The tool is installed with a PowerShell script on a Windows server, configured through InstallCyberArkTelemetry.json, and creates a scheduled task plus a `TelemetryUser` Vault account holding Auditor permissions and access to specific Safes. The results are rendered as a dashboard in the CyberArk Technical Community (Resources → Telemetry Dashboard), with current gauges and up to a year of trending.

*Why not the others:* A and C place the output in the wrong product. D confuses Telemetry with threat analytics. Note: if the upload to the community is declined, data is stored locally only and never appears in the dashboard.

<sub>Source area: Telemetry install / Telemetry dashboard</sub>

---

### Q67. Which PVWA report shows which accounts are NOT compliant with the policy that governs them?

- **A.** Privileged Accounts Inventory
- **B.** Privileged Accounts Compliance Status
- **C.** Entitlement Report
- **D.** Applications Inventory

**Answer: B**

*Why:* The Compliance Status report is the exception report: it lists accounts that are not being managed in line with their platform and Master Policy — passwords overdue for change, verification failures, accounts not managed at all. It is the report an auditor asks for.

*Why not the others:* A is the census of what exists (needs List Accounts + View Safe Members). C maps users to what they can reach. D lists applications using Application Access Manager (needs the Audit Users Vault authorization). Compliance Status needs List Accounts plus PVWAMonitor membership; running it for the whole Vault requires the Auditors group.

<sub>Source area: PVWA reports</sub>

---

### Q68. An auditor asks: "show me, for every user, which accounts they can reach and through which Safe." Which report do you run?

- **A.** Activity Log
- **B.** Entitlement Report
- **C.** Privileged Accounts Inventory
- **D.** Applications Inventory

**Answer: B**

*Why:* The Entitlement Report is the access-rights view: user by user, the accounts and Safes they are entitled to, including how that entitlement is derived. It requires either the Manage Users or the Audit Users Vault authorization.

*Why not the others:* A shows what was done, not what is possible. C inventories accounts without mapping them to people. D covers AAM applications.

<sub>Source area: PVWA reports — Entitlement</sub>

---

### Q69. How do you ensure the Windows team's reports only cover their own Safes?

- **A.** Grant the reporting permissions — List Accounts, View Safe Members, View Audit — only on their Safes, because report scope follows Safe membership
- **B.** Set AllowedSafes on their platform
- **C.** Add them to the Auditors group
- **D.** Deploy a second PVWA instance for that team

**Answer: A**

*Why:* There is no separate "report scope" setting. A report returns exactly the Safes the running user is a member of, with the permissions the report requires. Scoping a report therefore means scoping Safe membership — which is the exam objective "describe the use of safe permissions to limit the scope of reports for specific users".

*Why not the others:* B scopes a platform to Safes for the CPM, not a user's report. C does the opposite of what is asked: Auditors are added to **all** Safes automatically, widening the scope to the entire Vault. D is unnecessary and does not change permissions.

<sub>Source area: Reports — permissions and scope</sub>

---

### Q70. Where are generated PVWA reports stored?

- **A.** In the PVWAReports Safe
- **B.** In the System Safe
- **C.** On the PVWA server's file system only
- **D.** In PasswordManagerShared

**Answer: A**

*Why:* Generated reports are stored as objects in the `PVWAReports` Safe — which means they inherit Vault protections: encryption, access control by Safe membership, and a full audit trail of who retrieved them. Reports Safes are auto-purge enabled and cannot be CPM-managed.

*Why not the others:* B holds Vault system objects including License.xml. C would put audit output outside the Vault's protection. D is the CPM's shared platform Safe.

<sub>Source area: PVWA built-in Safes</sub>

---

### Q71. Your SIEM team wants raw Vault audit data in a format they can load into their own analytics platform. Which utility do you use?

- **A.** xRay
- **B.** EVD — Export Vault Data, which exports Vault data to text/CSV over the Vault protocol on port 1858
- **C.** PARestore
- **D.** The Telemetry Tool

**Answer: B**

*Why:* EVD exists to get Vault data out in a consumable, structured form for third-party analysis and custom reporting. It authenticates like any other component, over the Vault protocol on 1858.

*Why not the others:* A collects diagnostics for Support. C restores Safes from backup. D produces adoption metrics for a CyberArk-hosted dashboard, not raw audit data. Note that continuous audit streaming to a SIEM is a separate mechanism — syslog configured in dbparm.ini.

<sub>Source area: Export Vault Data (EVD)</sub>

---

### Q72. What does membership of the Auditors group grant automatically?

- **A.** Full control over every Safe in the Vault
- **B.** The Privileged Sessions tab, plus List Accounts / View Safe Members / View Audit on all Safes, and permissions on all Recording Safes
- **C.** The ability to change any account's password
- **D.** The same rights as Vault Admins

**Answer: B**

*Why:* Auditors get read-and-audit reach across the whole Vault without any ability to use credentials: they can see that accounts exist, see who has access, read the audit trail, and review session recordings. That is precisely the separation of duties an audit function needs.

*Why not the others:* A and C over-state it — Auditors cannot retrieve or change passwords. D confuses it with the administration group. Vault Admins get the Administration tab; Safe Managers can create Safes; Security Admins and Security Operators get the Security pane for PTA events.

<sub>Source area: Built-in groups — Auditors</sub>

---

### Q73. How do you locate a specific PSM session recording?

- **A.** Browse the PSMRecordings Safe directly in the PrivateArk Client
- **B.** Use the Monitoring / Privileged Sessions page in the PVWA and filter by user, target machine, date, connection component — or by risk score where PTA is integrated
- **C.** Search PSMConsole.log for the session ID
- **D.** Run an Entitlement Report

**Answer: B**

*Why:* The Privileged Sessions page is the purpose-built search surface: it indexes sessions with their metadata so an auditor can filter to the ones that matter, then play back video and search the accompanying text/command audit. With PTA integrated, each session carries a risk score so the highest-risk sessions can be reviewed first rather than sampled at random.

*Why not the others:* A gets you encrypted objects with no session context. C tells you a session happened, not what was in it. D is an access-rights report.

<sub>Source area: Monitor sessions / review recordings</sub>

---

### Q74. What is the security value of session isolation?

- **A.** It compresses recordings to save Vault storage
- **B.** The end-user device never touches the target and never receives the credential, so malware on the endpoint cannot reach the target and a credential stolen from the endpoint cannot be replayed
- **C.** It removes the need to rotate passwords
- **D.** It reduces licence consumption

**Answer: B**

*Why:* Isolation breaks the direct path in two places at once. The session originates from the hardened PSM, not the user's workstation, so endpoint malware has no route to the target — and because the PSM injects the credential, the user never possesses it, so there is nothing on the endpoint to steal, key-log or reuse. That is what stops lateral movement.

*Why not the others:* A and D are not security properties. C is the opposite of good practice — isolation and rotation are complementary controls, not alternatives.

<sub>Source area: Security value of session isolation</sub>

---

### Q75. Beyond video playback, what makes PSM session audit valuable?

- **A.** Recordings are held on the PSM server for the fastest possible playback
- **B.** Sessions also produce searchable text, keystroke and command audit, so an auditor can search for a command across many sessions instead of watching video — and the recordings live in the Vault under Safe permissions
- **C.** Only the PSM administrator is able to view them
- **D.** It prevents a session from being recorded twice

**Answer: B**

*Why:* Video alone does not scale — nobody watches ten thousand hours of RDP. The text and command audit makes the archive searchable, so "who ran this command last quarter?" becomes a query rather than an investigation. Because recordings are stored in Vault Safes, access to them is itself governed and audited.

*Why not the others:* A is wrong on both counts: recordings are uploaded to the Vault, and speed is not the value. C is wrong — Auditors and appropriately permissioned users can review them. D is not a real concern.

<sub>Source area: Configure video and text recordings</sub>

---

## Domain 6 — Configure Session Management

### Q76. "Activate privileged session management" is enabled in the Master Policy, but users still cannot see the Connect button on an account. What else must be true?

- **A.** They need List Accounts and Use Accounts on the Safe, and the platform must have at least one enabled connection component
- **B.** They need Retrieve Accounts on the Safe
- **C.** They must be members of the Auditors group
- **D.** Session recording must be switched off

**Answer: A**

*Why:* The Connect button is the intersection of three things: the Master Policy rule that turns PSM on, the Safe permissions List + **Use** Accounts, and a connection component enabled on the platform for the session to launch with. Missing any one of them and the button is absent.

*Why not the others:* B is the trap: List + **Retrieve** produces Show and Copy — the ability to see the password — not Connect. C is for monitoring. D is unrelated; recording changes what is captured, not whether you can connect.

<sub>Source area: Safe member permissions / Master Policy — session management</sub>

---

### Q77. The exam objective "configure a split workflow" is about separating who can see a credential from who can use it. Which configuration delivers that?

- **A.** Grant List + Use Accounts so the user connects through the PSM with the credential injected, and withhold Retrieve Accounts so it is never displayed — optionally adding Split Password Mode so that even a displayed password is split between two groups
- **B.** Grant List + Retrieve Accounts and remove Use Accounts
- **C.** Disable the PSM for that platform
- **D.** Store the account in two Safes with different members

**Answer: A**

*Why:* The separation is enforced by Safe permissions. **Use Accounts** lets someone establish a session where the PSM injects the credential; **Retrieve Accounts** lets someone see it. Granting the first without the second means the user does the work but never possesses the secret. Split Password Mode (`EnableSplitPassword`, with `PasswordFirstHalfGroup` and `PasswordSecondHalfGroup` under the platform's UI & Workflows) takes it further: each group sees only half, so no one person can reconstruct the password alone.

*Why not the others:* B is exactly backwards. C removes the mechanism that makes the separation possible. D duplicates data without changing who can see the credential. Note "split workflow" is exam-objective wording rather than a literal UI term — know the mechanisms behind it.

<sub>Source area: Safe member permissions / Split Password Mode</sub>

---

### Q78. Which platform parameters implement Split Password Mode?

- **A.** EnableSplitPassword, PasswordFirstHalfGroup and PasswordSecondHalfGroup, under the platform's UI & Workflows
- **B.** SessionRecorderSafe and SessionRecorderSafeRetention
- **C.** AllowSelectHTML5 and DefaultConnectionMethod
- **D.** PSMConnectionDefault and PSMServerID

**Answer: A**

*Why:* `EnableSplitPassword` (default No) turns the feature on; the two group parameters name who sees which half. A user in both groups sees the whole password; a user in neither sees nothing at all.

*Why not the others:* B configures recording storage. C governs HTML5 versus RDP-file delivery. D sets the default connection component and PSM server. All are real parameters — which is what makes them good distractors.

<sub>Source area: Platform Management — UI and Workflows</sub>

---

### Q79. Where do you enable a connection component for a particular platform, and which parameter decides which one is offered by default?

- **A.** Platform Management → the platform → Edit → UI & Workflows → Connection Components; PSMConnectionDefault sets the default
- **B.** Options → Connection Components; DefaultConnectionMethod sets the default
- **C.** In the Master Policy; there is no default setting
- **D.** In the Safe's properties; the first component alphabetically is the default

**Answer: A**

*Why:* Connection components are **defined** globally under System Configuration → Options → Connection Components, but they are **enabled per platform** under that platform's UI & Workflows → Connection Components (add the component ID, set Enable = Yes). `PSMConnectionDefault` names the one that appears pre-selected in the connect drop-down on the Account Details page.

*Why not the others:* B mixes the two locations and misuses `DefaultConnectionMethod`, which chooses HTML5 versus an RDP file — not which component runs. C and D are invented.

<sub>Source area: Configure connection components / default connection component</sub>

---

### Q80. Which of these is NOT an out-of-the-box PSM connection component?

- **A.** PSM-RDP
- **B.** PSM-TOAD
- **C.** PSM-WebApp
- **D.** PSM-WinSCP

**Answer: C**

*Why:* There is no built-in component called PSM-WebApp. Web application access uses the specific built-ins — PSM-PVWA, PSM-MS-Azure, PSM-AWSConsoleWithSTS — or a custom/universal web connector you build or import.

*Why not the others:* The documented built-ins are PSM-SSH, PSM-OpenSSH, PSM-RDP, PSM-Telnet, PSM-TOAD, PSM-SQLPlus, PSM-VSPHERE, PSM-SQLServerMgmtStudio, PSM-MS-Azure, PSM-PVWA, PSM-AWSConsoleWithSTS, PSM-PTA and PSM-WinSCP; for PSM for SSH, PSMP-SSH, PSMP-SCP, PSMP-SFTP and PSMP-Rsync. Note the official casing is PSM-TOAD.

<sub>Source area: Options — Connection Components</sub>

---

### Q81. Which statement about the PSM HTML5 Gateway is correct?

- **A.** It runs on Windows alongside the PSM and users reach it on port 3389
- **B.** It runs on Linux (RHEL or Rocky) or in a container, users reach it over a secure WebSocket on 443, and it connects onward to the PSM over RDP
- **C.** It replaces the PSM entirely, so no PSM server is needed
- **D.** It requires a client-side Java applet on the user's workstation

**Answer: B**

*Why:* The gateway is a Linux-based service built on Apache Guacamole components (guacd plus a Tomcat-hosted web application). The browser reaches it over HTTPS/secure WebSocket on 443, and the gateway then makes the RDP connection to the PSM server. The user needs nothing but a browser — no RDP client, no downloaded .rdp file.

*Why not the others:* A gets the OS and port wrong. C is the key misconception: the gateway is a front door to the PSM, not a replacement — the PSM still isolates, injects credentials and records. D describes a much older generation of web console.

<sub>Source area: Secure access with an HTML5 Gateway</sub>

---

### Q82. The HTML5 Gateway is installed, but users still receive an RDP file. Which two conditions must both be met for HTML5 sessions? (Choose two)

- **A.** DefaultConnectionMethod (Options → Privileged Session Management UI) must be set to HTML5 — the default is RDP
- **B.** The PSM server must be associated with an enabled gateway (Configured PSM Servers → Connection Details → Add PSM Gateway, Enable = Yes)
- **C.** The Vault service must be restarted after installing the gateway
- **D.** Session recording must be disabled for HTML5 to work

**Answer: A, B**

*Why:* This is a two-condition decision and questions often name only one. The gateway must be registered (Options → Privileged Session Management → Add Configured PSM Gateway Servers, with ID, FQDN and port) **and** associated with the specific PSM server, and the delivery method must be switched from the default RDP to HTML5. HTML5 sessions are only triggered for PSM machines that have an associated gateway.

*Why not the others:* C is not required. D is false — HTML5 sessions are recorded exactly like any other PSM session. A related per-component setting, AllowSelectHTML5, lets the user choose.

<sub>Source area: Secure access with an HTML5 Gateway</sub>

---

### Q83. What does the AllowSelectHTML5 parameter on a connection component do?

- **A.** Forces every session using that component to run through HTML5
- **B.** Lets the end user choose the connection method for that connection component
- **C.** Enables the HTML5 Gateway service itself
- **D.** Sets the keyboard layout for HTML5 sessions

**Answer: B**

*Why:* `AllowSelectHTML5` sits under the connection component's User Parameters and surfaces the choice to the user, rather than forcing one method. It is a user-experience setting layered on top of the system-wide `DefaultConnectionMethod`.

*Why not the others:* A is what DefaultConnectionMethod = HTML5 does. C is done by registering and associating the gateway. D is KeyboardLayout / ServerKeyboardLayout — real parameters on the same page.

<sub>Source area: Connection component user parameters</sub>

---

### Q84. Which platform parameter decides where recordings for that platform are stored, and what is its default value?

- **A.** SessionRecorderSafe — default PSMRecordings
- **B.** RecordingsSafe — default PSM
- **C.** SessionRecorderSafeRetention — default PSMRecordings
- **D.** PSMRecordingSafe — default PSM Sessions

**Answer: A**

*Why:* `SessionRecorderSafe` lives under the platform's UI & Workflows → Privileged Session Management, and defaults to `PSMRecordings`. It accepts a fixed name or a dynamic value such as `PSM-{AccountSafeName}`, which is how you get per-team or per-application recording Safes without creating them by hand.

*Why not the others:* B and D are plausible-sounding names that do not exist. C is a real parameter but it sets the retention period in days, not the Safe name — and it only applies to recording Safes created after it is set.

<sub>Source area: Platform Management — UI and Workflows</sub>

---

### Q85. When is a recording Safe created?

- **A.** During PSM installation, alongside the other PSM Safes
- **B.** When the first recording is uploaded to it — the PSM creates it automatically, using the PSMAppUsers group
- **C.** When the platform is duplicated
- **D.** Only manually, by a member of Safe Managers

**Answer: B**

*Why:* Recording Safes are created on demand. When the PSM has a recording to upload and the Safe named by `SessionRecorderSafe` does not yet exist, it is created at that moment. This is exactly why a dynamic value like `PSM-{AccountSafeName}` works — the Safes materialise as sessions occur.

*Why not the others:* A is a common wrong answer: PSM installation creates PSM, PSMLiveSessions, PSMNotifications, PSMRecordings-related infrastructure Safes and others, but a *custom* recording Safe is not among them. C and D are not the mechanism.

<sub>Source area: Configure video and text recordings</sub>

---

### Q86. Which group is added to recording Safes with all authorizations because it manages them?

- **A.** PSMAppUsers
- **B.** PSMMaster
- **C.** Auditors
- **D.** PVWAGWAccounts

**Answer: B**

*Why:* `PSMMaster` is described as the group that manages the Safes where recordings are stored, and it is added to Recording Safes with all authorizations.

*Why not the others:* A is close and worth separating carefully: PSMAppUsers retrieves configuration from the Vault, **creates** Recording Safes and uploads recordings. C get read access to all Recording Safes automatically, for review. D are the gateway accounts that make playback through the PVWA possible. Exam tactic: "manages" → PSMMaster; "creates and uploads" → PSMAppUsers.

<sub>Source area: Privileged Session Manager environment</sub>

---

### Q87. Where do you enable live session monitoring, and what is the difference between MonitoringLevel = View and MonitoringLevel = Control?

- **A.** Configuration Options → Privileged Session Management → General Settings → Server Settings → Live Sessions Monitoring Settings; View means watch only, Control means watch and take control of the session
- **B.** In the Master Policy; View means read-only recordings and Control means the ability to delete them
- **C.** In the Safe's properties; there is no functional difference
- **D.** In Basic_psm.ini; Control means terminate

**Answer: A**

*Why:* The Live Sessions Monitoring Settings node carries `AllowMonitor`, `MonitoringLevel`, `AllowTerminate` and `AllowPSMNotifications`. `View` gives an over-the-shoulder view of the live session; `Control` additionally lets the observer take control and intervene — which is a materially different privilege and should be granted deliberately.

*Why not the others:* B confuses live monitoring with recording review. C and D put the setting in the wrong place. Additional users and groups are added under the Terminating and Suspending Live Sessions nodes.

<sub>Source area: Active session monitoring in PSM</sub>

---

### Q88. Which group can terminate live sessions by default, and what else gates that ability?

- **A.** PSMLiveSessionTerminators, gated by AllowTerminate and by the members' own Safe ownership
- **B.** Auditors, gated by AllowMonitor
- **C.** Vault Admins, with no additional gate
- **D.** PSMMaster, gated by MonitoringLevel

**Answer: A**

*Why:* Members of `PSMLiveSessionTerminators` can suspend, terminate and resume live privileged sessions — but only where `AllowTerminate` is enabled and only for sessions on Safes they own. Both the group and the setting are needed.

*Why not the others:* B — Auditors can watch, not terminate. C — Vault Admins get the Administration tab; live-session control is not automatic. D — PSMMaster manages recording Safes.

<sub>Source area: Active session monitoring in PSM</sub>

---

### Q89. What is a PSM shadow user (PSM-<userid>)?

- **A.** A Vault user automatically created for each auditor
- **B.** A local Windows user created automatically on the PSM server for each Vault user, used for non-RDP-file connections, whose credentials are reset on every connection
- **C.** The account used to log on to the target machine
- **D.** The service account that runs the AppLocker configuration script

**Answer: B**

*Why:* Shadow users give each Vault user their own isolated Windows session on the PSM server, rather than everyone sharing one. They are created on demand, their passwords are reset at every connection, and they belong to the local `PSMShadowUsers` group — which must retain the "Allow log on locally" right.

*Why not the others:* A confuses them with Vault users. C is the managed target account, injected by the PSM. D is not a thing.

<sub>Source area: PSM shadow users</sub>

---

### Q90. What is the difference between PSMConnect and PSMAdminConnect?

- **A.** PSMConnect is the local Windows user under which end-user privileged sessions run; PSMAdminConnect is the local user used to monitor live sessions
- **B.** They are the Vault users the CPM uses to manage the PSM
- **C.** PSMAdminConnect uploads recordings to the Vault; PSMConnect records them
- **D.** They are the two HTML5 Gateway service accounts

**Answer: A**

*Why:* Both are local Windows users on the PSM server created at installation. Sessions initiated by end users run under `PSMConnect`; an auditor watching a live session connects as `PSMAdminConnect`, which is what keeps the observer's session separate from the session being observed.

*Why not the others:* B — the CPM does not manage the PSM. C — uploads are performed by the PSM application user in the PSMAppUsers group. D — the gateway is a separate Linux component with no such accounts.

<sub>Source area: PSM environment — local users</sub>

---

### Q91. Which two statements about PSM ad hoc (Secure Connect) sessions are correct? (Choose two)

- **A.** They are based on the PSMSecureConnect platform and allow connections using accounts that are not managed in PAM
- **B.** SSH keys can be used with unmanaged accounts in an ad hoc connection
- **C.** Access must be restricted by naming users or groups under Secure Connect Settings, after which only those users can start ad hoc connections
- **D.** Ad hoc sessions cannot be recorded

**Answer: A, C**

*Why:* Ad hoc connections let a user reach a machine through the PSM using credentials supplied at connect time, including accounts CyberArk does not manage. Because that is powerful, access is restricted by naming permitted users or groups under Secure Connect Settings — and subnet limits can be added with Connect User Access rules plus EnforceSubnetRules = Yes.

*Why not the others:* B is explicitly not supported: SSH keys cannot be used with unmanaged ad hoc accounts. D is false — ad hoc sessions are still recorded, with the recording Safe configurable per ad hoc platform. The real caveat is that the credentials used are not vaulted, so some of the PSM's security benefit is lost.

<sub>Source area: Configure ad hoc connections</sub>

---

### Q92. SessionRecorderSafeRetention is set to 90 on a platform. What does that mean, and what is the catch?

- **A.** Recordings older than 90 days are deleted — but the setting only takes effect for recording Safes created after it is configured, so existing Safes keep their original retention
- **B.** Only the last 90 recordings are kept per account
- **C.** The recording Safe is capped at 90 MB
- **D.** Individual sessions are cut off after 90 minutes

**Answer: A**

*Why:* `SessionRecorderSafeRetention` sets, in days, how long recordings are kept before deletion. The catch is that it is applied when the recording Safe is created — changing it later does not retroactively re-configure Safes that already exist; those must be adjusted at Safe level.

*Why not the others:* B describes version retention on a Safe. C is MaxSafeSize (default 50 MB in the template). D would be a session duration limit, which is set at platform level — and note that PSM active/idle session limits should be set to Never in the Windows session settings to avoid corrupted recordings.

<sub>Source area: Platform Management — UI and Workflows</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q93. Which statement about Vault-level and Safe-level authorizations is correct?

- **A.** Vault authorizations are assigned to individual users in the PrivateArk Client and are not inherited through groups; Safe permissions can be granted to users or groups and are inherited through group membership
- **B.** Both are assigned in the PVWA and both are inherited
- **C.** Vault authorizations are inherited from groups, Safe permissions are not
- **D.** Safe permissions can only ever be granted to individual users

**Answer: A**

*Why:* Two planes, two sets of rules. Vault authorizations (Add Safes, Audit Users, Manage Users, Backup All Safes, Restore All Safes, Manage Directory Mapping…) are per-user, set in the PrivateArk Client, and never inherited. Safe permissions are set in the PVWA or the PrivateArk Client, can be given to users **or** groups, and are inherited by group members. This distinction is examined repeatedly.

*Why not the others:* B, C and D each get one half backwards. The practical consequence of the real rule: always grant Safe permissions to groups, because permissions assigned directly to a user are lost if that user is ever deleted and recreated.

<sub>Source area: Vault and Safe authorizations</sub>

---

### Q94. A leaver's LDAP-mapped Vault user is deleted in the PrivateArk Client, but the user reappears the next day. Why, and what is the correct action?

- **A.** A backup restore recreated the user; restore again from an earlier point
- **B.** The user still exists in the directory and still matches a Directory Mapping, so they are recreated at their next authentication — remove them from the mapped LDAP group or disable the directory account instead
- **C.** The Vault caches deleted users for 24 hours before purging them
- **D.** AutoSyncExternalObjects must be disabled first

**Answer: B**

*Why:* Transparent (LDAP) users are provisioned on demand. Deleting the Vault object removes the local record, not the eligibility — as soon as the person authenticates again and still matches a mapping, the user is recreated. The fix belongs in the directory: remove them from the mapped group, or disable the account. And note what deletion costs you: any Safe permissions assigned to that user individually are gone, while group-derived permissions come straight back.

*Why not the others:* A and C invent mechanisms. D — AutoSyncExternalObjects governs synchronisation of external objects on a schedule, and disabling it does not stop on-demand provisioning at logon.

<sub>Source area: LDAP integration — transparent users</sub>

---

### Q95. A Directory Mapping specifies a User Template. When is that template applied?

- **A.** Every time a mapped user logs on, so template changes propagate to everyone
- **B.** Only at the user's first authentication — later changes to the template do not retroactively affect users who already exist
- **C.** When the CPM next completes a processing loop
- **D.** Never; the template is documentation only

**Answer: B**

*Why:* The User Template supplies the initial properties — authentication method, group memberships, Vault authorizations, restrictions — at the moment the transparent user is first created. After that the user is an independent object, so editing the template changes what *future* users get, not what existing ones have.

*Why not the others:* A is the intuitive assumption and the reason this is examined: administrators change a template expecting a fleet-wide update and get nothing. C and D are unrelated to the mechanism.

<sub>Source area: Directory mapping — user templates</sub>

---

### Q96. Which built-in user is the only one able to configure the LDAP integration and edit Directory Mappings?

- **A.** Master
- **B.** Administrator
- **C.** Auditor
- **D.** DR

**Answer: B**

*Why:* The **Administrator** user holds full Vault authorizations, installs the components, and is the only user who can configure LDAP integration and edit Directory Mappings. This is a favourite recall question.

*Why not the others:* A — the Master user has full, unremovable authorizations but is a break-glass identity: PrivateArk Client only, from the Vault console or the EmergencyStationIP, requiring the Master password and the Recovery private key. It is not for day-to-day configuration. C holds only the Audit Users authorization. D is the disaster-recovery user, an automatic owner of every Safe with Backup All Safes and Restore All Safes.

<sub>Source area: Built-in Vault users</sub>

---

### Q97. CyberArk Vendor PAM (Remote Access) is best described as:

- **A.** An on-premises VPN concentrator dedicated to third parties
- **B.** A SaaS service giving external third parties privileged access on Zero Trust principles — biometric MFA through the CyberArk Mobile app and just-in-time provisioning, with no VPN, no agent and no vendor password
- **C.** A drop-in replacement for the PSM
- **D.** A reporting add-on for the PVWA

**Answer: B**

*Why:* Vendor PAM is Remote Access bundled with PAM (Self-Hosted or Privilege Cloud). Remote Access itself is a SaaS service combining Zero Trust access, biometric authentication and just-in-time provisioning for remote vendors, consultants and maintenance personnel — the point being that the vendor needs no VPN, no installed agent and no credential of their own.

*Why not the others:* A describes the legacy approach it replaces. C — it works **with** the PSM, brokering the vendor's session through it. D understates it entirely.

<sub>Source area: Remote Access — get started</sub>

---

### Q98. Which component of Remote Access sits inside the customer's network and holds the secure data keys and certificates?

- **A.** The CyberArk Mobile app
- **B.** The Remote Access Connector — a container deployed behind the firewall, which also acts as a SAML identity provider and runs the VendorLDAP directory used to provision vendor users
- **C.** The Remote Access cloud tenant
- **D.** The PVWA

**Answer: B**

*Why:* The connector is what keeps the customer in control of their own secrets. It runs behind the firewall, holds the secure data keys and unique private certificates, acts as a SAML IdP, and runs a standalone OpenLDAP directory (VendorLDAP) whose certificate is installed on the Vault machine — a "VendorLDAP <site name>" directory then appears in the PVWA, and Directory Mappings map vendor users and groups to Vault objects, Safes and authentication methods.

*Why not the others:* A performs the biometric authentication. C orchestrates between the app and the connector but deliberately does not hold customer secrets. D is the PAM web interface. Note the fourth component: an internally deployed HTML5 Gateway that converts the inbound web protocol to outbound RDP over TLS.

<sub>Source area: Remote Access — architecture</sub>

---

### Q99. How does a vendor authenticate to Remote Access, and where is the biometric data held?

- **A.** A password plus SMS one-time code; biometric templates are stored in the cloud tenant
- **B.** Biometric authentication in the CyberArk Mobile app, enrolled with a unique, one-time, time-limited QR code — the biometric data stays on the phone and is never sent to or stored in the cloud service
- **C.** A smart card issued by the customer's PKI
- **D.** An LDAP password checked against the customer's Active Directory

**Answer: B**

*Why:* Enrolment is a one-time, time-limited QR code scanned with the CyberArk Mobile app; thereafter the vendor authenticates biometrically on their own device. The biometric never leaves the phone and is never stored in the cloud service — which is what makes the model deployable across vendors without a credential-issuance process.

*Why not the others:* A is a conventional MFA design and is not how this works — and the claim about cloud-stored biometrics is specifically wrong. C would require issuing hardware to every third party. D would require creating directory accounts for vendors, which the whole design avoids.

<sub>Source area: Remote Access — architecture and authentication</sub>

---

### Q100. A vendor connects through Vendor PAM to a Windows server. What happens to the target's credential?

- **A.** It is emailed to the vendor for the duration of the engagement
- **B.** The vendor never receives it — the session is brokered through the portal to the PSM via the internally deployed HTML5 Gateway, so the credential stays in the Vault and the session is isolated, monitored and recorded
- **C.** The vendor's own directory account is used instead
- **D.** It is stored in the Remote Access cloud tenant for the session

**Answer: B**

*Why:* This is the whole value proposition. Remote Access handles who the vendor is and whether they should have access right now; PAM handles the credential. The vendor lands in the PVWA or Privilege Cloud portal and connects through the PSM, so the credential is injected, never displayed, and the session is isolated, recorded and auditable exactly like an employee's.

*Why not the others:* A defeats the purpose. C would require provisioning directory accounts for third parties — the thing JIT provisioning exists to avoid. D is specifically not how it works: the connector keeps keys and certificates on the customer side, and the credential never leaves the Vault.

<sub>Source area: Connect to targets using Remote Access</sub>

---

## Domain 1 — Onboard Accounts

### Q101. PTA-driven Continuous Accounts Discovery can automatically onboard an unmanaged privileged account it sees being used. Which target types does it support out of the box?

- **A.** Windows only
- **B.** Windows, UNIX, AWS and Azure — anything else needs a custom PTA plug-in
- **C.** Any platform that exists in the Vault
- **D.** Only cloud platforms

**Answer: B**

*Why:* Continuous discovery is PTA noticing a connection made with a privileged account that is not stored in the Vault, and reacting. Out of the box that detection-and-onboard path covers Windows, UNIX, AWS and Azure; extending it to anything else means writing a custom PTA plug-in. PTA also continuously monitors Windows local Administrators groups for newly privileged accounts.

*Why not the others:* A is too narrow, C too broad, D omits the two on-premises platforms that make up most of the value.

<sub>Source area: PTA continuous discovery</sub>

---

### Q102. When an onboarding rule is created through the REST API, which filter is mandatory?

- **A.** `UserNameFilter`
- **B.** `SystemTypeFilter` — Windows or Unix
- **C.** `AddressFilter`
- **D.** `IsAdminIDFilter`

**Answer: B**

*Why:* `SystemTypeFilter` is the one mandatory filter, alongside the mandatory targets `TargetPlatformId` and `TargetSafeName`. Everything else — username, address, machine type, account category — is optional narrowing.

*Why not the others:* A, C and D are all real optional filters. `UserNameFilter` is capped at 512 characters and pairs with `UserNameMethod`; `AddressFilter` pairs with `AddressMethod`; `IsAdminIDFilter` is a boolean.

<sub>Source area: Add onboarding rule (REST)</sub>

---

### Q103. An onboarding rule's `UserNameMethod` and `AddressMethod` accept which values?

- **A.** Equals, Begins, Ends
- **B.** Contains, Regex, Exact
- **C.** Include, Exclude
- **D.** StartsWith, EndsWith, Wildcard

**Answer: A**

*Why:* Both matching methods take Equals, Begins or Ends. That is deliberately simple — rules are meant to be predictable and auditable, so there is no regular-expression matching here.

*Why not the others:* B, C and D all offer richer matching than the rule engine actually supports. Note the contrast with `AllowedSafes` on a platform, which *is* a regular expression — do not mix the two up.

<sub>Source area: Add onboarding rule (REST)</sub>

---

### Q104. Which values can an onboarding rule's Machine type and Account category filters take?

- **A.** Machine type: Any / Workstation / Server. Account category: Any / Privileged / Non-privileged
- **B.** Machine type: Windows / Unix. Account category: Local / Domain
- **C.** Machine type: Physical / Virtual. Account category: Service / Interactive
- **D.** Machine type: Server / Endpoint. Account category: Tier 0 / Tier 1 / Tier 2

**Answer: A**

*Why:* `MachineTypeFilter` is Any, Workstation or Server; `AccountCategoryFilter` is Any, Privileged or Non-privileged. Together with system type and a keyword these are what let you route, say, privileged accounts on servers into one Safe and workstation accounts into another.

*Why not the others:* B confuses machine type with system type. C and D invent categories that do not exist in the rule dialog.

<sub>Source area: Manage onboarding rules</sub>

---

### Q105. You want a Windows discovery to run every week rather than once. Where is that set?

- **A.** It cannot be — discovery is always a one-off and must be re-run manually
- **B.** In the Accounts Discovery definition itself, which supports a one-time scan or a recurring schedule
- **C.** With a Windows scheduled task on the CPM server calling the scanner binary
- **D.** In the Master Policy

**Answer: B**

*Why:* Recurrence is part of the discovery definition in the PVWA. Making the scan recurring is what turns discovery from a one-off inventory exercise into an ongoing control, so newly created privileged accounts keep surfacing in Pending Accounts.

*Why not the others:* A and C describe workarounds for a capability that is built in. D is unrelated — the Master Policy governs access workflows, not discovery.

<sub>Source area: Accounts Discovery</sub>

---

### Q106. Which permission does a user need to obtain a copy of an SSH private key stored in the Vault?

- **A.** Use Accounts
- **B.** List Accounts
- **C.** Retrieve Accounts
- **D.** Initiate CPM account management operations

**Answer: C**

*Why:* An SSH private key is retrieved exactly like a password: List Accounts to see it, Retrieve Accounts to get a copy of the secret itself. This is why the same split-workflow logic applies — a user who only needs to connect gets Use, not Retrieve.

*Why not the others:* A gives Connect through the PSM, not the key material. B only reveals that the account exists. D exposes the Change / Verify / Reconcile buttons.

<sub>Source area: Safe member permissions / SSH key management</sub>

---

### Q107. Besides Windows Services, Scheduled Tasks and IIS Application Pools, which two dependency types can Windows discovery detect? (Choose two)

- **A.** IIS Anonymous Access
- **B.** COM+ Applications
- **C.** Registry keys holding credentials
- **D.** ODBC connection strings

**Answer: A, B**

*Why:* The discoverable set is Windows services, scheduled tasks, IIS application pools, IIS anonymous access and COM+ applications — all of them registered in a machine's own configuration surface, so they can be enumerated programmatically.

*Why not the others:* C and D are credentials embedded in arbitrary storage. The CPM can manage them once you add them by hand, but nothing can reliably find them by scanning.

<sub>Source area: Dependent accounts / supported usages</sub>

---

### Q108. Which onboarding sources use the "Add discovered accounts" REST method? (Choose three)

- **A.** The CPM Scanner
- **B.** PTA
- **C.** DNA (Discovery & Audit)
- **D.** PARestore

**Answer: A, B, C**

*Why:* "Add discovered accounts" is the ingestion path for anything that *discovers* — the CPM Scanner, PTA's continuous discovery, DNA and third-party scanners. Crucially, accounts arriving this way are evaluated against the automatic onboarding rules; accounts added with the plain "Add account" method are not.

*Why not the others:* D is a backup restore utility, not a discovery source.

<sub>Source area: Onboard accounts and SSH keys</sub>

---

### Q109. Which statement about manually adding an account in the PVWA is correct?

- **A.** The address, username, platform and Safe are all required; the platform then determines which additional properties are mandatory
- **B.** Only the username and password are required
- **C.** The Safe is optional and defaults to PasswordManagerShared
- **D.** The platform is chosen automatically from the address

**Answer: A**

*Why:* Every account needs a location on the network (address), an identity (username), a Safe to live in and a target account platform to be governed by. The platform then dictates the rest — some platforms add mandatory properties such as a port, database name or domain.

*Why not the others:* B omits the two structural requirements. C and D are wrong: neither Safe nor platform is ever inferred, because both are deliberate access-control and policy decisions.

<sub>Source area: Add accounts</sub>

---

### Q110. PTA has detected an unmanaged AWS IAM access key in use. Which automatic remediation actions can PTA take? (Choose three)

- **A.** Onboard the unmanaged account into the Vault
- **B.** Rotate the credential
- **C.** Reconcile the credential
- **D.** Delete the IAM user

**Answer: A, B, C**

*Why:* PTA's automatic containment set is onboard, rotate and reconcile — bringing the credential under management and invalidating whatever the attacker may hold. For AWS specifically it detects unmanaged access keys and passwords for IAM accounts, compromised privileged IAM accounts and compromised EC2 accounts.

*Why not the others:* D is destructive and outside PTA's remit — containment is about taking control of the credential, not deleting the identity. Where PSM is integrated, PTA can also suspend or terminate a live session.

<sub>Source area: PTA — respond / automatic remediation</sub>

---

### Q111. Which onboarding path evaluates accounts against the automatic onboarding rules?

- **A.** "Add account" in the PVWA
- **B.** "Add multiple accounts from a file" (bulk CSV upload)
- **C.** "Add discovered accounts" — the path used by the CPM Scanner, PTA and DNA
- **D.** Restoring a Safe with PARestore

**Answer: C**

*Why:* Onboarding rules exist to triage *discovered* accounts. Only accounts arriving through the discovery ingestion path are compared against them; if none matches, the account lands in Pending Accounts for a human to place.

*Why not the others:* A and B are both deliberate acts where the operator has already chosen the Safe and platform, so there is nothing for a rule to decide. D is a restore operation.

<sub>Source area: Manage onboarding rules</sub>

---

### Q112. What must the first row of a bulk-upload CSV contain?

- **A.** The Safe name that all accounts will go into
- **B.** A header row of account property names
- **C.** A count of the accounts in the file
- **D.** The platform ID

**Answer: B**

*Why:* The first row is a header naming the properties each column carries, so the upload can map columns to account properties — including platform-specific ones. Downloading the sample CSV from the Add accounts from file window is the reliable way to get the header right.

*Why not the others:* A and D are per-account column values, not file-level headers — different rows can target different Safes and platforms. C is not part of the format.

<sub>Source area: Add multiple accounts from a file</sub>

---

### Q113. Before an onboarding rule that references a reconcile account can run successfully, what must be true?

- **A.** The reconcile account must already exist, per the rule's definition, alongside the target Safe
- **B.** The CPM will create the reconcile account on first use
- **C.** Reconcile accounts cannot be referenced by onboarding rules
- **D.** The reconcile account must be in the Pending Accounts list

**Answer: A**

*Why:* The documented prerequisite is to create the Safe *and* the reconcile account according to the rule's definition before the rule runs. A rule places accounts into a prepared structure; it does not build the structure.

*Why not the others:* B — nothing is auto-created. C is false. D confuses a working reconcile account with a discovered one.

<sub>Source area: Add onboarding rule — prerequisites</sub>

---

### Q114. Which of these best describes how CyberArk now recommends sequencing an onboarding programme?

- **A.** Onboard the largest account populations first to show rapid coverage numbers
- **B.** Work through a risk-versus-effort prioritisation — highest risk reduction for lowest implementation effort first
- **C.** Follow the five Blueprint stages in strict order
- **D.** Onboard alphabetically by Safe name so nothing is missed

**Answer: B**

*Why:* The Blueprint's five-stage model was retired in August 2024 and replaced by a risk-effort index: a prioritisation matrix weighing the risk impact of a use case against the effort to implement it. In practice that still puts Tier 0 first, but the framing is now explicitly about return on effort rather than a fixed sequence.

*Why not the others:* A optimises for a metric that does not reduce risk. C is the retired model — still taught in v12.6 material, so know it exists, but know it has been superseded. D is arbitrary.

<sub>Source area: CyberArk Blueprint — risk-effort index</sub>

---

### Q115. Which statement about discovered SSH keys is correct?

- **A.** They are discovered by Windows discovery
- **B.** UNIX discovery returns them along with local accounts, including the trust relationships between machines
- **C.** They can only be added manually
- **D.** They are stored outside the Vault, on the CPM

**Answer: B**

*Why:* UNIX discovery enumerates local accounts and SSH keys, and mapping the authorized/trusted key relationships is often the more valuable output — key-based trust paths are exactly how an attacker moves laterally across a UNIX estate.

*Why not the others:* A — Windows discovery has no SSH keys to find. C is false. D is false: keys are vaulted objects, protected like any other secret. Note that once a key is imported it should be rotated immediately, because the act of entering it exposed it.

<sub>Source area: Accounts Discovery — UNIX / onboard SSH keys</sub>

---

## Domain 2 — Manage the Application

### Q116. Which ports does PTA use to communicate with the Vault and the DR Vault?

- **A.** TCP 443 only
- **B.** TCP and UDP 1858
- **C.** TCP 9022
- **D.** UDP 514

**Answer: B**

*Why:* PTA needs both TCP and UDP on 1858 to the Vault and to the DR Vault — it consumes the Vault's activity stream as well as making requests. Administrator access to the PTA itself is over TCP 80/443.

*Why not the others:* A is the PVWA's user-facing port. C is the Remote Control Client to PARAgent. D is syslog, which is how PTA *receives* logs from other sources, not how it talks to the Vault.

<sub>Source area: PTA — operational notes</sub>

---

### Q117. PVWA-to-PTA calls have started failing. Which account is involved, and what is the documented remedy?

- **A.** `PVWAGWUser` — recreate its credential file
- **B.** `PTA_PAS_Gateway` — re-sync the PTA Vault users by running `VaultPermissionsValidation.sh` in the PTA server's utility folder
- **C.** `PasswordManager` — reset its password in the PrivateArk Client
- **D.** `Backup` — enable the user and set a password

**Answer: B**

*Why:* `PTA_PAS_Gateway` is the account used for REST calls between the PVWA and PTA. When that link breaks, the fix is to re-synchronise the PTA Vault users and that account by running `VaultPermissionsValidation.sh` from the utility folder on the PTA server — reachable with the `UTILITYDIR` alias.

*Why not the others:* A is the PVWA's gateway impersonation user. C is the CPM's user. D is the backup user used by PAReplicate.

<sub>Source area: PTA — operational notes</sub>

---

### Q118. From version 14.0 onwards, where are PTA settings configured?

- **A.** Only on the PTA appliance's own console
- **B.** In the PVWA interface
- **C.** In `dbparm.ini` on the Vault
- **D.** In the PrivateArk Client

**Answer: B**

*Why:* Version 14.0 moved PTA settings into the PVWA, alongside CIS Level 2 hardening on RHEL 8, event closure reasons and richer email notifications carrying Event and Session IDs. It is a good example of the general direction: configuration consolidating into the web interface.

*Why not the others:* A was the older model. C configures the Vault, not PTA. D manages Vault users, groups and Safes.

<sub>Source area: PTA — version notes</sub>

---

### Q119. What is the purpose of listing more than one address in a component's `Vault.ini`?

- **A.** Load balancing across multiple production Vaults
- **B.** Failover — the component tries the next address if the first is unreachable, which is how components find the DR Vault after a failover
- **C.** Replication configuration
- **D.** Specifying the PVWA and the Vault together

**Answer: B**

*Why:* `Vault.ini` holds the Vault's address and port, and multiple addresses can be listed comma-separated. On failover the component works down the list, which is what lets CPMs, PVWAs and PSMs reattach to the DR Vault without being reconfigured by hand.

*Why not the others:* A — the Vault is not load balanced this way. C is `PADR.ini`. D — the PVWA is not referenced in Vault.ini.

<sub>Source area: Vault.ini / DR failover</sub>

---

### Q120. A task requires setting a Vault-level authorization and creating a Network Area. Which interface do you use?

- **A.** The PVWA
- **B.** The PrivateArk Client
- **C.** PACLI
- **D.** The Remote Control Client

**Answer: B**

*Why:* The PrivateArk Client is the administrative interface for Vault-level objects: users and their Vault authorizations, groups, Network Areas, Safe properties such as the Restrictions tab, and Safe renaming. The PVWA is the day-to-day interface for accounts, Safes membership, platforms and policy.

*Why not the others:* A does not expose Network Areas. C is a scripting interface to Vault data. D controls Vault services remotely over 9022.

<sub>Source area: PAM interfaces</sub>

---

### Q121. Which component sends email notifications from the Vault, and which Safe supports it?

- **A.** The PVWA, using `PVWAConfig`
- **B.** The ENE (Event Notification Engine), using the `Notification Engine` Safe
- **C.** The CPM, using `PasswordManagerShared`
- **D.** PTA, using `VaultInternal`

**Answer: B**

*Why:* The Notification Engine is one of the three Safes created at Vault installation — `Notification Engine`, `System` and `VaultInternal` — and the ENE service uses it to hold notification configuration and templates. It relays over SMTP on port 25, and writes `ENEConsole.log` and `ENETrace.log`.

*Why not the others:* A, C and D each name a real Safe belonging to a different component. `PVWAConfig` holds `PVConfiguration.xml` and `Policies.xml`; `PasswordManagerShared` holds platform definitions.

<sub>Source area: ENE / built-in Safes</sub>

---

### Q122. Which file holds the Vault's SNMP settings, and which parameters would you set there?

- **A.** `dbparm.ini` — `Syslog`, `SyslogServerIP`
- **B.** `paragent.ini` — `SNMPHostIP`, `SNMPTrapPort`, `SNMPCommunity`
- **C.** `tsparm.ini` — `SNMPTarget`
- **D.** `my.ini` — `Server-id`

**Answer: B**

*Why:* `paragent.ini` configures the Remote Control Agent, and SNMP trap delivery is part of that agent's job — hence `SNMPHostIP`, `SNMPTrapPort` and `SNMPCommunity` living there rather than in the main Vault configuration.

*Why not the others:* A is where syslog/SIEM forwarding is configured — a different monitoring channel. C defines where the Safes are located on disk. D is database configuration.

<sub>Source area: paragent.ini / SNMP integration</sub>

---

### Q123. Which statement about forwarding Vault audit data to a SIEM is correct?

- **A.** It is configured in `dbparm.ini` and sent over syslog, typically on port 514
- **B.** It requires EVD to run on a schedule
- **C.** It is configured in the PVWA under Reports
- **D.** It uses the Remote Control Agent on 9022

**Answer: A**

*Why:* Syslog forwarding is a Vault-level setting in `dbparm.ini`, streaming audit records continuously to the SIEM over port 514 (TLS, TCP or UDP). Like every `dbparm.ini` change it needs a Vault restart to take effect.

*Why not the others:* B describes EVD, which is a pull-based export for custom reporting rather than a continuous feed. C generates reports into `PVWAReports`. D is service control.

<sub>Source area: SIEM / syslog integration</sub>

---

### Q124. Why does CyberArk care about NTP configuration across PAM components?

- **A.** It is only cosmetic — log timestamps look neater
- **B.** Clock skew breaks Kerberos authentication, certificate validation and the correlation of audit records across components
- **C.** NTP is required for the Vault licence to validate
- **D.** It controls the CPM processing interval

**Answer: B**

*Why:* Time is load-bearing in a PAM deployment. Kerberos rejects tickets outside a tight clock skew window, certificate validity checks depend on accurate time, and any forensic reconstruction depends on Vault, CPM, PSM and target logs agreeing on when things happened. Windows components are typically pointed at a reliable source with `w32tm /config /manualpeerlist:… /syncfromflags:manual /reliable:YES /update`.

*Why not the others:* A trivialises a real dependency. C and D are invented.

<sub>Source area: NTP integration</sub>

---

### Q125. What is the maximum size of a Distributed Vault deployment?

- **A.** Two servers — one primary and one DR
- **B.** Six servers — one Primary and five Satellites
- **C.** Ten servers in an active-active cluster
- **D.** Unlimited, limited only by licence

**Answer: B**

*Why:* A Distributed Vault tops out at six servers: one Primary plus five Satellites. Satellites serve read requests locally to reduce latency for geographically dispersed sites, while writes go to the Primary.

*Why not the others:* A describes a classic Vault plus DR pair. C confuses it with Cluster Vault, which is a two-node active-passive arrangement for local high availability. D is wrong — the limit is architectural.

<sub>Source area: Distributed Vaults</sub>

---

## Domain 3 — Perform Ongoing Maintenance & Troubleshooting

### Q126. You need deeper LDAP logging on the Vault. Which form does the `DebugLevel` entry in `dbparm.ini` take?

- **A.** A single number from 0 to 6
- **B.** Named modules with levels, e.g. `DebugLevel=LDAP(14,15)` or `DebugLevel=PE(1),PERF(1)`
- **C.** `DebugLevel=High`
- **D.** `DebugLevel=Trace`

**Answer: B**

*Why:* Vault debugging is per-module: you name the module and the levels you want, such as `PE(1),PERF(1)` for the policy engine and performance, or `LDAP(14,15)` for directory troubleshooting. That keeps `Trace.d0`–`Trace.d4` focused instead of drowning you in everything at once.

*Why not the others:* A is the CPM's `CPMDebugLevels` scale (0 none, 1 exceptions, 2 trace, 3–6 CASOS). C is the PVWA's style. D is not a valid value. Remember the change needs a Vault service restart.

<sub>Source area: Configuring debug levels</sub>

---

### Q127. Which values do the PVWA's `DebugLevel` and `InformationLevel` settings take?

- **A.** 0 to 6
- **B.** None, Low, High, Profiling
- **C.** 1 to 7
- **D.** Yes / No

**Answer: B**

*Why:* The PVWA uses named levels — None, Low, High and Profiling. Profiling is the heaviest and is for performance investigations rather than routine troubleshooting; leaving it on in production will fill the log folder quickly.

*Why not the others:* A is the CPM's scale. C is the PSM server trace range (the Recorder and Client sub-levels are 1–2). D is not a debug scale.

<sub>Source area: Configuring debug levels</sub>

---

### Q128. A PSM issue needs deeper tracing. Which statement about PSM `TraceLevels` is correct?

- **A.** There is a single level from 1 to 7 covering everything
- **B.** The Server level runs 1–7, while the Recorder and Client levels each run 1–2
- **C.** It is a Yes/No switch
- **D.** It is set in the Master Policy

**Answer: B**

*Why:* PSM tracing is split by subsystem: the PSM server itself has the widest range at 1–7, while the recorder and the client each have just two levels. Raising only the subsystem you suspect keeps the logs readable.

*Why not the others:* A misses the split. C describes the DR service's `EnableTrace=yes`. D is where access policy lives, not diagnostics.

<sub>Source area: Configuring debug levels</sub>

---

### Q129. Which two `PADR.ini` parameters determine how often the DR Vault replicates and how quickly it notices the production Vault is gone? (Choose two)

- **A.** `ReplicateInterval` — seconds between replications, default 3600
- **B.** `CheckInterval` — seconds between availability checks, default 60
- **C.** `EnableDbsync`
- **D.** `AccessVaultForInactivity`

**Answer: A, B**

*Why:* `ReplicateInterval` (3600 seconds, i.e. hourly) sets the data replication cadence. `CheckInterval` (60 seconds) is how often the DR service probes the production Vault; combined with `CheckRetriesCount` of 4 and a 30-second gap between retries, that is how long it takes before failover logic engages.

*Why not the others:* C controls database synchronisation and D controls whether the DR service accesses the Vault to test for inactivity — both real parameters, neither of which sets these two intervals. `EnableFailover` and `FailoverMode` govern whether failover happens at all.

<sub>Source area: PADR.ini</sub>

---

### Q130. Put the DR failover steps into the correct order.

- **A.** Start the PrivateArk Server → synchronise the database → start ENE → stop the DR service
- **B.** Synchronise the database → start the PrivateArk Server → start ENE → stop the DR service
- **C.** Stop the DR service → start the PrivateArk Server → synchronise the database → start ENE
- **D.** Start ENE → synchronise the database → start the PrivateArk Server → stop the DR service

**Answer: B**

*Why:* Synchronise first so the DR Vault holds the most complete data set available, then bring the Vault service up on that data, then start the notification engine, and only then stop the DR replication service — because while it is running it will keep trying to behave like a replica.

*Why not the others:* The other orders either start the Vault on unsynchronised data or stop the DR service before the Vault is serving, which is how people lose the last replication increment.

<sub>Source area: DR failover</sub>

---

### Q131. Production has been rebuilt and you are failing back from the DR Vault. What does the failback procedure require?

- **A.** Set `FailoverMode=No`, delete the last two lines of `PADR.ini` to force a full replication, and restart the DR service
- **B.** Reinstall the DR Vault from scratch
- **C.** Run `PARestore` against the production Vault
- **D.** Nothing — failback is automatic once production responds

**Answer: A**

*Why:* The last two lines of `PADR.ini` hold the replication position. Removing them makes the DR service forget where it was and perform a full replication rather than an incremental one, which is what you want when the production Vault's data has been rebuilt or diverged. `FailoverMode=No` returns the DR to replica behaviour.

*Why not the others:* B is unnecessarily destructive. C restores Safes from backup files, a different operation. D is dangerous — automatic failback risks split brain.

<sub>Source area: DR failback</sub>

---

### Q132. Which two conditions must be met before `PAReplicate.exe` can take a Vault backup? (Choose two)

- **A.** The built-in `Backup` user must be enabled and given a password
- **B.** A credential file for that user must exist, referenced with `/logonfromfile`
- **C.** The Vault service must be stopped for the duration
- **D.** The `DR` user must be suspended

**Answer: A, B**

*Why:* The command form is `PAReplicate.exe vault.ini /logonfromfile user.ini /FullBackup`. The `Backup` user ships disabled and without a password, so enabling it and setting one is a genuine setup step people forget, and like every component it authenticates with a credential file.

*Why not the others:* C is false and is the point of the replicator — backups run against a live Vault. D would break disaster recovery. Note that restoring with `PARestore.exe` requires the Restore All Safes authorization.

<sub>Source area: PAReplicate / backup</sub>

---

### Q133. Which authorization is required to restore a Safe with `PARestore.exe`?

- **A.** Backup All Safes
- **B.** Restore All Safes
- **C.** Manage Safe
- **D.** Audit Users

**Answer: B**

*Why:* Backup and restore are deliberately separate authorizations. Backup All Safes lets a user copy data out; Restore All Safes lets a user write data back in, which is the far more dangerous capability and is why the `DR` user holds both while the `Backup` user's role is narrower.

*Why not the others:* A permits the backup, not the restore. C is a Safe-level property permission. D is an audit authorization.

<sub>Source area: PARestore / Vault authorizations</sub>

---

### Q134. `DRNotificationThreshold = Yes, Yes, 2, 24, 30m`. What does the final value mean?

- **A.** Notifications stop after 30 minutes
- **B.** The DR status is checked every 30 minutes
- **C.** The first notification is sent after 30 minutes
- **D.** Replication runs every 30 minutes

**Answer: B**

*Why:* The fields are: monitor, notify, hours before the first notification, hours between subsequent notifications, and how often to check. The DR threshold is the one where that last value is expressed in **minutes** rather than hours — a deliberate difference from `BackupNotificationThreshold`, whose equivalent field is in hours.

*Why not the others:* A and C misread the position. D is `ReplicateInterval` in `PADR.ini`, a different setting in a different file.

<sub>Source area: dbparm.ini notification thresholds</sub>

---

### Q135. Which statement about CPM log handling is correct?

- **A.** Logs grow indefinitely and must be truncated manually
- **B.** Old logs are rotated into `Logs\Old`, with third-party plug-in logs going to `Logs\Old\ThirdParty`
- **C.** All CPM logs are uploaded to the Vault for retention
- **D.** Logs are written only to the Windows Event Log

**Answer: B**

*Why:* The CPM rotates its own logs into `Logs\Old`, with per-plug-in logs archived under `Logs\Old\ThirdParty`. Worth knowing alongside this: third-party plug-in logs are not uploaded to the Vault, so if you need one for a support case you must collect it from the CPM server.

*Why not the others:* A ignores built-in rotation. C over-states what is uploaded. D is wrong — CyberArk components log to files.

<sub>Source area: CPM logging</sub>

---

### Q136. After changing a PVWA configuration file on disk, what is the standard step to make IIS pick it up, and how do you confirm the service state?

- **A.** `iisreset /restart`, then `iisreset /status`
- **B.** Restart the PrivateArk Server service
- **C.** Run `CreateCredFile.exe`
- **D.** Wait 20 minutes for the automatic refresh

**Answer: A**

*Why:* The PVWA is an IIS application, so `iisreset /restart` reloads it and `iisreset /status` confirms the services came back. This is also the final step after PKI changes to `applicationHost.config`.

*Why not the others:* B restarts the Vault, which is unnecessary and disruptive. C rebuilds a credential file. D is the PVWA's periodic *configuration* refresh from the Vault — it does not reload files edited on the web server itself.

<sub>Source area: PVWA administration</sub>

---

### Q137. Which file and utility belong to a Cluster Vault deployment?

- **A.** `PADR.ini` and `PAReplicate.exe`
- **B.** `ClusterVault.ini` and `StorageManager.exe`
- **C.** `tsparm.ini` and `CAVaultManager`
- **D.** `Basic_psm.ini` and `PSMHardening.ps1`

**Answer: B**

*Why:* `ClusterVault.ini` carries the logical node names, the virtual IP, the peer and local public and private IPs, the `StorageIdentifier` and the `QuorumDiskIdentifier`. `StorageManager.exe` identifies the disks — `-q` for the quorum drive and `-s` for the shared storage drive, as in `StorageManager.exe -qE -sF`.

*Why not the others:* A belongs to DR replication. C is Vale storage location configuration and the Vault management utility. D is the PSM.

<sub>Source area: Cluster Vault</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q138. What is the relationship between the Master Policy and platforms?

- **A.** The Master Policy sets baseline access rules for the whole environment, and exceptions can be defined at platform level for populations that need different treatment
- **B.** Platforms override the Master Policy automatically
- **C.** The Master Policy applies only to Windows accounts
- **D.** They are alternative configuration models — you use one or the other

**Answer: A**

*Why:* The Master Policy is the single place where the organisation's baseline access rules are expressed — dual control, reason for access, exclusive access, one-time passwords, session monitoring and recording. Where one population genuinely needs different treatment, you add an exception scoped to a platform rather than weakening the baseline for everyone.

*Why not the others:* B inverts the model — an exception must be created deliberately, nothing overrides silently. C and D are wrong; the Master Policy is universal and works together with platforms.

<sub>Source area: Master Policy</sub>

---

### Q139. Which of these are Master Policy rules rather than platform parameters? (Choose three)

- **A.** Require dual control password access approval
- **B.** Enforce check-in/check-out exclusive access
- **C.** Enforce one-time password access
- **D.** `MinValidityPeriod`

**Answer: A, B, C**

*Why:* The Master Policy expresses *what the organisation requires* of privileged access — approval, exclusivity, one-time use, session monitoring, recording, reason for access. Those are policy statements, so they live centrally.

*Why not the others:* D is a platform parameter that controls *how* the mechanism behaves — the number of minutes the CPM waits after retrieval before replacing a one-time password. Policy says "one-time"; the platform parameter says "after 60 minutes". Keeping that division clear answers a lot of exam questions.

<sub>Source area: Master Policy rules</sub>

---

### Q140. You need dual control for production databases but not for test databases, and both use the same platform. What is the cleanest approach?

- **A.** Turn dual control off globally and rely on training
- **B.** Duplicate the platform so production and test have their own, then apply the exception to the production platform
- **C.** Move all databases into one Safe
- **D.** Edit the built-in platform directly

**Answer: B**

*Why:* Exceptions are scoped to a platform, so two different policies means two platforms. Duplicating the platform is the standard answer to "same system type, different policy" — it is the same reason you would split `LIN SSH 30` from `LIN SSH 90`.

*Why not the others:* A abandons the control. C makes the problem worse by merging populations that need different rules. D is not the way to customise, since built-in platforms are not meant to be edited and can be overwritten on upgrade.

<sub>Source area: Master Policy exceptions / duplicate a platform</sub>

---

### Q141. `EnforcePasswordVersionsHistory` is set to 7 on a platform. What does that mean?

- **A.** Seven password versions are retained in the Safe
- **B.** The CPM will not reuse any of the last seven generated passwords
- **C.** Passwords expire after seven days
- **D.** Seven failed changes trigger an alert

**Answer: B**

*Why:* This is password *history* enforcement — the CPM avoids regenerating any of the last seven values, mirroring the history rules the target operating system enforces itself. Valid values run 1–50, or -1 to disable.

*Why not the others:* A is Safe version retention, a Safe property ("save the latest N versions", default five). C and D are invented.

<sub>Source area: Automatic Password Management — Password Change</sub>

---

### Q142. `RotationLatency` is documented as applying only in one circumstance. Which?

- **A.** Only when `HeadStartInterval` is 0
- **B.** Only when the account uses one-time passwords
- **C.** Only for UNIX platforms
- **D.** Only during the FromHour/ToHour window

**Answer: A**

*Why:* `RotationLatency` (default 0, range 0–60 minutes) introduces a small random delay so that a large population of accounts due at the same moment does not all rotate simultaneously. It only applies when `HeadStartInterval` is 0 — because a head start already spreads the work across days.

*Why not the others:* B, C and D are not the documented condition. This pairing is exactly the kind of interaction between two parameters that exam questions like to probe.

<sub>Source area: Automatic Password Management — Password Change</sub>

---

### Q143. What do `FromHour` and `ToHour` control on a platform?

- **A.** The hours during which users may open the Safe
- **B.** The window during which the CPM may perform password operations for accounts on that platform
- **C.** The PSM session duration limit
- **D.** The hours during which reports may be generated

**Answer: B**

*Why:* They define the CPM's working window, so credential changes can be confined to a maintenance period rather than landing in the middle of a trading day. `ResetOveridesTimeFrame` (default Yes) lets an immediate reset ignore the window when something urgent is required.

*Why not the others:* A is the Safe's Restrictions tab in the PrivateArk Client — a different control that produces ITATS100E when breached. C and D are unrelated.

<sub>Source area: Automatic Password Management</sub>

---

### Q144. What does `ChangeNotificationPeriod` do, and what does -1 mean?

- **A.** The number of seconds before a change that a notification is issued in an Application Access Manager environment; -1 means no notification
- **B.** The number of days before expiry that the CPM starts changing; -1 means immediate
- **C.** The number of retries after a failed change; -1 means unlimited
- **D.** The number of minutes between CPM loops; -1 disables the platform

**Answer: A**

*Why:* It exists for application credentials: applications retrieving a credential through AAM need warning that the value is about to change so they can re-fetch rather than fail. Setting it to -1 turns notification off.

*Why not the others:* B is `HeadStartInterval`, which is in days. C is invented. D is `Interval`.

<sub>Source area: Automatic Password Management — Password Change</sub>

---

### Q145. What does the CPM do during a password verification?

- **A.** It changes the password and confirms the new one works
- **B.** It logs on to the target with the password stored in the Vault to confirm the two still match, and flags the account as unsynchronised if they do not
- **C.** It reads the password hash from the target and compares it
- **D.** It checks the password against the platform's complexity policy

**Answer: B**

*Why:* Verification is a read-only health check: prove the stored credential still opens the door. If it does not, the account is flagged unsynchronised — and with `RCAutomaticReconcileWhenUnsynched = Yes` that flag is what triggers reconciliation.

*Why not the others:* A is a change. C is impossible — passwords are stored as one-way hashes on the target. D is a policy check, not a verification.

<sub>Source area: Verify passwords</sub>

---

### Q146. An account is marked to reset immediately, but the platform's `MinValidityPeriod` has not yet elapsed and the current time is outside `FromHour`/`ToHour`. What happens with default settings?

- **A.** The reset waits for both conditions
- **B.** The reset proceeds — `ResetOveridesMinValidity` and `ResetOveridesTimeFrame` both default to Yes
- **C.** The reset is cancelled and must be re-issued
- **D.** Only the time frame is overridden

**Answer: B**

*Why:* Both override parameters default to Yes precisely because an immediate reset usually means something has gone wrong — a suspected compromise, a departure, an incident. Making it wait for a maintenance window would defeat the purpose.

*Why not the others:* A and D assume defaults that are not the shipped ones. C is not a behaviour the CPM has.

<sub>Source area: Automatic Password Management — Privileged Account Management</sub>

---

### Q147. What is an account group used for?

- **A.** Grouping Safe members for permission assignment
- **B.** Keeping several accounts synchronised on the same password value, for cases where the same credential must exist identically on multiple systems
- **C.** Grouping platforms for reporting
- **D.** Grouping accounts to be onboarded together

**Answer: B**

*Why:* Account groups solve the case where several accounts must genuinely hold the same password — a clustered application, a set of appliances sharing a service identity — so the CPM changes them as a unit and keeps the value identical.

*Why not the others:* A is Vault groups. C and D describe things account groups are often confused with. Note the related but distinct construct: a *group platform* determines when the coordinated change happens, while each account keeps its own target platform for the change mechanics.

<sub>Source area: Account groups / group platforms</sub>

---

### Q148. Which Safe permission puts the Change, Verify and Reconcile buttons in front of a user?

- **A.** Manage Safe
- **B.** Initiate CPM account management operations
- **C.** Retrieve Accounts
- **D.** Use Accounts

**Answer: B**

*Why:* That permission is what lets a Safe member trigger CPM work on demand rather than waiting for the scheduled loop. It is separate from being able to see or use the credential, which is the point of granular Safe permissions.

*Why not the others:* A governs Safe properties. C reveals the secret. D allows a PSM session. Note that a user can hold this without holding Retrieve — a genuinely useful separation for an operations team that must fix accounts without reading passwords.

<sub>Source area: Safe member permissions</sub>

---

### Q149. What is Object Level Access Control (OLAC), and what should you know before enabling it?

- **A.** It restricts a Safe by IP address; it can be toggled freely
- **B.** It allows permissions to be set on individual accounts within a Safe rather than only at Safe level — and once enabled on a Safe it cannot be disabled
- **C.** It encrypts individual objects with separate keys; it is enabled by default
- **D.** It limits the number of objects in a Safe; it is set at platform level

**Answer: B**

*Why:* OLAC moves the access-control boundary from the Safe down to individual objects inside it. The catch that matters operationally is that it is a one-way switch — a Safe with OLAC enabled cannot have it turned off, so it is a design decision rather than something to experiment with in production.

*Why not the others:* A describes network areas and restrictions. C confuses it with the encryption hierarchy, where every object already has its own File Key. D is `MaxSafeSize` and object limits.

<sub>Source area: Safe properties — OLAC</sub>

---

### Q150. A contractor needs access to a Safe for a fixed six-week engagement. What is the cleanest control?

- **A.** Set a membership expiration date on their Safe membership
- **B.** Set `FromHour`/`ToHour` on the platform
- **C.** Create a Master Policy exception
- **D.** Set the Safe's object retention to 42 days

**Answer: A**

*Why:* Safe membership carries an expiration date, which is the built-in way to make temporary access actually temporary rather than depending on someone remembering to remove it. Better still, apply it to a group membership so the pattern is repeatable.

*Why not the others:* B restricts when the CPM operates. C changes access workflow, not duration. D governs how long objects are kept before deletion — nothing to do with who may reach them.

<sub>Source area: Safe members — membership expiration</sub>

---

### Q151. A CPM password change for a domain service account succeeds in Active Directory, but updating one of its dependent Windows Services fails. What is the practical consequence?

- **A.** Nothing — the service keeps running with the old password
- **B.** The service will fail to start next time it restarts, because the credential it holds no longer matches the domain
- **C.** The domain password is rolled back automatically
- **D.** The account is deleted from the Safe

**Answer: B**

*Why:* A running service holds its token already, so nothing appears broken until it restarts — which is what makes this failure mode dangerous: it surfaces at the next reboot or patch window, long after the change. This is why dependency handling and `SearchForUsages` matter, and why the CPM logs dependency failures separately.

*Why not the others:* A is true only until the next restart, which is precisely the trap. C — there is no automatic rollback. D does not happen.

<sub>Source area: Manage dependent accounts</sub>

---

### Q152. What is a rotational group used for?

- **A.** Rotating the CPM that manages a Safe
- **B.** Rotating through a set of accounts that serve the same purpose, so a freshly rotated credential is always available for the next user
- **C.** Rotating recording Safes on a schedule
- **D.** Rotating platform assignments between environments

**Answer: B**

*Why:* Rotational groups exist for high-demand shared access: rather than one account being checked out, changed and unavailable, a pool of equivalent accounts is rotated so someone always has a ready credential. It is the fourth platform tab, alongside Targets, Dependents and Groups.

*Why not the others:* A is Safe-level CPM assignment. C and D are invented. Do not confuse it with a *group* platform, which changes several accounts together rather than cycling between them.

<sub>Source area: Manage platforms — rotational groups</sub>

---

### Q153. When you duplicate a platform, what is copied?

- **A.** The platform's settings only — accounts stay on the original platform until you move them
- **B.** The settings and every account associated with the original
- **C.** The settings and the Safe
- **D.** Nothing — a duplicate starts from defaults

**Answer: A**

*Why:* Duplication copies configuration, not data. Existing accounts remain associated with the original platform, and moving them is a separate deliberate action — which is what makes duplication safe to do in production while you prepare a new policy.

*Why not the others:* B would silently change the policy applied to live accounts. C — Safes are unrelated to platforms. D would defeat the purpose of duplicating.

<sub>Source area: Duplicate a platform</sub>

---

### Q154. Which statement about the CPM plug-in architecture is correct?

- **A.** Plug-ins run on the Vault
- **B.** Each managed platform type uses a plug-in on the CPM that knows how to verify, change and reconcile on that target, and it writes its own log under `Logs\ThirdParty\`
- **C.** Plug-ins are stored in the `System` Safe
- **D.** There is one universal plug-in for all platforms

**Answer: B**

*Why:* The CPM is a scheduler and a policy engine; the platform-specific knowledge of *how* to change a password on Oracle, or a Cisco appliance, or a Windows local account, lives in the plug-in. That separation is why the Marketplace can supply support for new target types without a CPM upgrade.

*Why not the others:* A — the Vault stores and protects, it does not connect to targets. C — platform definitions live in `PasswordManagerShared`; plug-ins are files on the CPM. D would make the Marketplace pointless.

<sub>Source area: CPM plug-ins</sub>

---

### Q155. An SSH key and a password for the same UNIX account are both to be managed. What must be true?

- **A.** They can share a Safe, but they need separate platforms
- **B.** They must be in separate Safes and can share a platform
- **C.** Both must use the `Unix via SSH` platform
- **D.** SSH keys cannot be managed alongside passwords

**Answer: A**

*Why:* The Safe is an access-control boundary and can hold both; the platform is the management policy, and password rotation and SSH key rotation are different mechanics, so each needs its own. Remember also that an imported key should be rotated immediately, because the act of entering it exposed it.

*Why not the others:* B reverses which one must be separate. C names the password platform only. D is false — SSH key management is a core capability.

<sub>Source area: SSH key management</sub>

---

### Q156. Which of these is the strongest reason to grant Safe permissions to groups rather than to individual users?

- **A.** Groups process faster in the CPM
- **B.** Individually-assigned permissions are lost if the user object is deleted and recreated — which happens routinely with LDAP-provisioned users
- **C.** The Vault has a limit on individual permissions
- **D.** Groups are required for reporting

**Answer: B**

*Why:* Transparent (LDAP) users are provisioned on demand and can be deleted and recreated by ordinary lifecycle events. Permissions attached to the user object vanish with it; permissions derived from group membership come straight back. It also makes access reviews tractable — you review a handful of groups instead of thousands of individual grants.

*Why not the others:* A is not a real performance consideration. C and D are invented.

<sub>Source area: Safe members / LDAP transparent users</sub>

---

### Q157. A platform's `AllowedSafes` is left at its default. What is that default and what does it mean?

- **A.** Empty — the platform cannot be used until Safes are named
- **B.** `.*` — the platform can be used in any Safe, and the CPM searches all of them for accounts using it
- **C.** `^PasswordManager` — only CPM Safes
- **D.** `*` — all Safes, but only for Windows platforms

**Answer: B**

*Why:* The default `.*` matches every Safe name. That is fine in a small deployment, but in a large one it means the CPM scans every Safe on every loop for every platform, which is a real performance cost — narrowing `AllowedSafes` is a standard CPM tuning step.

*Why not the others:* A would break the platform out of the box. C and D are invented values.

<sub>Source area: Automatic Password Management — General</sub>

---

### Q158. Approximately how many managed passwords can a single optimised CPM support, and what is one of the main levers for reaching that?

- **A.** 10,000; adding more Safes
- **B.** 100,000; tuning `AllowedSafes`, `Interval`, `MaxConcurrentConnections` and staggering `FromHour`/`ToHour` across platforms
- **C.** 1,000,000; increasing RAM
- **D.** 50,000; enabling OLAC

**Answer: B**

*Why:* Around 100,000 is the figure to remember for a well-tuned CPM. Reaching it is about not wasting work: scoping platforms to the Safes that matter, spreading the load across the day rather than piling every change into the same hour, and controlling concurrency to each target.

*Why not the others:* A and D understate it and name irrelevant levers. C overstates it dramatically. OLAC is an access-control feature with no bearing on CPM throughput.

<sub>Source area: CPM performance tuning</sub>

---

### Q159. Why is "require users to specify a reason for access" more than a paperwork exercise?

- **A.** It slows users down, which reduces credential use
- **B.** It attaches intent to each access event in the audit trail, so a later review can distinguish routine work from anomalous access — and it pairs with ticketing integration to tie access to an approved change
- **C.** It prevents credential theft outright
- **D.** It is required for the PSM to record

**Answer: B**

*Why:* Audit records show that access happened; the reason field records why the person said they needed it. That is what makes review possible at scale, and with a ticketing system integrated the reason can be validated against a real change record rather than free text.

*Why not the others:* A is not the intent. C over-claims — it is a detective and deterrent control, not a preventive one. D is false; recording is governed by its own Master Policy rule.

<sub>Source area: Master Policy — reason for access</sub>

---

### Q160. Which statement about the Safe as a design unit is most accurate?

- **A.** Safes should be as large as possible to reduce administration
- **B.** A Safe is the unit of access control, so its boundaries should follow who needs access — grouping accounts that share the same audience and the same owners
- **C.** Each account should have its own Safe for maximum granularity
- **D.** Safe design should follow the platform, one Safe per platform

**Answer: B**

*Why:* Everything about a Safe — membership, permissions, the CPM assignment, retention, the audit scope of a report — applies to the whole Safe. So the right boundary is the population of people who should see the same things. Get that wrong and you spend the rest of the deployment fighting it, because the Safe model is the hardest thing to change later.

*Why not the others:* A collapses access control. C is unmanageable at any real scale, and OLAC exists precisely so you do not have to do this. D conflates policy with access — one platform is often used across many Safes.

<sub>Source area: Safe model design</sub>

---

### Q161. An operations team needs to run Change and Verify on accounts but must never see the passwords. Which permission set delivers that?

- **A.** List Accounts + Initiate CPM account management operations, without Retrieve Accounts
- **B.** List Accounts + Retrieve Accounts
- **C.** Manage Safe
- **D.** Use Accounts + Retrieve Accounts

**Answer: A**

*Why:* The permissions are deliberately granular so this exact separation is possible: the team can see the accounts and trigger CPM operations on them, but the secret itself is never displayed to them. It is the same principle as the Use-versus-Retrieve split for session access.

*Why not the others:* B gives them the passwords. C gives Safe property administration and still not the operations buttons. D gives both a session and the credential.

<sub>Source area: Safe member permissions</sub>

---

### Q162. What is the practical benefit of deactivating platforms you do not use?

- **A.** It reduces licence consumption
- **B.** Better administration — deactivated platforms are hidden from users choosing a platform — and better performance, since the CPM does not process them
- **C.** It frees space in the Vault
- **D.** It is required before a platform can be deleted

**Answer: B**

*Why:* Two benefits, and the exam wants both. Fewer platforms in the picker means fewer wrong choices at onboarding time; and every active platform is work the CPM schedules on every loop, so deactivating the unused ones is genuine tuning.

*Why not the others:* A — licensing counts managed accounts. C — platform definitions are tiny. D is invented. Note that deactivating a target platform also deactivates its dependent platforms.

<sub>Source area: Manage platforms</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q163. What is the correct order of the Vault's hierarchical encryption?

- **A.** Server Key → Safe Key → File Key
- **B.** File Key → Safe Key → Server Key
- **C.** Recovery Key → File Key → Safe Key
- **D.** Safe Key → Server Key → File Key

**Answer: B**

*Why:* Every object is encrypted with its own File Key; the File Key is encrypted with the Safe Key; the Safe Key is encrypted with the Server Key. Reading it outward from the object is the reliable way to remember it: object → Safe → server. The consequence is that without the Server Key, nothing below it can be opened.

*Why not the others:* The other orders invert the hierarchy. The Recovery Key sits alongside rather than inside this chain: the Safe Key is *also* encrypted with the Recovery public key, so it can be recovered with the Recovery private key.

<sub>Source area: Vault hierarchical encryption</sub>

---

### Q164. Which Server Key storage option is described as both strong and convenient, and why?

- **A.** An external medium such as a USB device removed after startup — strong but inconvenient
- **B.** The local disk — convenient but weaker
- **C.** An HSM — strong and convenient, because the key is used inside the module and is never held in the Vault server's memory
- **D.** A network share protected by ACLs

**Answer: C**

*Why:* The three options trade off along one axis. External media is strong because the key can be physically removed after the Vault starts, but that makes unattended restarts impossible. Local disk restarts cleanly but leaves the key on the machine. An HSM resolves the tension: the key never leaves the module, so it is neither on disk nor in the Vault's RAM.

*Why not the others:* A and B are correctly described but are not the both-strong-and-convenient option. D is not a supported model and would be weaker than local disk.

<sub>Source area: Server Key storage</sub>

---

### Q165. Where should the Recovery private key be stored?

- **A.** On the Vault server, alongside the Server Key
- **B.** On physical media in at least two secure locations — typically the primary site and the DR site
- **C.** In the `System` Safe
- **D.** On the CPM server, protected by a credential file

**Answer: B**

*Why:* The Recovery private key is the last resort for opening the Vault's data, so it must be both protected and available. Storing it on the Vault it protects would defeat the purpose; storing only one copy risks losing everything to a single site event. Two secure physical locations — primary and DR — is the documented practice.

*Why not the others:* A destroys the separation the key exists to provide. C is inside the very system being recovered. D is unrelated — credential files protect component authentication.

<sub>Source area: Recovery keys</sub>

---

### Q166. How is the Safe Key protected so that recovery is possible?

- **A.** It is stored in plaintext on the Vault
- **B.** It is encrypted with the Server Key and also with the Recovery public key, so it can be recovered using the Recovery private key
- **C.** It is derived from the Master user's password
- **D.** It is stored in the `VaultInternal` Safe

**Answer: B**

*Why:* Two independent paths to the same Safe Key: the normal operational path through the Server Key, and the break-glass path through the Recovery key pair. That dual encryption is exactly what makes Master-user recovery possible when the Server Key is lost, without weakening day-to-day protection.

*Why not the others:* A would make the whole hierarchy pointless. C and D are invented mechanisms.

<sub>Source area: Vault hierarchical encryption / recovery</sub>

---

### Q167. PTA's detections fall into three families. Which set is correct?

- **A.** Malware, phishing and insider threat
- **B.** Attacks that bypass security controls; statistical anomalies; Active Directory risks
- **C.** Network, endpoint and cloud
- **D.** Preventive, detective and corrective

**Answer: B**

*Why:* Bypass detections cover abuse of privileged accounts whether or not CyberArk manages them — unmanaged privileged access, suspected credential theft, suspicious password change, suspicious in-session activity. Statistical anomalies use profiling to spot irregular hours, irregular source IPs, excessive access and dormant users waking up. AD risks are configuration weaknesses an attacker could abuse, flagged before they are abused.

*Why not the others:* A is generic security taxonomy. C describes data sources rather than detection families. D is a control classification.

<sub>Source area: PTA — detect</sub>

---

### Q168. Which PTA detections come from EPM (Endpoint Privilege Manager) rather than from the Vault, logs or AD? (Choose three)

- **A.** Suspected LSASS credentials harvesting
- **B.** Suspected SAM hash harvesting
- **C.** Suspected credentials theft from Chrome
- **D.** Excessive access to privileged accounts in the Vault

**Answer: A, B, C**

*Why:* The whole "harvesting / theft from <somewhere on the endpoint>" family comes from EPM, because those are endpoint memory and application events that only an endpoint agent can see — LSASS, SAM hashes, Chrome, Firefox, VNC, WinSCP, service accounts and cached domain credentials.

*Why not the others:* D is a Vault-behaviour anomaly derived from Vault activity. The memory hook is worth keeping: endpoint theft → EPM, Vault behaviour → Vault, delegation and SPN issues → AD.

<sub>Source area: PTA — detection sources</sub>

---

### Q169. Which of these are Active Directory risks that PTA proactively reports? (Choose three)

- **A.** Unconstrained Delegation
- **B.** Risky SPN
- **C.** Service account logged on interactively
- **D.** Access to the Vault from an irregular IP address

**Answer: A, B, C**

*Why:* These are configuration weaknesses that make an attacker's job easier, and PTA flags them so they can be fixed *before* they are exploited — which is a different value proposition from detecting an attack in progress. Dual Usage belongs to the same family.

*Why not the others:* D is a statistical anomaly derived from Vault activity, not an AD configuration risk.

<sub>Source area: PTA — Active Directory risks</sub>

---

### Q170. A Privileged Session Analysis and Response rule is defined by which attributes?

- **A.** Category, Pattern (a regular expression), Session response, Threat Score and Scope
- **B.** Safe, Platform, User and Action
- **C.** Severity, Date and Event Type
- **D.** Source IP, Destination IP and Port

**Answer: A**

*Why:* Category selects what is being watched — SSH, Universal Keystrokes, SCP, SQL or Windows title. Pattern is the regular expression to match. Session response is Suspend, Terminate or None. Threat Score runs 1–100. Scope narrows the rule to particular Vault users, accounts or machines.

*Why not the others:* B and D describe other objects entirely. C are the filters used to review PTA events in the Security pane, not the fields that define a response rule. CyberArk recommends studying the predefined rule set first, then modifying and adding rules to fit the organisation.

<sub>Source area: PTA — privileged session analysis and response</sub>

---

### Q171. With PTA and PSM integrated, what changes for an audit team reviewing recordings?

- **A.** Recordings are compressed to save space
- **B.** Each session is assigned a risk score, so reviewers can prioritise the riskiest sessions instead of sampling at random
- **C.** Recordings are automatically deleted if no risk is found
- **D.** Only failed sessions are recorded

**Answer: B**

*Why:* This is the practical answer to "nobody can watch ten thousand hours of RDP". PTA analyses session activity and scores it, which turns review from random sampling into a ranked queue — and the same integration allows automatic suspension or termination during high-risk activity.

*Why not the others:* A, C and D are not behaviours of the integration, and C in particular would destroy audit evidence.

<sub>Source area: PTA — PSM integration</sub>

---

### Q172. Which groups can see PTA security events in the PVWA, and where?

- **A.** Auditors, in the Privileged Sessions tab
- **B.** Security Admins and Security Operators, in the Security pane
- **C.** Vault Admins, in System Health
- **D.** PVWAMonitor, in Reports

**Answer: B**

*Why:* PTA events surface in the Security pane, which is scoped to Security Admins and Security Operators — a separate audience from the auditors reviewing recordings and the administrators managing the platform. Events are shown on a timeline and can be filtered by severity, event type and date.

*Why not the others:* A is where session recordings are reviewed. C shows component health. D is the reporting group. Each event card carries the last detection time, the event name, the score and severity, whether remediation has started, and the recommended or automatically taken action.

<sub>Source area: PTA — alert / Security pane</sub>

---

### Q173. Which statement best captures the Vault's defence-in-depth design?

- **A.** A single strong firewall protects the Vault
- **B.** The Vault runs a hardened, closed operating system with its own built-in firewall, no standard network services, no third-party access, and its own authentication and access control — several independent layers rather than one
- **C.** Security is provided by the network team's segmentation
- **D.** Encryption alone protects the data

**Answer: B**

*Why:* The Digital Vault's premise is that no single control should be load-bearing. The server is hardened and closed to everything except the CyberArk protocol on its own firewall, the operating system is not available for general use, the Vault authenticates and authorises independently of the domain, and the data is encrypted hierarchically underneath all of it.

*Why not the others:* A, C and D each describe one layer and treat it as sufficient — which is exactly the assumption the design rejects.

<sub>Source area: Vault security layers / Digital Vault Security Standard</sub>

---

### Q174. Playback of a PSM recording through the PVWA depends on which group?

- **A.** `PSMLiveSessionTerminators`
- **B.** `PVWAGWAccounts` — the gateway accounts that enable playback through the PVWA
- **C.** `Safe Managers`
- **D.** `Notification Engines`

**Answer: B**

*Why:* `PVWAGWAccounts` are the gateway accounts with access to password Safes that make PVWA-mediated operations, including recording playback, possible. Alongside them, `PSMAppUsers` creates recording Safes and uploads recordings, `PSMMaster` manages those Safes, and `Auditors` get read access to all of them.

*Why not the others:* A suspends and terminates live sessions. C is a role name rather than a predefined group. D relates to the ENE.

<sub>Source area: PSM environment — groups</sub>

---

### Q175. An auditor wants a report of everything a specific user did, and separately everything that happened in a specific Safe. Which permissions are involved?

- **A.** Audit Users for the user-activity view; View Audit on the Safe for the Safe-activity view
- **B.** Manage Users for both
- **C.** List Accounts for both
- **D.** Backup All Safes for both

**Answer: A**

*Why:* The two questions have two different scopes and therefore two different permissions. "What did this person do?" spans the Vault and needs the Vault-level Audit Users authorization. "What happened in this Safe?" is bounded by the Safe and needs View Audit on it.

*Why not the others:* B is a user-administration authorization — the Entitlement report accepts either Manage Users or Audit Users, but Activity Log scope works as described above. C only reveals that accounts exist. D is for backups.

<sub>Source area: Reports — Activity Log permissions</sub>

---

## Domain 6 — Configure Session Management

### Q176. Which statement correctly contrasts a PSM connection with a PSM for SSH connection?

- **A.** Both always go through the PVWA
- **B.** A PSM (Windows) session is normally launched from the PVWA, whereas PSM for SSH lets the user connect straight from a native SSH client without touching the web interface
- **C.** PSM for SSH requires the HTML5 Gateway
- **D.** Neither records the session

**Answer: B**

*Why:* That is the point of PSM for SSH: administrators keep their own terminal and workflow, connecting with a single SSH command, while the session is still brokered, isolated, recorded and audited. The Windows PSM flow normally starts from the PVWA's Connect button.

*Why not the others:* A ignores the direct SSH path. C — the HTML5 Gateway fronts the Windows PSM for browser-based sessions. D is wrong: both record.

<sub>Source area: PSM and PSM for SSH flows</sub>

---

### Q177. Which PSM for SSH connection string is correct?

- **A.** `ssh targetaccount@vaultuser@psmaddress@targetaddress`
- **B.** `ssh vaultuser@targetaccount@targetaddress@psmaddress`
- **C.** `ssh psmaddress@vaultuser@targetaccount@targetaddress`
- **D.** `ssh vaultuser@psmaddress@targetaccount@targetaddress`

**Answer: B**

*Why:* Read it as a sentence: who you are (your Vault user), what you want to become (the target account), where you are going (the target address), and finally what you actually connect to (the PSM). The PSM address is last because it is the host your SSH client is really opening a session to.

*Why not the others:* The other orders scramble those four elements. Building the sentence in your head is more reliable at exam time than memorising the string.

<sub>Source area: PSM for SSH</sub>

---

### Q178. Which connection components belong to PSM for SSH? (Choose three)

- **A.** `PSMP-SSH`
- **B.** `PSMP-SCP`
- **C.** `PSMP-SFTP`
- **D.** `PSM-WinSCP`

**Answer: A, B, C**

*Why:* The PSMP family covers the SSH world: `PSMP-SSH` for interactive sessions and `PSMP-SCP`, `PSMP-SFTP` and `PSMP-Rsync` for file transfer, all brokered and audited by PSM for SSH.

*Why not the others:* D is a Windows PSM connection component — WinSCP is a graphical Windows client launched inside a PSM session, which is a different mechanism from a native SSH file transfer through PSMP.

<sub>Source area: Connection components</sub>

---

### Q179. Estimate the recording storage for 30 days of retention, 250 sessions per day, 60 minutes per session, high-activity RDP.

- **A.** About 20 GB
- **B.** About 155 GB
- **C.** About 470 GB
- **D.** About 2 TB

**Answer: B**

*Why:* High-activity RDP is budgeted at 300 KB per minute. 30 days x 250 sessions x 60 minutes = 450,000 minutes; 450,000 x 300 KB = 135,000,000 KB, which is about 129 GB. The sizing formula then adds a constant 20 GB, giving roughly 150-155 GB.

*Why not the others:* Work it as sessions x minutes x rate x days, then add 20 GB. The rate is what usually goes wrong: memorise 100 / 200 / 300 KB per minute for SSH / low-activity RDP / high-activity RDP. Using 100 KB/min here would give about 63 GB; there is no arithmetic that reaches 470 GB or 2 TB at this volume.

<sub>Source area: PSM recording sizing</sub>

---

### Q180. You are sizing PSM servers for 240 concurrent sessions on virtual machines. How many servers should you plan for, before adding redundancy?

- **A.** Two — 100 sessions each with headroom
- **B.** Four — the guideline is 100 concurrent sessions per PSM server, reduced by up to 40% on a VM, so budget around 60 per virtual server
- **C.** One — a single PSM scales to 300
- **D.** Six — 40 sessions per server

**Answer: B**

*Why:* The published guideline is up to 100 concurrent sessions per PSM server, and virtualisation can cost up to 40% of that. At roughly 60 sessions per virtual server, 240 concurrent sessions needs four — and that is before you add capacity for failure of one node.

*Why not the others:* A applies the physical figure to virtual servers. C and D misremember the base number in opposite directions.

<sub>Source area: PSM sizing</sub>

---

### Q181. From version 14.4, what happens to a PSM recording that reaches 2 GB?

- **A.** The session is terminated
- **B.** The recording is split automatically and continues in a new file
- **C.** The recording is truncated and the rest is lost
- **D.** The recording is compressed in place

**Answer: B**

*Why:* Automatic splitting at 2 GB means very long sessions no longer produce a single unmanageable object, and nothing is lost. Before this, large recordings were a genuine operational problem for upload and playback.

*Why not the others:* A would disrupt legitimate work. C would destroy audit evidence — the exact thing recording exists to preserve. D is not the mechanism.

<sub>Source area: PSM recordings — version notes</sub>

---

### Q182. Which file and parameter define which users may connect to a PSM for SSH server for maintenance, bypassing the PSMP shell?

- **A.** `sshd_config` — `PSMP_MaintenanceUsers`
- **B.** `basic_psmpserver.conf` — `AdminUsers`
- **C.** `Basic_psm.ini` — `MaintenanceUsers`
- **D.** `PSMHardening.ps1` — `$PSM_CONNECT_USER`

**Answer: A**

*Why:* `PSMP_MaintenanceUsers` in `sshd_config` names the accounts allowed a normal shell on the PSM for SSH host, so administrators can still maintain the server itself without every SSH connection being intercepted and brokered.

*Why not the others:* B is the PSMP server's main configuration file but not where this is set. C is the Windows PSM's configuration. D is a Windows PSM hardening variable, alongside `$SUPPORT_WEB_APPLICATIONS`.

<sub>Source area: PSM for SSH configuration</sub>

---

### Q183. You have three PSM servers behind a load balancer. What must be true about recordings?

- **A.** Recordings stay on whichever PSM handled the session, so playback must be directed to that server
- **B.** Recordings are uploaded to the Vault, so playback does not depend on which PSM served the session
- **C.** Each PSM needs its own recording Safe named after it
- **D.** Load balancing is not supported with recording enabled

**Answer: B**

*Why:* Recordings are uploaded into Vault Safes, not left on the PSM host. That is what makes horizontal scaling straightforward — any PSM can serve any session and the audit trail lands in one governed place. It also means recording Safes inherit Vault protection and Safe-level access control.

*Why not the others:* A describes a pre-upload state only. C is possible with a dynamic `SessionRecorderSafe` value but is not a requirement. D is false.

<sub>Source area: PSM recordings / load balancing</sub>

---

### Q184. Which PSM hardening script variables would you review when a PSM must support web application connection components?

- **A.** `$SUPPORT_WEB_APPLICATIONS` and `$PSM_CONNECT_USER` in `PSMHardening.ps1`
- **B.** `AllowSelectHTML5` and `DefaultConnectionMethod`
- **C.** `SessionRecorderSafe` and `SessionRecorderSafeRetention`
- **D.** `AllowMonitor` and `AllowTerminate`

**Answer: A**

*Why:* Hardening a PSM locks down the interactive session environment, and browser-based connection components need some of that relaxed in a controlled way. `$SUPPORT_WEB_APPLICATIONS` governs that, and `$PSM_CONNECT_USER` identifies the session user the hardening applies to.

*Why not the others:* B controls HTML5-versus-RDP delivery. C configures recording storage. D governs live monitoring. All real settings, none of them hardening variables.

<sub>Source area: PSM hardening</sub>

---

### Q185. Why should the Windows active-session and idle-session limits on a PSM server be set to Never?

- **A.** To let users stay connected as long as they like
- **B.** Because a Windows-enforced disconnect can cut a session mid-write and corrupt the recording — session duration should instead be limited at platform level
- **C.** Because AppLocker requires it
- **D.** Because the HTML5 Gateway does not support timeouts

**Answer: B**

*Why:* Windows session timeouts and PSM recording do not mix: an abrupt disconnect can leave a recording incomplete or corrupt. The right place to bound a session is the platform, where the limit is applied by the PSM itself and the recording is closed cleanly.

*Why not the others:* A misreads the intent — the point is not unlimited sessions, it is enforcing the limit in the right layer. C and D are invented.

<sub>Source area: PSM configuration</sub>

---

### Q186. When registering an HTML5 Gateway in the PVWA, which three values are required?

- **A.** ID, Address (FQDN) and Port
- **B.** Username, password and certificate
- **C.** Safe, platform and connection component
- **D.** IP range, subnet mask and gateway

**Answer: A**

*Why:* Registration under Options → Privileged Session Management → Add Configured PSM Gateway Servers takes an ID, the gateway's fully qualified domain name and its port (443). The ID is then referenced when you associate the gateway with a specific PSM server under that PSM's Connection Details.

*Why not the others:* B, C and D belong to other configuration objects. Remember the two-step nature: registering the gateway is not enough on its own — it must also be associated with a PSM server and enabled.

<sub>Source area: Secure access with an HTML5 Gateway</sub>

---

### Q187. A user connecting through the HTML5 Gateway reports the wrong keyboard layout. Which settings are relevant?

- **A.** `KeyboardLayout` and `ServerKeyboardLayout`, with `AllowLanguageSelection` / `AllowedLanguages` controlling what the user can pick
- **B.** `DefaultConnectionMethod`
- **C.** `PSMConnectionDefault`
- **D.** `EnforceSubnetRules`

**Answer: A**

*Why:* The gateway carries its own keyboard and language parameters because it is translating browser input into RDP. `KeyboardLayout` and `ServerKeyboardLayout` set the client and server sides, while `AllowLanguageSelection`, `AllowedLanguages` and `DisableLanguageSelection` decide how much choice the user gets.

*Why not the others:* B selects HTML5 versus an RDP file. C sets the default connection component for a platform. D restricts ad hoc connections by subnet.

<sub>Source area: HTML5 Gateway parameters</sub>

---

### Q188. During a live session an observer sees something suspicious but wants to investigate before cutting the user off. What is the appropriate action?

- **A.** Terminate the session immediately
- **B.** Suspend the session — it can be resumed once the activity is understood, whereas termination is final
- **C.** Change the account password
- **D.** Delete the recording

**Answer: B**

*Why:* Suspend and terminate are separate deliberately. Suspension freezes the session and preserves the ability to resume, which suits investigation; termination ends it. Both require membership of `PSMLiveSessionTerminators` and the corresponding server setting, and PTA response rules can trigger either automatically on a high-risk pattern.

*Why not the others:* A forecloses the investigation. C does not stop the session in progress. D destroys evidence.

<sub>Source area: Active session monitoring in PSM</sub>

---

### Q189. Which statement about PSM text recording is correct?

- **A.** Text recording replaces video recording
- **B.** Text, keystroke and command audit is captured alongside video, and it is what makes the recording archive searchable
- **C.** Text recording is only available for SSH sessions
- **D.** Text recordings are stored on the PSM server

**Answer: B**

*Why:* The two are complementary. Video shows what the session looked like; the text and command audit is what an auditor can actually query — searching for a command across thousands of sessions rather than watching them. Windows sessions capture window titles and keystrokes; SSH sessions capture the command stream.

*Why not the others:* A treats them as alternatives. C is too narrow. D is wrong — recordings are uploaded to Vault Safes.

<sub>Source area: Configure video and text recordings</sub>

---

### Q190. Which Safes are created by a PSM installation? (Choose three)

- **A.** `PSM`
- **B.** `PSMLiveSessions`
- **C.** `PSMUnmanagedSessions`
- **D.** `PVWAReports`

**Answer: A, B, C**

*Why:* The PSM's own Safe set includes `PSM`, `PSMLiveSessions`, `PSMNotifications`, `PSMRecordings`, `PSM Sessions`, `PSMUniversalConnectors` and `PSMUnmanagedSessions` — infrastructure for configuration, live session state, notifications, connectors and unmanaged ad hoc sessions.

*Why not the others:* D belongs to the PVWA's set, alongside `PVWAConfig`, `PVWAPrivateUserPrefs`, `PVWAPublicData`, `PVWATaskDefinitions`, `PVWATicketingSystem` and `PVWAUserPrefs`.

<sub>Source area: Built-in Safes</sub>

---

### Q191. What is the security trade-off an administrator accepts when enabling ad hoc (Secure Connect) sessions?

- **A.** Sessions are not recorded
- **B.** The credentials used are supplied at connect time and are not vaulted, so part of the PSM's security benefit — a secret the user never possesses — is lost
- **C.** The PSM cannot isolate the session
- **D.** Ad hoc sessions bypass AppLocker

**Answer: B**

*Why:* Isolation and recording still apply, so the session is still brokered through the hardened PSM and still audited. What is lost is credential management: the user has and types the password, so it is neither rotated, nor unique, nor unknown to them. That is why ad hoc access should be scoped to named users or groups and, ideally, treated as a stepping stone to proper onboarding.

*Why not the others:* A and C are false — ad hoc sessions are recorded and isolated. D is false and would be a serious hardening gap.

<sub>Source area: Configure ad hoc connections</sub>

---

### Q192. Which parameter sets the default connection component offered for a platform, and where does it live?

- **A.** `PSMConnectionDefault`, under the platform's UI & Workflows → Connection Components
- **B.** `DefaultConnectionMethod`, under Privileged Session Management UI
- **C.** `PSMServerID`, under the Safe's properties
- **D.** `AllowSelectHTML5`, on the connection component

**Answer: A**

*Why:* `PSMConnectionDefault` names the component that appears pre-selected in the connect drop-down on the Account Details page — useful when a platform has several enabled components and one is the normal choice.

*Why not the others:* B decides HTML5 versus an RDP file, not which component runs. C is not a Safe property — PSM server association is set at platform level. D lets the user choose the connection method for a component. All four are real settings, which is what makes this a good discrimination question.

<sub>Source area: Default connection component</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q193. In Privilege Cloud, how does an Active Directory user end up with the right permissions on first login?

- **A.** An administrator creates the user manually in the portal beforehand
- **B.** Role Mappings associate AD groups with Privilege Cloud roles, and any AD user in a mapped group is automatically assigned the matching role on first login
- **C.** Every AD user gets the Privilege Cloud Users role by default
- **D.** Permissions come from the Vault's Directory Mappings, exactly as in self-hosted

**Answer: B**

*Why:* Role Mappings are the SaaS equivalent of transparent user provisioning: `CyberArk Vault Admins@acme.corp` maps to Privilege Cloud Administrators, `CyberArk Safe Managers@…` to Privilege Cloud Safe Managers, and so on. The user is assigned to the role the first time they log in.

*Why not the others:* A defeats the point of directory-driven provisioning. C would be a serious over-grant. D names the self-hosted mechanism — in Privilege Cloud the Identity layer does this. Note each role exists in standard, Basic and Lite versions; pick the standard one unless you specifically need the others.

<sub>Source area: Privilege Cloud — Identity role mappings</sub>

---

### Q194. In CyberArk Identity, what is the relationship between Authentication Profiles and Policy Sets?

- **A.** An Authentication Profile defines the MFA challenge chain; a Policy Set associates roles with an Authentication Profile
- **B.** A Policy Set defines the challenges; an Authentication Profile assigns them to users
- **C.** They are two names for the same object
- **D.** Policy Sets apply only to service accounts

**Answer: A**

*Why:* An Authentication Profile is the *what* — Challenge 1 might be Password and Challenge 2 an SMS confirmation code. A Policy Set is the *who* — it assigns specified roles and sets the default profile they must satisfy. Splitting them means one profile can serve several roles.

*Why not the others:* B reverses the two. C ignores a real separation. D is invented — Policy Sets are how ordinary users get their MFA requirements.

<sub>Source area: Privilege Cloud — Authentication Profiles and Policy Sets</sub>

---

### Q195. You are about to install a Privilege Cloud Connector and the installation fails to authenticate. What should you check first?

- **A.** The Vault's `dbparm.ini`
- **B.** The `installeruser` password — it expires every 24 hours and must be reset before each install session
- **C.** The CPM's credential file
- **D.** The Master user's Recovery key

**Answer: B**

*Why:* `installeruser` is the built-in Identity service account used during every component installation, and its password deliberately expires every 24 hours. If your install session is a day after you set it, it has already expired. Reset it under Core Services → Users → Set All Service Users before starting.

*Why not the others:* A is a self-hosted Vault file you do not control in Privilege Cloud. C is created *during* installation. D is a break-glass recovery artefact.

<sub>Source area: Privilege Cloud — installeruser</sub>

---

### Q196. Which Privilege Cloud prerequisite is easy to miss and blocks Connector deployment?

- **A.** Registering the Connector machines' IP addresses in the tenant's IP allowlist
- **B.** Installing the PrivateArk Client on each Connector
- **C.** Opening port 1858 to the internet
- **D.** Creating a DR Vault

**Answer: A**

*Why:* Privilege Cloud requires the IP addresses of machines running Connectors to be registered in the tenant's IP allowlist, under Administration → Advanced Settings. CIDR notation is accepted, and propagation can take up to ten minutes — so it is worth doing before you need it rather than while an installer is waiting.

*Why not the others:* B is not required. C would be a serious exposure — the Vault is CyberArk-hosted. D is not part of Connector deployment.

<sub>Source area: Privilege Cloud — IP allowlist</sub>

---

### Q197. Which description of Secure Infrastructure Access (SIA) is correct?

- **A.** An agent-based replacement for the PSM on Windows targets
- **B.** A non-intrusive, agentless SaaS solution giving VPN-less access to Windows, Linux, databases and Kubernetes, using native clients over an MFA-secured connection, with either zero standing privileges or vaulted credentials
- **C.** A reporting layer over Privilege Cloud
- **D.** A hardware appliance deployed in the customer data centre

**Answer: B**

*Why:* SIA — formerly DPA, Dynamic Privileged Access — is built for hybrid and cloud estates where installing agents everywhere is impractical. The two things to hold on to are the coverage (Windows, Linux, databases, Kubernetes; native clients; no VPN) and the two access models (ZSP or vaulted credentials).

*Why not the others:* A is wrong twice: SIA is agentless and it co-exists with the PSM rather than replacing it — PSM, WPM, SWS, SCA and Identity SSO still cover cloud consoles, web applications and thick clients. C and D misdescribe it entirely.

<sub>Source area: Secure Infrastructure Access (SIA)</sub>

---

### Q198. Which role grants the permissions needed to administer SIA?

- **A.** Privilege Cloud Administrators
- **B.** `DpaAdmin`
- **C.** Privilege Cloud Auditors
- **D.** `PSMMaster`

**Answer: B**

*Why:* SIA administration is gated by the Secure Infrastructure Access tile permissions, which come through the `DpaAdmin` role — a reminder that SIA was previously called DPA and that the older name survives in role and object names. In the lab mapping, `DpaAdmin` is mapped to the `CyberArk Vault Admins` AD group.

*Why not the others:* A administers Privilege Cloud generally but does not by itself carry the SIA tile. C is read-and-audit. D is a self-hosted PSM group for recording Safes.

<sub>Source area: SIA administration</sub>

---

### Q199. Under Zero Standing Privileges, how is an ephemeral account named, and what is the difference between the local and domain varieties?

- **A.** A random GUID; local and domain accounts behave identically
- **B.** The first seven characters of the username, a dash, then a random string to reach 20 characters — a local ephemeral account cannot reach the domain or shared resources by default, while a domain ephemeral account retains access to domain resources
- **C.** The full username plus a timestamp; only domain accounts are supported
- **D.** The Strong Account's name plus a counter; the difference is only the lifetime

**Answer: B**

*Why:* So `John@acme.corp` becomes something like `john-s3mGciK6D5N8Vkc`. The local-versus-domain distinction is the operational decision: local gives the tightest blast radius but no access to network shares; domain gives that access back, at the cost of consuming a Microsoft CAL under a per-user model — which is why per-device RDS CAL licensing is recommended.

*Why not the others:* A, C and D each get the naming convention wrong and miss the access distinction, which is the part that actually affects design.

<sub>Source area: ZSP — ephemeral accounts</sub>

---

### Q200. A Strong Account is being onboarded so SIA can create ephemeral accounts. What must be configured on the Safe holding it, and how should the account itself be hardened?

- **A.** Add the `DPA RDP Privilege Cloud Secrets Access` role as a member with the Read Only preset and Access Safe without confirmation; harden the account as sensitive and cannot be delegated, deny RDS logon, deny local logon, make it a service account, and apply least privilege
- **B.** Add the Auditors group with full permissions; no hardening is required
- **C.** Add `PSMAppUsers` with all authorizations; make the account a Domain Admin
- **D.** No Safe membership is needed; SIA reads the account directly

**Answer: A**

*Why:* SIA needs to retrieve the Strong Account without a human approval step, hence Read Only plus Access Safe without confirmation for the `DPA RDP Privilege Cloud Secrets Access` role (added from the CyberArk Cloud Directory as a Role member). The hardening list matters just as much: a Strong Account can create, delete and manage users and modify group membership, so it must never be usable interactively.

*Why not the others:* B and C both over-grant dramatically — making a Strong Account a Domain Admin is the opposite of least privilege. D is wrong: SIA retrieves it through the Vault like any other credential.

<sub>Source area: ZSP — Strong Accounts</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q201. A requirement says a password must change between 01:00 and 03:00 on Saturdays and Sundays, but it does not work consistently. Which platform setting is the likely cause?

- **A.** `Interval` is set too high
- **B.** `DaysToRun` is not set to Sat,Sun
- **C.** `ImmediateInterval` is set to 5
- **D.** `HeadStartInterval` is set to 0

**Answer: B**

*Why:* Two separate settings bound a CPM change window and both must be right: `FromHour`/`ToHour` set the hours (01:00–03:00 here) and **`DaysToRun`** restricts which days the change may run. Leaving `DaysToRun` at its default means the change fires on whatever day the interval brings it round to, so the hours look respected but the days do not.

*Why not the others:* A affects how often the CPM loops, not which days it may act. C governs user-initiated operations. D would start the change early relative to expiry — none of them constrains the day of week.

<sub>Source area: Automatic Password Management — FromHour / ToHour / DaysToRun</sub>

---

## Domain 1 — Onboard Accounts

### Q202. Which group must a CyberArk user belong to in order to create and manage automatic onboarding rules?

- **A.** Vault Admins
- **B.** Auditors
- **C.** PVWAMonitor
- **D.** The CPM user's group

**Answer: A**

*Why:* Onboarding rules are a system-configuration object, so managing them sits with Vault Admins — the group that gets the Administration tab. Separately, the rule's author also needs to be a member of the target Safe with Add Account permission, otherwise the rule cannot place accounts there.

*Why not the others:* B is read-and-audit. C is the reports group named by `ManageReportsGroup`. D is a component user's context, not an administrative group.

<sub>Source area: Manage onboarding rules</sub>

---

## Domain 6 — Configure Session Management

### Q203. You are reviewing a recording of a session by user jsmith. There is no option to fast-forward or scrub the video — playback only lets you jump between commands, and there is no download. What is the most likely explanation?

- **A.** It is a PSM for SSH session, so the recording is a text/command recording rather than video
- **B.** Your browser is out of date
- **C.** You lack the View Audit permission on the Safe
- **D.** The platform's screen-capture interval needs lowering

**Answer: A**

*Why:* PSM for SSH sessions produce command/text recordings, not video. The reviewer therefore navigates by command rather than by timeline, and there is no video file to download. Windows PSM sessions produce video plus keystroke and window-title audit, which is why they behave differently in the player.

*Why not the others:* B is a generic distractor — note that some third-party question banks give this as the answer, which is a good example of why their keys should not be trusted. C would prevent access to the recording entirely rather than changing the playback controls. D is not a real recording setting.

<sub>Source area: Configure video and text recordings / PSM for SSH</sub>

---

## Domain 1 — Onboard Accounts

### Q204. You are enabling PTA's automatic "Add to Pending" response for unmanaged credentials. Which Safe does the PTA user need permissions on, and roughly what kind of permissions?

- **A.** `PasswordManager_Pending` — enough to list and add accounts, update their properties and manage the Safe
- **B.** `PVWAReports` — read only
- **C.** `System` — full control
- **D.** `PSMRecordings` — add and delete

**Answer: A**

*Why:* "Add to Pending" writes discovered-but-unmanaged accounts into the Pending Accounts store, which is backed by the `PasswordManager_Pending` Safe. The PTA user therefore needs write-level membership there — listing, adding accounts including their properties, and Safe management — otherwise the remediation silently fails.

*Why not the others:* B holds generated reports. C is a Vault system Safe. D holds session recordings. All three are the wrong Safe for pending accounts.

<sub>Source area: PTA automatic remediation / pending accounts</sub>

---

## Domain 2 — Manage the Application

### Q205. A large enterprise has complicated network zoning between its data centres. What is the main reason to deploy more than one CPM?

- **A.** To load balance password management between CPMs
- **B.** To manage passwords on the DR Vault
- **C.** To avoid having to open complex firewall rules from one CPM to every zone
- **D.** Because a single CPM cannot manage more than 10,000 accounts

**Answer: C**

*Why:* A CPM has to reach every target it manages. In a segmented estate that means either a large and hard-to-justify set of cross-zone firewall rules, or a CPM placed inside each zone talking only outward to the Vault on 1858. The second is far easier to get approved and to maintain — which is why network topology, not throughput, is the usual driver.

*Why not the others:* A is the trap: CPMs are assigned per Safe and do **not** load balance or fail over between each other. B is not how DR works. D understates capacity — a tuned CPM handles around 100,000 managed passwords.

<sub>Source area: Multiple CPMs / CPM deployment</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q206. You must recover and decrypt an object from a Safe after a Vault failure. Which three items does the recovery need? (Choose three)

- **A.** The Recovery private key (RecPrv.key)
- **B.** The Recovery public key (RecPub.key)
- **C.** The Server key (Server.key)
- **D.** The Master user's password alone

**Answer: A, B, C**

*Why:* The chain has to be reassembled from the outside in: the Server key opens the Vault's own layer, and the Recovery key pair is what allows the Safe keys to be decrypted independently of normal operation — the Safe key is encrypted both with the Server key and with RecPub, so RecPrv is what unlocks it during recovery.

*Why not the others:* D is not sufficient on its own. The Master password gets the Master user *logged on*, but without the recovery key material there is nothing to decrypt the Safe key with. This is why the Recovery private key must be stored on physical media in at least two secure locations.

<sub>Source area: Vault recovery / encryption keys</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q207. A user's dual-control request is waiting and nobody knows who can approve it. Where do you look to identify the approvers?

- **A.** Platform Management → the platform → UI & Workflows → Dual Control → Approvers
- **B.** The Safe's members: Access Control (Safes) → Safe Members → Workflow → the permission that authorizes account/password requests
- **C.** The account's Advanced Settings → Dual Control → Direct Managers
- **D.** PrivateArk Client → Users and Groups → Auditors

**Answer: B**

*Why:* Dual control has two halves and this question tests the second one. The Master Policy rule decides *that* approval is required; the Safe membership decides *who* can give it. So the approvers are simply the Safe members holding the Confirm requests / authorize account requests permission — look at the Safe, not the platform.

*Why not the others:* A is where session and password-display behaviour is configured, not approvers. C is invented. D is the audit group, which grants visibility rather than approval rights.

<sub>Source area: Dual control / Safe member workflow permissions</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q208. You are configuring the Vault for LDAP over SSL. Which certificate must be imported, and where?

- **A.** The CA certificate that signed the external directory's certificate, imported into the Vault machine's Windows certificate store
- **B.** A CA-signed certificate for the Vault server
- **C.** A CA-signed certificate for the PVWA server
- **D.** A self-signed certificate generated on the Vault

**Answer: A**

*Why:* For LDAPS the Vault is the *client*: it must be able to validate the certificate the directory presents. That means trusting the issuer — so you import the CA certificate that signed the directory's certificate into the Vault machine's certificate store.

*Why not the others:* B and C would be needed if the Vault or PVWA were presenting a certificate, which is not what happens here. D would not establish trust in the directory. Ports to remember alongside this: 389 LDAP, 636 LDAPS, 3268/3269 for the Global Catalog.

<sub>Source area: LDAP over SSL</sub>

---

### Q209. A member of the Vault Administrators team can log in but has no Vault Admin rights. Where do you check that the Vault Admins directory mapping points at the right AD group?

- **A.** PrivateArk Client → Tools → Administrative Tools → Directory Mapping
- **B.** In the PVWA, under User Provisioning → LDAP Integration, at the mapping's criteria
- **C.** PVWA → Administration → LDAP Integration → AD Groups
- **D.** On the Vault, in `dbparm.ini`

**Answer: B**

*Why:* Directory mappings are listed in the PVWA under User Provisioning → LDAP Integration, each with a map order, a map name and its mapping criteria — the LDAP group(s) it matches. That is where you confirm that the "Vault Admins" map is pointing at the group the person is actually in.

*Why not the others:* A and C name paths that do not exist in this form. D holds Vault configuration such as `AutoSyncExternalObjects`, not the mappings themselves. Remember mappings are evaluated in order, so map order matters as much as the criteria.

<sub>Source area: LDAP integration — directory mappings</sub>

---

## Domain 2 — Manage the Application

### Q210. A customer wants the Safes data stored on drive D rather than drive C. Which file do you edit?

- **A.** `tsparm.ini`
- **B.** `Vault.ini`
- **C.** `dbparm.ini`
- **D.** `user.ini`

**Answer: A**

*Why:* `tsparm.ini` defines the directories where the Safes are located, so relocating Safe storage to another drive is a `tsparm.ini` change. It is a genuinely useful one to know because Vault storage growth is a common operational problem.

*Why not the others:* B holds the Vault's address and port for components. C is the main Vault configuration — debug level, firewall rules, syslog, thresholds. D is a credential file. All four are Vault-adjacent .ini files, which is exactly why they get confused.

<sub>Source area: tsparm.ini</sub>

---

## Domain 6 — Configure Session Management

### Q211. You are setting up a Linux host as an HTML5 Gateway for PSM sessions. Which servers must the Linux host trust for the communication to be secured?

- **A.** The PSM and the PVWA
- **B.** The PSM and the CPM
- **C.** The PVWA and the Vault
- **D.** The Vault and the PSM

**Answer: A**

*Why:* The gateway sits between the browser and the PSM, and it validates a token issued by the PVWA. So it needs to trust both ends of what it brokers: the **PVWA** (which authenticates the user and issues the session token) and the **PSM** (which it opens the RDP connection to).

*Why not the others:* The Vault appears in two distractors, but the gateway never talks to the Vault — it has no Vault credential and opens no session on 1858. The CPM is not in this path at all.

<sub>Source area: Secure access with an HTML5 Gateway</sub>

---

## Domain 3 — Perform Ongoing Maintenance & Troubleshooting

### Q212. You have pointed a stand-alone Vault at the organisation's NTP servers. What is the last step to make the change effective?

- **A.** Restart the Vault application from the PrivateArk Client
- **B.** Restart the Vault application using the PrivateArk Server Central Administration Console
- **C.** Restart the organisation's NTP servers
- **D.** Restart the Event Notification Engine service

**Answer: B**

*Why:* Time configuration is picked up when the Vault application restarts, and on a hardened Vault the supported way to stop and start the application is the Server Central Administration Console on the Vault itself (the Remote Control Client does the equivalent from an administration station over 9022).

*Why not the others:* A — the PrivateArk Client is a data and user administration interface; it does not control the Vault service. C is outside your control and unnecessary. D restarts notifications only.

<sub>Source area: NTP integration / Vault administration</sub>

---

## Domain 6 — Configure Session Management

### Q213. Match the built-in connection component to what it connects to. Which mapping is entirely correct?

- **A.** PSM-SSH → UNIX; PSM-RDP → Windows; PSM-WinSCP → UNIX file transfer; PSM-SQLPlus → database; PSM-OS390 → mainframe
- **B.** PSM-SSH → Windows; PSM-RDP → UNIX; PSM-WinSCP → database; PSM-SQLPlus → mainframe
- **C.** PSM-SSH → UNIX; PSM-RDP → Windows; PSM-WinSCP → database; PSM-SQLPlus → UNIX file transfer
- **D.** PSM-SSH → database; PSM-RDP → Windows; PSM-WinSCP → mainframe; PSM-SQLPlus → UNIX

**Answer: A**

*Why:* The names describe the client the PSM launches, so the mapping follows the tool: SSH for UNIX shells, RDP for Windows desktops, WinSCP for file transfer to UNIX, SQL*Plus for Oracle databases, and OS390 for mainframe sessions. Matching-style questions like this are common, and reasoning from the client name is faster than memorising a table.

*Why not the others:* The other rows shuffle the pairings. Also worth holding: PSM-TOAD and PSM-SQLServerMgmtStudio are database clients too, and PSM-PVWA, PSM-MS-Azure and PSM-AWSConsoleWithSTS cover web consoles.

<sub>Source area: Connection components</sub>

---

## Domain 3 — Perform Ongoing Maintenance & Troubleshooting

### Q214. You are working through the post-installation tasks after a PSM installation. Which of these is one of them?

- **A.** Disable the screen saver for the PSM local users
- **B.** Create the `PSMShadowUsers` group manually
- **C.** Reset the `PSMAdminConnect` password every 24 hours
- **D.** Enable load balancing on the PSM server itself

**Answer: A**

*Why:* A screen saver kicking in inside a PSM session interferes with the session and its recording, so disabling it for the PSM local users is a documented post-install step — alongside checking the installation logs, enabling maintenance users to log on remotely, configuring users for PSM sessions, and the RDS considerations.

*Why not the others:* B — `PSMShadowUsers` is created by the installation. C is not a required routine. D — load balancing is arranged in front of the PSM servers, not switched on inside one.

<sub>Source area: PSM post-installation tasks</sub>

---

### Q215. Which two utilities are involved in renaming a CPM? (Choose two)

- **A.** The APIKeyManager utility
- **B.** The CreateCredFile utility
- **C.** `PMTerminal.exe`
- **D.** `CPMinDomain_Hardening.ps1`

**Answer: A, B**

*Why:* Renaming a CPM means the component's identity changes, so its authentication material has to be reissued: `CreateCredFile` rebuilds the credential file for the renamed user, and `APIKeyManager` handles the key material where the component authenticates with an API key. Remember too that three Safe names must **not** be renamed alongside it — `PasswordManager_Pending`, `PasswordManagerShared` and `PasswordManagerTemp`.

*Why not the others:* C is a terminal plug-in used by CPM plug-ins to drive text-based targets. D is a hardening script. Neither participates in the rename.

<sub>Source area: Rename a CPM</sub>

---

### Q216. A DR Vault is operating normally in replication mode. Which set of service states is correct?

- **A.** PrivateArk Server stopped; PrivateArk Database running; Hardened Windows Firewall running; CyberArk Vault Disaster Recovery running; Event Notification Engine stopped
- **B.** All five services running
- **C.** PrivateArk Server running; CyberArk Vault Disaster Recovery stopped
- **D.** PrivateArk Server running; Event Notification Engine running; Disaster Recovery running

**Answer: A**

*Why:* In replication mode the DR machine is a replica, not a Vault: the **PrivateArk Server is deliberately stopped** so it cannot serve clients, while the database and the firewall run, and the Disaster Recovery service runs because it is the thing doing the replicating. ENE stays stopped so the DR does not send duplicate notifications.

*Why not the others:* B and D describe a failed-over Vault, not a replica — and if the PrivateArk Server were running on both, you would have split brain. C inverts the two services that matter most. Recall the failover order: synchronise the database, start the PrivateArk Server, start ENE, then stop the DR service.

<sub>Source area: DR Vault — replication mode</sub>

---

## Domain 2 — Manage the Application

### Q217. Which components support fault tolerance?

- **A.** CPM and PVWA
- **B.** PVWA and PSM
- **C.** PSM and PTA
- **D.** CPM and PTA

**Answer: B**

*Why:* PVWAs sit behind a load balancer and PSMs can be pooled, so both scale out and tolerate the loss of a node. The **CPM deliberately does not**: two CPMs acting on the same Safe would fight over the same accounts, so a Safe has exactly one active CPM and there is no automatic failover between them.

*Why not the others:* Every wrong option includes the CPM or PTA. If a CPM is lost, recovery is a deliberate reassignment of its Safes to another CPM — which is exactly why CPM placement and Safe assignment deserve thought at design time.

<sub>Source area: Component high availability</sub>

---

### Q218. Distributed Vaults are being used together with the PSM. What additional component must be present on the Vault?

- **A.** RabbitMQ
- **B.** A second Disaster Recovery Vault
- **C.** The Remote Control Client
- **D.** A dedicated Distributed Vault Server role

**Answer: A**

*Why:* A message broker is needed so session data — recordings and live-session state — is propagated correctly between the Primary Vault and its Satellites when the PSM is in the picture. RabbitMQ fills that role in a Distributed Vault deployment.

*Why not the others:* B is a separate disaster-recovery topology. C administers Vault services over 9022. D is not a separate installable component — a Distributed Vault is up to six Vault servers, one Primary and five Satellites.

<sub>Source area: Distributed Vaults with PSM</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q219. In the PrivateArk Client, how do you add an LDAP group to a CyberArk group?

- **A.** Select Update on the CyberArk group, then Add → LDAP Group
- **B.** Select Update on the LDAP group, then Add → LDAP Group
- **C.** Select Member Of on the CyberArk group, then Add → LDAP Group
- **D.** Select Member Of on the LDAP group, then Add → LDAP Group

**Answer: A**

*Why:* You are editing the CyberArk group's membership, so you update **that** group and add the LDAP group into it. Nesting an LDAP group inside a CyberArk group is the clean way to grant Safe permissions: permissions go to the CyberArk group, and directory membership decides who lands in it.

*Why not the others:* B and D start from the wrong object. C confuses the two tabs: *Member Of* shows which groups an object belongs to; *Update* is where you edit an object's own membership list.

<sub>Source area: PrivateArk Client — users and groups</sub>

---

### Q220. Which option in the PrivateArk Client is used to change which Vault groups a user belongs to?

- **A.** Update → General tab
- **B.** Update → Authorizations tab
- **C.** Update → Member Of tab
- **D.** Update → Group tab

**Answer: C**

*Why:* *Member Of* is the tab that lists the groups a user belongs to and lets you add or remove them. Getting this right matters because group membership is how Safe permissions should be delivered — permissions granted to a user directly are lost if that user object is ever deleted and recreated.

*Why not the others:* A holds identifying details. B is where Vault-level authorizations are set — a different permission plane entirely. D does not exist.

<sub>Source area: PrivateArk Client — users and groups</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q221. You need a licence capacity report showing how much of the licence is consumed. Which tool produces it?

- **A.** The PVWA Reports tab
- **B.** The PrivateArk Client
- **C.** The DiagnoseDB report
- **D.** The REST API only

**Answer: B**

*Why:* Licence information is exposed through the PrivateArk Client's administrative tools, because the licence is a Vault-level object — `License.xml` living in the `System` Safe. The PVWA's reports are about accounts, compliance, entitlements and activity, not licence consumption.

*Why not the others:* A produces the account and audit reports. C is a database diagnostic. D — while much is scriptable, the licence capacity view is not the documented answer here. Note the Telemetry Tool also surfaces licence utilisation, but as an adoption dashboard in the Technical Community rather than as a Vault report.

<sub>Source area: Vault licence management</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q222. You have just configured a usage (a credential embedded in a web.config file) in CyberArk and want to update its password. What is the least intrusive way?

- **A.** Use the Change button on the usage's own details page
- **B.** Use the Change button on the parent account's details page
- **C.** Use the Sync button on the usage's details page
- **D.** Use the Reconcile button on the parent account's details page

**Answer: B**

*Why:* A usage is a *copy* of the parent account's credential, not an independent secret. Changing the parent is what triggers the CPM to generate the new value, set it on the target, and then propagate it into every usage — which is the whole point of dependency management. Acting on the parent is therefore both the correct and the least intrusive route.

*Why not the others:* A and C would treat the usage as independent, risking the copy diverging from the account it belongs to. D is a heavier operation that uses the reconcile account to force a new password, appropriate when the credential is unknown or out of sync — not for a routine update.

<sub>Source area: Manage dependent accounts / usages</sub>

---

## Domain 1 — Onboard Accounts

### Q223. Which properties are mandatory in a bulk account upload file? (Choose three)

- **A.** Safe name
- **B.** Platform ID
- **C.** Any additional properties the selected platform marks as required
- **D.** Hostname

**Answer: A, B, C**

*Why:* The upload screen states it plainly: Safe name and Platform ID are mandatory, and other properties may be required depending on the platform policy. That last clause is the one people miss — a platform such as an Oracle or Windows domain platform can require a port, database name or domain, and rows missing them fail.

*Why not the others:* D is not a mandatory upload property. Also worth remembering from the same screen: up to 10,000 accounts per file, accounts are created only in Safes that already exist, and only target accounts can be created — not linked or dependent accounts.

<sub>Source area: Add multiple accounts from a file</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q224. The organisation requires that users check out a password *and* connect to the target with that same account through the PSM. Which Master Policy configuration delivers this?

- **A.** Enforce check-in/check-out exclusive access = active; Require privileged session monitoring and isolation = active
- **B.** Both rules inactive
- **C.** Exclusive access inactive; Record and save session activity active
- **D.** Exclusive access active; Record and save session activity inactive

**Answer: A**

*Why:* The requirement has two halves and each maps to one rule. "Check out" is exclusive access — one user holds the account at a time and must check it back in. "Connect through the PSM" is the session monitoring and isolation rule, which is what puts the Connect button in front of the user and brokers the session.

*Why not the others:* B delivers neither. C drops the check-out half. D switches on the wrong second rule — recording governs whether session activity is captured, which is valuable but is not what makes the PSM connection happen.

<sub>Source area: Master Policy — session management and exclusive access</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q225. PTA raises a "Suspected Credential Theft" event. Which automatic remediation is configurable for that detection?

- **A.** Add to Pending
- **B.** Rotate credentials
- **C.** Disable the account
- **D.** Delete the account

**Answer: B**

*Why:* Match the response to the problem. If a credential is suspected stolen, the containment that actually helps is changing it, which invalidates whatever the attacker holds. Rotation is therefore the configurable automatic response for this detection.

*Why not the others:* A is the right response to a *different* detection — unmanaged privileged access, where the account is not in the Vault yet and needs onboarding. C and D are not part of PTA's remediation set; PTA's actions are onboard, rotate and reconcile, plus suspend or terminate a live session where PSM is integrated.

<sub>Source area: PTA — automatic remediation</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q226. You need to log in as the Master user to recover an orphaned Safe. What is required?

- **A.** The Master CD, the Master password, console access to the Vault server, and the PrivateArk Client
- **B.** The Operator CD, the Master password, console access to the PVWA server and PVWA access
- **C.** The Operator CD, the Master password, console access to the Vault server and Recover.exe
- **D.** The Master CD, the Master password, console access to the PVWA server and Recover.exe

**Answer: A**

*Why:* The Master user is a deliberately awkward break-glass identity, and every element of that awkwardness is a control. It logs on **only through the PrivateArk Client**, **only from the Vault console** (or from the address named by `EmergencyStationIP`), and it needs the Master CD holding the Private Recovery Key alongside the Master password.

*Why not the others:* Every wrong option substitutes the PVWA for the Vault console, or the Operator CD for the Master CD. The Master user never logs on through the web interface — that restriction is the point.

<sub>Source area: Master user / Vault recovery</sub>

---

## Domain 3 — Perform Ongoing Maintenance & Troubleshooting

### Q227. A CPM password change fails with: "Error in changepass to user domain\user on domain server (winRc=5) Access is denied." The CPM can log on and verify the account successfully. What should you investigate first?

- **A.** That the account has permission to change its own password
- **B.** That the domain controller is unreachable
- **C.** That the CPM service is stopped
- **D.** That the Vault firewall is blocking 1858

**Answer: A**

*Why:* The diagnostic clue is that logon and verification work — so connectivity, credentials and the CPM itself are all fine. What fails is specifically the change operation, and winRc=5 is a Windows access-denied on that operation. That points at rights: the account cannot change its own password, so either it needs that right or the platform needs a reconcile account with the privilege to change it on its behalf.

*Why not the others:* B and C would break verification too, which is the detail the question gives you to rule them out. D would stop the CPM authenticating to the Vault entirely. Minimum password age is a real cause of change failures, but it produces a different error than access-denied.

<sub>Source area: CPM troubleshooting — password change failures</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q228. A new domain controller has been added. Which locations must you update so the CyberArk infrastructure can authenticate against it?

- **A.** The hosts file on the Vault server, and the directory's host list in the PVWA under LDAP Integration → Directories
- **B.** The hosts file on the Vault server and the hosts file on the PVWA server
- **C.** PrivateArk Client → Tools → Administrative Tools → Directory Mapping
- **D.** The certificate store on both the Vault and the PVWA

**Answer: A**

*Why:* Two places, because two things need to know about the new DC. The hardened Vault resolves the directory host through its own hosts file, and the LDAP integration definition in the PVWA carries an explicit list of directory hosts that the configuration uses. Add the DC in both or authentication will keep favouring the old ones.

*Why not the others:* B updates name resolution twice and never updates the integration definition. C is where users and groups are mapped to Vault objects, not where DC hosts are listed. D would matter for LDAPS trust, but adding a DC is not a certificate problem.

<sub>Source area: LDAP integration — directories and hosts</sub>

---

## Domain 2 — Manage the Application

### Q229. Which component must be installed before the first CPM installation?

- **A.** PTA
- **B.** PSM
- **C.** PVWA
- **D.** EPM

**Answer: C**

*Why:* The PVWA comes first because the CPM's registration and configuration flow depends on it — which is the same dependency that later makes CPM → PVWA on TCP 443 a hard requirement for Accounts Discovery. The usual build order is Vault, then PrivateArk Client, then DR, then PVWA, then CPM, then PSM.

*Why not the others:* A, B and D are all installed later and none of them is a prerequisite for the CPM. PTA and EPM are optional components entirely.

<sub>Source area: Component installation order</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q230. Which statement about the Vault's key and credential files is correct?

- **A.** `Backup.Key` encrypts the Vault's backup sets and is itself encrypted with the Server key
- **B.** `VaultEmergency.Pass` is protected with the Server key
- **C.** `Server.pvk` is stored unencrypted so the Vault can start
- **D.** `RecPub.key` is used to decrypt Safe keys

**Answer: A**

*Why:* The pattern to hold on to is that almost everything hangs off the Server key, with one deliberate exception. `Backup.Key`, `VaultUser.Pass` and the `Server.pvk` private key are all encrypted with the Server key; `VaultEmergency.Pass` is the exception, protected with the Master key (RecPrv.key) so emergency database access survives loss of the Server key.

*Why not the others:* B names the exception and gets it backwards. C is false — the Vault certificate's private key is encrypted like the rest. D inverts the key pair: RecPub **encrypts** the Safe keys and RecPrv decrypts them.

<sub>Source area: Vault key files</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q231. You are creating a shared Safe for the help desk. Which naming constraint is correct?

- **A.** The name may not exceed 20 characters
- **B.** The characters \ . " : < > | are not allowed in a Safe name
- **C.** Safe owners should choose the name so it is memorable to them
- **D.** Environments, owners and platforms should be combined to minimise the number of Safes

**Answer: B**

*Why:* Safe names cannot contain the characters `\ . " : < > |`. Alongside that, the name is capped at 28 characters and the Safe is the unit of access control, so a short consistent convention such as `HD-WIN-PRD` works and free text does not.

*Why not the others:* A gets the limit wrong — it is 28, not 20. C hands naming to individuals and produces an unmanageable estate. D is the opposite of good design: merging populations that need different access into one Safe destroys the access boundary.

<sub>Source area: Safe naming conventions</sub>

---

## Domain 2 — Manage the Application

### Q232. You are configuring the Vault to send syslog audit data to a SIEM. Which is a valid value for the `SyslogServerProtocol` parameter in `dbparm.ini`?

- **A.** TLS
- **B.** SSH
- **C.** SMTP
- **D.** SNMP

**Answer: A**

*Why:* `SyslogServerProtocol` accepts the transports syslog itself supports — TLS, TCP and UDP — with TLS being the one to choose for an audit feed, since it encrypts records in transit. The default port is 514, and like every `dbparm.ini` change it needs a Vault restart.

*Why not the others:* B is a remote shell protocol. C is email — that is the ENE's channel. D is SNMP, configured separately in `paragent.ini` with `SNMPHostIP`, `SNMPTrapPort` and `SNMPCommunity`.

<sub>Source area: SIEM / syslog integration</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q233. What must be done before CyberArk can be configured to use RADIUS authentication?

- **A.** Define the CyberArk Vault as a client (agent) on the RADIUS server
- **B.** Set the authentication method to RADIUS on each user in the PrivateArk Client
- **C.** Run `CAVaultManager SecureSecretFiles` in the Vault installation folder
- **D.** Set `RadiusServersInfo` in `dbparm.ini`

**Answer: A**

*Why:* RADIUS is a mutual arrangement: the RADIUS server only answers requests from clients it knows, so the Vault must first be registered there as a RADIUS client or agent with a shared secret. Everything on the CyberArk side comes afterwards.

*Why not the others:* B and D are both real later steps — you do set `RadiusServersInfo` in `dbparm.ini` and you do set each user's authentication method — but neither works until the RADIUS server accepts the Vault. C is a Vault secrets utility unrelated to RADIUS.

<sub>Source area: RADIUS authentication</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q234. You are onboarding 5,000 UNIX root accounts. The CPM cannot log in directly as root and must use a secondary account. What is the least-privilege way to configure this?

- **A.** Configure each CPM to use the correct logon account
- **B.** Configure each CPM to use the correct reconcile account
- **C.** Configure the UNIX platform to use the correct logon account
- **D.** Configure the UNIX platform to use the correct reconcile account

**Answer: C**

*Why:* Two decisions here. First, the problem is *reaching* the account, not that the password is unknown — so it is a **logon** account, which can be low-privilege and simply elevates. Second, the linkage belongs on the **platform**, so one configuration covers all 5,000 accounts instead of being repeated per CPM.

*Why not the others:* A and B put the setting in the wrong place — a CPM is a worker, not a policy container. D reaches for the reconcile account, which is far more privileged than this situation needs; save it for when the password is unknown or out of sync.

<sub>Source area: Linked accounts — logon accounts</sub>

---

### Q235. Your organisation requires that all passwords be rotated every 90 days. Where do you express that requirement?

- **A.** The Master Policy
- **B.** Safe templates
- **C.** `PVWAConfig.xml`
- **D.** Individually on each platform

**Answer: A**

*Why:* A regulatory requirement that applies to everything is exactly what the Master Policy is for — it is the single place the organisation's baseline is stated, so there is one thing to point an auditor at. Platforms then handle the mechanics, and genuine exceptions are added deliberately and visibly.

*Why not the others:* B governs default Safe properties. C is a PVWA configuration file. D would scatter the same rule across dozens of platforms with no single source of truth — the classic mistake this question is testing.

<sub>Source area: Master Policy</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q236. Which built-in PVWA report shows the number of days remaining until a password is due to expire?

- **A.** Privileged Accounts Inventory
- **B.** Privileged Accounts Compliance Status
- **C.** Activity Log
- **D.** Applications Inventory

**Answer: B**

*Why:* Compliance Status is the forward-looking report: it shows whether each account is being managed in line with its policy, including how long is left before the next required change. That makes it the one to run when you want to see what is about to fall out of compliance rather than what already has.

*Why not the others:* A is a census of what exists. C is a record of what has already happened. D covers applications using Application Access Manager.

<sub>Source area: PVWA reports</sub>

---

## Domain 3 — Perform Ongoing Maintenance & Troubleshooting

### Q237. Match the component to where its logs live. Which set is correct?

- **A.** PTA: `/opt/tomcat/logs` · PSM for SSH: `/var/opt/CARKpsmp/logs` · DR: `…\PrivateArk\Server\PADR`
- **B.** PTA: `/var/opt/CARKpta` · PSM for SSH: `/opt/tomcat/logs` · DR: `…\PrivateArk\Server\Logs`
- **C.** PTA: `/opt/PTA/logs` · PSM for SSH: `/opt/psmp/logs` · DR: `…\PrivateArk\Safes`
- **D.** All three write to the Vault's `Logs` folder

**Answer: A**

*Why:* PTA runs on Tomcat, so its logs sit under `/opt/tomcat/logs`. PSM for SSH keeps its own set under `/var/opt/CARKpsmp/logs` (`PSMPConsole.log`, `PSMPTrace.log`). The DR service logs to the `PADR` folder under the PrivateArk Server directory, where `PADR.log` lives.

*Why not the others:* The other rows shuffle the paths. A useful hook: PTA is a Tomcat application, PSMP is a CARK* package under `/var/opt`, and DR belongs to the PrivateArk Server installation.

<sub>Source area: Component log locations</sub>

---

### Q238. Email alert settings on PTA need changing after installation. Which script do you run?

- **A.** `/opt/tomcat/utility/emailConfiguration.sh`
- **B.** `/opt/PTA/emailConfiguration.sh`
- **C.** `/opt/PTA/utility/emailConfig.sh`
- **D.** `/opt/tomcat/utility/emailSetup.sh`

**Answer: B**

*Why:* PTA's post-install email configuration is handled by `emailConfiguration.sh` under `/opt/PTA`. It is worth pairing in your memory with the other PTA utility you may need — `vaultPermissionsValidation.sh` in the utility folder, for re-syncing the `PTA_PAS_Gateway` account.

*Why not the others:* The other options mix up the directory (`/opt/tomcat` is where PTA's logs live, not its utilities) or the script name. Version 14.0 also moved many PTA settings into the PVWA interface, so check there first on current versions.

<sub>Source area: PTA — post-installation configuration</sub>

---

### Q239. A network glitch caused the PrivateArk Server to become active on the DR Vault while the Primary Vault was still running normally, and all components stayed pointed at the Primary. What restores DR replication?

- **A.** Replicate data from the DR Vault to the Primary, then shut down the PrivateArk Server on DR, then start replication
- **B.** Shut down the PrivateArk Server on the DR Vault, then start replication on the DR Vault
- **C.** Shut down the PrivateArk Server on the Primary, replicate from DR to Primary, shut down DR, start replication
- **D.** Shut down the PrivateArk Server on DR, replicate DR to Primary, shut down DR again, start replication

**Answer: B**

*Why:* The key detail is that the components never left the Primary — so the Primary holds the authoritative data and nothing on the DR needs preserving. You simply put the DR back into replica mode: stop its PrivateArk Server (a replica must not serve) and restart replication, which pulls a fresh copy from the Primary.

*Why not the others:* A, C and D all replicate *from* the DR to the Primary, which would push stale or divergent data over the good copy. Recognising which side is authoritative is the whole question.

<sub>Source area: DR Vault — recovering from split brain</sub>

---

## Domain 2 — Manage the Application

### Q240. Which parameters can be used to harden a credential file when it is generated with `CreateCredFile`? (Choose three)

- **A.** The operating system username the file may be used by
- **B.** The host IP address
- **C.** The client hostname
- **D.** The operating system type (Linux / Windows / HP-UX)

**Answer: A, B, C**

*Why:* Hardening a credential file means binding it to the context it is allowed to be used from — the OS user, the machine's IP address and its hostname, plus an entropy file. Present it from anywhere else and the Vault rejects it, which is why copying a credential file to another server never works.

*Why not the others:* D is not one of the hardening parameters. Nor are the Vault's own IP address or a time frame — all plausible-sounding, none of them real.

<sub>Source area: CreateCredFile utility</sub>

---

## Domain 3 — Perform Ongoing Maintenance & Troubleshooting

### Q241. Following a Vault installation, which service must be set to Automatic (delayed start)?

- **A.** Windows Time service
- **B.** PrivateArk Database
- **C.** Windows Update service
- **D.** PrivateArk Server

**Answer: A**

*Why:* The Windows Time service is set to Automatic (delayed start) so time synchronisation is running but does not compete with the Vault services during boot. Accurate time matters more than it looks: it underpins Kerberos, certificate validity and the correlation of audit records across components.

*Why not the others:* B and D are Vault services set to start normally. C should be tightly controlled on a hardened Vault — a Vault is patched deliberately, not by automatic Windows Update.

<sub>Source area: Following Vault installation</sub>

---

### Q242. Users cannot launch web-type connection components from the PSM server and Support has asked for logs. Which three help? (Choose three)

- **A.** `PSMConsole.log`
- **B.** `PSMTrace.log`
- **C.** `<Session_ID>.Component.log` under `PSM\Logs\Components`
- **D.** `ITALog.log`

**Answer: A, B, C**

*Why:* Diagnosis works from general to specific: `PSMConsole.log` shows what the PSM service did, `PSMTrace.log` adds detail once tracing is raised, and the per-session component log under `PSM\Logs\Components` captures what the launched client itself did — which is where a failing web connector actually shows up.

*Why not the others:* D is the Vault's main log and knows nothing about a browser failing to start on a PSM. `PSMDebug.log` and `PMconsole.log` are also distractors — the latter belongs to the CPM.

<sub>Source area: PSM log files</sub>

---

### Q243. What is the default username for the PSM for SSH maintenance user?

- **A.** `proxymng`
- **B.** `psmp_maintenance`
- **C.** `psmpmaintenanceuser`
- **D.** `psmpmnguser`

**Answer: A**

*Why:* `proxymng` is the default maintenance account on a PSM for SSH server — the identity you use to administer the host itself rather than being intercepted and brokered like an ordinary SSH connection. Which accounts get that treatment is controlled by `PSMP_MaintenanceUsers` in `sshd_config`.

*Why not the others:* The other three are invented names that follow the pattern you would expect, which is exactly why this is asked as a recall question.

<sub>Source area: PSM for SSH — maintenance users</sub>

---

## Domain 6 — Configure Session Management

### Q244. A customer wants to keep PSM recordings for 100 days and expects 10 Windows sessions per day of 100 minutes each. Roughly how much storage should you plan for the Vault?

- **A.** About 40 GB
- **B.** About 250 GB
- **C.** About 500 GB
- **D.** About 5 GB

**Answer: A**

*Why:* Work it through: 100 days × 10 sessions × 100 minutes = 100,000 minutes. At 200 KB per minute for low-activity RDP that is 20,000,000 KB ≈ 19 GB; at 300 KB per minute for high-activity RDP it is about 29 GB. Add the 20 GB constant the sizing formula includes and you land near 39–49 GB.

*Why not the others:* B and C over-estimate by roughly an order of magnitude — and note that some third-party question banks give 250 GB here, which the arithmetic does not support. D forgets the 20 GB constant. Remember the rates: 100 / 200 / 300 KB per minute for SSH / low-activity RDP / high-activity RDP.

<sub>Source area: PSM recording sizing</sub>

---

## Domain 2 — Manage the Application

### Q245. What is mandatory for a PVWA installation?

- **A.** A DNS entry for the PVWA URL
- **B.** A company-signed TLS certificate imported into the server
- **C.** A Vault administrative user, used to register the PVWA with the Vault
- **D.** Data Execution Prevention must be disabled

**Answer: C**

*Why:* The PVWA has to introduce itself to the Vault: registration creates its component users and its Safes (`PVWAConfig`, `PVWAReports`, `PVWAUserPrefs` and the rest), and that requires an administrative Vault user. Without it the installation cannot complete.

*Why not the others:* A and B are strongly recommended in production but are not installation blockers. D is a security feature you would never disable on a CyberArk component.

<sub>Source area: PVWA installation requirements</sub>

---

## Domain 6 — Configure Session Management

### Q246. User `neil` needs to reach Linux target 192.168.1.164 as the **domain** account `linuxuser01` on domain `acme.corp`, through the PSM for SSH server 192.168.65.145. What is the correct syntax?

- **A.** `ssh neil@linuxuser01:acme.corp@192.168.1.164@192.168.65.145`
- **B.** `ssh neil@linuxuser01#acme.corp@192.168.1.164@192.168.65.145`
- **C.** `ssh neil@linuxuser01@192.168.1.164@192.168.65.145`
- **D.** `ssh neil@linuxuser01@acme.corp@192.168.1.164@192.168.65.145`

**Answer: B**

*Why:* The base pattern is `vaultuser@targetaccount@targetaddress@psmpaddress`. When the target account is a **domain** account, the domain is attached to the account with a **hash**: `targetaccount#domainaddress`. So the four elements stay in the same order and only the second one gains the `#domain` suffix.

*Why not the others:* A uses a colon. C omits the domain entirely, which would look for a local account. D separates the domain with `@`, which breaks the four-part structure by adding a fifth element.

<sub>Source area: PSM for SSH — connection syntax</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q247. A company requires challenge/response multi-factor authentication for PSM for SSH sessions. Which server must be integrated with the Vault?

- **A.** LDAP
- **B.** PKI
- **C.** SAML
- **D.** RADIUS

**Answer: D**

*Why:* RADIUS is the protocol built around a challenge/response exchange, which is what lets a token, push or one-time code be demanded as a second factor. That is why it is the integration behind MFA for PSMP sessions.

*Why not the others:* A authenticates and provisions users but is single-factor on its own. B is certificate-based. C is a web browser federation protocol and does not apply to an SSH session. Note the related fact: PSM for SSH supports CyberArk password, LDAP and RADIUS authentication.

<sub>Source area: RADIUS authentication / PSM for SSH</sub>

---

## Domain 6 — Configure Session Management

### Q248. Which browser is supported for PSM web connectors built with the CyberArk Plugin Generator Utility (PGU)?

- **A.** Internet Explorer
- **B.** Google Chrome
- **C.** Microsoft Edge
- **D.** Firefox

**Answer: B**

*Why:* PGU-generated web connectors drive Chrome, which is why PSM hardening includes a Chrome-specific step (`PSMChromeHardening`) and why the hardening variable `$SUPPORT_WEB_APPLICATIONS` exists — a browser inside a PSM session needs some of the lockdown relaxed in a controlled way.

*Why not the others:* A is legacy and long out of support for this purpose. C and D are not the supported target for PGU connectors.

<sub>Source area: PSM — Plugin Generator Utility</sub>

---

## Domain 2 — Manage the Application

### Q249. Which Vault authorizations does the CyberArk user performing a CPM installation need?

- **A.** Add Safes, Add/Update Users, Manage Directory Mapping
- **B.** Add Safes, Add/Update Users, Reset Users' Passwords, Activate Users, Manage Server File Categories
- **C.** Manage Directory Mapping, Backup All Safes, Restore All Safes
- **D.** Audit Users, Activate Users, Add Network Areas, Manage Directory Mapping

**Answer: B**

*Why:* Reason from what the installer actually does: it creates the CPM's Safes (Add Safes), creates and configures its component users (Add/Update Users, Reset Users' Passwords, Activate Users) and registers the file categories the CPM needs (Manage Server File Categories).

*Why not the others:* A is incomplete and includes directory mapping, which the CPM install does not touch. C is a backup and recovery set. D is an audit and directory set. None of them can create the component users the CPM needs.

<sub>Source area: CPM installation requirements</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q250. When configuring SAML authentication for the PVWA, which value must be identical on both sides?

- **A.** The IdP's EntityID and the `PartnerIdentityProvider Name` in `saml.config`
- **B.** The IdP's user name and `SingleSignOnServiceUrl`
- **C.** The IdP's Audience and the `ServiceProviderName` in `saml.config`
- **D.** The IdP's hash algorithm and the certificate

**Answer: C**

*Why:* `ServiceProviderName` is the issuer string that identifies the **PVWA** to the identity provider, and it must match the Audience the IdP is configured to expect. A mismatch here is the classic "SAML response rejected" cause.

*Why not the others:* A describes a real pairing but in the wrong direction: `PartnerIdentityProvider Name` is where you enter the *IdP's* EntityID so the PVWA can recognise it — that is the mirror of the correct answer, not the same thing. B and D combine unrelated settings. `saml.config` is created by copying `saml.config.template` in the PasswordVault installation folder.

<sub>Source area: SAML authentication — saml.config</sub>

---

## Domain 1 — Onboard Accounts

### Q251. You are using the AccountUploader utility to create accounts with SSH keys. Which parameter gives the path to the private key file to attach?

- **A.** `KeyPath`
- **B.** `KeyFile`
- **C.** `ObjectName`
- **D.** `Address`

**Answer: B**

*Why:* `KeyFile` takes the full or relative path of the SSH private key file that will be attached to the account being created. The utility is the scripted equivalent of onboarding a key by hand, and the same rule applies afterwards: rotate the key immediately, because entering it exposed it.

*Why not the others:* A is a plausible-sounding name that does not exist. C names the object in the Safe and D is the target address — both real properties, neither of them the key file.

<sub>Source area: AccountUploader utility</sub>

---

## Domain 2 — Manage the Application

### Q252. What is the recommended way for a load balancer to decide that a PVWA is unavailable and should be removed from the pool?

- **A.** Monitor port 443 on the PVWA server
- **B.** Monitor port 1858 on the PVWA server
- **C.** Ping the PVWA server
- **D.** Monitor port 3389 on the PVWA server

**Answer: A**

*Why:* Health-check the port that actually carries the service. Users reach the PVWA over HTTPS on 443, so a check against 443 tests the thing that matters — the web application responding — rather than something adjacent to it.

*Why not the others:* B is the PVWA's outbound connection to the Vault; it can be perfectly healthy while IIS is down. C only proves the operating system is alive, which is the classic false-positive health check. D is RDP and has nothing to do with the service.

<sub>Source area: PVWA load balancing</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q253. Which data sources feed PTA's "unmanaged privileged account" detection?

- **A.** Logs, plus AWS and Azure where those integrations are configured
- **B.** The Vault only
- **C.** The PTA Windows Agent only
- **D.** Active Directory only

**Answer: A**

*Why:* PTA sees an unmanaged privileged account by observing it being *used* — so the signal comes from machine and network logs, extended to AWS and Azure where those integrations exist. That is also why the matching automatic remediation is "onboard the account" rather than "rotate".

*Why not the others:* B feeds the Vault-behaviour anomalies (irregular hours, irregular IP, excessive access, dormant users). C feeds the endpoint credential-theft family (LSASS, SAM hashes, browsers). D feeds the AD risk family (unconstrained delegation, risky SPN, service account logged on interactively).

<sub>Source area: PTA — detection sources</sub>

---

## Domain 2 — Manage the Application

### Q254. Which statement is correct about CPM behaviour in a Distributed Vault environment?

- **A.** CPMs can access all Vaults, Primary and Satellite
- **B.** CPMs can access only the Satellite Vaults
- **C.** CPMs can only access the Primary Vault; if it is unavailable the CPM cannot work until another Vault is promoted to Primary
- **D.** CPMs automatically fail over to the nearest Satellite

**Answer: C**

*Why:* Satellites serve **reads** to keep latency low for distributed sites; all **writes** go to the Primary. Since the CPM's whole job is writing new credentials into the Vault, it can only talk to the Primary — and if the Primary is gone, credential management stops until a Satellite is promoted.

*Why not the others:* A and B misread the read/write split. D would be a write conflict waiting to happen. This is the same principle as "a Safe has exactly one active CPM": CyberArk consistently avoids two writers.

<sub>Source area: Distributed Vaults — components and features</sub>

---

### Q255. Which components can connect to a Satellite Vault in a Distributed Vault architecture?

- **A.** CPM, EPM and PTA
- **B.** PVWA and PSM
- **C.** CPM, PVWA and PSM
- **D.** CPM and PSM

**Answer: B**

*Why:* Satellites exist to serve local read traffic, so the read-oriented components attach to them: the **PVWA** (users browsing and retrieving) and the **PSM** (fetching a credential to inject into a session). Everything that writes stays with the Primary.

*Why not the others:* Every wrong option includes the CPM, which writes new passwords and therefore needs the Primary. PTA also connects to the Primary and DR Vaults.

<sub>Source area: Distributed Vaults — components and features</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q256. You need to move a platform from using PMTerminal to the Terminal Plugin Controller (TPC). What do you do?

- **A.** In the PVWA, edit the platform → Automatic Password Management → CPM Plug-in, and set `ExeName` to `CyberArk.TPC.exe`
- **B.** Open the platform's .ini file in `PasswordManagerShared` and add `UseTPC = True`
- **C.** Add `use TPC=yes` under the States section of the platform's process file
- **D.** It cannot be changed — import a new platform version that supports TPC

**Answer: A**

*Why:* The plug-in the CPM runs for a platform is named by the `ExeName` parameter under Automatic Password Management → CPM Plug-in, so switching terminal engines is a matter of pointing that at `CyberArk.TPC.exe`. It is a good illustration of the general pattern: what the CPM executes for a platform is platform configuration, edited in the PVWA.

*Why not the others:* B and C describe hand-editing files in a Safe or a process file, which is neither the supported route nor necessary. D is wrong — the switch is a setting, not a re-import.

<sub>Source area: CPM plug-ins — Terminal Plugin Controller</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q257. Which configuration file and Vault utility are used to migrate the Server key to an HSM?

- **A.** `DBParm.ini` and `CAVaultManager.exe`
- **B.** `VaultKeys.ini` and `CAVaultManager.exe`
- **C.** `DBParm.ini` and `ChangeServerKeys.exe`
- **D.** `VaultKeys.ini` and `ChangeServerKeys.exe`

**Answer: A**

*Why:* The sequence is: stop the Vault, run `CAVaultManager.exe LoadServerKeyToHSM` (with `/WrapKey` on HSMs that require the key to be encrypted in transit), confirm it loaded, then set `ServerKey=HSM` in `DBParm.ini` and start the PrivateArk Server. After that the key is used inside the HSM and never sits in the Vault server's memory — which is why the HSM option is described as both strong and convenient.

*Why not the others:* B and D invent a `VaultKeys.ini`. C invents a `ChangeServerKeys.exe`. `CAVaultManager` is the Vault's general-purpose management utility — the same one behind `CollectLogs`, `RestoreDB` and `RecoverBackupFiles`.

<sub>Source area: Configuring HSM key management</sub>

---

### Q258. In a default installation, which group must a user belong to in order to see the Reports page in the PVWA?

- **A.** PVWAMonitor
- **B.** ReportUsers
- **C.** PVWAReports
- **D.** Operators

**Answer: A**

*Why:* `PVWAMonitor` is the default value of the `ManageReportsGroup` setting, so it is the group that gates the Reports page. Note that membership only opens the page — what a report actually returns is still bounded by the Safe permissions the running user holds.

*Why not the others:* B and C are invented; `PVWAReports` is the **Safe** that generated reports are stored in, which is what makes it a convincing distractor. D is a predefined group but not the reporting one.

<sub>Source area: PVWA reports — ManageReportsGroup</sub>

---

## Domain 1 — Onboard Accounts

### Q259. Which configuration file does the CPM Scanner use when scanning UNIX and Linux devices?

- **A.** `UnixPrompts.ini`
- **B.** `plink.exe`
- **C.** `dbparm.ini`
- **D.** `PVConfig.xml`

**Answer: A**

*Why:* Scanning a UNIX host means driving an interactive shell, so the scanner needs to recognise the prompts and responses it will meet. `UnixPrompts.ini` holds those patterns, which is also why an unusual shell banner or prompt can make a scan fail on an otherwise reachable host.

*Why not the others:* B is the SSH client binary the CPM uses to connect — a program, not a configuration file, and useful for manually testing connectivity. C is the Vault's configuration. D is a PVWA file.

<sub>Source area: Accounts Discovery — UNIX</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q260. Which is a valid combination of primary and secondary authentication for a two-factor policy?

- **A.** RSA SecurID in the PVWA and LDAP authentication
- **B.** CyberArk authentication and RADIUS authentication
- **C.** Oracle SSO and SAML authentication
- **D.** LDAP authentication and RADIUS authentication

**Answer: B**

*Why:* A second factor has to be a genuinely different kind of proof. CyberArk authentication (something you know, held in the Vault) plus RADIUS (a challenge/response token or push) satisfies that, which is why it is the documented valid pairing.

*Why not the others:* D looks reasonable but LDAP is still a password — two password checks are not two factors. A and C combine methods that do not chain as a primary/secondary pair in this way. Remember RADIUS also needs the Vault registered as a client on the RADIUS server first.

<sub>Source area: Two-factor authentication</sub>

---

## Domain 6 — Configure Session Management

### Q261. Which of these is a valid PSM recording customisation?

- **A.** Windows events text recorder with automatic play-back
- **B.** Windows events text recorder and universal keystrokes recording running simultaneously
- **C.** Universal keystrokes text recorder with the Windows events text recorder disabled
- **D.** Custom audio recording for Windows events

**Answer: C**

*Why:* The two text recorders are alternatives, not companions: you either capture Windows events (window titles and application events) or you capture universal keystrokes, and turning the keystroke recorder on means turning the events recorder off. Which you pick depends on whether the audit question is "what did they open?" or "what did they type?".

*Why not the others:* B is the trap — running both at once is not a supported configuration. A and D describe capabilities that do not exist. Video recording continues alongside whichever text recorder you choose.

<sub>Source area: Configure video and text recordings</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q262. Match each permission to the level it is granted at. Which mapping is entirely correct?

- **A.** Add Accounts → Safe · Initiate CPM account management operations → Safe · Add/Update Users → Vault · Add Safes → Vault
- **B.** Add Accounts → Safe · Initiate CPM account management operations → Safe · Add/Update Users → Vault · Add Safes → Safe
- **C.** All four are Safe-level permissions
- **D.** All four are Vault-level authorizations

**Answer: A**

*Why:* Ask what each one acts on. Adding an account and triggering CPM operations act on the contents of one Safe, so they are Safe permissions. Creating users and creating Safes act on the Vault itself, so they are Vault authorizations — granted per user in the PrivateArk Client and not inherited through groups.

*Why not the others:* B is the one to watch: some third-party question banks place **Add Safes** at Safe level, which is self-contradictory — you cannot hold a permission inside a Safe that does not exist yet. C and D collapse the distinction entirely.

<sub>Source area: Vault and Safe authorizations</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q263. A set of shared accounts will be used by end users, and the account owner wants to know who is holding a given account at any moment. Which control delivers that?

- **A.** One-time passwords alone
- **B.** Exclusive access (check-out / check-in), so only one user holds the account at a time and the Vault records who
- **C.** Object Level Access Control on the Safe
- **D.** Shared account mode on the Safe

**Answer: B**

*Why:* "Who has it right now" is a question about exclusivity. Check-out/check-in means the account is held by exactly one named Vault user until it is checked back in, and the Vault shows that state — nothing else gives you a live answer.

*Why not the others:* A is the common wrong answer and it is close: one-time passwords guarantee the value used can be tied back to one retrieval *after the fact*, which is excellent for non-repudiation but does not tell you who holds it now. In practice the two are combined — exclusive access plus one-time passwords — which is the strongest answer where it is offered. C is per-object access control. D is not a control that reveals current holders.

<sub>Source area: Exclusive access and one-time passwords</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q264. Which built-in Vault user is an internal user that cannot be logged on to, and performs internal tasks such as clearing expired user and Safe history?

- **A.** Administrator
- **B.** Auditor
- **C.** Batch
- **D.** Master

**Answer: C**

*Why:* The **Batch** user is the Vault's own internal worker. It exists so housekeeping — expiring history, clearing aged records — happens under a real identity in the audit trail, but nobody can log on as it.

*Why not the others:* A sits at the top of the user hierarchy with all permissions and can create and manage other users. B sits at the top of the hierarchy for *visibility*, producing reports of Safe and user activity. D holds all Safe member authorizations except authorizing password requests, manages full recovery, and cannot be removed from any Safe.

<sub>Source area: Predefined Vault users</sub>

---

### Q265. You are creating a new REST API user that will use CyberArk authentication. What is the correct way to provision it?

- **A.** PrivateArk Client → Tools → Administrative Tools → Users and Groups → New → User
- **B.** PrivateArk Client → Tools → Administrative Tools → Directory Mapping → Add
- **C.** PVWA → User Provisioning → LDAP Integration → Add Mapping
- **D.** PVWA → User Provisioning → Users and Groups → New → User

**Answer: A**

*Why:* A REST API user authenticating with CyberArk credentials is an **internal** Vault user, and internal users are created in the PrivateArk Client under Users and Groups. That is also where its Vault-level authorizations are set, on the user's Authorizations tab.

*Why not the others:* B and C provision *transparent* users from a directory, which is a different model — the account would live in LDAP, not in the Vault. D names a PVWA path that does not create internal Vault users this way.

<sub>Source area: Users and groups — PrivateArk Client</sub>

---

## Domain 6 — Configure Session Management

### Q266. Which authentication methods does PSM for SSH support?

- **A.** CyberArk password, LDAP, RADIUS and SAML
- **B.** LDAP, Windows authentication and SSH keys
- **C.** RADIUS, Oracle SSO and CyberArk password
- **D.** CyberArk password, LDAP and RADIUS

**Answer: D**

*Why:* PSM for SSH accepts the three methods that work over an SSH connection: the user's CyberArk password, LDAP, or RADIUS — RADIUS being what enables challenge/response MFA for PSMP sessions.

*Why not the others:* A adds SAML, which is a browser federation protocol and cannot be completed inside an SSH client. B and C add methods PSMP does not support. Do not confuse the *user's* authentication to the PSMP with the *target* account's credential, which may well be an SSH key.

<sub>Source area: PSM for SSH — authentication</sub>

---

## Domain 5 — Manage Security and Audit Functions

### Q267. You are running a Privileged Accounts Inventory report on a specific Safe. Which permissions are required on that Safe for the report to show complete account inventory information?

- **A.** List Accounts and View Safe Members
- **B.** Manage Safe Owners
- **C.** List Accounts and Access Safe without confirmation
- **D.** Manage Safe and View Audit

**Answer: A**

*Why:* The report answers two things at once — which accounts exist, and who can reach them — so it needs the permission for each: **List Accounts** to enumerate the accounts and **View Safe Members** to resolve who has access. Missing the second gives you a report with the ownership columns blank.

*Why not the others:* B, C and D each supply at most one half. This is the clearest example of the general rule that report scope follows Safe permissions rather than any separate reporting setting.

<sub>Source area: PVWA reports — required permissions</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q268. CyberArk provides an out-of-the-box target platform called "UNIX Via SSH Keys". How are the keys managed?

- **A.** CyberArk stores the private keys in the Vault and updates the public keys on the target systems
- **B.** CyberArk stores the public keys in the Vault and updates the private keys on the targets
- **C.** CyberArk stores neither, and uses a reconcile account to create keys on demand
- **D.** CyberArk stores both and can update targets with either key

**Answer: A**

*Why:* It mirrors how SSH itself works. The **private** key is the secret, so that is what the Vault protects and hands out under Retrieve Accounts; the **public** key is what has to sit in `authorized_keys` on each target, so that is what the CPM writes out when it rotates.

*Why not the others:* B inverts the two, which would leave the secret scattered across targets. C describes something CyberArk does not do here. D over-states it — a public key in the Vault is of no protective value on its own.

<sub>Source area: SSH key management</sub>

---

## Domain 1 — Onboard Accounts

### Q269. You are onboarding several accounts at once from the Pending Accounts list. Which associated setting must be the same across all the selected accounts?

- **A.** Platform
- **B.** Connection component
- **C.** CPM
- **D.** Vault

**Answer: A**

*Why:* Onboarding in bulk means applying one set of decisions to the whole selection, and the platform is the decision that governs how every one of those accounts will be managed. Accounts needing different platforms have to be onboarded in separate batches.

*Why not the others:* B is a platform setting, not something chosen at onboarding. C follows from the Safe you place them in, since CPM assignment is a Safe property. D is not a per-account choice.

<sub>Source area: Onboard accounts from the pending accounts list</sub>

---

## Domain 2 — Manage the Application

### Q270. Which files does the Vault Installation Wizard prompt you for during the Vault install?

- **A.** The Operator CD and the licence file
- **B.** The Master CD and the licence file
- **C.** The Operator CD and the Vault certificate
- **D.** The Master CD and `DBparm.ini`

**Answer: A**

*Why:* The installation needs the **Operator CD**, which carries the keys the Vault uses in normal operation, plus the licence file that becomes `License.xml` in the `System` Safe. The **Master CD**, holding the Private Recovery Key, is deliberately not consumed by the installer — it is break-glass material, kept on physical media in at least two secure locations.

*Why not the others:* B and D reach for the Master CD, which is precisely the thing that should not be sitting in the installer's hands. C substitutes a certificate for the licence.

<sub>Source area: Vault installation</sub>

---

## Domain 6 — Configure Session Management

### Q271. A customer asks you to help scope their PSM deployment. Which of these belongs in that conversation?

- **A.** The recordings file path
- **B.** The recordings codec
- **C.** The recordings retention period
- **D.** The recordings file type

**Answer: C**

*Why:* Retention is the input that drives everything else in a PSM design: multiplied by sessions per day, session length and the per-minute bit rate, it gives the Vault storage requirement — and it is a business and compliance decision the customer has to make, not something you can choose for them.

*Why not the others:* A, B and D are implementation details the product handles. Recordings are uploaded to Vault Safes rather than left on a file path, and the format is not a customer choice. Retention is configured per platform with `SessionRecorderSafeRetention`.

<sub>Source area: PSM sizing and scoping</sub>

---

## Domain 3 — Perform Ongoing Maintenance & Troubleshooting

### Q272. You are enabling PKI authentication for the PVWA (version 10 and above) and need to append the SSL access settings for the `/api/auth/pki/logon` location. Which file do you edit?

- **A.** `%WinDir%\System32\Inetsrv\Config\applicationHost.config`
- **B.** `C:\inetpub\adminscripts\web.config`
- **C.** `PasswordVault\CustomAuthenticationDlls\CyberArk.Authentication.CustomPKIPN.dll`
- **D.** `C:\inetpub\wwwroot\PasswordVaultEnv`

**Answer: A**

*Why:* The `<location>` block requiring a client certificate (`SslFlags="Ssl, SslNegotiateCert, SslRequireCert"`) is IIS server configuration, so it belongs in `applicationHost.config` under `%WinDir%\System32\Inetsrv\Config`. Follow it with `iisreset` for the change to take effect.

*Why not the others:* B is not the PVWA's web.config and not where location-scoped SSL flags live. C is a DLL, not a configuration file. D is not a real path.

<sub>Source area: PKI authentication for the PVWA</sub>

---

## Domain 1 — Onboard Accounts

### Q273. Which statement about the Password Upload Utility is correct?

- **A.** It uploads many password objects into the Vault from a pre-prepared file, and can create the Safes and folders they are placed into
- **B.** It runs from the PVWA and creates platforms as well as accounts
- **C.** It replaces the CPM for the accounts it uploads
- **D.** It can only add accounts to Safes that a CPM already manages

**Answer: A**

*Why:* The Password Upload Utility is a bulk-loading tool that works **directly against the Vault** rather than through the PVWA, reading a file of password objects and their properties and creating the Safes and folders needed to hold them. It is the older sibling of the PVWA's "Add multiple accounts from a file" and the REST bulk-upload endpoint, which are the routes you would normally use today.

*Why not the others:* B is wrong on both counts — it is not a PVWA feature and it does not create platforms; platforms are created in Platform Management, usually by duplicating an existing one. C confuses loading data with managing it: uploaded accounts are managed by the CPM exactly like any other. D is the reverse of the truth, since the utility can create the Safes itself.

<sub>Source area: Password Upload Utility</sub>

---

### Q274. Which CyberArk components can discover Windows Services and Scheduled Tasks that run under privileged accounts? (Choose two)

- **A.** Discovery and Audit (DNA)
- **B.** Accounts Discovery (the CPM Scanner)
- **C.** Export Vault Data (EVD)
- **D.** On-Demand Privileges Manager (OPM)

**Answer: A, B**

*Why:* Both of these go out and look. **DNA** is a standalone assessment tool that scans an environment and reports the privileged accounts and dependencies it finds, including services and scheduled tasks — typically used before a deployment, to size the problem. **Accounts Discovery**, run by the CPM Scanner, is the in-product equivalent that feeds Pending Accounts and the onboarding rules.

*Why not the others:* C exports Vault data outward for reporting — it looks *inside* the Vault, not at the estate. D is a privilege-elevation product for UNIX and Linux and does no discovery at all. The discoverable dependency set remains Windows services, scheduled tasks, IIS application pools, IIS anonymous access and COM+ applications.

<sub>Source area: Discovery and Audit (DNA) / Accounts Discovery</sub>

---

## Domain 7 — Configure User Management (incl. Vendor PAM, Privilege Cloud, SIA/ZSP)

### Q275. Safe permissions can be granted to which of these? (Choose four)

- **A.** Vault users
- **B.** Vault groups
- **C.** LDAP users
- **D.** LDAP groups

**Answer: A, B, C, D**

*Why:* All four. That is the defining difference from Vault-level authorizations, which are per-user only and are not inherited. Safe membership accepts users or groups, internal or directory-based — and granting to **groups**, ideally LDAP groups nested inside a CyberArk group, is the recommended pattern, because permissions attached to an individual are lost if that user object is deleted and recreated.

*Why not the others:* There is no wrong option here — the point of the question is that the Safe permission plane is deliberately broad, while the Vault authorization plane is deliberately narrow. If you assumed one of these was excluded, revisit the Vault-versus-Safe distinction.

<sub>Source area: Safe members / Vault and Safe authorizations</sub>

---

## Domain 4 — Configure and Manage Passwords

### Q276. Where is the reconcile account for a set of accounts specified?

- **A.** In the Master Policy, as a rule that applies to the whole environment
- **B.** On the platform (or overridden on an individual account), under Automatic Password Management
- **C.** On the Safe, alongside the CPM assignment
- **D.** In `dbparm.ini` on the Vault

**Answer: B**

*Why:* This is the Master Policy versus platform division again. The Master Policy states *what the organisation requires* — approval, exclusivity, one-time use, session monitoring. **How** an account is managed, including which reconcile account to use when a password is unknown or out of sync, is platform configuration (`ReconcileAccountSafe`, `ReconcileAccountFolder`, `ReconcileAccountName`), and can be overridden per account.

*Why not the others:* A is the trap and a common exam statement to reject — there is no reconcile account rule in the Master Policy. C confuses it with CPM assignment, which genuinely is a Safe property. D is Vault configuration.

<sub>Source area: Configure a reconcile account / Master Policy</sub>

---

## Domain 6 — Configure Session Management

### Q277. You are enabling PSM connections to a target Windows server. Which of these is actually required on the **target**?

- **A.** The PSM software must be installed on the target server
- **B.** `PSMConnect` must be created as a local user on the target server
- **C.** RDP must be enabled on the target server
- **D.** The HTML5 Gateway must be installed on the target server

**Answer: C**

*Why:* The PSM connects outward to the target over RDP, so RDP has to be enabled and reachable there — that is the only target-side requirement in this list. Everything else in a PSM deployment lives on the PSM server itself.

*Why not the others:* A is the misconception this question exists to kill: the PSM is a **jump server**, deliberately separate from the targets, and installing it on a target would defeat isolation entirely. B misplaces `PSMConnect`, which is a local Windows user created on the **PSM server** during installation and is the identity end-user sessions run under (with `PSMAdminConnect` for monitoring). D belongs on a separate Linux host in front of the PSM.

<sub>Source area: PSM architecture / connecting to Windows targets</sub>

---

## Corrections this set makes to older material and to circulating answer keys

Some answers here deliberately differ from the v12.6 course material, and some differ from the answer keys circulating in third-party question banks. Know both — if an exam question clearly wants the older answer, give it — but understand why it changed:

- **Blueprint** — the five-stage model was replaced by a risk-versus-effort prioritisation index, and the first guiding principle was reworded from *prevent credential theft* to *prevent identity compromise*. Tier 0/1/2 belongs to the PAM Implementation Program Phase 1, not the Blueprint, and there is no Tier 3.
- **Onboarding rule precedence** — the newest rule gets precedence 1 and the first match wins. Current docs also state dependencies are onboarded *with* the account, contradicting the older "rules do not apply to accounts with dependencies" teaching.
- **Safe renaming** — Safes *can* be renamed by a user with Add Safes. What cannot change after creation is the Encryption tab configuration and OLAC once enabled.
- **LDAP administration** — gated by *Manage Directory Mapping* plus Audit Users and Vault Admins membership, not restricted to the built-in Administrator user.
- **xRay** — current docs say the package comes from your CyberArk representative; older material says the Marketplace.
- **Verification parameters** carry a `VF` prefix (`VFPerformPeriodicVerification`, `VFVerificationPeriod`), with no documented defaults.
- **`PSM-WebApp` does not exist** as an out-of-the-box connection component. Use `PSM-PVWA`, `PSM-MS-Azure` or `PSM-AWSConsoleWithSTS`. Official casing is `PSM-TOAD`.
- **"Time of use restrictions"** and **"split workflow"** are exam-objective wording with no matching UI element — see Q40 and Q77 for what they actually map to.
- **Recording Safe parameter** is `SessionRecorderSafe` (default `PSMRecordings`); the Safe is created on first upload, never at install. `SessionRecorderSafeRetention` defaults to 180 days and applies only to Safes created after it is set.
- **Master Policy rule names** — the rule enabling the PSM is "Require privileged session monitoring and isolation"; its companion is "Record and save session activity".
- **PSM shadow users** are created for every PSM connection, not only non-RDP-file ones.
- **Linux paths are case-sensitive** — `/var/opt/CARKpsmp/logs`, `basic_psmpserver.conf`, `vaultPermissionsValidation.sh`. Course slides often show the wrong casing.
- **ZSP ephemeral naming** — the dash appears only when the username is shorter than seven characters. Per-Device RDS CALs are *required* to avoid licence consumption by domain ephemeral accounts.
- **PSM recording sizing (Q244)** — a widely circulated key answers 250 GB for 100 days × 10 sessions × 100 minutes. The arithmetic gives roughly 40–50 GB. Always compute: sessions × minutes × days × bit rate, then add the 20 GB constant.
- **PSM for SSH recording playback (Q203)** — a circulating key blames an out-of-date browser for the missing fast-forward control. The real reason is that a PSMP session produces a *text/command* recording rather than video.
- **Permission levels (Q262)** — a circulating key places **Add Safes** at Safe level. It is a Vault-level authorization; you cannot hold a permission inside a Safe that does not exist yet.
- **Tracking who holds a shared account (Q263)** — a circulating key answers one-time passwords alone. OTP gives you non-repudiation after the fact; **exclusive access** is what tells you who holds the account right now. In practice combine both.
- **Reconcile account (Q276)** — it is specified on the **platform** (or per account), never as a Master Policy rule. Some circulating material states the opposite.
- **PSM on the target (Q277)** — the PSM is never installed on the target, and `PSMConnect` is a local user on the **PSM server**, not on the target. Only RDP needs to be enabled target-side.
- **Privilege Cloud naming** — CyberArk documentation now carries the Idira brand, and SIA is the current name for what the course calls DPA. The `DpaAdmin` role and the `DPA RDP Privilege Cloud Secrets Access` Safe role still carry the old string.

## A note on the third-party sample questions reviewed

Of the roughly 130 sample questions reviewed, a substantial share test **PAM-SEN (Sentry)** material rather than Defender: Vault and PVWA installation sequences, hardening script ordering, AWS/Azure EC2 sizing, load-balancer topology design, PVWA and PSM count design, cluster heartbeat behaviour. Those were deliberately left out. What was pulled through is the Defender-relevant remainder — platform parameters, Safe and Vault permissions, PSM and PSM-for-SSH behaviour, PTA detections and responses, reports, DR operations, LDAP/RADIUS/SAML, and troubleshooting.

## How to use this in the last two weeks

1. Run all 277 in practice mode, domain by domain, and note every domain scoring below 80%.
2. Re-read the corresponding docs (`01`–`17`) for those domains only.
3. Run doc `20`'s 100 questions the same way.
4. Two days before, run exam simulation (60 questions, 90 minutes) cold — no notes.
5. Morning of the exam, read `19-exam-cram-sheet.md` and the corrections list above.
