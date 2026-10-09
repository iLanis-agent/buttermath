# Butter math

Three butter-making calculators as a small static site - exact arithmetic,
every borrowed number labeled:

- **Cream to butter** - cream weight becomes butter (labeled 45% yield) and
  buttermilk, with a batch-size band.
- **Churn time** - method (jar 20 / hand mixer 10 / stand mixer 6 / processor
  4 min per 500 g, labeled) and cream weight become minutes, with an effort band.
- **Salt and wash** - butter weight becomes salt (labeled 1.5% for salted),
  3 rinse rounds and rinse water (labeled 1 mL per g per round).

## Files

- `index.html` - landing page
- `app.html` - the three calculators
- `engine.js` - all arithmetic, shared by the page and the tests
- `oracle.py` - independent Python mirror of the engine; regenerates `expected.json`
- `expected.json` - 49 cases (per-card values plus error cases)
- `test.js` - runs the engine against `expected.json` (node test.js)

## Tests

```
python3 oracle.py   # regenerate expected cases
node test.js        # engine vs oracle
```
