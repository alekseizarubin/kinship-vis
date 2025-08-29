
# kinship-vis

Visualize pairwise kinship results (PLINK `.genome` or KING `.kin0`) as component graphs with:
- Static PNG/TIFF **(Matplotlib)** — edges colored by kinship class, nodes filled by MT haplogroup and outlined by Y haplogroup.
- Interactive HTML **(Plotly)** — same color scheme, hover tooltips, optional legend including haplogroups.

## Installation
```bash
pip install kinship-vis
```

## Quick start
```bash
kinship-vis results.genome \
  --samplesheet samples.tsv --label-col short_id \
  --haplogroup-Y y_hg.tsv \
  --haplogroup-MT mt_hg.tsv \
  --output out/kinship --legend
```

Input tips:
- **PLINK .genome** must have `IID1 IID2 PI_HAT [Z1]`.
- **KING .kin0** with columns `ID1 ID2 Kinship` is supported; `PI_HAT` is computed as `2*Kinship` (Z1 is absent).
- **Samplesheet** (optional) can be TSV, CSV, or whitespace-delimited; a `sample_id` column is required and the delimiter is auto-detected.

## Haplogroup overlays (optional)

You can color nodes by mitochondrial (MT) haplogroup (node fill) and Y-chromosome haplogroup (node border).
Provide **two simple two-column TSV files without header**:

- `y_hg.hg` — `sample<TAB>Y_haplogroup`
- `mt_hg.txt` — `sample<TAB>MT_haplogroup`

The first column must match the sample IDs used in `IID1/IID2`. Delimiters (tab/space/comma) are auto-detected.

Example usage:
```bash
kinship-vis results.genome \
  --samplesheet samples.tsv --label-col short_id \
  --haplogroup-Y y_hg.hg \
  --haplogroup-MT mt_hg.txt \
  --output out/kinship --legend  # adds legend for edges and haplogroups
```

### How to obtain haplogroups (suggested tools)
- **MT haplogroups:** *HaploGrep* (CLI or web). Export a mapping `sample \t haplogroup`.
- **Y haplogroups:** *Y-LineageTracker* (`classify` subcommand) from WGS/VCF. Export `sample \t haplogroup`.

> Tip: Keep the two-column TSV without header so the reader can parse it directly.

See `kinship_vis/cli.py` for all options.
