# Calculus 3 — TeX notes

Multivariable calculus: vector geometry, vector functions, partial derivatives,
gradients, extrema, multiple integrals, vector fields, and the Green / Stokes / Divergence theorems.

## Layout

```
calc3.tex                                       main document
preamble.tex                                    shared preamble
sections/01-vectors-geometry.tex
sections/02-vector-functions.tex
sections/03-partial-derivatives.tex
sections/04-gradients-directional.tex
sections/05-extrema-lagrange.tex
sections/06-multiple-integrals.tex
sections/07-vector-fields-line-integrals.tex
sections/08-greens-stokes-divergence.tex
build.ps1                                       convenience build script
calc3.pdf                                       rendered output
```

## Build

```powershell
./build.ps1                  # Windows
tectonic calc3.tex           # any platform
latexmk -pdf calc3.tex       # TeX Live / MiKTeX
```
