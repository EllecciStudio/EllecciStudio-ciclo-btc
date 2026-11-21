# Indice di rischio: regole decise prima di vedere i risultati (21/11/2026)

Dati: BTC/USD giornaliero Bitstamp dal 18/08/2011, chiusure settimanali (settimana che finisce la domenica, ora UTC).

Varianti (tutte mostrate nel risultato, nessuna esclusa):
- **A (principale)**: x = ln(chiusura settimanale / media semplice 200 settimane). Rischio = percentile di x tra tutti i valori
  di x fino a quella settimana compresa (solo passato). Prima di avere 52 valori di x l'indice non c'è.
- **B**: come A ma con la media semplice a 50 settimane.
- **C**: media di A e B.

Prova: per ogni settimana, rendimento del prezzo nelle 26 e 52 settimane dopo; si raggruppa per fasce di rischio
(0-0,2 · 0,2-0,4 · 0,4-0,6 · 0,6-0,8 · 0,8-1). Controprova: tutte le settimane insieme (comprare in un giorno qualsiasi).
Si guarda anche la tenuta nelle due metà (prima e dopo il 01/01/2021).

L'indice «funziona» se:
1. il rendimento mediano a 52 settimane della fascia 0-0,2 è più alto di quello di tutte le settimane, e quello della fascia 0,8-1 più basso;
2. il rendimento mediano a 52 settimane scende passando dalle fasce basse a quelle alte (al massimo un'inversione tra fasce vicine);
3. le condizioni 1 valgono in tutte e due le metà.
Limite dichiarato: i cicli di BTC sono pochi (3-4), le settimane si sovrappongono: è un controllo di buon senso, non una prova statistica.
