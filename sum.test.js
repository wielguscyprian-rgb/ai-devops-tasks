// sum.test.js
const sum = require('./sum');

test('dodaje 1 + 2, dając wynik 3', () => {
  expect(sum(1, 2)).toBe(3);
});

test('poprawnie dodaje liczby ujemne', () => {
  expect(sum(-2, -3)).toBe(-5);
});