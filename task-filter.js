function getCompletedTaskTitles(tasks) {
    return tasks
      .filter(task => task.status === 'completed')
      .sort((a, b) => a.id - b.id)
      .map(task => task.title);
  }