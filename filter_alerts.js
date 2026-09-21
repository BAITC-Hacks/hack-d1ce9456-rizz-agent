const fs = require('fs');

const events = fs
  .readFileSync('events.json', 'utf8')
  .trim()
  .split(/\r?\n/)
  .map(JSON.parse);

const criticalEvents = events.filter((event) => event.level === 'critical');

criticalEvents.forEach((event) => console.log(event.event));
console.log(`критичных ${criticalEvents.length}`);
