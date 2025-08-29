
from __future__ import annotations
import os, sys
import pandas as pd

def _read_table(path: str, **kwargs) -> pd.DataFrame:
    """Thin wrapper over pandas.read_csv that treats consecutive whitespace as a single delimiter; supports .gz and http(s)."""
    # Allow caller to override the separator while defaulting to whitespace
    sep = kwargs.pop("sep", r"\s+")
    return pd.read_csv(path, sep=sep, engine="python", **kwargs)

def read_pairs_table(fp: str) -> pd.DataFrame:
    """
    Read PLINK .genome or KING .kin0 and normalize to columns:
      IID1, IID2, PI_HAT, Z1  (Z1 may be 0 if absent).
    """
    # Allow URLs and local files; only error if it's a local path that doesn't exist
    if not (fp.startswith("http://") or fp.startswith("https://")) and not os.path.exists(fp):
        sys.exit(f"[ERROR] genome/kinship file not found: {fp}")
    df = _read_table(fp, sep=r"\s+", dtype=str)
    cols = set(df.columns)

    # PLINK .genome
    if {"IID1","IID2","PI_HAT"}.issubset(cols):
        out = df.copy()
        out["PI_HAT"] = out["PI_HAT"].astype(float)
        out["Z1"] = out["Z1"].astype(float) if "Z1" in cols else 0.0
        return out[["IID1","IID2","PI_HAT","Z1"]]

    # KING .kin0 (ID1/ID2/Kinship)
    if {"ID1","ID2","Kinship"}.issubset(cols):
        out = df.rename(columns={"ID1":"IID1","ID2":"IID2"}).copy()
        out["PI_HAT"] = out["Kinship"].astype(float) * 2.0  # PI_HAT ≈ 2*Kinship
        out["Z1"] = 0.0  # KING lacks Z1
        return out[["IID1","IID2","PI_HAT","Z1"]]

    sys.exit("[ERROR] Unrecognized pairs file; expected PLINK .genome (IID1 IID2 PI_HAT [Z1]) or KING .kin0 (ID1 ID2 Kinship).")

def read_haplogroups(fp: str):
    """Read two-column file: <sample><tab><haplogroup> (no header). Returns Series index=sample."""
    s = pd.read_csv(fp, sep=None, engine="python", header=None, usecols=[0,1], names=["sample","hg"], dtype=str)
    s["sample"] = s["sample"].astype(str).str.strip()
    s["hg"] = s["hg"].astype(str).str.strip()
    return s.set_index("sample")["hg"]

def read_samplesheet(fp: str) -> pd.DataFrame:
    """Read a samplesheet that must contain a 'sample_id' column; trims whitespace for object columns."""
    df = pd.read_csv(fp, sep=None, engine="python", dtype=str)
    if "sample_id" not in df.columns:
        raise ValueError("samplesheet must contain column 'sample_id'")
    return df.apply(lambda c: c.str.strip() if c.dtype == "object" else c)
