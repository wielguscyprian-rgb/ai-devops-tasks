#!/bin/bash

echo "Sprawdzanie statusu usługi Docker..."

# systemctl is-active zwraca kod 0 jeśli usługa działa, --quiet ukrywa standardowe wyjście
if systemctl is-active --quiet docker; then
    echo "Usługa Docker jest już uruchomiona."
else
    echo "Docker nie działa. Próba uruchomienia..."
    
    # Uruchomienie usługi (wymaga uprawnień roota/sudo)
    sudo systemctl start docker
    
    # Weryfikacja, czy uruchomienie się powiodło
    if systemctl is-active --quiet docker; then
        echo "Usługa Docker została pomyślnie uruchomiona."
    else
        echo "Błąd: Nie udało się uruchomić usługi Docker. Sprawdź logi poleceniem: journalctl -u docker.service"
        exit 1
    fi
fi