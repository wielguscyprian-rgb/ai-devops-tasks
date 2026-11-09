Oto ścisłe wyrażenie regularne sprawdzające poprawność adresu IPv4 (zakres `0.0.0.0` – `255.255.255.255`):

```regex
^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$

```

### Wyjaśnienie elementów wzorca

* **`^` oraz `$**` – kotwice oznaczające początek i koniec sprawdzanego ciągu znaków (zapobiegają dopasowaniu adresu będącego częścią dłuższego tekstu).
* **`(?: ... )`** – grupa przechwytująca bez zapamiętywania (zwiększa wydajność).
* **`25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]`** – reguła dla pojedynczego oktetu (zakres 0–255 bez wiodących zer):
* `25[0-5]` – liczby od 250 do 255
* `2[0-4][0-9]` – liczby od 200 do 249
* `1[0-9][0-9]` – liczby od 100 do 199
* `[1-9]?[0-9]` – liczby od 0 do 99


* **`\.`** – kropka rozdzielająca oktety.
* **`{3}`** – powtórzenie powyższej sekwencji (oktet + kropka) dokładnie 3 razy.
* **Ostatnia sekcja** – czwarty oktet bez kropki na końcu.

---

### Przykłady dopasowań

| Adres | Status | Powód |
| --- | --- | --- |
| `192.168.1.1` | Poprawny | Poprawny zakres |
| `0.0.0.0` | Poprawny | Poprawny zakres |
| `255.255.255.255` | Poprawny | Poprawny zakres |
| `256.100.0.1` | Błędny | `256` przekracza zakres 255 |
| `192.168.1` | Błędny | Brak czwartego oktetu |
| `192.168.01.1` | Błędny | Wiodące zero w `01` |

----------------drugi prompt--------------------


Wyrażenie `^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$` rozbija proces walidacji adresu IPv4 na trzy kluczowe mechanizmy: ścisłe kotwice brzegowe, precyzyjny zakres dla pojedynczego oktetu (0–255) oraz kontrolę powtórzeń.

---

### Anatomia wyrażenia krok po kroku

1. **Kotwice brzegowe (`^` oraz `$`)**
* `^` wymusza dopasowanie od pierwszego znaku ciągu.
* `$` wymusza zakończenie dopasowania na ostatnim znaku.
* *Skutek:* Wyrażenie nie dopasuje adresu wyciętego z dłuższego tekstu (np. z ignorowaniem `prefix_192.168.1.1_suffix`).


2. **Logika jednego oktetu `(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])**`
Zamiast naiwnego wzorca `\d{1,3}` (który akceptuje nieistniejące wartości, np. `999`), przedział 0–255 został podzielony na 4 wykluczające się warunki połączone operatorem alternatywy `|`:
* `25[0-5]` – dopasowuje liczby od **250 do 255**.
* `2[0-4][0-9]` – dopasowuje liczby od **200 do 249**.
* `1[0-9][0-9]` – dopasowuje liczby od **100 do 199**.
* `[1-9]?[0-9]` – dopasowuje liczby od **0 do 99** (np. `0`, `5`, `42`). Zapis ten świadomie odrzuca liczby z wiodącym zerem (np. `01` czy `007`), które w standardach sieciowych bywają interpretowane jako zapis w systemie ósemkowym.


3. **Grupa nieprzechwytująca `(?: ... )**`
Przedrostek `?:` nakazuje silnikowi regex niezapamiętywanie dopasowań w zmiennych podręcznych (brak rejestrowania grup przechwytujących), co ogranicza zużycie pamięci i przyspiesza działanie skryptu.
4. **Kropka i kwantyfikator `\.){3}**`
* `\.` – dosłowny znak kropki (zniesienie specjalnego znaczenia kropki w regex).
* `{3}` – wymusza powtórzenie sekwencji `(oktet + kropka)` dokładnie 3 razy z rzędu.


5. **Ostatni segment**
Koniec wzorca powtarza regułę oktetu, ale bez kropki na końcu, domykając oczekiwaną strukturę `X.X.X.X`.

---

### Testy na przykładach

#### Przykłady poprawne

| Testowany ciąg | Wynik | Wyjaśnienie |
| --- | --- | --- |
| `192.168.1.1` | **Dopasowano** | Oktety 192 i 168 pasują do `1[0-9][0-9]`, a oktety 1 pasują do `[1-9]?[0-9]`. |
| `0.0.0.0` | **Dopasowano** | Najniższy adres IPv4. Każde `0` spełnia regułę `[1-9]?[0-9]`. |
| `255.255.255.255` | **Dopasowano** | Najwyższy adres IPv4 (skrajny zakres górny). Każdy oktet pasuje do `25[0-5]`. |
| `10.240.0.50` | **Dopasowano** | Wszystkie oktety (10, 240, 0, 50) mieszczą się w wyznaczonych podzakresach. |

#### Przykłady niepoprawne

| Testowany ciąg | Wynik | Powód odrzucenia |
| --- | --- | --- |
| `256.1.1.1` | **Odrzucono** | `256` przekracza limit. Reguła `25[0-5]` akceptuje maksymalnie 255. |
| `192.168.01.1` | **Odrzucono** | `01` zawiera niepoprawne wiodące zero. Reguła `[1-9]?[0-9]` akceptuje `1` lub `10–99`, ale nie `01`. |
| `192.168.1.1.1` | **Odrzucono** | Adres zawiera 5 oktetów. Kwantyfikator `{3}` w połączeniu z `$` dopuszcza wyłącznie 4 oktety. |
| `192.168.1` | **Odrzucono** | Zbyt mało oktetów (3 zamiast 4). |
| `192.168.1.1000` | **Odrzucono** | Czwarty oktet ma 4 cyfry i przekracza dopuszczalny zakres. |
| `192.168.1.a` | **Odrzucono** | Znak `a` nie jest cyfrą. |