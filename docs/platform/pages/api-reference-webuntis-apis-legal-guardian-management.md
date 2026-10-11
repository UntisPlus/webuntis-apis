# Legal Guardian Management

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/legal-guardian-management/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Manage legal guardian (parent) master-data and user accounts. Use this API for parent portal integrations, guardian account provisioning, and communication workflows.

v1  Read & Write   **Endpoints:** 4

---

## Use cases

Parent portal

Provision guardian accounts for parent-facing portals and communication
systems.

SIS sync

Synchronize guardian records from external student information systems.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getLegalGuardianById` | Get a single legal guardian by ID |
| `GET` | `getLegalGuardians` | List all legal guardians |
| `POST` | `createLegalGuardians` | Create legal guardians (batch) |
| `PUT` | `updateLegalGuardians` | Update legal guardians (batch) |

---

## Related pages

[Student Management](api-reference-webuntis-apis-student-management.md)  Students are linked to guardians via master-data.

[Messaging](api-reference-webuntis-apis-messaging.md)  Send messages to guardians after provisioning their accounts.

---

## API reference
