CHUNK_PROMPT = """
Genera un riassunto di massimo 100 parole data la trascrizione di una chiamata su Microsoft Teams che ti verrà fornita di seguito.
Il riassunto deve essere una descrizione dei punti più importanti menzionati nella trascrizione.
Devi identificare i punti più importanti e riportarli con delle frasi autoconclusive e concise.
Rifletti sul tuo task punto per punto e genera il riassunto.

Testo:
{text}

Riassunto:
"""


EMAIL_PROMPT = """
Sei un PM incaricato di generare delle email di recap che siano consistenti e ben fatte.
Genera una email di riassunto partendo dalla trascrizione testuale di una chiamata su Microsoft Teams. 
La mail deve essere di massimo 300 parole e devi selezionare i punti più importanti dati i seguenti testi.
Nella mail scrivi inizialmente un piccolo riassunto del tema principale, inserendo successivamente un elenco puntato con al massimo 10 punti salienti per la trascrizione.
Puoi anche usare meno di 10 punti per l'elenco puntato, ma non utilizzarne più di 10.
Concludi la mail con una frase di congedo.

Trascrizione:
{testi}

Email:
"""


RECAP_PROMPT = """
Genera un riassunto dettagliato circa la trascrizione che ti verrà fornita. Il recap deve
essere in formato .md, avere quindi un titolo principale riguardo il macro argomento, dei sottotitoli per ogni sezione
e ovviamente i paragrafi. Formatta bene nel formato .md.
Restituisci un riassunto pulito, scritto bene e utile per chiunque lo legga. Non tralasciare parti importanti.

Trascrizione:
{testi}

Riassiunto:
"""
