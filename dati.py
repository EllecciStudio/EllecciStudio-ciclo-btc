"""Aggiorna i dati dell'app (dati/ciclo.json). Gira ogni giorno con GitHub Actions; in locale: python dati.py [--senza-rete]

Fonti gratuite: Bitstamp (BTC/USD giornaliero dal 2011), alternative.me (indice paura e avidità), calendario economico
della settimana (nfs.faireconomy.media). Se una fonte non risponde, si tiene il dato di prima e l'app lo dice.
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import requests

from calcoli import MEDIE, fascia_rischio, indicatori, settimanali

BASE = Path(__file__).resolve().parent
CSV = BASE / "dati/bitstamp_btcusd_1d.csv"
USCITA = BASE / "dati/ciclo.json"
ROMA = ZoneInfo("Europe/Rome")
SENZA_RETE = "--senza-rete" in sys.argv
BOT_MEDIA, BOT_BANDA = 110, 0.025   # regole del bot Con banda (bot/impostazioni.json del repository del bot)


def _get(url, params=None, tentativi=4):
    for k in range(tentativi):
        try:
            r = requests.get(url, params=params, timeout=30, headers={"User-Agent": "Mozilla/5.0 (EllecciStudio ciclo-btc)"})
            if r.status_code == 200:
                return r.json()
            print("risposta", r.status_code, url, r.text[:200])
        except requests.RequestException as e:
            print("errore di rete", url, e)
        time.sleep(2 + 3 * k)
    return None


def prezzi():
    vecchio = pd.read_csv(CSV)
    righe = vecchio.to_dict("records")
    inizio = int(vecchio["t"].iloc[-1]) + 86400
    oggi = int(datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    while not SENZA_RETE and inizio < oggi:
        j = _get("https://www.bitstamp.net/api/v2/ohlc/btcusd/", {"step": 86400, "limit": 1000, "start": inizio})
        blocco = (j or {}).get("data", {}).get("ohlc", [])
        if not blocco:
            break
        for x in blocco:
            righe.append({"t": int(x["timestamp"]), "o": float(x["open"]), "h": float(x["high"]),
                          "l": float(x["low"]), "c": float(x["close"])})
        inizio = int(blocco[-1]["timestamp"]) + 86400
        time.sleep(0.4)
    df = pd.DataFrame(righe).drop_duplicates("t", keep="last").sort_values("t")
    df = df[df["t"] < oggi]                    # solo giorni chiusi
    df.to_csv(CSV, index=False)
    return df


def paura_avidita(precedente):
    if SENZA_RETE:
        return precedente
    j = _get("https://api.alternative.me/fng/", {"limit": 0})
    if not j or not j.get("data"):
        return precedente
    d = sorted(((int(x["timestamp"]), int(x["value"])) for x in j["data"]))
    return {"t": [datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d") for t, _ in d], "v": [v for _, v in d]}


TRADUZIONI = {
    "CPI m/m": "Inflazione (CPI) mese su mese", "CPI y/y": "Inflazione (CPI) anno su anno",
    "Core CPI m/m": "Inflazione di fondo (CPI core) mese su mese", "Core CPI y/y": "Inflazione di fondo (CPI core) anno su anno",
    "PPI m/m": "Prezzi alla produzione (PPI)", "Core PPI m/m": "Prezzi alla produzione di fondo (PPI core)",
    "Non-Farm Employment Change": "Nuovi posti di lavoro (non agricoli)", "Unemployment Rate": "Tasso di disoccupazione",
    "Average Hourly Earnings m/m": "Salari orari medi", "Unemployment Claims": "Richieste di sussidio di disoccupazione",
    "ADP Non-Farm Employment Change": "Nuovi posti di lavoro privati (ADP)", "JOLTS Job Openings": "Posti di lavoro vacanti (JOLTS)",
    "Federal Funds Rate": "Decisione sui tassi della Fed", "FOMC Statement": "Comunicato della Fed (FOMC)",
    "FOMC Press Conference": "Conferenza stampa della Fed", "FOMC Meeting Minutes": "Verbali della riunione Fed",
    "Fed Chair Powell Speaks": "Discorso del presidente della Fed", "Fed Chair Speaks": "Discorso del presidente della Fed",
    "Advance GDP q/q": "PIL trimestrale (prima stima)", "Prelim GDP q/q": "PIL trimestrale (seconda stima)", "Final GDP q/q": "PIL trimestrale (stima finale)",
    "Core PCE Price Index m/m": "Inflazione PCE di fondo", "PCE Price Index m/m": "Inflazione PCE",
    "Retail Sales m/m": "Vendite al dettaglio", "Core Retail Sales m/m": "Vendite al dettaglio di fondo",
    "ISM Manufacturing PMI": "Indice ISM manifatturiero", "ISM Services PMI": "Indice ISM servizi",
    "Flash Manufacturing PMI": "PMI manifatturiero (stima)", "Flash Services PMI": "PMI servizi (stima)",
    "Prelim UoM Consumer Sentiment": "Sentiment consumatori USA (Michigan, stima)", "Revised UoM Consumer Sentiment": "Sentiment consumatori USA (Michigan, finale)",
    "Prelim UoM Inflation Expectations": "Attese di inflazione (Michigan, stima)", "Revised UoM Inflation Expectations": "Attese di inflazione (Michigan, finale)",
    "CB Consumer Confidence": "Fiducia dei consumatori (Conference Board)", "Durable Goods Orders m/m": "Ordini di beni durevoli",
    "Core Durable Goods Orders m/m": "Ordini di beni durevoli di fondo", "Pending Home Sales m/m": "Vendite di case in corso",
    "Existing Home Sales": "Vendite di case esistenti", "New Home Sales": "Vendite di case nuove", "Building Permits": "Permessi di costruzione",
    "Empire State Manufacturing Index": "Indice manifatturiero di New York", "Philly Fed Manufacturing Index": "Indice manifatturiero di Philadelphia",
    "Trade Balance": "Bilancia commerciale", "Bank Holiday": "Festa: mercati USA chiusi",
}
GIORNI = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]


def calendario(precedente):
    if SENZA_RETE:
        return precedente
    j = _get("https://nfs.faireconomy.media/ff_calendar_thisweek.json")
    if not isinstance(j, list):
        return precedente
    eventi = []
    for x in j:
        if x.get("country") != "USD" or x.get("impact") not in ("High", "Medium"):
            continue
        try:
            quando = datetime.fromisoformat(x["date"]).astimezone(ROMA)
        except (KeyError, ValueError):
            continue
        titolo = x.get("title", "")
        eventi.append({"quando": quando.isoformat(), "giorno": GIORNI[quando.weekday()], "ora": quando.strftime("%H:%M"),
                       "titolo": TRADUZIONI.get(titolo, titolo), "originale": titolo,
                       "importanza": "alta" if x["impact"] == "High" else "media",
                       "previsto": x.get("forecast") or "", "precedente": x.get("previous") or ""})
    return {"aggiornato": datetime.now(ROMA).isoformat(timespec="minutes"), "eventi": sorted(eventi, key=lambda e: e["quando"])}


def stato_bot(c: pd.Series):
    """Rifà le regole del bot Con banda su tutto lo storico: dentro sopra la banda alta, fuori sotto la banda bassa."""
    m = c.rolling(BOT_MEDIA).mean()
    dentro, serie = False, []
    for p, media in zip(c.to_numpy(), m.to_numpy()):
        if not np.isnan(media):
            if not dentro and p > media * (1 + BOT_BANDA):
                dentro = True
            elif dentro and p < media * (1 - BOT_BANDA):
                dentro = False
        serie.append(dentro)
    return m, pd.Series(serie, index=c.index)


def r(x, n=2):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


def main():
    precedente = json.loads(USCITA.read_text()) if USCITA.exists() else {}
    g = prezzi()
    w = indicatori(settimanali(g))
    d = g.copy()
    d.index = pd.to_datetime(d["t"], unit="s")
    for n in MEDIE:
        d[f"sma{n}"] = d["c"].rolling(n).mean()
    d["sopra"] = sum((d["c"] > d[f"sma{n}"]).astype(int) for n in MEDIE)
    d["media_bot"], d["bot_dentro"] = stato_bot(d["c"])

    chiuse = w[w["chiusa"]]
    u, ud = chiuse.iloc[-1], d.iloc[-1]
    sett = w[w.index >= "2013-01-01"]
    giorni = d[d.index >= "2023-01-01"]
    prova = json.loads((BASE / "dati/prova_rischio.json").read_text())

    out = {
        "aggiornato": datetime.now(ROMA).isoformat(timespec="minutes"),
        "ultimo_giorno": str(d.index[-1].date()),
        "ultima_settimana": str(chiuse.index[-1].date()),
        "oggi": {
            "prezzo": r(ud.c), "rischio": r(u.A, 3), "rischio_fascia": fascia_rischio(u.A),
            "sma200w": r(u.sma200), "sma300w": r(u.sma300), "sma400w": r(u.sma400),
            "sotto_sma200w": bool(u.c < u.sma200),
            "sopra_medie": int(ud.sopra), "medie": {str(n): r(ud[f"sma{n}"]) for n in MEDIE},
            "bot_dentro": bool(ud.bot_dentro), "media_bot": r(ud.media_bot),
            "banda_alta": r(ud.media_bot * (1 + BOT_BANDA)), "banda_bassa": r(ud.media_bot * (1 - BOT_BANDA)),
        },
        "settimanale": {
            "t": [str(x.date()) for x in sett.index], "c": [r(x) for x in sett.c],
            "sma200": [r(x) for x in sett.sma200], "sma300": [r(x) for x in sett.sma300], "sma400": [r(x) for x in sett.sma400],
            "rischio": [r(x, 3) for x in sett.A], "chiusa": [bool(x) for x in sett.chiusa],
        },
        "giornaliero": {
            "t": [str(x.date()) for x in giorni.index], "c": [r(x) for x in giorni.c],
            **{f"sma{n}": [r(x) for x in giorni[f"sma{n}"]] for n in MEDIE},
            "media_bot": [r(x) for x in giorni.media_bot], "bot_dentro": [bool(x) for x in giorni.bot_dentro],
        },
        "bot": {"media_giorni": BOT_MEDIA, "banda": BOT_BANDA},
        "prova_rischio": prova,
        "paura_avidita": paura_avidita(precedente.get("paura_avidita")),
        "calendario": calendario(precedente.get("calendario")),
    }
    USCITA.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print("ok", out["ultimo_giorno"], out["oggi"], "kB", USCITA.stat().st_size // 1024)


if __name__ == "__main__":
    main()
