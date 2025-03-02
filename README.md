# 📜 PDF Translator

Um aplicativo em Python para traduzir arquivos PDF usando a biblioteca **PyMuPDF (fitz)** e **GoogleTranslator**.

## 📥 Instalação

Antes de executar o programa, instale as dependências necessárias com o **pip**:

```bash
pip install pymupdf deep-translator fpdf tk
```

## 🚀 Como Usar

1. Execute o script Python:
   ```bash
   python nome_do_arquivo.py
   ```
2. Uma janela será aberta. Clique no botão "Selecionar PDF".
3. Escolha um arquivo PDF.
4. O arquivo será traduzido automaticamente para o português e salvo com o sufixo `_translated.pdf`.
5. Aguarde a barra de progresso atingir 100%.

## 📌 Tecnologias Utilizadas

- **PyMuPDF (fitz)** → Para manipulação de PDFs.
- **GoogleTranslator (deep_translator)** → Para tradução automática do texto.
- **FPDF** → Para gerar novos PDFs com o texto traduzido.
- **Tkinter** → Para interface gráfica.
- **Threading** → Para evitar que a interface trave durante a execução.

## 📷 Interface

A aplicação abre uma interface gráfica simples, permitindo ao usuário selecionar um arquivo PDF para tradução.

## 📄 Estrutura do Código

- `PDF(FPDF)`: Classe para criar o PDF traduzido.
- `translate_pdf(file_path, target_lang, progress_bar)`: Função que traduz o conteúdo do PDF.
- `select_file(progress_bar)`: Função para selecionar o arquivo via interface gráfica.
- `main()`: Configura e inicia a interface gráfica.

## 🛠 Melhorias Futuras

- Adicionar suporte a múltiplos idiomas.
- Melhorar a formatação do texto traduzido.
- Permitir escolher o idioma de destino na interface.

## 📜 Licença

Este projeto está sob a licença MIT.

---

📌 **Desenvolvido por Andrey-Soares8**
