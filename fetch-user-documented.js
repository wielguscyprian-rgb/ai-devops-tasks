/**
 * Pobiera dane użytkownika z zewnętrznego API na podstawie jego identyfikatora.
 *
 * @param {string|number} userId - Unikalny identyfikator użytkownika.
 * @returns {Promise<{name: string, email: string, lastLogin: Date} | null>} Obietnica (Promise) zwracająca sformatowane dane użytkownika lub `null` w przypadku błędu sieci/HTTP.
 */
function fetchUserData(userId) {
    return fetch(`https://api.example.com/users/${userId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        return {
          name: data.name,
          email: data.email,
          lastLogin: new Date(data.lastLoginTimestamp)
        };
      })
      .catch(error => {
        console.error('Fetch error:', error);
        return null;
      });
  }