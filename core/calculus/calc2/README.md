# Calculus 2 — TeX notes

Sequences, series, power series, polar/parametric curves, and first-order ODEs.

## Layout

```
calc2.tex                            main document
preamble.tex                         shared preamble
sections/01-sequences.tex
sections/02-series.tex
sections/03-convergence-tests.tex
sections/04-power-series.tex
sections/05-taylor-series.tex
sections/06-parametric.tex
sections/07-polar.tex
sections/08-odes.tex
build.ps1                            convenience build script
calc2.pdf                            rendered output
```

## Build

```powershell
./build.ps1                  # Windows
tectonic calc2.tex           # any platform
latexmk -pdf calc2.tex       # TeX Live / MiKTeX
```
