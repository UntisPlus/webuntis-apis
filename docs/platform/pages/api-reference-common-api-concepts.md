# Common API Concepts

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/common-api-concepts/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Both OneRoster and Untis Platform API families share the same pagination, sorting, and filtering mechanism. Every list endpoint on the platform uses the [OneRoster 1.1 specification](https://www.imsglobal.org/oneroster-v11-final-specification#_Toc480451995) for these operations — regardless of which API family you call.

Caution

Pagination is **mandatory** for client-side implementation. Even if an
endpoint could return all results in a single response, you must implement
pagination to handle growth in data volume over time.

---

## Pagination

All list endpoints accept two query parameters:

| Parameter | Description |
| --- | --- |
| `limit` | Maximum number of results to return per page |
| `offset` | Number of results to skip before returning data |

**Example — fetch the first 100 students:**

```
GET {{API_URL}}/ims/oneroster/v1p1/students?limit=100&offset=0
```

Increment `offset` by your `limit` value to page through results. Continue until a response returns fewer items than the requested `limit`.

---

## Sorting

Use the `sort` query parameter with a field name. Use the optional `orderBy` parameter to control direction (`asc` or `desc`). If `orderBy` is omitted, the sort order is implementation-dependent.

**Ascending:**

```
GET {{API_URL}}/ims/oneroster/v1p1/users?sort=familyName&orderBy=asc
```

**Descending:**

```
GET {{API_URL}}/ims/oneroster/v1p1/users?sort=familyName&orderBy=desc
```

---

## Filtering

Use the `filter` query parameter with a simple query syntax:

```
GET {{API_URL}}/ims/oneroster/v1p1/users?filter=role='student'
```

Single operator only

The `filter` parameter supports **at most one operator**. Combining multiple conditions (e.g. `AND`/`OR`) is not supported — apply additional filtering on your side.

Consult the [OneRoster 1.1 specification](https://www.imsglobal.org/oneroster-v11-final-specification#_Toc480451995) for the complete filtering syntax and supported operators.

---

## Combining parameters

Pagination, sorting, and filtering can be combined in a single request:

```
GET {{API_URL}}/ims/oneroster/v1p1/users?filter=role='student'&sort=familyName&orderBy=asc&limit=50&offset=0
```

---
