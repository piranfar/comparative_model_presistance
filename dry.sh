#!/bin/sh
export PYTHONIOENCODING=utf-8
run(){
echo ""; echo "===== DRYAD q=[$2] ====="
curl -s --max-time 60 "https://datadryad.org/api/v2/search?q=$1&per_page=100" -o dry.json
python -c "
import json
try: d=json.load(open('dry.json'))
except Exception: print('  (no json)'); raise SystemExit
print('  count:', d.get('count'))
for x in d.get('_embedded',{}).get('stash:datasets',[]):
    print('  %s | %s' % (x.get('identifier'), (x.get('title') or '')[:130].encode('ascii','replace').decode()))
"
}
run "tuberculosis" 'tuberculosis'
run "%22colony%20forming%22" 'colony forming'
run "CFU%20antibiotic" 'CFU antibiotic'
run "killing%20kinetics" 'killing kinetics'
run "antibiotic%20tolerance" 'antibiotic tolerance'
run "persister" 'persister'
