Zbyt duże zużycie pamięci przez kontener zazwyczaj wynika z wycieków pamięci w kodzie aplikacji, braku nałożonych limitów alokacji na poziomie infrastruktury lub błędnego doboru parametrów środowiska uruchomieniowego (np. maszyny wirtualnej Javy czy V8 dla Node.js).

Oto jak zdiagnozować problem i wdrożyć odpowiednie limity.

1. **Identyfikacja obciążonego kontenera:** 1 min.
Uruchom podgląd statystyk w czasie rzeczywistym, aby sprawdzić, który kontener konsumuje najwięcej zasobów. W terminalu wpisz polecenie `docker stats`.
*Verification:* Zlokalizujesz kontener, którego wartość w kolumnie `MEM USAGE / LIMIT` niepokojąco rośnie lub osiąga maksimum przydzielonej puli.


2. **Sprawdzenie procesów wewnętrznych:** 1 min.
Sprawdź, który konkretnie proces wewnątrz kontenera zużywa pamięć, używając polecenia: `docker top <nazwa_kontenera>`. Jeśli obraz bazowy na to pozwala, możesz też wejść do kontenera poleceniem `docker exec -it <nazwa_kontenera> top` (lub `htop`).
*Verification:* Zobaczysz listę procesów i zidentyfikujesz ten o najwyższym zużyciu (kolumna %MEM).


3. **Weryfikacja historii zabicia procesu (OOMKilled):** 1 min.
Sprawdź, czy kontener nie był już wcześniej resetowany przez system hosta z powodu całkowitego braku pamięci (Out of Memory). Wpisz: `docker inspect <nazwa_kontenera> --format='{{.State.OOMKilled}}'`.
*Verification:* Wynik `true` potwierdza, że kontener wyczerpał dostępne zasoby RAM hosta i został siłowo zatrzymany. Wynik `false` oznacza, że proces wciąż działa.


### Wdrażanie limitów pamięci (Ograniczenie zużycia)

Aby zapobiec sytuacji, w której jeden kontener zawiesza cały serwer (hosta), musisz nałożyć na niego twarde limity.

**1. Opcja dla Docker Compose (Zalecane)**
Dodaj sekcję `deploy` i `resources` w swoim pliku `docker-compose.yml`. Dzięki temu kontener nigdy nie przekroczy wskazanej wartości.

```yaml
services:
  moja_aplikacja:
    image: moj_obraz:latest
    deploy:
      resources:
        limits:
          memory: 512M # Twardy limit pamięci RAM
        reservations:
          memory: 256M # Gwarantowana pamięć dla kontenera

```

**2. Opcja dla polecenia Docker Run**
Jeśli uruchamiasz kontenery ręcznie z poziomu terminala, użyj flagi `-m` (lub `--memory`):

```bash
docker run -d -p 3000:3000 -m 512m --memory-swap 1g moja_aplikacja

```

*Uwaga:* Ustawienie `--memory-swap` na dwukrotność RAMu to bezpieczny standard, który zapobiega natychmiastowemu "ubiciu" procesu w momencie krótkotrwałego piku zapotrzebowania.
---------------ODpowiedź 2 ------------------------
Z perspektywy inżyniera DevOps, samo nałożenie twardych limitów (o których wspomniałem wcześniej) to jedynie leczenie objawów. Jeśli aplikacja ma wyciek pamięci (memory leak), nałożenie limitu sprawi jedynie, że kontener będzie szybciej i częściej ubijany przez mechanizm OOM (Out Of Memory) z kodem 137.

Aby całkowicie rozwiązać problem, musimy przejść od prostej reakcji do pełnej obserwowalności (observability) i profilowania.

Oto zaawansowany proces diagnozy i naprawy na poziomie infrastruktury:

1. **Wyizolowanie rzeczywistego zużycia pamięci (RSS):** Weryfikacja Page Cache.
Wejdź do cgroups działającego kontenera, aby sprawdzić dokładne statystyki pamięci bezpośrednio w kernelu. Użyj polecenia: `docker exec -it <nazwa_kontenera> cat /sys/fs/cgroup/memory/memory.stat` (dla cgroups v1) lub `... /sys/fs/cgroup/memory.stat` (dla v2).
*Verification:* Odszukaj wartość `total_rss` (lub `anon`). Jeśli jest ona zbliżona do limitu kontenera, aplikacja faktycznie zużywa cały RAM. Jeśli dominuje `cache`, problemem nie jest aplikacja, a system plików, co jest naturalnym zachowaniem Linuxa.


2. **Podłączenie systemu monitoringu metryk (cAdvisor):** Analiza historyczna.
Uruchom kontener z Google cAdvisor podłączony do Prometheusa i Grafany. Narzędzia CLI dają tylko podgląd na żywo, a wycieki pamięci diagnozuje się w czasie.
*Verification:* Na wykresie w Grafanie zaobserwujesz wzorzec. Jeśli wykres przypomina "zęby piły" (rośnie, gwałtownie spada i znów rośnie) - to klasyczny wyciek i restart OOMKilled. Jeśli jest to płaska linia pod samym sufitem - aplikacja jest po prostu zbyt „ciężka” na przydzielone zasoby.


3. **Wykonanie zrzutu pamięci z wewnątrz kontenera (Heap Dump):** Profilowanie kodu.
Wygeneruj zrzut sterty (heap dump) z działającego procesu, zanim zostanie zabity. Dla Node.js uruchom proces z flagą `--inspect` i użyj narzędzia takiego jak `clinic.js` lub podłącz Chrome DevTools z zewnątrz. Dla Javy użyj `jmap -dump:live,format=b,file=/tmp/dump.hprof <PID>`.
*Verification:* W katalogu `/tmp/` kontenera powstanie duży plik (np. `.heapsnapshot` lub `.hprof`), który następnie możesz skopiować na hosta (`docker cp`) i załadować do analizatora, aby zobaczyć, które dokładnie obiekty nie są usuwane przez Garbage Collector.


4. **Wdrożenie strategii Auto-Healing:** Liveness Probes.
Zamiast czekać, aż kontener zostanie brutalnie zabity przez kernel (co przerywa trwające zapytania użytkowników), zaimplementuj endpoint `/health/memory` w aplikacji. Jeśli zużycie wewnętrzne przekroczy bezpieczny próg (np. 85%), aplikacja powinna zacząć zwracać kod HTTP 503.
*Verification:* Twój orchestrator (Docker Swarm / Kubernetes) usunie ten kontener z load balancera, pozwoli mu dokończyć obecne zapytania, a następnie bezpiecznie go zrestartuje (Graceful Shutdown).


### Dobre praktyki DevOps w zarządzaniu zasobami

1. **Kubernetes - Requests vs. Limits:** W środowiskach produkcyjnych zawsze oddzielaj to, czego aplikacja potrzebuje na start (`requests`), od maksymalnej wartości, po której ma zginąć (`limits`). Brak `requests` prowadzi do nadmiernego upychania (overprovisioning) kontenerów na jednym węźle.
2. **OOM Score Adjust:** Jeśli masz krytyczny kontener, który nie może zostać zabity (np. baza danych), możesz w pliku `docker-compose.yml` ustawić `oom_score_adj: -1000`. Sprawi to, że kernel Linuxa potraktuje go priorytetowo i w przypadku braku RAMu zabije inne, mniej ważne procesy w pierwszej kolejności.
3. **Konfiguracja Garbage Collectora:** Pamiętaj, że kontenery izolują procesy, ale procesy nie zawsze zdają sobie z tego sprawę. Uruchomienie aplikacji w Node.js 18 lub Javie 17+ automatycznie respektuje limity cgroups, ale w starszych wersjach Garbage Collector "widzi" cały RAM hosta i zwalnia z czyszczeniem pamięci, co prowadzi do sztucznego wyczerpania RAMu kontenera.