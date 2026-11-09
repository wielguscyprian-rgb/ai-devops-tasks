W logach uwieczniono sekwencję awarii kontenera `78a2b3c4`, spowodowaną utratą połączenia z zewnętrzną usługą (port 5432 sugeruje bazę danych PostgreSQL):

1. **10:15:32** – Kontener `78a2b3c4` pomyślnie przeszedł początkowy test sprawności i zmienił stan z `starting` na `healthy`.
2. **10:16:45** (ok. 73 s później) – Aplikacja wewnątrz kontenera próbowała połączyć się z adresem `172.17.0.3:5432`, ale połączenie zostało odrzucone (`connection refused`).
3. **10:16:47** – Dwie sekundy po błędzie sieciowym system kontenera oblał test sprawności (`HEALTHCHECK`), a Docker zmienił jego status z `healthy` na `unhealthy`.

---

### Zidentyfikowane problemy i potencjalne przyczyny

* **Awaria lub brak gotowości bazy danych (`connection refused`)**
* Kontener z bazą danych pod adresem `172.17.0.3` uległ awarii, został zatrzymany lub uległ przeładowaniu.
* Proces bazy danych nasłuchuje wyłącznie na interfejsie pętli zwrotnej (`127.0.0.1`) wewnątrz swojego kontenera zamiast na wszystkich interfejsach (`0.0.0.0`).


* **Używanie sztywnych adresów IP w Dockerze (Antywzorzec)**
* Adres `172.17.0.3` to domyślny adres IP z podsieci `docker0` (bridge). Adresy IP kontenerów są dynamiczne i zmieniają się przy każdym ich restarcie. Jeśli baza danych zrestartowała się i otrzymała nowy adres IP (np. `172.17.0.4`), kontener aplikacji nadal próbuje połączyć się ze starym adresem.


* **Niezależny cykl życia kontenerów i brak obsługi ponowień (Retry Logic)**
* Kontener aplikacji oznaczono jako `healthy` przed weryfikacją ciągłości połączenia. Gdy baza przestała odpowiadać, aplikacja nie obsłużyła błędu połączenia i uległa awarii, co przełożyło się na spadek statusu zdrowia kontenera do `unhealthy`.



---

### Krok po kroku: Jak to naprawić?

1. **Sprawdź stan i logi bazy danych:**
```bash
docker ps -a
docker logs <id_lub_nazwa_kontenera_bazy>

```


2. **Przejdź na zdefiniowaną sieć Dockera (User-Defined Network):**
Zamiast używać adresów IP (`172.17.0.3`), stwórz sieć i używaj nazw kontenerów/usług jako nazw hostów (wbudowany DNS Dockera):
```bash
docker network create moja-siec
docker run --network moja-siec --name postgres-db ...
docker run --network moja-siec --name app ...

```


W konfiguracji aplikacji zmienną połączenia ustaw na `postgres-db:5432` zamiast adresu IP.
3. **Użyj `healthcheck` oraz `depends_on` w Docker Compose:**
Jeśli korzystasz z Docker Compose, uzależnij start aplikacji od pełnej gotowości bazy danych:
```yaml
services:
  db:
    image: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
  app:
    build: .
    depends_on:
      db:
        condition: service_healthy

```