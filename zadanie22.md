Simple Task APIOpisSimple Task API to RESTful API służące do zarządzania zadaniami. Aplikacja została zbudowana przy użyciu środowiska Node.js, frameworka Express oraz bazy danych MongoDB. Umożliwia łatwe zarządzanie cyklem życia zadań, ich filtrowanie oraz zabezpieczenie zasobów poprzez podstawową autoryzację użytkowników.Główne funkcjeCRUD zadań: Tworzenie, odczytywanie, aktualizacja oraz usuwanie zadań.Filtrowanie: Sortowanie i filtrowanie zadań według statusu (np. pending, in_progress, completed) oraz priorytetu (low, medium, high).Autoryzacja użytkowników: Rejestracja, logowanie oraz zabezpieczanie endpointów za pomocą tokenów JWT (JSON Web Token).WymaganiaPrzed uruchomieniem projektu upewnij się, że posiadasz zainstalowane:Node.js (wersja 18 lub wyższa)MongoDB (lokalna instancja lub baza w chmurze MongoDB Atlas)GitInstalacjaSklonuj repozytorium:git clone https://github.com/twoj-login/simple-task-api.git
cd simple-task-api
Zainstaluj zależności:npm install
Skonfiguruj zmienne środowiskowe:
Utwórz plik .env w głównym katalogu projektu i dodaj następujące zmienne:PORT=3000
MONGO_URI=mongodb://localhost:27017/simple-task-db
JWT_SECRET=twoj_tajny_klucz_jwt
UżycieUruchomienie w trybie produkcyjnym:npm start
Uruchomienie w trybie deweloperskim (z automatycznym przeładowaniem):npm run dev
Po uruchomieniu serwer będzie dostępny pod adresem: http://localhost:3000Endpointy APIAutentykacja (/api/auth)MetodaEndpointOpisWymaga autoryzacjiPOST/api/auth/registerRejestracja nowego użytkownikaNiePOST/api/auth/loginLogowanie i pobranie tokenu JWTNieZarządzanie zadaniami (/api/tasks)Uwaga: Wszystkie ponizsze endpointy wymagają nagłówka autoryzacyjnego:Authorization: Bearer <TWOJ_TOKEN_JWT>MetodaEndpointOpisGET/api/tasksPobieranie listy zadań (z obsługą filtrów)POST/api/tasksTworzenie nowego zadaniaGET/api/tasks/:idPobieranie szczegółów konkretnego zadaniaPUT/api/tasks/:idAktualizacja zadaniaDELETE/api/tasks/:idUsuwanie zadaniaFiltrowanie zadań (GET /api/tasks)Możesz filtrować wyniki przekazując parametry w zapytaniu (query parameters):status – np. GET /api/tasks?status=completedpriority – np. GET /api/tasks?priority=highŁączenie filtrów: GET /api/tasks?status=pending&priority=highPrzykładowy obiekt zadania (JSON){
  "id": "60d5ec49f1b2c81184a2b3c4",
  "title": "Przygotować raport kwartalny",
  "description": "Zebrać statystyki sprzedaży z ostatnich 3 miesięcy.",
  "status": "in_progress",
  "priority": "high",
  "createdAt": "2026-03-10T10:00:00.000Z"
}