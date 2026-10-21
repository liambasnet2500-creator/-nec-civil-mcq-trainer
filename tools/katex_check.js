const katex = require(process.env.KATEX||'katex');
const bank = require(process.argv[2] || './bank.json');
let bad = 0, n = 0;
for (const q of bank) {
  const fields = {stem: q.stem, reason: q.reason, note: q.note, ...q.options};
  for (const [k, v] of Object.entries(fields)) {
    if (!v) continue;
    const parts = v.split('$');
    if (parts.length % 2 === 0) { console.log(`UNBALANCED $ #${q.id} ${k}: ${v}`); bad++; continue; }
    for (let i = 1; i < parts.length; i += 2) {
      n++;
      try { katex.renderToString(parts[i], {throwOnError: true, strict: 'error'}); }
      catch (e) { bad++; console.log(`#${q.id} ${k}: ${parts[i]}  -> ${e.message.slice(0, 120)}`); }
    }
  }
}
console.log(`checked ${n} math segments, ${bad} errors`);
