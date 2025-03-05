import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from fpdf import FPDF
import unicodedata
import threading

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PDF Traduzido', 0, 1, 'C')
        self.set_draw_color(0, 0, 0)
        self.rect(5, 5, 200, 287)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# Remove caracteres especiais não suportados pelo FPDF
def remove_special_characters(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if ord(c) < 256)

# Traduz um texto em blocos para evitar limitações da API
def translate_text(text, target_lang='pt'):
    translator = GoogleTranslator(source='auto', target=target_lang)
    translated_text = ""
    
    for i in range(0, len(text), 4000):
        chunk = text[i:i+4000]
        try:
            translated_text += translator.translate(chunk) + "\n\n"
        except Exception as e:
            return None, f"Erro na tradução: {str(e)}"
    
    return remove_special_characters(translated_text), None

# Traduz o PDF e gera um novo arquivo
def translate_pdf(file_path, target_lang='pt', progress_bar=None, loading_label=None):
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir o PDF: {str(e)}")
        return None
    
    output_file = file_path.replace(".pdf", "_translated.pdf")
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(200, 20, "Tradução de Documento", ln=True, align='C')
    pdf.ln(10)
    
    num_pages = len(doc)
    for i, page in enumerate(doc):
        pdf.add_page()
        text = page.get_text("text")
        
        if text.strip():
            translated_text, error = translate_text(text, target_lang)
            if error:
                messagebox.showerror("Erro", error)
                return None
            pdf.multi_cell(0, 10, translated_text)
        
        if progress_bar:
            progress_bar["value"] = (i + 1) / num_pages * 100
            progress_bar.update_idletasks()
    
    pdf.output(output_file, 'F')
    
    if loading_label:
        loading_label.config(text="Tradução concluída!")
    
    messagebox.showinfo("Sucesso", f"Tradução concluída! Arquivo salvo em:\n{output_file}")
    return output_file

# Seleciona um arquivo PDF e inicia a tradução
def select_file(progress_bar, loading_label):
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        loading_label.config(text="Processando, aguarde...")
        threading.Thread(target=translate_pdf, args=(file_path, 'pt', progress_bar, loading_label)).start()

# Interface gráfica principal
def main():
    root = tk.Tk()
    root.title("Tradutor de PDF")
    root.geometry("400x200")
    root.minsize(400, 200)
    
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)
    
    label = tk.Label(frame, text="Selecione um arquivo PDF para traduzir", font=("Arial", 12))
    label.pack(pady=10)
    
    btn = tk.Button(frame, text="Selecionar PDF", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, command=lambda: select_file(progress_bar, loading_label))
    btn.pack(pady=10)
    
    style = ttk.Style()
    style.theme_use('clam')  
    style.configure("TProgressbar", thickness=10, troughcolor="#ddd", background="#4CAF50")
    
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate", style="TProgressbar")
    progress_bar.pack(pady=10)
    
    loading_label = tk.Label(root, text="", fg="blue", font=("Arial", 10))
    loading_label.pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()
