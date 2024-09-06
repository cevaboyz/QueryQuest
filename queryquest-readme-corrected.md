# QueryQuest 🔍

QueryQuest è uno strumento avanzato per l'analisi e la clusterizzazione dei termini di ricerca di Amazon Ads, progettato per esperti di SEO e pubblicità digitale.

QueryQuest is an advanced tool for analyzing and clustering Amazon Ads search terms, designed for SEO and digital advertising experts.

## 🇮🇹 Italiano

### Descrizione
QueryQuest automatizza il processo di clusterizzazione dei termini di ricerca di Amazon Ads, fornendo insights preziosi per ottimizzare le campagne pubblicitarie. Utilizzando l'API di OpenAI, lo script categorizza i termini di ricerca in gruppi coerenti, facilitando l'analisi e la strategia delle keyword.

### Funzionalità Principali
- 🤖 Integrazione con l'API di OpenAI per la clusterizzazione intelligente
- 📊 Analisi dettagliata dei termini di ricerca di Amazon Ads
- 🏷️ Generazione automatica di cluster/etichette rilevanti
- 🔢 Supporto per l'identificazione degli ASIN
- 💾 Salvataggio dei risultati in formato Excel
- 🔄 Opzione per clusterizzazione personalizzata
- ✅ Controllo di coerenza per i cluster generati
- 🧹 Pulizia e normalizzazione dei dati

### Installazione
1. Clona la repository:
   ```
   git clone https://github.com/tuouser/QueryQuest.git
   ```
2. Naviga nella directory del progetto:
   ```
   cd QueryQuest
   ```
3. Installa le dipendenze:
   ```
   pip install -r requirements.txt
   ```

### Utilizzo
1. Esegui lo script:
   ```
   python str_v3.py
   ```
2. Segui le istruzioni a schermo per:
   - Inserire la chiave API di OpenAI
   - Selezionare il modello di OpenAI da utilizzare
   - Scegliere il file di input (CSV o Excel)
   - Specificare la colonna contenente i termini di ricerca
   - Personalizzare il prompt per la clusterizzazione
   - Rivedere e confermare i cluster generati
   - Scegliere il numero di righe da processare
   - Opzionalmente, eseguire una clusterizzazione personalizzata

### Componenti dello Script
- Gestione delle dipendenze e installazione automatica
- Interfaccia utente interattiva con finestre di dialogo
- Integrazione con l'API di OpenAI
- Funzioni per il caricamento, l'elaborazione e il salvataggio dei dati
- Logica di clusterizzazione e generazione delle etichette
- Controllo di coerenza dei cluster
- Gestione dei limiti di richieste API e conteggio dei token

### Requisiti
- Python 3.7+
- Librerie: pandas, openai, openpyxl, tiktoken

### Contribuire
Siamo aperti a contributi! Se hai suggerimenti o miglioramenti, non esitare a aprire una issue o una pull request.

---

## 🇬🇧 English

### Description
QueryQuest automates the process of clustering Amazon Ads search terms, providing valuable insights to optimize advertising campaigns. Using the OpenAI API, the script categorizes search terms into coherent groups, facilitating keyword analysis and strategy.

### Key Features
- 🤖 Integration with OpenAI API for intelligent clustering
- 📊 Detailed analysis of Amazon Ads search terms
- 🏷️ Automatic generation of relevant clusters/labels
- 🔢 Support for ASIN identification
- 💾 Saving results in Excel format
- 🔄 Option for custom clustering
- ✅ Coherence check for generated clusters
- 🧹 Data cleaning and normalization

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/QueryQuest.git
   ```
2. Navigate to the project directory:
   ```
   cd QueryQuest
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage
1. Run the script:
   ```
   python str_v3.py
   ```
2. Follow the on-screen instructions to:
   - Enter the OpenAI API key
   - Select the OpenAI model to use
   - Choose the input file (CSV or Excel)
   - Specify the column containing search terms
   - Customize the clustering prompt
   - Review and confirm generated clusters
   - Choose the number of rows to process
   - Optionally perform custom clustering

### Script Components
- Dependency management and automatic installation
- Interactive user interface with dialog windows
- OpenAI API integration
- Functions for loading, processing, and saving data
- Clustering logic and label generation
- Cluster coherence checking
- API request limit and token count management

### Requirements
- Python 3.7+
- Libraries: pandas, openai, openpyxl, tiktoken

### Contributing
We're open to contributions! If you have suggestions or improvements, feel free to open an issue or a pull request.

