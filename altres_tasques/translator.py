# translator.py
"""Codi per traduir del català al castellà.
Es pot fer servir des de la consola o processant un arxiu Word sencer."""

from abc import ABC, abstractmethod
from docx import Document
from time import time
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


DEBUG = True
MAX_TOKENS = 256
TOKEN_VARIATION = 0.75 # Considered token variation between languages
    # Careful:
    # If Catalan does not exceed MAX_TOKENS * TOKEN_VARIATION
    # but Spanish exceeds MAX_TOKENS, the output gets truncated to MAX_TOKENS.


# Translation layer ____________________________________________________________

class Translator(ABC):

    @abstractmethod
    def translate(self, text: str) -> str:
        pass


class NLLBTranslator(Translator):

    def __init__(self):
        print("Loadind NLLB model and tokenizer...")
        model_name = "facebook/nllb-200-distilled-600M"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.model.eval()

    def translate(self, text: str):
        src_lang = "cat_Latn"
        tgt_lang = "spa_Latn"

        # Tokenize input text with source language context
        self.tokenizer.src_lang = src_lang
        inputs = self.tokenizer(text, return_tensors="pt")

        # MAX_TOKENS hard limit ------------------------------------------------
        token_count = inputs["input_ids"].shape[1]

        if token_count > MAX_TOKENS:
        
            print("\n" + "=" * 80 + "\n" + "ERROR: Chunk exceeds MAX_TOKENS * TOKEN_VARIATION")
            print(f"Tokens: {token_count}")
            print(f"Limit : {MAX_TOKENS * TOKEN_VARIATION}")
            print("Text:" + "\n", text)
            print("=" * 80 + "\n")
        
            raise ValueError(
                f"Chunk contains {token_count} tokens "
                f"(limit = {MAX_TOKENS * TOKEN_VARIATION})"
            )
        # ----------------------------------------------------------------------
    
        # Generate translated tokens
        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(tgt_lang),
            max_length=MAX_TOKENS,
        )

        # Decode and print output
        translated_text = self.tokenizer.batch_decode(
            translated_tokens, skip_special_tokens=True
        )[0]
        return translated_text


def manual_console_translation():
    """Translate a message given by the user interacting through the console."""
    print("Maual translation mode started.")
    print("Initializing translator...")
    translator = NLLBTranslator()
    while True:
        in_text = input("Write the text you want to translate from Catalan to Spanish: ")
        print("Calling the translator...")
        out_text = translator.translate(in_text)
        print("Translation:")
        print(out_text)     


# Parsing layer ________________________________________________________________

class TextChunk:
    def __init__(self, runs, text, highlight):
        self.runs = runs
        self.text = text
        self.highlight = highlight


def paragraph_to_chunks(paragraph):
    """
    Creates translation chunks.

    Consecutive runs are merged together unless
    the highlight color changes.
    """
    chunks = []
    current_runs = []
    current_text = ""
    current_highlight = None

    for run in paragraph.runs:
        text = run.text
        if not text:
            continue

        highlight = run.font.highlight_color

        if (current_runs and highlight != current_highlight):
            chunks.append(TextChunk(current_runs, current_text, current_highlight))
            current_runs = []
            current_text = ""

        current_runs.append(run)
        current_text += text
        current_highlight = highlight

    if current_runs:
        chunks.append(TextChunk(current_runs, current_text, current_highlight))

    return chunks


def iter_paragraphs_table(table):

    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                yield paragraph
            for nested_table in cell.tables:
                yield from iter_paragraphs_table(nested_table)


def iter_all_paragraphs(doc):

    # Main document
    for paragraph in doc.paragraphs:
        yield paragraph

    # Tables
    for table in doc.tables:
        yield from iter_paragraphs_table(table)

    # Headers / Footers
    for section in doc.sections:
        for paragraph in section.header.paragraphs: yield paragraph
        for paragraph in section.footer.paragraphs: yield paragraph
        for table in section.header.tables: yield from iter_paragraphs_table(table)
        for table in section.footer.tables: yield from iter_paragraphs_table(table)


# .docx translation layer ______________________________________________________

class DocumentTranslator:

    def __init__(self, translator):
        self.translator = translator

    def translate_chunk(self, chunk):

        original = chunk.text

        if not original.strip():
            return

        if DEBUG: print("=" * 80 + "\n" + "Translating chunk:" + "\n", repr(original))

        translated = self.translator.translate(original)

        if DEBUG: print("Result:", repr(translated), "\n")

        # Put translated text into first run
        chunk.runs[0].text = translated

        # Empty remaining runs
        for run in chunk.runs[1:]:
            run.text = ""

    def translate_paragraph(self, paragraph):

        chunks = paragraph_to_chunks(paragraph)

        for chunk in chunks:
            self.translate_chunk(chunk)

    def translate_document(self, doc):

        for paragraph in iter_all_paragraphs(doc):
            self.translate_paragraph(paragraph)

        return doc

    
def translate_docx(input_path: str, output_path: str, translator):
    t0 = time()

    doc = Document(input_path)
    engine = DocumentTranslator(translator)
    engine.translate_document(doc)
    doc.save(output_path)

    if DEBUG: print(f"Trasnlation took {(time() - t0) / 60} minutes")


# Main _________________________________________________________________________

def main():
    # manual_console_translation()
    translate_docx(
        r"C:\Users\55182183p\OneDrive - Generalitat de Catalunya\Obsidian_vaults\Gencat Energia\Bloc B - Reescriptura de les FAQs\Carpeta compartida Revisió FAQs\Seccions FAQs\Seccions existents\Rev FAQs Productors - CAT.docx",
        "./translated_docx_test.docx",
        NLLBTranslator()
    )

if __name__ == "__main__":
    main()