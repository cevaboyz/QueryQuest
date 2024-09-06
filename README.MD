# QueryQuest 🔍

QueryQuest è uno strumento potente per l'analisi e la clusterizzazione di search terms di Amazon Ads, progettato per esperti di SEO e advertising digitale.

QueryQuest is a powerful tool for analyzing and clustering Amazon Ads search terms, designed for SEO and digital advertising experts.

## 🇮🇹 Italiano

### Descrizione
QueryQuest automatizza il processo di clusterizzazione dei search terms di Amazon Ads, fornendo insights preziosi per ottimizzare le campagne pubblicitarie. Utilizzando l'intelligenza artificiale di OpenAI, lo script categorizza i termini di ricerca in gruppi coerenti, facilitando l'analisi e la strategia di keyword.

### Funzionalità Principali
- 🤖 Integrazione con l'API di OpenAI per la clusterizzazione intelligente
- 📊 Analisi dettagliata dei search terms di Amazon Ads
- 🏷️ Generazione automatica di cluster/etichette rilevanti
- 🔢 Supporto per l'identificazione degli ASIN
- 💾 Salvataggio dei risultati in formato Excel
- 🔄 Opzione per clusterizzazione personalizzata
- ✅ Controllo di coerenza per i cluster generati

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
1. Esegui lo script principale:
   ```
   python main.py
   ```
2. Segui le istruzioni a schermo per:
   - Inserire la chiave API di OpenAI
   - Selezionare il file di input (CSV o Excel)
   - Scegliere le opzioni di clusterizzazione
   - Rivedere e confermare i cluster generati

### Componenti dello Script
- `main.py`: Script principale che orchestra il processo di clusterizzazione
- `api_utils.py`: Funzioni per l'interazione con l'API di OpenAI
- `data_processing.py`: Funzioni per il caricamento e la manipolazione dei dati
- `clustering.py`: Logica di clusterizzazione e generazione delle etichette
- `ui_helpers.py`: Funzioni per l'interfaccia utente e l'input/output

### Requisiti
- Python 3.7+
- Librerie: pandas, openai, openpyxl, tiktoken

### Contribuire
Siamo aperti a contributi! Se hai suggerimenti o miglioramenti, non esitare a aprire una issue o una pull request.

---

## 🇬🇧 English

### Description
QueryQuest automates the process of clustering Amazon Ads search terms, providing valuable insights to optimize advertising campaigns. Using OpenAI's artificial intelligence, the script categorizes search terms into coherent groups, facilitating keyword analysis and strategy.

### Key Features
- 🤖 Integration with OpenAI API for intelligent clustering
- 📊 Detailed analysis of Amazon Ads search terms
- 🏷️ Automatic generation of relevant clusters/labels
- 🔢 Support for ASIN identification
- 💾 Saving results in Excel format
- 🔄 Option for custom clustering
- ✅ Coherence check for generated clusters

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
1. Run the main script:
   ```
   python main.py
   ```
2. Follow the on-screen instructions to:
   - Enter the OpenAI API key
   - Select the input file (CSV or Excel)
   - Choose clustering options
   - Review and confirm generated clusters

### Script Components
- `main.py`: Main script orchestrating the clustering process
- `api_utils.py`: Functions for interacting with the OpenAI API
- `data_processing.py`: Functions for loading and manipulating data
- `clustering.py`: Clustering logic and label generation
- `ui_helpers.py`: Functions for user interface and input/output

### Requirements
- Python 3.7+
- Libraries: pandas, openai, openpyxl, tiktoken

### Contributing
We're open to contributions! If you have suggestions or improvements, feel free to open an issue or a pull request.

