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
        self.rect(5, 5, 200, 287)  # Borda ao redor da página

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def remove_special_characters(text):
    """
    Remove caracteres especiais que não são suportados pelo FPDF (latin-1).
    """
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if ord(c) < 256)

def translate_pdf(file_path, target_lang='pt', progress_bar=None):
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir o arquivo PDF: {str(e)}")
        return None

    translator = GoogleTranslator(source='auto', target=target_lang)
    output_file = file_path.replace(".pdf", "_translated.pdf")

    try:
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        
        num_pages = len(doc)
        for i, page in enumerate(doc):
            pdf.add_page()  # Adiciona uma nova página para cada página do original
            text = page.get_text("text")

            if text.strip():
                translated_text = ""
                
                # Divide em blocos menores para evitar erros
                for j in range(0, len(text), 4000):  
                    chunk = text[j:j+4000]
                    try:
                        translated_chunk = translator.translate(chunk)
                        translated_text += translated_chunk + "\n\n"
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro na tradução: {str(e)}")
                        return None
                    
                # Remove caracteres especiais
                safe_text = remove_special_characters(translated_text)

                # Ajusta para parágrafos normais e mantém estrutura da página
                pdf.multi_cell(0, 10, safe_text)  

            # Atualiza a barra de progresso
            if progress_bar:
                progress = (i + 1) / num_pages * 100
                progress_bar['value'] = progress
                progress_bar.update_idletasks()
        
        pdf.output(output_file, 'F')
        messagebox.showinfo("Sucesso", f"Tradução concluída! Arquivo salvo em:\n{output_file}")
        return output_file
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        return None

def select_file(progress_bar):
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        threading.Thread(target=translate_pdf, args=(file_path, 'pt', progress_bar)).start()

def main():
    root = tk.Tk()
    root.title("Tradutor de PDF")
    
    label = tk.Label(root, text="Selecione um arquivo PDF para traduzir", padx=20, pady=10)
    label.pack()
    
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    
    btn = tk.Button(btn_frame, text="Selecionar PDF", command=lambda: select_file(progress_bar))
    btn.pack(side=tk.LEFT, padx=10)

    # Adiciona a barra de progresso
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
