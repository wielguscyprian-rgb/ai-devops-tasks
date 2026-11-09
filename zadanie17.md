const tasks = [
  { id: 3, title: 'Przygotowanie raportu', status: 'completed' },
  { id: 1, title: 'Weryfikacja logów', status: 'pending' },
  { id: 2, title: 'Naprawa błędu w API', status: 'completed' },
  { id: 4, title: 'Wdrożenie na produkcję', status: 'in_progress' }
];

const result = getCompletedTaskTitles(tasks);
console.log(result); 
// Wyjście: ['Naprawa błędu w API', 'Przygotowanie raportu']