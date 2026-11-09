Skrypt jest w jenkins-manager.py. Łączy się z Jenkinsem przez REST API (Basic Auth: użytkownik + token API), przy uruchamianiu zadania pobiera crumb CSRF i zamienia błędy sieci, HTTP 401/403/404 oraz zły JSON na czytelny komunikat.

Potrzebna jest biblioteka requests:


pip install requests
Ustaw dane logowania w zmiennych środowiskowych (token z profilu użytkownika w Jenkinsie: Configure → API Token):


$env:JENKINS_URL = "http://localhost:8080"
$env:JENKINS_USER = "twoj-user"
$env:JENKINS_TOKEN = "twoj-token"
Potem:


python jenkins-manager.py list
python jenkins-manager.py status --job nazwa-zadania --count 5
python jenkins-manager.py build nazwa-zadania
python jenkins-manager.py build nazwa-zadania --param BRANCH=main --param ENV=staging
list — wszystkie zadania z poziomu głównego i status ostatniego builda (blue → SUCCESS, red → FAILURE itd.).
status — ostatnie buildy jednego zadania albo wszystkich. Zadanie w folderze podajesz jako folder/zadanie.
build — kolejkuje wybrane zadanie. Parametry idą przez buildWithParameters.