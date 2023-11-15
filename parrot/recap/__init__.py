CHUNK_PROMPT = """
Genera un riassunto di massimo 100 parole data la trascrizione di una chiamata su Microsoft Teams che ti verrà fornita di seguito.
Il riassunto deve essere una descrizione dei punti più importanti menzionati nella trascrizione.
Devi identificare i punti più importanti e riportarli con delle frasi autoconclusive e concise.
Rifletti sul tuo task punto per punto e genera il riassunto.

Testo:
{text}

Riassunto:
"""


TOTAL_SUMMARIZATION_PROMPT = """
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
