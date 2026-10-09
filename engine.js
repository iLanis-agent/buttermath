/* Butter math - exact arithmetic, labeled kitchen norms.
   Labeled norms shown in the UI: butter yield 45% of cream weight, buttermilk
   is the rest; churn minutes scale from a 500 g base by method (jar 20,
   hand mixer 10, stand mixer 6, processor 4); salted butter 1.5% salt;
   3 rinse rounds, rinse water 1 mL per g of butter per round. */
(function (root) {
  'use strict';

  var METHODS = { jar: 20, hand: 10, stand: 6, processor: 4 };
  var YIELD = 0.45, SALT = 0.015, RINSES = 3;

  function num(v, name) {
    if (typeof v !== 'number' || !isFinite(v)) throw new Error(name + ' must be a number');
    return v;
  }
  function creamOf(creamG) {
    creamG = num(creamG, 'cream');
    if (!Number.isInteger(creamG)) throw new Error('weigh cream in whole grams');
    if (creamG <= 0) throw new Error('cream must be positive');
    if (creamG > 10000) throw new Error('keep it under 10 kg (labeled)');
    return creamG;
  }

  function creamToButter(creamG) {
    creamG = creamOf(creamG);
    var butter = Math.round(creamG * YIELD);
    var verdict = creamG < 300 ? 'a small jar batch' : creamG < 1000 ? 'a kitchen batch' : 'a churn day';
    return { butter_g: butter, buttermilk_g: creamG - butter, verdict: verdict };
  }

  function churnTime(creamG, method) {
    creamG = creamOf(creamG);
    var base = METHODS[String(method).toLowerCase()];
    if (base === undefined) throw new Error('method is jar, hand, stand or processor (labeled)');
    var minutes = Math.round(base * (creamG / 500) * 10) / 10;
    var verdict = minutes < 10 ? 'a quick churn' : minutes < 25 ? 'an arm workout' : 'call it a project';
    return { minutes: minutes, verdict: verdict };
  }

  function saltAndWash(butterG, style) {
    butterG = num(butterG, 'butter');
    if (!Number.isInteger(butterG)) throw new Error('weigh butter in whole grams');
    if (butterG <= 0) throw new Error('butter must be positive');
    if (butterG > 5000) throw new Error('keep it under 5 kg (labeled)');
    style = String(style).toLowerCase();
    var salt = style === 'unsalted' ? 0 : style === 'salted' ? Math.round(butterG * SALT * 10) / 10
      : (function(){ throw new Error('style is salted or unsalted (labeled)'); })();
    var verdict = salt === 0 ? 'no salt to weigh' : salt < 2 ? 'a pinch' : salt < 10 ? 'a modest pinch' : 'weigh it carefully';
    return { salt_g: salt, rinses: RINSES, rinse_water_ml: RINSES * butterG, verdict: verdict };
  }

  var api = { creamToButter: creamToButter, churnTime: churnTime, saltAndWash: saltAndWash };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.ButterMath = api;
})(typeof window !== 'undefined' ? window : globalThis);
