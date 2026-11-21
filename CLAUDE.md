# EllecciStudio-ciclo-btc · CycleDial

App di Luigi (Ellecci Studio) per seguire **il ciclo di Bitcoin** in una pagina. Nata il 21/11/2026 dal video della «Tana della Tartaruga»
(scheda 118 del secondo cervello, `video/2026-11-21-07-tana-tartaruga-btc.md`): Luigi ha chiesto di rifare per sé le sue sezioni su BTC.
Nome e logo provvisori: **CycleDial** (la «C» di Ellecci diventa un quadrante con la lancetta), colore principale azzurro `#5CC8FF`.
Luigi non è uno sviluppatore: spiegagli tutto in italiano semplice. Non invia ordini e non tocca soldi.

## Regole
- Repository **pubblico** (GitHub Pages gratis, minuti di Actions gratis): solo prezzi pubblici, niente dati personali, niente chiavi.
- La sezione «La mia strategia» è stata tolta il 21/11/2026 su richiesta di Luigi; al suo posto **Legge di potenza** (teoria di Giovanni Santostasi, citato per nome:
  è una teoria pubblica): tendenza = 1,0117e-17 × giorni dal 03/01/2009^5,82, supporto = 0,42 × tendenza (valori come pubblicati, riportati da bgeometrics);
  la linea «× 2,5» è dei siti che la usano, non sua. Le prove di stabilità (esponente con altre date d'inizio e con i soli dati fino a una data) le calcola `potenza()` in `dati.py`.
  Al 15/11/2026 il prezzo è sotto il supporto (0,41 × tendenza, minimo di sempre 0,40 il 14/11): prima solo 2 giorni nel 2015 e 2 a giugno 2026.
- Nell'app non si nomina la fonte del video (né «Tartaruga» né il suo autore): l'idea è sua, le regole e i calcoli sono nostri e dichiarati.
- Nessuna formula segreta: ogni indicatore ha la regola scritta nella pagina. L'indice di rischio segue `dati/REGOLE_RISCHIO.md`
  (decise prima dei risultati, varianti A/B/C, nessuna informazione futura). **Non cambiare le regole dopo aver visto i risultati**: una versione nuova
  si aggiunge come variante in più, si prova da zero e si mostra insieme alle altre.
- Esito della prova (21/11/2026): nessuna variante passa. La fascia bassa funziona (rischio < 0,2 → un anno dopo in guadagno 95 volte su 100,
  mediana +121% contro +56%), la fascia alta no (sopra 0,8 mediana +146%). L'app lo dice chiaramente: utile per i prezzi bassi, non per vendere.
- Stile: kit Ellecci (`DESIGN.md` degli altri progetti, skill `ellecci-design-system`), due temi come le altre app: `vetro` scuro predefinito
  e `chiaro`; scelta in `localStorage` `cd_tema`. Dal 21/11/2026 stile delle ultime app («quadrante a marea»): luce azzurra che respira dietro il quadrante
  (`body::before`, animazione `cdRespiro`) + riflesso viola in basso (`body::after`), scheda principale `.scheda.vetro` in vetro colorato azzurro, le altre schede
  smerigliate con un filo azzurro sul bordo alto, numeri eroe Unbounded 600 (spessi, regola di DESIGN.md). Sul computer l'app riempie la finestra (niente colonna stretta; sopra 1600 px i blocchi si allargano); sul telefono la tabella delle previsioni diventa a schede. Movimento «da dashboard», niente doppio asse nei grafici.
- Online: https://elleccistudio.github.io/EllecciStudio-ciclo-btc/ (GitHub Pages dal ramo `main`, attivato da Luigi il 21/11/2026).

- **Cicli** (21/11/2026, dal video 119 e dai grafici di Bitbo): cicli sovrapposti per giorni dall'halving (prezzo ÷ minimo dei 2 anni prima dell'halving; halving 2028
  stimato al 17/04/2028 in `HALVING`), ripetizione del ciclo di 4 anni fa (1.458 giorni, moltiplicato per partire da oggi; prova: stesso segno dell'anno dopo 82%
  contro 52% della controprova), rendimenti mensili, settimane rosse di fila (solo settimane chiuse). Calcoli in `cicli()` di `dati.py`.

## Dove sono le cose
- `index.html`: tutta l'app (HTML, CSS, JS), grafici con `lib/chart.umd.js` (Chart.js 4.4.1 locale). Pagine con l'hash: `#oggi`, `#rischio`, `#medie`, `#interesse`, `#cicli`, `#potenza`.
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
