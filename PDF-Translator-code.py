import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from fpdf import FPDF
import unicodedata  
import threading

class PDF(FPDF):
    # Cabeçalho padrão para cada página do PDF
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PDF Traduzido', 0, 1, 'C')
        self.set_draw_color(0, 0, 0)
        self.rect(5, 5, 200, 287)  # Adiciona uma borda ao redor da página

    # Rodapé padrão para cada página do PDF
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# Função para remover caracteres especiais não suportados pelo FPDF

def remove_special_characters(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if ord(c) < 256)

# Função para traduzir o conteúdo do PDF e gerar um novo arquivo traduzido

def translate_pdf(file_path, target_lang='pt', progress_bar=None, loading_label=None):
    try:
        doc = fitz.open(file_path)  # Abre o arquivo PDF
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir o arquivo PDF: {str(e)}")
        return None

    translator = GoogleTranslator(source='auto', target=target_lang)  # Configuração do tradutor
    output_file = file_path.replace(".pdf", "_translated.pdf")  # Nome do arquivo de saída

    try:
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        # Adicionando uma página de capa
        pdf.add_page()
        pdf.set_font("Arial", style='B', size=24)
        pdf.cell(200, 20, "Tradução de Documento", ln=True, align='C')
        pdf.ln(10)

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
        
        pdf.output(output_file, 'F')  # Salva o PDF traduzido

        if loading_label:
            loading_label.config(text="Tradução concluída!")
        
        messagebox.showinfo("Sucesso", f"Tradução concluída! Arquivo salvo em:\n{output_file}")
        return output_file
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        return None

# Função para selecionar o arquivo PDF e iniciar a tradução

def select_file(progress_bar, loading_label):
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        loading_label.config(text="Processando, aguarde...")  # Exibe uma mensagem de carregamento
        threading.Thread(target=translate_pdf, args=(file_path, 'pt', progress_bar, loading_label)).start()

# Configuração da interface gráfica (Tkinter)

def main():
    root = tk.Tk()
    root.title("Tradutor de PDF")
    root.geometry("400x200")  # Define um tamanho fixo para a janela
    root.minsize(400, 200)  # Impede que a janela fique menor que esse tamanho

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)

    label = tk.Label(frame, text="Selecione um arquivo PDF para traduzir", font=("Arial", 12))
    label.pack(pady=10)

    btn = tk.Button(frame, text="Selecionar PDF", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, command=lambda: select_file(progress_bar, loading_label))
    btn.pack(pady=10)

    # Adicionando a barra de progresso estilizada
    style = ttk.Style()
    style.theme_use('clam')  
    style.configure("TProgressbar", thickness=10, troughcolor="#ddd", background="#4CAF50")
    
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate", style="TProgressbar")
    progress_bar.pack(pady=10)
    
    # Mensagem de status
    loading_label = tk.Label(root, text="", fg="blue", font=("Arial", 10))
    loading_label.pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()
