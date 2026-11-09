flowchart TD
    Start([Git Push / PR Trigger]) --> Checkout[1. Checkout kodu]

    subgraph CI ["Wciąganie i Weryfikacja (CI)"]
        Checkout --> Build[2. Budowanie aplikacji]
        Build --> UnitTest[3. Testy jednostkowe]
        UnitTest --> StaticAnalysis[4. Analiza statyczna kodu<br/><i>np. SonarQube</i>]
        StaticAnalysis --> SecurityScan[5. Skanowanie bezpieczeństwa<br/><i>np. Snyk / Trivy / OWASP</i>]
        SecurityScan --> DockerBuild[6. Budowanie i push obrazu Docker<br/><i>do Docker Registry / ECR</i>]
    end

    subgraph CD_Staging ["Środowisko Przejściowe (Staging)"]
        DockerBuild --> DeployStaging[7. Wdrożenie na Staging]
        DeployStaging --> IntTests[8. Testy integracyjne & E2E]
    end

    subgraph CD_Prod ["Środowisko Produkcyjne (Production)"]
        IntTests --> Approval{Warunek & Akceptacja<br/><i>np. gałąź main + manual gate</i>}
        Approval -- Zatwierdzono --> DeployProd[9. Wdrożenie na Produkcję]
        Approval -- Odrzucono / Błąd --> Fail([Stop / Notyfikacja])
        DeployProd --> Success([Koniec / Sukces])
    end

    style CI fill:#f9f9f9,stroke:#333,stroke-width:1px
    style CD_Staging fill:#edf2f7,stroke:#333,stroke-width:1px
    style CD_Prod fill:#e6fffa,stroke:#333,stroke-width:1px