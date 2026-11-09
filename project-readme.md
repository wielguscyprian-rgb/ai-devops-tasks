# Simple Task API

## Opis

**Simple Task API** to RESTful API służące do zarządzania zadaniami. Aplikacja została zbudowana przy użyciu środowiska **Node.js**, frameworka **Express** oraz bazy danych **MongoDB**. Umożliwia łatwe zarządzanie cyklem życia zadań, ich filtrowanie oraz zabezpieczenie zasobów poprzez podstawową autoryzację użytkowników.

### Główne funkcje
* **CRUD zadań:** Tworzenie, odczytywanie, aktualizacja oraz usuwanie zadań.
* **Filtrowanie:** Sortowanie i filtrowanie zadań według statusu (np. `pending`, `in_progress`, `completed`) oraz priorytetu (`low`, `medium`, `high`).
* **Autoryzacja użytkowników:** Rejestracja, logowanie oraz zabezpieczanie endpointów za pomocą tokenów JWT (JSON Web Token).

---

## Wymagania

Przed uruchomieniem projektu upewnij się, że posiadasz zainstalowane:
* [Node.js](https://nodejs.org/) (wersja 18 lub wyższa)
* [MongoDB](https://www.mongodb.com/) (lokalna instancja lub baza w chmurze MongoDB Atlas)
* [Git](https://git-scm.com/)

---

## Instalacja

1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/twoj-login/simple-task-api.git
   cd simple-task-api
   ```

2. **Zainstaluj zależności:**
   ```bash
   npm install
   ```

3. **Skonfiguruj zmienne środowiskowe:**
   Utwórz plik `.env` w głównym katalogu projektu i dodaj następujące zmienne:
   ```env
   PORT=3000
   MONGO_URI=mongodb://localhost:27017/simple-task-db
   JWT_SECRET=twoj_tajny_klucz_jwt
   ```

---

## Użycie

### Uruchomienie w trybie produkcyjnym:
```bash
npm start
```

### Uruchomienie w trybie deweloperskim (z automatycznym przeładowaniem):
```bash
npm run dev
```

Po uruchomieniu serwer będzie dostępny pod adresem: `http://localhost:3000`

---

## Endpointy API

### Autentykacja (`/api/auth`)

| Metoda | Endpoint | Opis | Wymaga autoryzacji |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/auth/register` | Rejestracja nowego użytkownika | Nie |
| `POST` | `/api/auth/login` | Logowanie i pobranie tokenu JWT | Nie |

---

### Zarządzanie zadaniami (`/api/tasks`)

> **Uwaga:** Wszystkie ponizsze endpointy wymagają nagłówka autoryzacyjnego:  
> `Authorization: Bearer <TWOJ_TOKEN_JWT>`

| Metoda | Endpoint | Opis |
| :--- | :--- | :--- |
| `GET` | `/api/tasks` | Pobieranie listy zadań (z obsługą filtrów) |
| `POST` | `/api/tasks` | Tworzenie nowego zadania |
| `GET` | `/api/tasks/:id` | Pobieranie szczegółów konkretnego zadania |
| `PUT` | `/api/tasks/:id` | Aktualizacja zadania |
| `DELETE` | `/api/tasks/:id` | Usuwanie zadania |

#### Filtrowanie zadań (`GET /api/tasks`)
Możesz filtrować wyniki przekazując parametry w zapytaniu (query parameters):
* `status` – np. `GET /api/tasks?status=completed`
* `priority` – np. `GET /api/tasks?priority=high`
* **Łączenie filtrów:** `GET /api/tasks?status=pending&priority=high`

---

## Przykładowy obiekt zadania (JSON)

```json
{
  "id": "60d5ec49f1b2c81184a2b3c4",
  "title": "Przygotować raport kwartalny",
  "description": "Zebrać statystyki sprzedaży z ostatnich 3 miesięcy.",
  "status": "in_progress",
  "priority": "high",
  "createdAt": "2026-03-10T10:00:00.000Z"
}
```