## PROMPT Storage for different languages (actually english and italian)

# ITALIAN

CHUNK_PROMPT_IT = """
Genera un riassunto di massimo 100 parole data la trascrizione di una chiamata su Microsoft Teams che ti verrà fornita di seguito.
Il riassunto deve essere una descrizione dei punti più importanti menzionati nella trascrizione.
Devi identificare i punti più importanti e riportarli con delle frasi autoconclusive e concise.
Rifletti sul tuo task punto per punto e genera il riassunto.

Testo:
{text}

Riassunto:
"""


EMAIL_PROMPT_IT = """
Sei un PM incaricato di generare delle email di recap che siano consistenti e ben fatte.
Genera una email di riassunto partendo dalla trascrizione testuale di una chiamata su Microsoft Teams. 
La mail deve essere di massimo 300 parole e devi selezionare i punti più importanti dati i seguenti testi.
Nella mail scrivi inizialmente un piccolo riassunto del tema principale, inserendo successivamente un elenco puntato con al massimo 10 punti salienti per la trascrizione.
Puoi anche usare meno di 10 punti per l'elenco puntato, ma non utilizzarne più di 10.
Concludi la mail con una frase di congedo. La mail deve necessariamente concludersi senza interruzioni. 
Deve contenere massimo 300 parole.

Trascrizione:
{texts}

E-mail:
"""


REPORT_PROMPT_IT = """
Sulla base delle informazioni contenute nella trascrizione seguente, genera un report.
Il report dovrebbe fornire un'analisi dettagliata di ciascun argomento discusso, spiegando come ciascun argomento ha contribuito alla riunione.
Concentrati sulla pertinenza, l’affidabilità e il significato di ciascun argomento.
Assicurati che il report sia ben strutturato, informativo, approfondito e segua una sintassi Markdown.
Separa le varie sezioni con titoli ed eventuali sottotitoli.
Includi fatti, domande e numeri rilevanti quando disponibili.
Il report dovrà avere una lunghezza minima di 1.200 parole e di massimo 2,500 parole.

Trascrizione:
{texts}

Report:
"""

# ENGLISH

CHUNK_PROMPT_EN = """
Generate a summary of up to 100 words given the Microsoft Teams call transcript provided below.
The summary should be a description of the most important points mentioned in the transcript.
You must identify the most important points and report them in self-contained and concise sentences.
Reflect on your task point by point and generate the summary.

Text:
{text}

Summary:
"""


EMAIL_PROMPT_EN = """
You are a PM tasked with generating delivery emails that are consistent and well-crafted.
Generate a summary email starting from the text transcription of a call on Microsoft Teams.
The email must be a maximum of 300 words and you must select the most important points given the following texts.
In the email, initially write a small summary of the main theme, subsequently inserting a bulleted list with a maximum of 10 salient points for transcription.
You can also use fewer than 10 bullet points, but don't use more than 10.
Conclude the email with a parting sentence. The email must necessarily end without interruption.
Must contain a maximum of 300 words.

Transcription:
{texts}

E-mail:
"""


REPORT_PROMPT_EN = """
Based on the information in the following transcription, generate a report. 
The report should provide a detailed analysis of each discussed topic, explaining how each topic contributed to the meeting.
Focus on the relevance, reliability, and significance of each topic.
Ensure that the report is well-structured, informative, in-depth, and follows Markdown syntax.
Split the various sections with titles and possibly subtitles.
Include relevant facts, questions, and numbers whenever available.
The report should have a minimum length of 1,200 words and maximum of 2,500.

Transcription:
{texts}

Report:
"""
