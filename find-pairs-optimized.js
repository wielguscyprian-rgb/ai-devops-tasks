function findPairsOptimized(arr, targetSum) {
    const pairs = [];
    const freqMap = new Map();
  
    for (const num of arr) {
      const complement = targetSum - num;
      
      // Jeśli dopełnienie wystąpiło wcześniej, dodajemy parę dla każdego jego wystąpienia
      if (freqMap.has(complement)) {
        const count = freqMap.get(complement);
        for (let i = 0; i < count; i++) {
          pairs.push([complement, num]);
        }
      }
      
      // Zapisujemy wystąpienie aktualnej liczby
      freqMap.set(num, (freqMap.get(num) || 0) + 1);
    }
  
    return pairs;
  }