Najbardziej wydajnym podejściem jest użycie zbiorów (set), co pozwala zredukować złożoność czasową do $\mathcal{O}(N)$.Optymalna wersja z użyciem zbiorów (set)Zbiory w Pythonie są oparte na tablicach mieszających (hash table), dzięki czemu sprawdzanie obecności elementu (in) oraz dodawanie (add) odbywa się w średnim czasie $\mathcal{O}(1)$.

Cecha,Oryginalny kod,Wersja ze zbiorami (set)
Złożoność czasowa,O(N2),O(N)
Złożoność pamięciowa,O(K) (gdzie K to liczba duplikatów),O(N) (gdzie N to liczba wszystkich elementów)
Wyszukiwanie duplikatu,Przeszukiwanie całej listy duplicates O(K),Haszowanie w zbiorze O(1)

Dla małych list (np. 10 elementów) różnica będzie niezauważalna, ale dla listy zawierającej 100 000 elementów:

Oryginalny kod wykona setki milionów porównań i może działać kilkadziesiąt sekund.

Wersja ze zbiorami wykona operację w ułamku sekundy


def find_duplicates(list_of_items):
    duplicates = []
    for i in range(len(list_of_items)):
        for j in range(i+1, len(list_of_items)):
            if list_of_items[i] == list_of_items[j] and list_of_items[i] not in duplicates:
                duplicates.append(list_of_items[i])
    return duplicates
--------zoptymalizowana:-------------
Python
def find_duplicates(list_of_items):
    seen = set()
    duplicates = set()
    
    for item in list_of_items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
            
    return list(duplicates)