1. **Uruchamianie procesów jako użytkownik inny niż root**
Domyślnie procesy wewnątrz kontenera wykonują się z uprawnieniami roota. W przypadku podatności w aplikacji zwiększa to ryzyko przejęcia kontroli nad samym hostem (*container breakout*). W pliku `Dockerfile` należy jawnie utwożyć i przełączyć się na użytkownika nieuprzywilejowanego:

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

```

2. **Korzystanie z minimalnych obrazów i skanowanie podatności (CVE)**
Stosowanie obrazów typu Alpine, Distroless lub budowanych od zera (`FROM scratch`) drastycznie zmniejsza powierzchnię ataku, usuwając zbędne powłoki (bash) i narzędzia systemowe (curl, netcat). Każdy obraz trafiający na produkcję powinien być automatycznie skanowany pod kątem znanych podatności w pipeline CI/CD przy użyciu narzędzi takich jak Trivy, Grype czy Clair.
3. **Bezpieczne zarządzanie sekretami (Secrets Management)**
Klucze API, passwords do baz danych i certyfikaty nie mogą znajdować się w pliku `Dockerfile` (w instrukcjach `ENV` lub `ARG`), w repozytorium ani w warstwach budowanego obrazu. Sekrety należy wstrzykiwać dynamicznie podczas uruchamiania kontenera przy użyciu mechanizmów takich jak Docker Secrets, HashiCorp Vault lub zmiennych środowiskowych przekazywanych z zewnętrznego magazynu w orchestratorze (np. Kubernetes).
4. **Restrykcyjne ograniczenie uprawnień Kernela i `read-only**`
Zminimalizuj możliwości wykonania szkodliwych akcji wewnątrz kontenera poprzez odebranie domyślnych uprawnień systemu Linux oraz zablokowanie zapisu na dysku:

* Odbierz wszystkie uprawnienia systemowe i przywróć tylko te niezbędne: `--cap-drop=ALL --cap-add=NET_BIND_SERVICE`.
* Zabroń procesom podnoszenia uprawnień: `--security-opt=no-new-privileges:true`.
* Uruchamiaj system plików kontenera w trybie tylko do odczytu: `--read-only` (z montowaniem katalogów zapisywalnych w pamięci RAM jako `tmpfs`).

5. **Izolacja sieciowa i twarde limity zasobów**
Brak ograniczeń zasobów wystawia środowisko na ataki typu Denial of Service (DoS) – jeden kontener z wyciekiem pamięci lub pętlą CPU może zawiesić cały serwer.

* Zawsze definiuj limity RAM i CPU: `--memory="512m" --cpus="1.0"`.
* Unikaj domyślnej sieci `bridge` oraz `host network`. Stwarzaj dedykowane, odizolowane sieci (`user-defined bridge networks`) i wystawiaj porty wyłącznie na adres pętli zwrotnej (`127.0.0.1:3000:3000`), udostępniając aplikację na zewnątrz wyłącznie poprzez skonfigurowane Reverse Proxy (np. NGINX, Traefik).
--------------implementacja:----------------
### 1. Implementacja w `Dockerfile`

W `Dockerfile` tworzy się dedykowaną grupę i użytkownika bez uprawnień administracyjnych (lub korzysta z użytkownika dostarczanego domyślnie przez obraz bazowy), przydziela mu się prawa do plików aplikacji, a następnie przełącza kontekst wykonywania komend za pomocą instrukcji `USER`.

#### Przykład dla obrazu Alpine Linux:

```dockerfile
FROM node:20-alpine

WORKDIR /app

# 1. Tworzenie grupy i użytkownika nieuprzywilejowanego (z wyłączoną powłoką logowania)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -D -H

# 2. Kopiowanie plików z bezpośrednim nadaniem praw własności dla nowego użytkownika
COPY --chown=appuser:appgroup package*.json ./

RUN npm ci --only=production

COPY --chown=appuser:appgroup . .

# 3. Przełączenie na użytkownika nieuprzywilejowanego przed uruchomieniem aplikacji
USER appuser

EXPOSE 3000

CMD ["node", "index.js"]

```

> **Wskazówka (Obrazy Node.js):** Obrazy z rodziny `node` posiadają już domyślnie utworzonego użytkownika `node` (z identyfikatorem UID `1000`). Zamiast tworzyć nowego użytkownika, można użyć:
> ```dockerfile
> COPY --chown=node:node . .
> USER node
> 
> ```
> 
> 

---

### 2. Implementacja w `docker-compose.yml`

W pliku `docker-compose.yml` można nadpisać użytkownika z zewnątrz przy użyciu klucza `user`. Pozwala to na uruchomienie kontenera z identyfikatorem konta (UID i GID) odpowiadającym użytkownikowi na hoście, co ułatwia zarządzanie uprawnieniami do montowanych wolumenów.

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    # Uruchomienie kontenera jako konkretny UID:GID (np. 1000:1000)
    user: "1000:1000"

```

Alternatywnie można podać słowną nazwę użytkownika zdefiniowanego w `Dockerfile`:

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    user: "appuser" # lub user: "node"

```

---

### Najważniejsze zasady bezpieczeństwa przy tej konfiguracji

1. **Numer UID zamiast nazwy w produkcjach:** Stosowanie numerycznych identyfikatorów (`USER 10001:10001` lub w Compose `user: "1000:1000"`) jest bezpieczniejsze dla mechanizmów takich jak Kubernetes czy Docker Bench Security. System operacyjny hosta i mechanizmy izolacji (np. AppArmor/seccomp) weryfikują uprawnienia na poziomie liczbowych identyfikatorów UID/GID, a nie nazw tekstowych.
2. **Kolejność w Dockerfile:** Instrukcja `USER` musi znaleźć się po komendach instalacji pakietów systemowych (`RUN apk add...` lub `apt-get install...`), ponieważ te operacje wymagają uprawnień roota.
3. **Porty poniżej 1024:** Użytkownik inny niż root nie może nasłuchiwać na portach zastrzeżonych (np. port `80` lub `443`). Aplikacja wewnątrz kontenera powinna zawsze nasłuchiwać na wyższym porcie (np. `3000` lub `8080`), a ewentualne przekierowanie na port `80` wykonuje się na poziomie hosta lub Reverse Proxy.