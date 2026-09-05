import numpy as np

def report(name, kfast, kslow, tc, fd):
    left  = np.exp(-kfast*tc)              # N(tc^-)/N0
    right = fd + (1-fd)*1.0                # N(tc^+)/N0  = 1 exactly
    print(f"\n== {name}: k_fast={kfast}/h, k_slow={kslow}/h, tc={tc}h, Nd/N0={fd}")
    print(f"   N(tc-)/N0 = {left:.3e}   N(tc+)/N0 = {right:.3f}   JUMP = x{right/left:,.4g}  ({np.log10(right/left):.2f} log10 resurrection)")
    print(f"   long-time asymptote N(inf)/N0 = {fd}  -> never sterilizes (floor {fd*1e6:.3g} CFU/mL from 1e6 inoculum)")
    # correct continuous piecewise
    print(f"   continuous fix: N(t>=tc) = N(tc-)*exp(-k_slow(t-tc)) -> N(240h)/N0 = {left*np.exp(-kslow*(240-tc)):.3e}")
    # implied tc if biexponential with persister fraction fd
    tc_imp = np.log((1-fd)/fd)/(kfast-kslow)
    print(f"   biexponential-implied crossover tc = {tc_imp:.2f} h  (paper asserts {tc} h -> inconsistent by {tc/tc_imp:.1f}x)")

report("M. tuberculosis (Results tc=80h)", 0.1, 0.001, 80, 0.0358)
report("S. aureus (Results tc=12h)",       0.5, 0.01,  12, 0.0005)
report("S. aureus (ABSTRACT tc=80h)",      0.5, 0.01,  80, 0.0005)

print("\n== Resistance equation N_R = N0*exp((r-kR)t), no carrying capacity")
for sp, r, kR in [("Mtb",0.03,0.002), ("S. aureus",0.5,0.01)]:
    for t in (24, 240):
        print(f"   {sp:10s} t={t:3d}h -> N/N0 = 1e{np.log10(np.exp((r-kR)*t)):.1f}")
print("   (logistic K declared in Methods is never applied; S. aureus exceeds total bacterial mass of Earth)")
