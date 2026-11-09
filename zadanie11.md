```javascript
// sum.js
function sum(a, b) {
  return a + b;
}

module.exports = sum;

```

```javascript
// sum.test.js
const sum = require('./sum');

test('dodaje 1 + 2, dając wynik 3', () => {
  expect(sum(1, 2)).toBe(3);
});

test('poprawnie dodaje liczby ujemne', () => {
  expect(sum(-2, -3)).toBe(-5);
});

```

---

## Czym jest Jest?

**Jest** to framework do testowania kodu w języku JavaScript i TypeScript, stworzony przez Meta (Facebook). Umożliwia pisanie i automatyczne wykonywanie testów jednostkowych, integracyjnych oraz komponentów interfejsu.

Działa bez konieczności skomplikowanej konfiguracji (*zero-config*) i zawiera w jednym pakiecie:

* **Test Runner:** Narzędzie automatycznie wyszukujące i wykonujące pliki z testami.
* **Bibliotekę asercji:** Zestaw funkcji (np. `expect()`, `toBe()`) do weryfikacji, czy wynik działania kodu jest zgodny z oczekiwaniami.
* **Narzędzie do mierzenia pokrycia kodu (Code Coverage):** Generuje raporty pokazujące, jaka część kodu została przetestowana.

---

## Struktura plików projektu

Dla powyższego przykładu plik testowy umieszcza się obok pliku z kodem źródłowym:

```text
moj-projekt/
├── node_modules/
├── package.json
├── package-lock.json
├── sum.js
└── sum.test.js

```

*Pliki z testami muszą mieć rozszerzenie `.test.js` lub `.spec.js`, aby Jest automatycznie je rozpoznał.*

---

## Instalacja i konfiguracja

1. **Inicjalizacja projektu Node.js:** Terminal.
Jeśli w projekcie nie ma jeszcze pliku `package.json`, utwórz go poleceniem:

```bash
npm init -y

```


2. **Instalacja pakietu Jest:** Terminal.
Zainstaluj Jest jako zależność deweloperską (`devDependencies`):

```bash
npm install --save-dev jest

```


3. **Dodanie skryptu testującego:** package.json.
Otwórz plik `package.json` i skonfiguruj polecenie `test` w sekcji `scripts`:

```json
{
  "name": "moj-projekt",
  "version": "1.0.0",
  "scripts": {
    "test": "jest"
  },
  "devDependencies": {
    "jest": "^29.7.0"
  }
}

```


---

## Uruchomienie testu

Wpisz w terminalu poniższe polecenie:

```bash
npm test

```

Jest znajdzie plik `sum.test.js`, wykona zdefiniowane w nim asercje i wyświetli wynik w konsoli:

```text
 PASS  ./sum.test.js
  ✓ dodaje 1 + 2, dając wynik 3 (2 ms)
  ✓ poprawnie dodaje liczby ujemne (1 ms)

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
Snapshots:   0 total
Time:        0.5 s

```