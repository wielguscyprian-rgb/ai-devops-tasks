### Szczegółowa analiza każdego etapu w Jenkinsfile

Oto omówienie poszczególnych sekcji i etapów (`stages`) skryptu pod kątem ich roli w cyklu CI/CD:

#### 1. Konfiguracja globalna (`environment` i `tools`)

* **`environment`**: Zdefiniowane tu zmienne są dostępne w całym potoku. Wykorzystanie `IMAGE_TAG = "${BUILD_NUMBER}"` gwarantuje, że każdy zbudowany obraz Dockerowy otrzyma unikalny identyfikator powiązany z numerem uruchomienia w Jenkinsie.
* **`tools { nodejs 'NodeJS-18' }`**: Nakazuje Jenkinsowi automatyczne ustawienie środowiska Node.js w wersji 18 w zmiennej PATH węzła wykonawczego.

#### 2. Etapy wykonawcze (`stages`)

* **`stage('Checkout')`**
* **Co się dzieje:** Instrukcja `checkout scm` automatycznie pobiera kod źródłowy z repozytorium Git, które uruchomiło dany pipeline (pobiera odpowiednią gałąź i konkretny commit).


* **`stage('Install Dependencies')`**
* **Co się dzieje:** Wykonuje polecenie `npm ci`. Zamiast standardowego `npm install`, narzędzie odczytuje dokładnie plik `package-lock.json` i instaluje zapamiętane wersje zależności. Zapobiega to sytuacjom, w których nowsza sub-zależność psuje budowanie na serwerze CI.


* **`stage('Run Tests')`**
* **Co się dzieje:** Uruchamia testy jednostkowe i integracyjne (`npm test`). Jeśli którykolwiek test zakończy się niepowodzeniem (kod wyjścia inny niż `0`), pipeline natychmiast przerwie działanie i nie przejdzie do etapu budowania.


* **`stage('Build Application')`**
* **Co się dzieje:** Wykonuje kompilację kodu źródłowego (np. transpilację z TypeScript do JavaScript, bundle plików statycznych).


* **`stage('Build Docker Image')`**
* **Co się dzieje:** Blok `script` uruchamia klasyczny kod Groovy/Docker DSL. Jenkins buduje obraz kontenera z plików w obszarze roboczym na podstawie lokalnego `Dockerfile`, nadając mu nazwę i tag z numerem buildu.


* **`stage('Publish Docker Image')`**
* **Co się dzieje:** Konstrukcja `docker.withRegistry(...)` pobiera zaszyfrowane poświadczenia z magazynu Jenkinsa (`REGISTRY_CREDENTIALS`), bezpiecznie loguje się do rejestru (np. Docker Hub, ECR, Harbor) i wysyła obraz (`docker push`) pod dwoma tagami: unikalnym numerem kompilacji oraz tagiem `latest`.



#### 3. Blok po-wykonawczy (`post`)

* **`always { cleanWs() }`**: Czyści katalog roboczy (`workspace`) po zakończeniu pracy potoku – niezależnie od tego, czy budowanie zakończyło się sukcesem, czy błędem. Zapobiega to zapchaniu dysku na agencie Jenkinsa.
* **`success` / `failure**`: Miejsce na wyzwolenie akcji zwrotnych, np. wysłanie powiadomienia na Slacka lub e-mail.

---

### Najważniejsze dobre praktyki dla pipeline'ów w Jenkinsie

#### 1. Trzymaj definicję potoku w kodzie (Pipeline as Code)

* Zawsze przechowuj plik `Jenkinsfile` w głównym katalogu repozytorium projektu (w systemie kontroli wersji Git), zamiast wpisywać skrypty ręcznie w panelu WWW Jenkinsa.

#### 2. Buduj w kontenerach (`agent { docker { ... } }`)

* Zamiast instalować narzędzia (Node.js, Java, Python) bezpośrednio na maszynie z agentem Jenkinsa, uruchamiaj etapy wewnątrz kontenerów Dockerowych. Zapewnia to idealne odizolowanie środowiska i eliminuje problem *"u mnie działa, a na serwerze nie"*.

```groovy
agent {
    docker {
        image 'node:20-alpine'
    }
}

```

#### 3. Nigdy nie hardkoduj sekretów

* Dostęp do rejestrów, kluczy SSH czy haseł powinien odbywać się wyłącznie przez bezpieczny magazyn **Jenkins Credentials** oraz bloki `withCredentials` lub `withRegistry`.

#### 4. Zarządzaj czasem i historią (`options`)

* Zawsze definiuj maksymalny czas wykonania potoku (`timeout`), aby zawieszone procesy nie blokowały zasobów serwera, oraz ograniczaj liczbę przechowywanych kompilacji:

```groovy
options {
    timeout(time: 1, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '15'))
    ansiColor('xterm')
}

```

#### 5. Używaj `npm ci` zamiast `npm install`

* W środowiskach CI/CD stosuj `npm ci` (lub odpowiedniki typu `yarn install --frozen-lockfile`). Zapewnia to deterministyczną powtarzalność budowania i skraca czas instalacji pakietów.

#### 6. Optymalizuj czas wykonania (Równoległość)

* Zależności, które nie wpływają na siebie nawzajem (np. testy jednostkowe, linter, skanowanie bezpieczeństwa SonarQube), uruchamiaj równolegle za pomocą sekcji `parallel`:

```groovy
stage('Quality Checks') {
    parallel {
        stage('Lint') { steps { sh 'npm run lint' } }
        stage('Unit Tests') { steps { sh 'npm test' } }
        stage('Security Scan') { steps { sh 'npm run audit' } }
    }
}

```