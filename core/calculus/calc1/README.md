# Calculus 1 — TeX notes

Single-variable calculus cheat sheet built from modular `.tex` sources.

## Layout

```
calc1.tex                 main document
preamble.tex              shared preamble (packages, theorems, macros)
sections/01-limits.tex
sections/02-continuity.tex
sections/03-derivatives.tex
sections/04-differentiation-rules.tex
sections/05-applications-derivatives.tex
sections/06-integrals.tex
sections/07-techniques-integration.tex
sections/08-applications-integrals.tex
build.ps1                 convenience build script (Windows / PowerShell)
calc1.pdf                 rendered output (regenerate with build.ps1)
```

## Build

The PDF is produced with [Tectonic](https://tectonic-typesetting.github.io/), a single-binary
LaTeX engine that auto-fetches packages on first run.

```powershell
# Windows / PowerShell
./build.ps1
```

```bash
# Any platform, if tectonic is on PATH
tectonic calc1.tex
```

Any TeX Live / MiKTeX install also works:

```bash
latexmk -pdf calc1.tex
```
