"""Prova dell'indice di rischio (regole in dati/REGOLE_RISCHIO.md). Uso: python strumenti/prova_rischio.py"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from calcoli import settimanali, rischio  # noqa: E402

BASE = Path(__file__).resolve().parents[1]
FASCE = [0, 0.2, 0.4, 0.6, 0.8, 1.0001]
NOMI = ["0-0,2", "0,2-0,4", "0,4-0,6", "0,6-0,8", "0,8-1"]


def tabella(df, col, h):
    fut = df["c"].shift(-h) / df["c"] - 1
    d = pd.DataFrame({"r": df[col], "f": fut}).dropna()
    righe = []
    for i, nome in enumerate(NOMI):
        s = d[(d.r >= FASCE[i]) & (d.r < FASCE[i + 1])]["f"]
        righe.append({"fascia": nome, "settimane": int(len(s)),
                      "mediana_pct": round(float(s.median()) * 100, 1) if len(s) else None,
                      "media_pct": round(float(s.mean()) * 100, 1) if len(s) else None,
                      "positivi_pct": round(float((s > 0).mean()) * 100, 0) if len(s) else None})
    tutte = d["f"]
    righe.append({"fascia": "tutte (controprova)", "settimane": int(len(tutte)),
                  "mediana_pct": round(float(tutte.median()) * 100, 1), "media_pct": round(float(tutte.mean()) * 100, 1),
                  "positivi_pct": round(float((tutte > 0).mean()) * 100, 0)})
    return righe


def giudizio(t):
    med = [r["mediana_pct"] for r in t[:5]]
    tutte = t[5]["mediana_pct"]
    ok1 = med[0] is not None and med[4] is not None and med[0] > tutte and med[4] < tutte
    validi = [m for m in med if m is not None]
    inversioni = sum(1 for a, b in zip(validi, validi[1:]) if b > a)
    return ok1, inversioni


def main():
    g = pd.read_csv(BASE / "dati/bitstamp_btcusd_1d.csv")
    w = settimanali(g)
    w = rischio(w)
    w["C"] = (w["A"] + w["B"]) / 2
    out = {}
    for col in ["A", "B", "C"]:
        out[col] = {}
        for h in (26, 52):
            out[col][str(h)] = tabella(w, col, h)
        ok1, inv = giudizio(out[col]["52"])
        meta = {}
        for nome, parte in (("prima_2021", w[w.index < "2021-01-01"]), ("dal_2021", w[w.index >= "2021-01-01"])):
            # il rendimento futuro usa i prezzi interi: si taglia solo il punto di partenza
            fut = w["c"].shift(-52) / w["c"] - 1
            sub = w.loc[parte.index].assign(f=fut.loc[parte.index])
            d = pd.DataFrame({"r": sub[col], "f": sub["f"]}).dropna()
            basso = d[d.r < 0.2]["f"].median()
            alto = d[d.r >= 0.8]["f"].median()
            meta[nome] = {"mediana_basso_pct": None if np.isnan(basso) else round(basso * 100, 1),
                          "mediana_alto_pct": None if np.isnan(alto) else round(alto * 100, 1),
                          "mediana_tutte_pct": round(d["f"].median() * 100, 1),
                          "settimane_basso": int((d.r < 0.2).sum()), "settimane_alto": int((d.r >= 0.8).sum())}
        ok3 = all(m["mediana_basso_pct"] is not None and m["mediana_basso_pct"] > m["mediana_tutte_pct"]
                  and (m["mediana_alto_pct"] is None or m["mediana_alto_pct"] < m["mediana_tutte_pct"]) for m in meta.values())
        out[col]["meta"] = meta
        out[col]["esito"] = {"cond1": ok1, "inversioni": inv, "cond2": inv <= 1, "cond3": ok3,
                             "funziona": bool(ok1 and inv <= 1 and ok3)}
    out["ultimo"] = {"settimana": str(w.index[-1].date()), "prezzo": round(float(w["c"].iloc[-1]), 2),
                     **{k: round(float(w[k].iloc[-1]), 3) for k in ["A", "B", "C"]}}
    (BASE / "dati/prova_rischio.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for col in ["A", "B", "C"]:
        print("== variante", col, out[col]["esito"])
        for r in out[col]["52"]:
            print("  52 sett.", r)
        print("  metà:", out[col]["meta"])
    print("ultimo:", out["ultimo"])


if __name__ == "__main__":
    main()
