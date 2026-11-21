# EllecciStudio-ciclo-btc · CycleDial

App di Luigi (Ellecci Studio) per seguire **il ciclo di Bitcoin** in una pagina. Nata il 21/11/2026 da un video analizzato nel secondo cervello (scheda 118; le fonti delle altre parti: schede 119, 120 e 121).
Nome e logo provvisori: **CycleDial** (la «C» di Ellecci diventa un quadrante con la lancetta), colore principale azzurro `#5CC8FF`.
Luigi non è uno sviluppatore: spiegagli tutto in italiano semplice. Non invia ordini e non tocca soldi.

## Regole
- Repository **pubblico** (GitHub Pages gratis, minuti di Actions gratis): solo prezzi pubblici, niente dati personali, niente chiavi.
- La sezione «La mia strategia» è stata tolta il 21/11/2026 su richiesta di Luigi; al suo posto **Legge di potenza**: tendenza = 1,0117e-17 × giorni dal 03/01/2009^5,82, supporto = 0,42 × tendenza (valori come pubblicati dall'autore della teoria);
  la linea «× 2,5» è un tetto indicativo di alcuni siti, non fa parte della teoria. Le prove di stabilità (esponente con altre date d'inizio e con i soli dati fino a una data) le calcola `potenza()` in `dati.py`.
  Al 15/11/2026 il prezzo è sotto il supporto (0,41 × tendenza, minimo di sempre 0,40 il 14/11): prima solo 2 giorni nel 2015 e 2 a giugno 2026.
- **Nell'app (e in questo repository pubblico) non si nomina nessuno** (regola di Luigi, ribadita il 21/11/2026): né le persone né i video, le live o i siti
  da cui sono nate le idee, nemmeno l'autore della legge di potenza. Nei testi dell'app nemmeno i fornitori dei dati: si scrive «dati di mercato pubblici»,
  «chiusura giornaliera», «prezzo di adesso» (i nomi restano solo negli indirizzi e nei commenti tecnici di `dati.py`, dove servono per funzionare).
  I nomi stanno solo nelle schede del secondo cervello. Prima di ogni push cerca nel codice nomi di persone, canali, video, live e siti.
- Nessuna formula segreta: ogni indicatore ha la regola scritta nella pagina. L'indice di rischio segue `dati/REGOLE_RISCHIO.md`
  (decise prima dei risultati, varianti A/B/C, nessuna informazione futura). **Non cambiare le regole dopo aver visto i risultati**: una versione nuova
  si aggiunge come variante in più, si prova da zero e si mostra insieme alle altre.
- Esito della prova (21/11/2026): nessuna variante passa. La fascia bassa funziona (rischio < 0,2 → un anno dopo in guadagno 95 volte su 100,
  mediana +121% contro +56%), la fascia alta no (sopra 0,8 mediana +146%). L'app lo dice chiaramente: utile per i prezzi bassi, non per vendere.
- Stile: kit Ellecci (`DESIGN.md` degli altri progetti, skill `ellecci-design-system`), due temi come le altre app: `vetro` scuro predefinito
  e `chiaro`; scelta in `localStorage` `cd_tema`. Dal 21/11/2026 sera **Kit Ellecci 2** (prima app a riceverlo, `DESIGN.md` > Kit Ellecci 2): fondo quasi nero tinto `#080C0E` con grana finissima ferma (`body::before`), niente luci né aloni, fascia azzurra in cima con la C fatta di archi (`.banda`: sfumatura di un solo colore; una C grande fatta di 8 archi concentrici sottili aperti a destra, due più spessi, quelli esterni che si assottigliano, a destra della fascia e sfumata verso il basso: Luigi ha scartato la versione piccola) e vetro solo sulle schede del primo blocco sopra la fascia e sulla pillola del telefono, schede piene con bordo 1px, etichette e intestazioni in testo normale, niente scritte sopra i titoli, niente puntini «·» né frecce «›» nei testi (link con un verbo: «Apri lo storico»), chip con angoli da 6 px, le quattro tessere di Oggi come colonne aperte sotto un filetto, numero eroe più grande (fino a 4,4rem), il quadrante come «arco della C». Movimento «da dashboard» **ogni volta che si apre una sezione** (regola del 16/11/2026 di tutte le app; corretto il 21/11/2026: prima partiva solo la prima volta): `mostra()` ridisegna la pagina, `contaTutti()` fa contare i numeri, `graficiQuandoVisibili()` fa costruire i grafici quando arrivano sullo schermo, `cascata()` fa entrare le schede; il prezzo di adesso scorre dalla chiusura con un lampo verde/rosso; solo le schede cliccabili reagiscono al mouse; il tema cambia con il cerchio dal pulsante. Sul computer la barra in alto resta fissa: un rettangolo di vetro trasparente su tutta la larghezza (logo a sinistra, tema a destra) e l'isola delle sezioni al centro, che quando la pagina scorre diventa anche lei un po' trasparente (classe `scorre` su `header.testa` e `nav.menu`). Sul telefono c'è la pillola fissa in basso. Nelle schede di vetro sopra la fascia (tema scuro) le scritte secondarie e i numeri degli assi diventano bianco attenuato (`sulVetro()`) per il contrasto. Il cerchio del cambio sezione parte dal centro della C ed è lento (1,1 s) per far vedere da dove nasce; la C (estremità squadrate) si vede attenuata anche dietro le schede di vetro (sfocatura 8 px; nel tema chiaro vetro bianco al 36%): sul computer l’arco spesso si vede tutto, in parte dietro la scheda dell’indice di rischio. Niente doppio asse nei grafici.
- Online: https://elleccistudio.github.io/EllecciStudio-ciclo-btc/ (GitHub Pages dal ramo `main`, attivato da Luigi il 21/11/2026).

- **Cicli** (21/11/2026, idea dalla scheda 119): cicli sovrapposti per giorni dall'halving (prezzo ÷ minimo dei 2 anni prima dell'halving; halving 2028
  stimato al 17/04/2028 in `HALVING`), ripetizione del ciclo di 4 anni fa (1.458 giorni, moltiplicato per partire da oggi; prova: stesso segno dell'anno dopo 82%
  contro 52% della controprova), rendimenti mensili, settimane rosse di fila (solo settimane chiuse). Calcoli in `cicli()` di `dati.py`.

## Dove sono le cose
- `index.html`: tutta l'app (HTML, CSS, JS), grafici con `lib/chart.umd.js` (Chart.js 4.4.1 locale). Pagine con l'hash: `#oggi`, `#rischio`, `#medie`, `#interesse`, `#cicli`, `#potenza`.
- `manifest.webmanifest` + `assets/icona-180/192/512.png` (logo Ellecci Studio, come le altre app): nome «CycleDial · Ellecci Studio» quando la si installa sul computer o sul telefono.
- `calcoli.py`: chiusure settimanali (domenica UTC), medie, indice di rischio (percentile solo sul passato).
- `dati.py`: scarica Bitstamp (aggiorna `dati/bitstamp_btcusd_1d.csv`, solo giorni chiusi), alternative.me (paura e avidità), calendario della settimana
  (nfs.faireconomy.media, solo USA importanza alta/media, titoli tradotti in `TRADUZIONI`) e scrive `dati/ciclo.json`. Se una fonte non risponde tiene il dato di prima.
  `--senza-rete` per provare in locale. La banda del bot (110 giorni, 2,5%) è ricalcolata dai prezzi: lo stato vero resta quello di BandPilot.
- `strumenti/prova_rischio.py`: prova dell'indice → `dati/prova_rischio.json` (letto da `dati.py`).
- `.github/workflows/dati.yml`: ogni giorno 01:23 UTC (riserva 07:47) su `ubuntu-latest` + a ogni modifica dei calcoli; fa commit su `main` dei soli dati.
- Prezzo «adesso»: chiesto dal browser a Binance (riserva Coinbase); se non risponde si mostra la chiusura giornaliera (nella pagina senza nomi).

## Collaudo
Playwright a 390 e 1440 px, temi scuro e chiaro, tutte e 5 le pagine: niente errori in console, niente scorrimento orizzontale.
Dalla sessione cloud Bitstamp, alternative.me e il calendario sono bloccati: si prova con `--senza-rete` e dati finti solo nel collaudo.
