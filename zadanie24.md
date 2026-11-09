```python
req_count = 15000
errors_5xx = 120
error_rate = (errors_5xx / req_count) * 100

avg_mem = 2.1
max_mem = 3.5
total_mem = 4.0

avg_mem_pct = (avg_mem / total_mem) * 100
max_mem_pct = (max_mem / total_mem) * 100

rps_avg = req_count / (24 * 3600)

print(f"Error Rate: {error_rate:.2f}%")
print(f"Avg Memory Pct: {avg_mem_pct:.1f}%")
print(f"Max Memory Pct: {max_mem_pct:.1f}%")
print(f"Avg RPS: {rps_avg:.2f}")


```

```text
Error Rate: 0.80%
Avg Memory Pct: 52.5%
Max Memory Pct: 87.5%
Avg RPS: 0.17


```

Wskaźnik błędów 5xx na poziomie **0,8%** (120 zapytań na 15 000) oraz wartość 99. percentyla czasu odpowiedzi wynosząca **1200 ms** przy tak niedużym średnim natężeniu ruchu (~0,17 RPS) wskazują na niestabilność aplikacji w momentach szczytowego obciążenia.

### 1. Interpretacja metryk i zidentyfikowane problemy

* **Przekroczony margines błędów 5xx (0,8%):** Dla produkcyjnych interfejsów API akceptowalny poziom błędów serwera (SLA $99{,}9\%$) wynosi zazwyczaj $<0{,}1\%$. Wynik 0,8% oznacza, że średnio co 125. zapytanie kończy się awarią.
* **Ryzyko awarii OOM (Out-Of-Memory):** Szczytowe zużycie pamięci na poziomie **3,5 GB z 4 GB dostępnych (87,5%)** znajduje się w strefie krytycznej. Przekroczenie progu 90% grozi nagłym ubiciem procesu przez systemowy OOM Killer lub kontener Dockera.
* **Wysoki "long tail" opóźnień (p99 = 1200 ms):** Podczas gdy średni czas odpowiedzi wynosi 230 ms, najwolniejszy 1% zapytań (150 żądań) czeka ponad 1,2 sekundy.
* **Wysokie użycie CPU w pikach (80%):** Skoki obciążenia procesora w połączeniu ze skokami RAM sugerują wykonywanie ciężkich, nie zoptymalizowanych operacji I/O, braki w indeksowaniu bazy danych lub przetwarzanie dużych zbiorów danych w pamięci operacyjnej.

---

### 2. Sugestie poprawek i plan działań

#### Krok 1: Naprawa natychmiastowa i diagnostyka

1. **Korelacja logów ze szczytami obciążenia:** Przeanalizuj logi z momentów, w których CPU osiągało 80%, a RAM 3,5 GB. Sprawdź, które konkretnie endpointy generowały kody 5xx (błędy unhandled exceptions vs timeouty bazy danych).
2. **Tymczasowy margines pamięci:** Zwiększ pamięć przydzieloną kontenerowi/maszynie (np. do 6–8 GB) lub skonfiguruj parametr Node.js `--max-old-space-size=3072`, aby zapobiec wyciekowi i awariom typu CrashLoopBackOff podczas poszukiwania przyczyny problemu.

#### Krok 2: Optymalizacja wydajnościowa

1. **Wdrożenie paginacji (Stronicowania):** Gwałtowny wzrost zużycia RAM z 2,1 GB do 3,5 GB najczęściej świadczy o pobieraniu pełnych kolekcji/tabel z bazy do pamięci RAM aplikacji. Zastąp pobieranie wszystkich rekordów paginacją (cursor-based lub limit/offset).
2. **Optymalizacja zapytań i indeksów:** Przeprowadź analizę `EXPLAIN` dla zapytań obsługujących endpointy odpowiedzialne za p99 (1200 ms) i dodaj brakujące indeksy w bazie danych.
3. **Pula połączeń (Connection Pool):** Sprawdź rozmiar puli połączeń do bazy danych. Wartości p99 i kody 5xx często wynikają z kolejkowania zapytań z powodu wyczerpania wolnych połączeń.
4. **Horyzontalne skalowanie (Skalowanie w poprzek):** Zamiast jednej pojedynczej instancji z 4 GB RAM, rozważ uruchomienie 2–3 mniejszych instancji za prostym Load Balancerem. Zapewni to odporność na awarie (High Availability) i wyeliminuje wąskie gardła procesora w szczycie.