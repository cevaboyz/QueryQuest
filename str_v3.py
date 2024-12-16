import sys
import subprocess
import os
import time
import pandas as pd
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox

def install(package):
    """Installs missing Python packages using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure all required libraries are installed
libraries = ['pandas', 'openai', 'openpyxl', 'tiktoken']
for lib in libraries:
    try:
        if lib == 'tiktoken':
            print(f"Installing {lib}...")
            install(lib)
            print(f"{lib} installed successfully.")
        __import__(lib)
    except ImportError:
        print(f"Installing {lib}...")
        install(lib)
        print(f"{lib} installed successfully.")

import openai
import tiktoken

# ASCII Art
ASCII_ART = """

███████╗████████╗██████╗     ████████╗███████╗███╗   ██╗ █████╗  ██████╗████████╗ █████╗      ██╗    ██████╗ 
██╔════╝╚══██╔══╝██╔══██╗    ╚══██╔══╝██╔════╝████╗  ██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗    ███║   ██╔═████╗
███████╗   ██║   ██████╔╝       ██║   █████╗  ██╔██╗ ██║███████║██║        ██║   ███████║    ╚██║   ██║██╔██║
╚════██║   ██║   ██╔══██╗       ██║   ██╔══╝  ██║╚██╗██║██╔══██║██║        ██║   ██╔══██║     ██║   ████╔╝██║
███████║   ██║   ██║  ██║       ██║   ███████╗██║ ╚████║██║  ██║╚██████╗   ██║   ██║  ██║     ██║██╗╚██████╔╝
╚══════╝   ╚═╝   ╚═╝  ╚═╝       ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝     ╚═╝╚═╝ ╚═════╝ 
                                                                                                             

"""

# Pricing information for specific models
MODEL_PRICING = {
    "gpt-4o-2024-08-06": {"input": 0.00250, "output": 0.01000},
    "gpt-4o": {"input": 0.00500, "output": 0.01500},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.00060},
    "gpt-4o-mini-2024-07-18": {"input": 0.000150, "output": 0.000600},
    "gpt-4o-2024-05-13": {"input": 0.00500, "output": 0.01500},
    "gpt-4-turbo": {"input": 0.00500, "output": 0.01500}
}

def load_api_key_from_file(file_path):
    """Load the OpenAI API key from a file."""
    with open(file_path, 'r') as file:
        content = file.read().strip()
        if content.startswith("api/API="):
            return content.split("=")[1]
        return content

def get_api_key():
    """Interactive dialog to get the API key."""
    root = tk.Tk()
    root.withdraw()

    choice = simpledialog.askstring("API Key Input",
                                    "Choose input method:\n1. Paste API key\n2. Select file with API key",
                                    initialvalue="1")

    if choice == "1":
        api_key = simpledialog.askstring("API Key Input", "Paste your OpenAI API key:", show='*')
        if api_key:
            return api_key.strip()
        else:
            print("No API key provided. Operation cancelled.")
            return None
    elif choice == "2":
        file_path = filedialog.askopenfilename(
            title="Select the file containing your OpenAI API key",
            filetypes=[("Text Files", "*.txt")],
            initialdir=os.getcwd()
        )
        if file_path:
            return load_api_key_from_file(file_path)
        else:
            print("No file selected. Operation cancelled.")
            return None
    else:
        print("Invalid choice. Operation cancelled.")
        return None

def get_available_models(client):
    """Get a list of available models from OpenAI."""
    try:
        models = client.models.list()
        return [model.id for model in models.data if model.id.startswith('gpt')]
    except Exception as e:
        print(f"Error fetching models: {e}")
        return list(MODEL_PRICING.keys())  # Fallback to models with pricing info

def select_model(available_models):
    """Interactive dialog to select a model."""
    root = tk.Tk()
    root.withdraw()

    print("Available models:")
    for i, model in enumerate(available_models):
        print(f"{i + 1}. {model}")

    while True:
        choice = simpledialog.askstring("Model Selection",
                                        f"Enter the number of the model you want to use (1-{len(available_models)}):")
        if choice and choice.isdigit() and 1 <= int(choice) <= len(available_models):
            return available_models[int(choice) - 1]
        print("Invalid selection. Please try again.")

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count the number of tokens in the given text using the specified model's tokenizer."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def create_openai_client(api_key):
    """Create and return an OpenAI client instance."""
    return openai.OpenAI(api_key=api_key)

def generate_content(client, prompt: str, model: str) -> str:
    """Generate content using OpenAI's API."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        raise Exception(f"OpenAI API request failed: {str(e)}")

def calculate_cost(tokens: int, model: str, is_input: bool = True) -> float:
    """Calculate the cost for the given number of tokens."""
    if model in MODEL_PRICING:
        price_per_1k = MODEL_PRICING[model]["input" if is_input else "output"]
        return (tokens / 1000) * price_per_1k
    return 0  # Return 0 if pricing is not available for the model

def schedule_request(client, prompt: str, tracker: dict, model: str) -> dict:
    """Schedule and make a request to the OpenAI API, respecting rate limits."""
    current_time = time.time()

    if int(current_time) % 60 == 0 or int(current_time) % 86400 == 0:
        tracker['request_count'] = 0
        tracker['token_count'] = 0
        tracker['start_minute'] = current_time
        tracker['start_day'] = current_time

    if tracker['request_count'] >= REQUESTS_PER_MINUTE_LIMIT:
        print("Rate limit reached. Waiting...")
        time.sleep(60 - (current_time % 60))
        return schedule_request(client, prompt, tracker, model)

    if tracker['request_count'] >= REQUESTS_PER_DAY_LIMIT:
        raise Exception("Daily request limit reached.")

    input_tokens = count_tokens(prompt, model)
    if (tracker['token_count'] + input_tokens) > TOKENS_PER_MINUTE_LIMIT:
        print("Token limit reached. Waiting...")
        time.sleep(60 - (current_time % 60))
        return schedule_request(client, prompt, tracker, model)

    tracker['request_count'] += 1
    tracker['token_count'] += input_tokens
    start_time = time.time()
    ai_text = generate_content(client, prompt, model)
    end_time = time.time()

    output_tokens = count_tokens(ai_text, model)
    input_cost = calculate_cost(input_tokens, model, True)
    output_cost = calculate_cost(output_tokens, model, False)

    return {
        'ai_text': ai_text,
        'tracker': tracker,
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'input_cost': input_cost,
        'output_cost': output_cost,
        'time_taken': end_time - start_time
    }


def choose_prompt():
    """Let user choose between hardcoded, file, or manual input prompt."""
    product_type = simpledialog.askstring("Product Information",
                                          "What type of product generated these search keywords?")
    brand = simpledialog.askstring("Brand Information", "What is the brand associated with these keywords?")

    hardcoded_prompt = f"""Sei un esperto di SEO e ADVERTISING incaricato di clusterizzare efficacemente un elenco di Search Terms ottenuti da Amazon ADS.

Contesto:
- Prodotto: {product_type} (nello specifico, piastre per capelli)
- Brand: {brand} (includendo Bellissima Imetec, Bellissima, e Imetec come varianti)

Istruzioni:
1. Analizza TUTTI i search terms forniti.
2. Crea un numero adeguato (devono avere all'interno almeno 5 search terms) di etichette/cluster pertinenti che aiutino in una futura analisi del dataset.
3. Identifica e etichetta gli ASIN (es. B08JV7QK54) come "ASIN" (iniziano con B maiuscola seguita da lettere/numeri).
4. Restituisci SOLO l'elenco numerato di etichette/cluster, senza spiegazioni aggiuntive.
5. Le etichette/cluster DEVONO essere in italiano, indipendentemente dalla lingua dei search terms.

Esempi di possibili cluster questo è un esempio a cui puoi ispirarti ma non devi limitarti a questi, sempre se possibile:
1. Brand Competitor [Esempio prodotto + Philips / GHD / Rowenta etccc]
2. Tipo di Capello [specifico per i prodotti per i capelli]
3. Tipo di Risultato
4. Caratteristiche Tecniche
5. Accessori
6. Fascia di Prezzo
7. Occasione d'Uso
8. Problematiche Capelli [specifica per i prodotti per capelli]
9. Tecnologia Specifica
10. ASIN
11. Termini Generici
12. Varianti di Prodotto

Formato di output:
1. [Nome Cluster 1]
2. [Nome Cluster 2]
3. [Nome Cluster 3]
...

"""

    print("\nHardcoded prompt:")
    print(hardcoded_prompt)
    print("\n")

    choice = simpledialog.askstring("Prompt Selection",
                                    "Choose prompt input method:\n1. Hardcoded\n2. File\n3. Manual Input")
    if choice == "1":
        return hardcoded_prompt
    elif choice == "2":
        file_path = filedialog.askopenfilename(title="Select prompt file", filetypes=[("Text Files", "*.txt")])
        with open(file_path, 'r') as file:
            return file.read().strip()
    elif choice == "3":
        return simpledialog.askstring("Manual Prompt Input", "Enter your prompt:")
    else:
        print("Invalid choice. Using default hardcoded prompt.")
        return hardcoded_prompt


def confirm_clusters(clusters):
    """Ask for confirmation of each cluster and handle rejections."""
    confirmed_clusters = []
    rejected_clusters = []
    print("\nGenerated clusters:")
    for i, cluster in enumerate(clusters, 1):
        print(f"{i}. {cluster}")
        confirm = messagebox.askyesno("Confirm Cluster", f"Is this cluster okay?\n\n{i}. {cluster}")
        if confirm:
            confirmed_clusters.append(cluster)
        else:
            rejected_clusters.append(cluster)

    if rejected_clusters:
        print("\nThe following clusters were rejected:")
        for cluster in rejected_clusters:
            print(cluster)

        choice = simpledialog.askstring("Rejected Clusters",
                                        "How do you want to handle rejected clusters?\n1. Load replacements from file\n2. Manual input")
        if choice == "1":
            file_path = filedialog.askopenfilename(title="Select replacement clusters file",
                                                   filetypes=[("Text Files", "*.txt")])
            with open(file_path, 'r') as file:
                replacements = file.read().splitlines()
            confirmed_clusters.extend(replacements[:len(rejected_clusters)])
        elif choice == "2":
            for cluster in rejected_clusters:
                replacement = simpledialog.askstring("Manual Replacement", f"Enter replacement for: {cluster}")
                confirmed_clusters.append(replacement)

    return confirmed_clusters


def generate_clusters(client, full_prompt, model):
    """Generate clusters using the OpenAI API."""
    result = schedule_request(client, full_prompt, {'request_count': 0, 'token_count': 0}, model)
    clusters = result['ai_text'].split('\n')
    return [cluster.strip() for cluster in clusters if cluster.strip()]


def classify_search_term(client, search_term, clusters, model):
    """Classify a single search term into one of the provided clusters."""
    prompt = f"Classify the following search term into one of the provided clusters. Respond with only the cluster name in italics or '#NA' if not applicable.\n\nSearch term: {search_term}\n\nClusters:\n" + "\n".join(
        clusters)
    result = schedule_request(client, prompt, {'request_count': 0, 'token_count': 0}, model)
    classification = result['ai_text'].strip()
    return classification if classification != "#NA" else "#NA"


def save_temporary_results(data, save_dir, custom_filename, index):
    """Save temporary results to a CSV file."""
    temp_file_path = os.path.join(save_dir, f"{custom_filename}_temp.csv")
    data.iloc[:index + 1].to_csv(temp_file_path, index=False)


def save_final_results(data, save_dir, custom_filename):
    """Save final results to an Excel file."""
    final_file_path = os.path.join(save_dir, f"{custom_filename}.xlsx")
    data.to_excel(final_file_path, index=False, engine='openpyxl')
    print(f"Analysis completed. Results saved in '{final_file_path}'")


def perform_custom_clustering(data, client, model):
    """Perform custom clustering using user-provided cluster names."""
    file_path = filedialog.askopenfilename(title="Select custom clusters file", filetypes=[("Text Files", "*.txt")])
    with open(file_path, 'r') as file:
        custom_clusters = file.read().splitlines()

    custom_column = "CLUSTER CUSTOM"
    data[custom_column] = ""

    for i, row in data.iterrows():
        search_term = row[data.columns[0]]  # Assuming the first column contains search terms
        cluster = classify_search_term(client, search_term, custom_clusters, model)
        data.at[i, custom_column] = cluster
        print(f"Processed row {i + 1}: {search_term} -> {cluster}")


def perform_coherence_check(data, client, model):
    """Perform coherence check between search terms and assigned clusters."""
    check_column = "CHECK"
    data[check_column] = ""

    for i, row in data.iterrows():
        search_term = row[data.columns[0]]  # Assuming the first column contains search terms
        cluster = row["CLUSTERIZZAZIONE 1"]
        prompt = f"Is the following search term coherent with its assigned cluster? Respond with only TRUE or FALSE.\n\nSearch term: {search_term}\nCluster: {cluster}"
        result = schedule_request(client, prompt, {'request_count': 0, 'token_count': 0}, model)
        coherence = result['ai_text'].strip().upper()
        data.at[i, check_column] = coherence
        print(f"Coherence check for row {i + 1}: {search_term} -> {cluster} : {coherence}")


def display_results(data):
    """Display the first 10 rows of results."""
    print("\nFirst 10 rows of results:")
    print(data.head(10))


def normalize_and_clean_columns(data, columns_to_clean):
    """Normalize and remove whitespace and asterisks from specified columns."""
    for column in columns_to_clean:
        if column in data.columns:
            data[column] = data[column].str.strip().str.lower().str.replace('*', '', regex=False)
    return data


def main():
    print(ASCII_ART)

    api_key = get_api_key()
    if not api_key:
        return

    client = create_openai_client(api_key)

    available_models = get_available_models(client)
    selected_model = select_model(available_models)
    print(f"Selected model: {selected_model}")

    file_path = filedialog.askopenfilename(
        title="Select the CSV or Excel file",
        filetypes=[("Excel Files", "*.xlsx;*.xls"), ("CSV Files", "*.csv")],
        initialdir=os.getcwd()
    )
    if not file_path:
        print("No file selected. Operation cancelled.")
        return

    try:
        data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading the file: {e}")
        return

    # Print the first 10 rows
    print("\nFirst 10 rows of the dataset:")
    print(data.head(10))

    # Print total number of rows
    total_rows = len(data)
    print(f"\nTotal number of rows in the dataset: {total_rows}")

    print("\nAvailable columns:")
    for i, column in enumerate(data.columns):
        print(f"{i}: {column}")

    search_term_column = input("Enter the number or name of the column containing the search terms: ")
    if search_term_column.isdigit() and int(search_term_column) < len(data.columns):
        search_term_column = data.columns[int(search_term_column)]
    elif search_term_column not in data.columns:
        print("Invalid column selection. Operation cancelled.")
        return

    search_terms = "\n".join(data[search_term_column])
    total_tokens = count_tokens(search_terms, selected_model)
    print(f"Total tokens for search terms: {total_tokens}")

    prompt = choose_prompt()
    full_prompt = f"{prompt}\n\n{search_terms}"

    # Print the full payload
    print("\nFull payload to be sent to the AI:")
    print(full_prompt)

    prompt_tokens = count_tokens(full_prompt, selected_model)
    print(f"\nTotal tokens including prompt: {prompt_tokens}")
    print(f"Percentage of context used: {(prompt_tokens / 127000) * 100:.2f}%")

    clusters = generate_clusters(client, full_prompt, selected_model)
    confirmed_clusters = confirm_clusters(clusters)

    cluster_column = "CLUSTERIZZAZIONE 1"
    new_column_name = simpledialog.askstring("Column Name",
                                             f"Enter name for the clustering column (default: {cluster_column}):",
                                             initialvalue=cluster_column)
    cluster_column = new_column_name if new_column_name else cluster_column
    data[cluster_column] = ""

    save_dir = filedialog.askdirectory(title="Select directory to save results")
    if not save_dir:
        print("No directory selected. Using current directory.")
        save_dir = os.getcwd()

    custom_filename = simpledialog.askstring("File Name",
                                             "Enter the name for the final file (without extension):",
                                             initialvalue="clustering_results")
    if not custom_filename:
        custom_filename = "clustering_results"

    rows_to_process = simpledialog.askstring("Rows to Process",
                                             f"Enter 'all' to process all rows, a number to process up to that row, or a range (e.g., '1-100'). Total rows: {total_rows}")

    if rows_to_process.lower() == 'all':
        start_row, end_row = 0, total_rows
    elif '-' in rows_to_process:
        start_row, end_row = map(int, rows_to_process.split('-'))
    else:
        start_row, end_row = 0, int(rows_to_process)

    total_cost = 0
    for i, row in data.iloc[start_row:end_row].iterrows():
        search_term = row[search_term_column]
        result = schedule_request(client,
                                  f"Classify this search term into one of the following clusters. Respond with only the cluster name in italics or '#NA' if not applicable:\nSearch term: {search_term}\nClusters:\n" + "\n".join(
                                      confirmed_clusters), {'request_count': 0, 'token_count': 0},
                                  selected_model)

        cluster = result['ai_text'].strip()
        data.at[i, cluster_column] = cluster

        total_cost += result['input_cost'] + result['output_cost']

        print(f"Processed row {i + 1}: {search_term} -> {cluster}")
        print(f"Input tokens: {result['input_tokens']}, Output tokens: {result['output_tokens']}")
        print(f"Cost: ${result['input_cost'] + result['output_cost']:.4f}")

        save_temporary_results(data, save_dir, custom_filename, i)

    save_final_results(data, save_dir, custom_filename)
    print(f"Total cost of analysis: ${total_cost:.4f}")

    if messagebox.askyesno("Custom Clustering", "Do you want to perform a custom clustering?"):
        perform_custom_clustering(data, client, selected_model)
        save_final_results(data, save_dir, f"{custom_filename}_with_custom")

    # Perform coherence check only on processed rows
    perform_coherence_check(data.iloc[start_row:end_row], client, selected_model)

    # Normalize and clean columns
    columns_to_clean = [cluster_column, "CLUSTER CUSTOM", "CHECK"]
    data = normalize_and_clean_columns(data, columns_to_clean)

    save_final_results(data, save_dir, f"{custom_filename}_final_cleaned")
    print(f"Analysis completed. Cleaned results saved in '{save_dir}/{custom_filename}_final_cleaned.xlsx'")

    display_results(data)

    os.startfile(save_dir)


if __name__ == "__main__":
    REQUESTS_PER_MINUTE_LIMIT = 60
    TOKENS_PER_MINUTE_LIMIT = 90000
    REQUESTS_PER_DAY_LIMIT = 5000
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        input("Press Enter to close the terminal...")