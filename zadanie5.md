Stwórz prosty diagram ASCII Art przedstawiający połączenie klienta, serwera aplikacji i bazy danych.
+-------------+                 +--------------------+                 +---------------+
|             |  1. Żądanie     |                    |  2. Zapytanie   |               |
|   Klient    | --------------> |  Serwer Aplikacji  | --------------> |  Baza Danych  |
| (Web / App) | <-------------- |     (Backend)      | <-------------- |  (Magazyn)    |
|             |  4. Odpowiedź   |                    |  3. Wynik       |               |
+-------------+                 +--------------------+                 +---------------+
Dodaj do diagramu opisy elementów i kierunki przepływu danych.
+-----------------------+                +-----------------------+                +-----------------------+
|        KLIENT         |                |   SERWER APLIKACJI    |                |      BAZA DANYCH      |
|-----------------------|                |-----------------------|                |-----------------------|
| Funkcje:              |  1. Żądanie    | Funkcje:              |  2. Zapytanie  | Funkcje:              |
| - Interfejs (UI)      | =============> | - Logika biznesowa    | =============> | - Trwały zapis        |
| - Renderowanie widoku |  (HTTP/REST)   | - Walidacja i Auth    |  (TCP / SQL)   | - Wyszukiwanie danych |
| - Reakcja na akcje    |  [Dane Usera]  | - Integracja usług    |  [Instrukcje]  | - Gwarancja spójności |
|                       |                |                       |                |                       |
|                       | <============= |                       | <============= |                       |
| (Frontend/Urządzenie) |  4. Odpowiedź  |       (Backend)       |    3. Wynik    |      (Magazyn)        |
|                       |  (Kody HTTP)   |                       | (Format bazy)  |                       |
|                       |  [Widok/JSON]  |                       |  [Rekordy]     |                       |
+-----------------------+                +-----------------------+                +-----------------------+