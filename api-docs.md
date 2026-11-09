# GET /api/users

Pobiera stronicowaną listę użytkowników z możliwością filtrowania według roli.

## Parametry zapytania (Query Parameters)

| Parametr | Typ | Wymagany | Domyślnie | Opis |
| --- | --- | --- | --- | --- |
| `page` | Integer | Nie | `1` | Numer pobieranej strony (wartość $\ge 1$). |
| `limit` | Integer | Nie | `10` | Liczba wyników zwracanych na stronę (maksymalnie `100`). |
| `role` | String | Nie | — | Opcjonalny filtr roli użytkownika (np. `admin`, `user`, `editor`). |

---

## Przykładowe żądanie

```bash
curl -X GET "https://api.example.com/api/users?page=1&limit=2&role=admin" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer <TWOJ_TOKEN_API>"

```

---

## Przykładowa odpowiedź

### Status: `200 OK`

```json
{
  "data": [
    {
      "id": 101,
      "name": "Jan Kowalski",
      "email": "jan.kowalski@example.com",
      "role": "admin",
      "createdAt": "2026-01-15T08:30:00Z"
    },
    {
      "id": 104,
      "name": "Anna Nowak",
      "email": "anna.nowak@example.com",
      "role": "admin",
      "createdAt": "2026-03-02T11:20:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 2,
    "totalItems": 15,
    "totalPages": 8
  }
}

```

### Możliwe kody błędów

* **`400 Bad Request`** – przekazano niepoprawne parametry (np. `limit` przekraczający 100 lub ujemny numer strony `page`).
* **`401 Unauthorized`** – brak lub niepoprawny token autoryzacyjny.