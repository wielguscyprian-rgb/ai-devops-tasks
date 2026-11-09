Oto rozbicie tego skryptu na czynniki pierwsze. Omówimy każdą linijkę tak, aby wszystko było jasne, nawet jeśli dopiero zaczynasz przygodę z Linuksem i programowaniem.

**`#!/bin/bash`**
To jest tzw. *shebang*. Ten znak na samej górze pliku to informacja dla systemu operacyjnego: "Hej, ten plik tekstowy to skrypt. Kiedy go uruchomisz, użyj programu o nazwie **bash** (najpopularniejszego terminala w Linuksie), aby go odczytać".

**`echo "Sprawdzanie statusu usługi Docker..."`**
Polecenie `echo` działa dokładnie tak jak echo w górach – odrzuca (wypisuje na ekranie) to, co do niego powiesz. W tym przypadku po prostu wyświetli tekst w terminalu, żebyś wiedział, co skrypt w danym momencie robi.

**`if systemctl is-active --quiet docker; then`**
To jest początek warunku. Słowo `if` oznacza "jeśli", a `then` "wtedy/to". Pomiędzy nimi znajduje się właściwe sprawdzenie:

* `systemctl` to główne narzędzie w Linuksie do zarządzania działającymi w tle programami (usługami).
* `is-active` pyta system: "Czy to teraz działa?".
* `--quiet` (z ang. cicho) oznacza: "Tylko sprawdź, ale nie wypisuj na ekranie żadnych zbędnych technicznych detali, interesuje mnie tylko ostateczny wynik".
* `docker` to nazwa usługi, którą sprawdzamy.
Całość czytamy: *Jeśli sprawdzisz w ciszy, że docker jest aktywny, to...*

**`echo "Usługa Docker jest już uruchomiona."`**
Skoro warunek z poprzedniej linijki okazał się prawdziwy (Docker działa), po prostu wyświetlamy radosny komunikat i w tym miejscu pierwsza część skryptu się kończy.

**`else`**
To słowo oznacza "w przeciwnym razie". Czyli program wejdzie w tę część kodu TYLKO wtedy, gdy Docker był wyłączony.

**`echo "Docker nie działa. Próba uruchomienia..."`**
Skoro jesteśmy w sekcji `else`, informujemy użytkownika, że przechodzimy do akcji i spróbujemy włączyć Dockera.

**`sudo systemctl start docker`**
To najważniejsze polecenie skryptu:

* `sudo` oznacza "wykonaj jako superużytkownik" (administrator). Standardowy użytkownik zazwyczaj nie ma uprawnień do włączania głównych usług systemu, więc `sudo` to poświadczenie władzy (może zapytać Cię o hasło).
* `systemctl start docker` to dosłowne wydanie komendy systemowi: "Uruchom usługę Docker".

**`if systemctl is-active --quiet docker; then`**
Skoro przed chwilą wydaliśmy polecenie włączenia, teraz musimy sprawdzić, czy to się faktycznie udało. Ponownie używamy tego samego warunku "jeśli", co na samym początku.

**`echo "Usługa Docker została pomyślnie uruchomiona."`**
Jeśli po naszej próbie uruchomienia usługa jest aktywna, wyświetlamy komunikat o sukcesie.

**`else`**
Znowu "w przeciwnym razie". Ten przypadek zadziała, jeśli mimo naszej komendy włączającej (`start`), Docker nadal pozostaje nieaktywny (bo np. brakuje plików, jest awaria systemu, albo nie podaliśmy poprawnego hasła do `sudo`).

**`echo "Błąd: Nie udało się uruchomić usługi Docker. Sprawdź logi poleceniem: journalctl -u docker.service"`**
Informujemy użytkownika o porażce. Dodatkowo podpowiadamy mu, jakiego narzędzia (`journalctl`) powinien użyć, aby przeczytać wewnętrzny dziennik błędów systemu (logi) i dowiedzieć się, co dokładnie wybuchło.

**`exit 1`**
Zatrzymuje działanie całego skryptu. Liczba `1` jest tutaj bardzo ważna. W świecie Linuksa i skryptów zasada jest prosta: kod wyjścia `0` oznacza pełen sukces, a każda inna liczba (np. `1`) to sygnał awarii. Dzięki temu inne automatyczne programy będą wiedziały, że ten skrypt zakończył się niepowodzeniem.

**`fi`**
To zabawny element basha – słowo `fi` to po prostu `if` napisane od tyłu. Służy do zamykania bloku warunkowego. Informuje skrypt: "Tutaj kończy się zachowanie uzależnione od warunku". (Mamy dwa `fi` na końcu, ponieważ mieliśmy dwa `if` – jedno wewnątrz drugiego).