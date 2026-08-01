import argparse, math, json

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

def main(argv=None):
    ap=argparse.ArgumentParser(description='Plan LLM eval sample size and cost.')
    ap.add_argument('--baseline', type=float, required=True, help='current pass rate, e.g. 0.72')
    ap.add_argument('--target', type=float, required=True, help='target pass rate, e.g. 0.80')
    ap.add_argument('--input-tokens', type=int, default=1200)
    ap.add_argument('--output-tokens', type=int, default=500)
    ap.add_argument('--input-price', type=float, default=1.0)
    ap.add_argument('--output-price', type=float, default=5.0)
    ns=ap.parse_args(argv)
    n=estimate(ns.baseline, ns.target)
    dollars=cost(n, ns.input_tokens, ns.output_tokens, ns.input_price, ns.output_price)
    print(json.dumps({'samples_per_candidate':n,'candidates':2,'estimated_cost_usd':round(dollars,4),'minimum_detectable_delta':round(abs(ns.target-ns.baseline),4)}, indent=2))
if __name__=='__main__': main()
