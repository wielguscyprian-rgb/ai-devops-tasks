Wyjaśnienie użytych znaczników JSDoc:
@param {string|number} userId – Określa akceptowane typy argumentu userId (łańcuch znaków lub liczba) oraz podaje jego opis.

@returns {Promise<... | null>} – Informuje, że funkcja asynchroniczna zwraca Promise.

{name: string, email: string, lastLogin: Date} – Szablon struktury obiektu zawartego w obietnicy po pomyślnym przetworzeniu odpowiedzi z API.

| null – Sygnalizuje podpowiadaczom składni (np. w VS Code), że funkcja może zwrócić null, jeśli przechwyci błąd w bloku .catch().