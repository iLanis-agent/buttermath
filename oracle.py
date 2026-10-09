#!/usr/bin/env python3
# Oracle for buttermath. Mirrors engine.js float ops exactly (IEEE 754 doubles).
import math, json, os

METHODS = {'jar': 20, 'hand': 10, 'stand': 6, 'processor': 4}
YIELD, SALT, RINSES = 0.45, 0.015, 3

def jround(x):
    return math.floor(x + 0.5)

def creamToButter(creamG):
    butter = jround(creamG * YIELD)
    verdict = 'a small jar batch' if creamG < 300 else 'a kitchen batch' if creamG < 1000 else 'a churn day'
    return {'butter_g': butter, 'buttermilk_g': creamG - butter, 'verdict': verdict}

def churnTime(creamG, method):
    base = METHODS[method]
    minutes = jround(base * (creamG / 500) * 10) / 10
    verdict = 'a quick churn' if minutes < 10 else 'an arm workout' if minutes < 25 else 'call it a project'
    return {'minutes': minutes, 'verdict': verdict}

def saltAndWash(butterG, style):
    salt = 0 if style == 'unsalted' else jround(butterG * SALT * 10) / 10
    verdict = 'no salt to weigh' if salt == 0 else 'a pinch' if salt < 2 else 'a modest pinch' if salt < 10 else 'weigh it carefully'
    return {'salt_g': salt, 'rinses': RINSES, 'rinse_water_ml': RINSES * butterG, 'verdict': verdict}

FUN = {'creamToButter': creamToButter, 'churnTime': churnTime, 'saltAndWash': saltAndWash}

CASES = [
  {'card':'creamToButter','args':[250]},  {'card':'creamToButter','args':[500]},
  {'card':'creamToButter','args':[1000]}, {'card':'creamToButter','args':[300]},
  {'card':'creamToButter','args':[999]},  {'card':'creamToButter','args':[2000]},
  {'card':'creamToButter','args':[150]},  {'card':'creamToButter','args':[750]},
  {'card':'creamToButter','args':[4500]}, {'card':'creamToButter','args':[111]},
  {'card':'creamToButter','args':[833]},  {'card':'creamToButter','args':[3000]},
  {'card':'creamToButter','args':[0],'error':'positive'},
  {'card':'creamToButter','args':[-500],'error':'positive'},
  {'card':'creamToButter','args':[2.5],'error':'whole grams'},
  {'card':'creamToButter','args':[12000],'error':'under 10 kg'},
  {'card':'churnTime','args':[500,'jar']},   {'card':'churnTime','args':[1000,'jar']},
  {'card':'churnTime','args':[250,'jar']},   {'card':'churnTime','args':[3000,'jar']},
  {'card':'churnTime','args':[500,'hand']},  {'card':'churnTime','args':[1200,'hand']},
  {'card':'churnTime','args':[500,'stand']}, {'card':'churnTime','args':[2000,'stand']},
  {'card':'churnTime','args':[500,'processor']}, {'card':'churnTime','args':[900,'processor']},
  {'card':'churnTime','args':[150,'hand']},  {'card':'churnTime','args':[4500,'jar']},
  {'card':'churnTime','args':[750,'stand']}, {'card':'churnTime','args':[2000,'hand']},
  {'card':'churnTime','args':[0,'jar'],'error':'positive'},
  {'card':'churnTime','args':[500,'blender'],'error':'method is'},
  {'card':'churnTime','args':[2.5,'jar'],'error':'whole grams'},
  {'card':'saltAndWash','args':[225,'salted']},  {'card':'saltAndWash','args':[450,'salted']},
  {'card':'saltAndWash','args':[225,'unsalted']},{'card':'saltAndWash','args':[100,'salted']},
  {'card':'saltAndWash','args':[130,'salted']},  {'card':'saltAndWash','args':[133,'salted']},
  {'card':'saltAndWash','args':[660,'salted']},  {'card':'saltAndWash','args':[667,'salted']},
  {'card':'saltAndWash','args':[2000,'salted']}, {'card':'saltAndWash','args':[50,'unsalted']},
  {'card':'saltAndWash','args':[1350,'salted']}, {'card':'saltAndWash','args':[900,'unsalted']},
  {'card':'saltAndWash','args':[0,'salted'],'error':'positive'},
  {'card':'saltAndWash','args':[225,'sweet'],'error':'style is'},
  {'card':'saltAndWash','args':[2.5,'salted'],'error':'whole grams'},
  {'card':'saltAndWash','args':[6000,'salted'],'error':'under 5 kg'},
]

out = []
for c in CASES:
    row = dict(c)
    if 'error' not in c:
        row['expect'] = FUN[c['card']](*c['args'])
    out.append(row)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expected.json')
with open(path, 'w') as fh:
    json.dump(out, fh, indent=1)
    fh.write('\n')
print(len(out), 'cases written')
