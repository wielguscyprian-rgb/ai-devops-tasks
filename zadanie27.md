Opis przebiegu potoku
Checkout kodu: Pobranie aktualnego kodu z repozytorium (np. Git).

Budowanie (Build): Kompilacja kodu źródłowego oraz instalacja zależności (np. npm run build, mvn clean package).

Testy jednostkowe (Unit Tests): Uruchomienie szybkiej weryfikacji poszczególnych komponentów.

Analiza statyczna kodu: Sprawdzenie jakości kodu, długu technologicznego i podatności w narzędziach typu SonarQube.

Skanowanie bezpieczeństwa: Analiza podatności w bibliotekach zewnętrznych (SCA) oraz analizowanie obrazów/zależności (Trivy/Snyk).

Budowanie obrazu Docker: Utworzenie kontenera aplikacji, nadanie odpowiedniego taga i wypchnięcie (push) do rejestru (np. Docker Hub, GHCR, Harbor).

Wdrożenie na Staging: Automatyczne wdrożenie gotowego kontenera na środowisko testowe odzwierciedlające produkcję.

Testy integracyjne / E2E: Uruchomienie testów scenariuszy biznesowych oraz integracji z zewnętrznymi usługami/bazą danych na żywym środowisku Staging.

Wdrożenie na Produkcję: Po sprawdzeniu gałęzi (main/master) oraz ewentualnej ręcznej akceptacji (manual gate), obraz trafia na środowisko produkcyjne (np. klastry Kubernetes, AWS ECS).