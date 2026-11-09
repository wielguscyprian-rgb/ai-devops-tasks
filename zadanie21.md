### Proces konwersji JSON do CSV

Konwersja danych z formatu hierarcheskiego (JSON) na format płaski/tabelaryczny (CSV) składa się z 4 głównych etapów:

1. **Parsowanie struktury źródłowej:** Odczytanie drzewa obiektów JSON i przekształcenie go na struktury danych w pamięci (np. listy słowników).
2. **Ekstrakcja unikalnych kluczy (Nagłówków):** Przeskanowanie obiektów w celu wyznaczenia kompletnej listy kolumn. Jeśli obiekty mają różną strukturę, należy zebrać sumę wszystkich występujących pól.
3. **Spłaszczanie i transformacja wartości (Flattening):** Przekształcenie zagnieżdżonych obiektów i tablic na pojedyncze wartości tekstowe lub liczbowe pasujące do komórek tabeli.
4. **Escaping i formatowanie wyjściowe:** Zapisanie danych wiersz po wierszu z uwzględnieniem znaków ucieczki (quotes) i właściwego kodowania znaków (np. UTF-8).

---

### Potencjalne wyzwania i sposoby ich rozwiązania

#### 1. Reprezentacja tablic w komórce CSV (np. pole `roles`)

CSV jest formatem dwuwymiarowym i nie obsługuje natywnie struktur listowych. Istnieją cztery główne podejścia do tego problemu:

* **Połączenie wartości ciągiem znaków (Delimited String) – *zastosowane w poprzednim przykładzie***
* *Opis:* Elementy tablicy łączy się w jeden ciąg tekstowy za pomocą separatora (np. przecinek, średnik lub pionowa kreska `|`).
* *Przykład:* `"admin, user"` lub `"admin|user"`
* *Zalety:* Proste w odbiorze, nie zmienia liczby wierszy ani kolumn.
* *Wada:* Wymaga ujęcia całej komórki w cudzysłów, aby separator wewnątrz ciągu nie został zinterpretowany jako podział na nową kolumnę.


* **Kodowanie binarne / One-Hot Encoding (Kolumny dla każdej roli)**
* *Opis:* Tworzy się osobną kolumnę dla każdej możliwej wartości w tablicy z wartościami logicznymi (`TRUE`/`FALSE` lub `1`/`0`).
* *Przykład kolumn:* `role_admin`, `role_user`, `role_editor`
* *Zalety:* Bardzo łatwa filtracja w Excelu i w modelach uczenia maszynowego.
* *Wada:* Znaczny wzrost liczby kolumn przy dużej liczbie unikalnych ról.


* **Serializacja do surowego ciągu JSON**
* *Opis:* Zapisanie tablicy w komórce w jej dokładnej postaci tekstowej z JSON-a.
* *Przykład:* `"[ \"admin\", \"user\" ]"`
* *Zalety:* Pozwala na łatwe odtworzenie struktury przy ponownym parsowaniu pliku przez skrypty.
* *Wada:* Słaba czytelność dla użytkownika otwierającego plik w arkuszu kalkulacyjnym.


* **Normalizacja relacyjna (Multi-row expansion)**
* *Opis:* Powielenie wiersza dla każdego elementu z tablicy lub wydzielenie drugiego pliku CSV (relacja 1-do-wielu).
* *Przykład:* Dwa wiersze dla Jana Kowalskiego – jeden z rolą `admin`, drugi z rolą `user`.
* *Wada:* Zwielokrotnienie pozostałych danych (duplikacja wierszy).



---

#### 2. Głęboko osadzone obiekty (Nested Objects)

Gdy obiekt JSON zawiera w sobie inne obiekty (np. `user.address.city`), stosuje się tzw. **notację kropkową** (Dot Notation) w nagłówkach kolumn:

* JSON: `"address": { "city": "Gdańsk", "zip": "80-000" }`
* Kolumny CSV: `address.city`, `address.zip`

#### 3. Niespójność schematu (Heterogeniczne obiekty)

W JSON-ie każdy obiekt w tablicy może mieć zupełnie zestaw pól. CSV wymaga stałej liczby kolumn dla każdego wiersza.

* *Rozwiązanie:* Przed generowaniem CSV należy wykonać pełny przebieg po wszystkich obiektach, zdefiniować superset wszystkich unikalnych kluczy, a dla obiektów nieposiadających danego pola wpisywać wartość pustą (`null` / `""`).

#### 4. Znaki specjalne i Escaping

Jeśli wartość tekstowa zawiera:

* Przecinek (separator kolumn),
* Znak nowej linii (`\n` lub `\r\n`),
* Cudzysłów (`"`),

wówczas cała wartość w CSV musi zostać ujęta w cudzysłów, a wewnętrzne cudzysłowy zduplikowane (np. `"Wartość z \"cytatem\""` zmienia się w `"Wartość z ""cytatem"""`).

#### 5. Kodowanie znaków i zgodność z MS Excel

Standardowym kodowaniem dla JSON i CSV jest `UTF-8`. Jednak Microsoft Excel otwierany dwuklikiem na plik `.csv` często nie rozpoznaje znaków diakrytycznych (np. polskich liter `ą, ę, ł`).

* *Rozwiązanie:* Zapis pliku CSV z nagłówkiem **UTF-8 BOM** (Byte Order Mark), co wymusza na programach takich jak Excel poprawne odczytanie polskich znaków.