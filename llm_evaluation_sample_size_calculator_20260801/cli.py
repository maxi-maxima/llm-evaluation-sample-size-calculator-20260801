import argparse, csv, json, math

def estimate(baseline, target, confidence=0.95, power=0.8):
    z_alpha={0.90:1.645,0.95:1.96,0.99:2.576}.get(round(confidence,2),1.96)
    z_power={0.8:0.84,0.9:1.28,0.95:1.645}.get(round(power,2),0.84)
    p=(baseline+target)/2
    diff=abs(target-baseline)
    if diff<=0: raise ValueError('target must differ from baseline')
    n=2*((z_alpha+z_power)**2)*p*(1-p)/(diff**2)
    return max(1, math.ceil(n))

def cost(samples, input_tokens, output_tokens, input_per_million, output_per_million, candidates=2):
    return samples*candidates*((input_tokens/1_000_000)*input_per_million + (output_tokens/1_000_000)*output_per_million)

def plan(row):
    baseline=float(row['baseline'])
    target=float(row['target'])
    candidates=int(row.get('candidates') or 2)
    samples=estimate(baseline, target)
    dollars=cost(samples, int(row.get('input_tokens') or 1200), int(row.get('output_tokens') or 500), float(row.get('input_price') or 1.0), float(row.get('output_price') or 5.0), candidates)
    out={'samples_per_candidate':samples,'candidates':candidates,'estimated_cost_usd':round(dollars,4),'minimum_detectable_delta':round(abs(target-baseline),4)}
    if row.get('name'):
        out={'name':row['name'], **out}
    return out

def load_scenarios(path):
    with open(path, newline='', encoding='utf-8') as handle:
        return [plan(row) for row in csv.DictReader(handle)]

def main(argv=None):
    ap=argparse.ArgumentParser(description='Plan LLM eval sample size and cost.')
    ap.add_argument('--baseline', type=float, help='current pass rate, e.g. 0.72')
    ap.add_argument('--target', type=float, help='target pass rate, e.g. 0.80')
    ap.add_argument('--input-tokens', type=int, default=1200)
    ap.add_argument('--output-tokens', type=int, default=500)
    ap.add_argument('--input-price', type=float, default=1.0)
    ap.add_argument('--output-price', type=float, default=5.0)
    ap.add_argument('--candidates', type=int, default=2)
    ap.add_argument('--scenarios-csv', help='CSV with baseline,target and optional token/price/candidates/name columns')
    ns=ap.parse_args(argv)
    if ns.scenarios_csv:
        print(json.dumps({'scenarios':load_scenarios(ns.scenarios_csv)}, indent=2))
        return
    if ns.baseline is None or ns.target is None:
        ap.error('--baseline and --target are required unless --scenarios-csv is used')
    print(json.dumps(plan(vars(ns)), indent=2))
if __name__=='__main__': main()
