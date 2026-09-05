# Antia-Koella-Perrot (1996) within-host mycobacterial model, as restated in Chakraborty, Batabyal & Ganusov 2024

Source: Chakraborty D, Batabyal S, Ganusov VV. "A brief overview of mathematical
modeling of the within-host dynamics of Mycobacterium tuberculosis."
Front Appl Math Stat. 2024;10:1355373. doi:10.3389/fams.2024.1355373
Licence: CC BY 4.0. Quoted below with attribution.

Section: "Deterministic models of within-host Mtb dynamics".
The review attributes the model to reference [33] =
Antia R, Koella JC, Perrot V. "Models of the within-host dynamics of persistent
mycobacterial infections." Proc R Soc Lond B. 1996;263:257-63.
doi:10.1098/rspb.1996.0040 (PMID 8920248).

## Short-term dynamics model (Equations 1-3, verbatim from the VOR)

    dP/dt = rP - hPX - fP + gQ            (1)
    dQ/dt = fP - gQ                       (2)
    dX/dt = a + sX * P/(k+P) - dX         (3)

Variable and parameter definitions, quoted:

> "where P denotes the density of actively replicating pathogen, Q is the
> density of dormant (non-replicating) bacteria, X represents the immune
> response, h is the killing rate of Mtb by the immune response, f and g are
> the rates of dormancy and reactivation of the bacteria, s and d are the rates
> of T cell proliferation and death, a is the rate of production of new T cells
> from the thymus, and k the Mtb density at which the rate of T cell
> proliferation is half-maximal."

## Parameter provenance statement (quoted verbatim, VOR p.4)

> "Parameter values were assumed ad hoc to provide a plausible pathogen and
> immune response dynamics [33, 37, 38]; however, the model predictions were
> not compared to actual experimental data."

where [33] = Antia, Koella & Perrot 1996; [37] = Reibnegger et al. 1989
(Proc Natl Acad Sci 86:2026-30); [38] = Antia, Levin & May 1994
(Am Nat 144:457-72).

## Long-term dynamics model (Equations 4-6): Hayflick-limit T-cell extension

    dx_1/dt = a1/(a2^m + P^m) - s*P/(k+P)*x_1 - d*x_1              (4)
    dx_i/dt = 2s*P/(k+P)*x_{i-1} - s*P/(k+P)*x_i - d*x_i           (5)
    dx_n/dt = 2s*P/(k+P)*x_{n-1} - s*P/(k+P)*x_n - d*x_n           (6)

with X = sum_i^n x_i substituted into Equation 3; x_i is the number of T cells
that have undergone i = 1...n divisions and n is the Hayflick limit after which
T cells stop dividing; a1 is the production of new T cells, m the conversion
coefficient of the function (linear to convex), a2 the half-saturation rate of
the thymus due to the parasite.

Note: Equations 7-9 in the same paper are a different model (Gill et al. 2009 /
McDaniel et al. 2016 plasmid-segregation model of Mtb replication and death),
not part of the Antia lineage.
