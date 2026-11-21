"""Calcoli comuni del ciclo di BTC (usati dallo script dei dati e dalla prova dell'indice di rischio).

Tutto usa solo il passato: medie semplici/esponenziali sulle chiusure settimanali fino a quella settimana,
indice di rischio = percentile tra i valori già visti. Regole dell'indice in dati/REGOLE_RISCHIO.md.
"""
import numpy as np
import pandas as pd

MEDIE = [21, 50, 200, 300, 400]   # settimane


def settimanali(g: pd.DataFrame) -> pd.DataFrame:
    """Giornaliero (colonne t in secondi, o, h, l, c) → settimanale con la settimana che finisce la domenica (UTC)."""
    d = g.copy()
    d.index = pd.to_datetime(d["t"], unit="s")
    w = d.resample("W-SUN").agg({"o": "first", "h": "max", "l": "min", "c": "last"}).dropna()
    ultimo_giorno = d.index[-1]
    w["chiusa"] = w.index <= ultimo_giorno.normalize() if ultimo_giorno.weekday() == 6 else w.index < ultimo_giorno.normalize()
    return w


def percentile_passato(x: pd.Series, minimo: int = 52) -> pd.Series:
    v = x.to_numpy()
    out = np.full(len(v), np.nan)
    visti = []
    for i, a in enumerate(v):
        if np.isnan(a):
            continue
        visti.append(a)
        if len(visti) >= minimo:
            arr = np.asarray(visti)
            out[i] = (arr <= a).mean()
    return pd.Series(out, index=x.index)


def rischio(w: pd.DataFrame) -> pd.DataFrame:
    w = w.copy()
    w["sma200"] = w["c"].rolling(200).mean()
    w["sma50"] = w["c"].rolling(50).mean()
    w["A"] = percentile_passato(np.log(w["c"] / w["sma200"]))
    w["B"] = percentile_passato(np.log(w["c"] / w["sma50"]))
    return w


def indicatori(w: pd.DataFrame) -> pd.DataFrame:
    w = rischio(w)
    for n in MEDIE + [300, 400]:
        w[f"sma{n}"] = w["c"].rolling(n).mean()
    w["sma20"] = w["c"].rolling(20).mean()
    w["ema21"] = w["c"].ewm(span=21, adjust=False).mean()
    w["sopra_medie"] = sum((w["c"] > w[f"sma{n}"]).astype(int) for n in MEDIE)
    w["medie_pronte"] = sum(w[f"sma{n}"].notna().astype(int) for n in MEDIE)
    return w


def fascia_rischio(r: float) -> str:
    if r is None or np.isnan(r):
        return "—"
    return ["Molto basso", "Basso", "Medio", "Alto", "Molto alto"][min(4, int(r * 5))]
