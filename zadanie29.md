Plik konfiguracyjny Jenkins Configuration as Code (`jenkins.yaml`) wdraża się na dwa główne sposoby: poprzez **zbudowanie własnego kontenera Docker** (podejście zalecane w środowiskach produkcyjnych i CI/CD) lub poprzez **wczytanie go do istniejącej instancji Jenkinsa**.

---

### Metoda 1: Uruchomienie w Dockerze (Zalecane)

Jest to najszybszy i powtarzalny sposób na uruchomienie gotowego do pracy Jenkinsa bez konieczności przeklikiwania się przez panel WWW.

1. **Przygotuj pliki w jednym katalogu:**
Utwórz nowy folder na dysku i umieść w nim trzy pliki:
* **`jenkins.yaml`** – plik z wygenerowaną wcześniej konfiguracją JCasC.
* **`plugins.txt`** – lista wtyczek wymaganych przez konfigurację:



```text
configuration-as-code
job-dsl
build-timeout
git
workflow-aggregator
docker-workflow
nodejs
maven-plugin

```

* **`Dockerfile`** – instrukcja budowania obrazu:

```dockerfile
FROM jenkins/jenkins:lts

# Wyłączenie wstępnego kreatora konfiguracji
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Wskazanie ścieżki do pliku JCasC
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/jenkins.yaml

# Instalacja wtyczek z pliku plugins.txt
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

# Skopiowanie szablonu konfiguracyjnego JCasC
COPY jenkins.yaml /var/jenkins_home/jenkins.yaml

```

2. **Zbuduj obraz Docker:**
Otwórz terminal w katalogu z plikami i wykonaj polecenie:
```bash
docker build -t custom-jenkins:jcasc .

```


*Weryfikacja:* Proces budowania powinien zakończyć się bez błędów pobierania wtyczek.
3. **Uruchom kontener:**
```bash
docker run -d \
  --name jenkins-jcasc \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  custom-jenkins:jcasc

```


4. **Sprawdź działanie:**
Wejdź w przeglądarce pod adres `http://localhost:8080`.
*Weryfikacja:* Jenkins uruchomi się od razu (z pominięciem ekranu logowania i wyboru wtyczek). Na stronie głównej zobaczysz utworzone automatycznie zadanie `sample-web-app-pipeline`, a w sekcji *Zarządzaj Jenkinsem -> Global Tool Configuration* znajdziesz skonfigurowane instalatory dla Node.js, Mavena i Dockera.

---

### Metoda 2: Wczytanie pliku na istniejącej instancji Jenkinsa

Jeśli masz już uruchomiony serwer Jenkins i chcesz na nim zastosować konfigurację:

1. **Zainstaluj wymagane wtyczki:**
* Przejdź do **Zarządzaj Jenkinsem** (*Manage Jenkins*) -> **Wtyczki** (*Plugins*).
* Zainstaluj wtyczkę **Configuration as Code** (`configuration-as-code`) oraz **Job DSL** (`job-dsl`).


2. **Wskazanie pliku w panelu administracyjnym:**
* Przejdź do **Zarządzaj Jenkinsem** -> **Configuration as Code**.
* W polu **Path or URL** wpisz bezwzględną ścieżkę do pliku na serwerze, np.:
* Linux: `/var/jenkins_home/jenkins.yaml`
* Windows: `C:\jenkins\jenkins.yaml`


* Kliknij przycisk **Apply new configuration**.
*Weryfikacja:* Jeśli składnia pliku jest poprawna, pojawi się komunikat o pomyślnym załadowaniu konfiguracji bez błędów parsowania.


3. **Automatyzacja przez zmienną środowiskową (opcjonalnie):**
Aby Jenkins ładował ten plik przy każdym swoim restarcie, ustaw zmienną środowiskową na serwerze przed uruchomieniem procesu Jenkinsa:
* **Linux/macOS:** `export CASC_JENKINS_CONFIG=/sciezka/do/jenkins.yaml`
* **Windows (CMD):** `set CASC_JENKINS_CONFIG=C:\sciezka\do\jenkins.yaml`