Wyjaśnienie błędów i poprawek
Literówka w składni Jenkins (etap Build)

Problem: Słowo kluczowe zostało napisane jako stesp.

Naprawa: Poprawiono na steps. W potoku deklaratywnym Jenkinsa blok steps jest wymagany do zdefiniowania kroków wykonywanych w danym etapie – literówka powoduje błąd parsowania składni.

Złe umiejscowienie bloku when (etap Deploy)

Problem: Blok when { branch 'master' } umieszczono na końcu etapu, po bloku steps.

Naprawa: Przeniesiono blok when przed blok steps. W potokach deklaratywnych dyrektywy warunkowe oraz konfiguracyjne etapu (np. when, environment, agent) muszą wyprzedzać sekcję z krokami do wykonania.

Nieprawidłowe polecenie npm (etap Build)

Problem: Polecenie npm build nie uruchamia skryptu budującego zdefiniowanego w pliku package.json (jest to stary wewnętrzny alias npm).

Naprawa: Zmieniono komendę na npm run build, która poprawnie wywołuje skrypt budujący aplikacji.

Niejawne tagowanie obrazu Docker (etap Deploy)

Problem: Komenda docker build -t myapp . nie określała jawnie tagu w nazwie podczas budowania, a krok niżej wypychał myapp:latest.

Naprawa: Ujednolicono komendę budującą do docker build -t myapp:latest ., zapewniając spójność przy wypychaniu obrazu do rejestru.

Wskazówka: Jeśli Twoje repozytorium używa domyślnej nazwy głównej gałęzi main zamiast master, pamiętaj o zaktualizowaniu kryterium w sekcji when { branch 'main' }.