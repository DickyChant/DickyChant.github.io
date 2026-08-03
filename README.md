# Sitian Qian — research portfolio

A source-first Hugo site for [dickychant.github.io](https://dickychant.github.io/). This version aligns the biographical material with the CERN homepage while replacing the 2021 generated output with a maintainable, responsive portfolio.

## What is here

- An editorial one-page design for research, biography, selected pieces, appointments, education, and contact
- Selected work on CaloTrilogy, Particle Transformer, structured state-space models, quantum machine learning, four CMS analyses, and lepton-collider studies
- A compact combined biography covering Northwestern–Fermilab, UW–Madison and the U.S. CMS LPC, Peking University, and CMS Offline Samples convenership
- Responsive, locally processed images with explicit CERN credits
- Accessible navigation, reduced-motion support, social metadata, and structured person data
- A current GitHub Pages workflow using Hugo 0.164.0

Photon-specific material is intentionally outside this update and can be added as a focused follow-up.

## Local development

Install [Hugo 0.164.0](https://github.com/gohugoio/hugo/releases/tag/v0.164.0) or newer, then run:

    hugo server --buildDrafts

For the production build:

    hugo --gc --minify
    python3 scripts/check_site.py public

The generated public directory is ignored. GitHub Pages builds it from source through [the deployment workflow](.github/workflows/hugo.yaml).

## Editing the site

- Biography, research cards, selected pieces, focus areas, appointments, and education: [data/home.toml](data/home.toml)
- Page structure: [layouts/index.html](layouts/index.html)
- Visual system: [assets/css/main.css](assets/css/main.css)
- Images: [assets/images/](assets/images/)
- Site metadata and profile links: [hugo.toml](hugo.toml)

## Research links

Project descriptions are grounded in their primary records:

- [CaloTrilogy](https://arxiv.org/abs/2606.04165)
- [Particle Transformer](https://proceedings.mlr.press/v162/qu22b.html) and its [reference implementation](https://github.com/jet-universe/particle_transformer)
- [Structured state-space models for high-energy physics](https://proceedings.mlr.press/v258/jiang25c.html)
- [Knowledge distillation for quantum neural networks](https://arxiv.org/abs/2603.21586)
- [Quantum machine learning for a CEPC Higgs study](https://arxiv.org/abs/2209.12788)
- [CMS study of WH production through vector-boson scattering](https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-23-007/)
- [CMS measurement of top-pair production in lead–lead collisions](https://cms-results.web.cern.ch/cms-results/public-results/publications/HIN-24-021/) and its [PbPb jet-tagging performance note](https://cds.cern.ch/record/2915245)
- [CMS search for light pseudoscalars in the four-electron final state](https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-24-031/)
- [CMS search for Majorana neutrinos in vector-boson fusion](https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-21-003/)
- [DELPHI simulation pipeline](https://github.com/delphi-fullDST-edm4hep/delphi-sim-pipeline)
- [Google Scholar profile](https://scholar.google.com/citations?user=D7mhn64AAAAJ)

## Image credits

- Open CMS detector: CERN / CMS Collaboration, from the [CERN article](https://home.cern/first-observation-single-top-quark-production-w-and-z-bosons/)
- CMS HGCAL modules: André David Tinoco Mendes / CERN, © 2025 CERN, [CERN Document Server record 2941188](https://cds.cern.ch/record/2941188)
- Header headshot, event portrait, and trail companion: personal archive

The CERN images are used for informational purposes with attribution under the [CERN terms of use](https://copyright.web.cern.ch/). No CERN endorsement is implied.

## Deployment

After reviewing the local changes, push main and set the repository’s Pages source to **GitHub Actions**. The included workflow builds and deploys the site; no generated HTML needs to be committed.
