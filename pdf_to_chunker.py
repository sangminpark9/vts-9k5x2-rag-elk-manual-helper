import os
import json
import random
import logging
from typing import List, Dict, Any
import pdfplumber
from dataclasses import dataclass

@dataclass
class ChunkConfig:
    chunk_size: int = 1000
    overlap: int = 50

class PDFChunker:
    def __init__(self, config: ChunkConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def chunk_pdf(self, pdf_path: str) -> List[str]:
        chunks = []
        current_chunk = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        words = text.split()
                        for word in words:
                            if len(current_chunk) + len(word) + 1 > self.config.chunk_size:
                                chunks.append(current_chunk.strip())
                                current_chunk = current_chunk[-self.config.overlap:] + word + " "
                            else:
                                current_chunk += word + " "
            if current_chunk:
                chunks.append(current_chunk.strip())
        except Exception as e:
            self.logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
        return chunks

    def process_pdf(self, pdf_path: str, output_file: str) -> List[Dict[str, Any]]:
        if not os.path.exists(pdf_path):
            self.logger.error(f"File not found: {pdf_path}")
            return []

        self.logger.info(f"Starting to process PDF file: {pdf_path}")
        chunks = self.chunk_pdf(pdf_path)
        filename = os.path.basename(pdf_path)
        
        all_chunks = []
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "file": filename,
                "chunk_id": f"{filename}_chunk_{i}",
                "content": chunk
            })
            if (i + 1) % 100 == 0:
                self.logger.info(f"Processed: {i+1} chunks created")
        
        self.logger.info(f"Processing completed: {filename} (Total chunks: {len(chunks)})")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
        
        return all_chunks

    @staticmethod
    def preview_chunks(chunks: List[Dict[str, Any]], num_samples: int = 5):
        samples = random.sample(chunks, min(num_samples, len(chunks)))
        for i, sample in enumerate(samples, 1):
            print(f"\nSample {i}:")
            print(f"File: {sample['file']}")
            print(f"Chunk ID: {sample['chunk_id']}")
            print(f"Content: {sample['content'][:100]}...")  # Print first 100 chars

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    manual_dir = "./data/manuals/"
    file_name = "User_Manual_VTS-9K5X2_V1.5_EN.pdf"
    pdf_path = os.path.join(manual_dir, file_name)
    output_file = "./data/chunks.json"
    
    config = ChunkConfig(chunk_size=1000, overlap=50)
    chunker = PDFChunker(config)
    
    logging.info("Starting PDF chunking process...")
    chunks = chunker.process_pdf(pdf_path, output_file)
    logging.info(f"Chunks saved to {output_file}")
    logging.info(f"Total chunks created: {len(chunks)}")

    print("\nChunk sample preview:")
    PDFChunker.preview_chunks(chunks)

if __name__ == "__main__":
    main()