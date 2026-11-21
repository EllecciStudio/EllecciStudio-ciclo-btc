# EllecciStudio-ciclo-btc · CycleDial

App di Luigi (Ellecci Studio) per seguire **il ciclo di Bitcoin** in una pagina. Nata il 21/11/2026 dal video della «Tana della Tartaruga»
(scheda 118 del secondo cervello, `video/2026-11-21-07-tana-tartaruga-btc.md`): Luigi ha chiesto di rifare per sé le sue sezioni su BTC.
Nome e logo provvisori: **CycleDial** (la «C» di Ellecci diventa un quadrante con la lancetta), colore principale azzurro `#5CC8FF`.
Luigi non è uno sviluppatore: spiegagli tutto in italiano semplice. Non invia ordini e non tocca soldi.

## Regole
- Repository **pubblico** (GitHub Pages gratis, minuti di Actions gratis): solo prezzi pubblici, niente dati personali, niente chiavi.
  «La mia strategia» si salva solo nel browser (`localStorage` `cd_strategia`); le regole di partenza nel codice sono quelle del bot, senza importi.
- Nell'app non si nomina la fonte del video (né «Tartaruga» né il suo autore): l'idea è sua, le regole e i calcoli sono nostri e dichiarati.
- Nessuna formula segreta: ogni indicatore ha la regola scritta nella pagina. L'indice di rischio segue `dati/REGOLE_RISCHIO.md`
  (decise prima dei risultati, varianti A/B/C, nessuna informazione futura). **Non cambiare le regole dopo aver visto i risultati**: una versione nuova
  si aggiunge come variante in più, si prova da zero e si mostra insieme alle altre.
- Esito della prova (21/11/2026): nessuna variante passa. La fascia bassa funziona (rischio < 0,2 → un anno dopo in guadagno 95 volte su 100,
  mediana +121% contro +56%), la fascia alta no (sopra 0,8 mediana +146%). L'app lo dice chiaramente: utile per i prezzi bassi, non per vendere.
- Stile: kit Ellecci (`DESIGN.md` degli altri progetti, skill `ellecci-design-system`), due temi come le altre app: `vetro` scuro predefinito
  (luce «marea» azzurra che sale dal basso) e `chiaro`; scelta in `localStorage` `cd_tema`. Movimento «da dashboard», niente doppio asse nei grafici.

## Dove sono le cose
- `index.html`: tutta l'app (HTML, CSS, JS), grafici con `lib/chart.umd.js` (Chart.js 4.4.1 locale). Pagine con l'hash: `#oggi`, `#rischio`, `#medie`, `#interesse`, `#strategia`.
- `calcoli.py`: chiusure settimanali (domenica UTC), medie, indice di rischio (percentile solo sul passato).
- `dati.py`: scarica Bitstamp (aggiorna `dati/bitstamp_btcusd_1d.csv`, solo giorni chiusi), alternative.me (paura e avidità), calendario della settimana
  (nfs.faireconomy.media, solo USA importanza alta/media, titoli tradotti in `TRADUZIONI`) e scrive `dati/ciclo.json`. Se una fonte non risponde tiene il dato di prima.
  `--senza-rete` per provare in locale. La banda del bot (110 giorni, 2,5%) è ricalcolata dai prezzi: lo stato vero resta quello di BandPilot.
- `strumenti/prova_rischio.py`: prova dell'indice → `dati/prova_rischio.json` (letto da `dati.py`).
- `.github/workflows/dati.yml`: ogni giorno 01:23 UTC (riserva 07:47) su `ubuntu-latest` + a ogni modifica dei calcoli; fa commit su `main` dei soli dati.
- Prezzo «adesso»: chiesto dal browser a Binance (riserva Coinbase); se non risponde si mostra la chiusura di Bitstamp.

## Collaudo
Playwright a 390 e 1440 px, temi scuro e chiaro, tutte e 5 le pagine: niente errori in console, niente scorrimento orizzontale.
Dalla sessione cloud Bitstamp, alternative.me e il calendario sono bloccati: si prova con `--senza-rete` e dati finti solo nel collaudo.
