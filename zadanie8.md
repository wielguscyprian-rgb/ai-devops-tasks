Ten błąd oznacza, że Docker próbuje przypisać port `3000` Twojego komputera (hosta) do uruchamianego kontenera, ale **ten port jest już zajęty przez inny program**. Może to być inna instancja Twojej aplikacji (np. uruchomiona lokalnie w Node.js bez użycia Dockera), stary, zawieszony kontener lub zupełnie inna usługa.

Aby rozwiązać ten problem, masz dwie główne drogi: zwolnić port `3000` lub przypisać kontenerowi inny, wolny port.

### Rozwiązanie 1: Zwolnienie portu 3000 (Zalecane)

1. **Zidentyfikuj proces zajmujący port:** Terminal.
Użyj polecenia sieciowego w swoim systemie operacyjnym, aby znaleźć identyfikator procesu (PID), który aktualnie nasłuchuje na porcie 3000.

**Linux / macOS:**

```bash
sudo lsof -i :3000
# lub
sudo netstat -tulpn | grep :3000

```

**Windows (Wiersz polecenia jako Administrator):**

```cmd
netstat -ano | findstr :3000

```

*Verification:* Zobaczysz listę wyników. Zlokalizuj kolumnę zawierającą numer PID (Process ID) - zazwyczaj jest to ostatnia kolumna na systemie Windows lub druga kolumna w wyniku `lsof`.


2. **Zakończ blokujący proces:** Zabicie zadania.
Mając numer PID, wymuś zamknięcie tego procesu. Zastąp `<PID>` znalezionym numerem.

**Linux / macOS:**

```bash
sudo kill -9 <PID>

```

**Windows:**

```cmd
taskkill /PID <PID> /F

```

*Verification:* Ponowne wykonanie komendy z Kroku 1 nie powinno zwrócić żadnych wyników, co oznacza, że port jest teraz całkowicie wolny.


3. **Uruchom ponownie kontener:** Docker.
Spróbuj ponownie uruchomić swoją aplikację za pomocą narzędzia, którego używałeś wcześniej.

```bash
docker-compose up -d
# lub
docker start app

```

*Verification:* Zobaczysz komunikat o pomyślnym uruchomieniu kontenera (`Started` lub `Done`), a błąd `bind: address already in use` już się nie pojawi.


---

### Rozwiązanie 2: Zmiana portu w konfiguracji Dockera

Jeśli nie chcesz zatrzymywać programu, który aktualnie działa na porcie 3000, możesz poinstruować Dockera, aby udostępnił aplikację na innym porcie na Twoim komputerze (np. 3001).

**Jeśli używasz pliku `docker-compose.yml`:**
Odszukaj sekcję `ports` w swoim pliku i zmień lewą stronę mapowania (port hosta). Prawa strona (port wewnątrz kontenera) pozostaje bez zmian.

```yaml
services:
  app:
    # ...
    ports:
      - "3001:3000" # Zmieniono port hosta z 3000 na 3001

```

**Jeśli używasz polecenia `docker run`:**
Zmień pierwszą wartość we flagach portów:

```bash
docker run -p 3001:3000 nazwa_twojego_obrazu

```

Po tej zmianie aplikacja będzie dostępna w Twojej przeglądarce pod adresem `