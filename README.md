# NFT Art Project


# Front-end

All'interno della cartella runnare il nomando "npm install" per installare le dipendenze necessarie a runnare l'applucazione su Angular 13.
Eseguire il comando "ng serve" per servire l'applicazione sulla porta 4200.
Dopo aver buildato l'app dovrebbe essere accessibile su "localhost:4200" del browser.
Se il comando "ng serve" non funziona, installare angular con il seguente comando: "npm install -g @angular/cli"



# Back-end

All'interno della cartella be-app c'è un solo file python per un semplice server,
Lanciare il server con il comando "python3 main.py", il server rimane in ascolto sulla porta 3000.
C'è un un'unica funzione che però prende in input il base64 dell'immagine scattata tramite webcam, dovrebbe essere facile portarle in openCV che volevi ma non ho avuto tempo.
Insieme all'immagine della webcam in input arriva anche l'id dell'nft su cui vogliamo fare la personalizzazione, per il momento le immagini sono disponibili nella cartella fe-app/src/app/assets/nft, sono 8, chiaramente l'id che arriva in input sulla chiamata corrisponde al nome del file.
Fammi sapere se hai problemi.
Baci <3
