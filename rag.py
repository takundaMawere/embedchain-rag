import dropbox 
import os
from pdf2image import convert_from_path
import pytesseract
import sentence_transformers
import poppler
from embedchain import App
# Replace this with your HF token
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"
os.environ["DROPBOX_ACCESS_TOKEN"] = "sl.B33Cb3G0oKbvOCUC_GSVMch_pir4Tn3n2idDegqWCtOrac0XbqAkmdIr9EZ0M754IQLjf6ey2WK9wqot7Bmz6gnRMhCJJ1fFQBuUpDZsC15nlx-32arBwL7FfrFtTA8m3iCtIEei1_GcTg9zbZ1zPV0"
config = {
  'llm': {
    'provider': 'huggingface',
    'config': {
      'model': 'mistralai/Mistral-7B-Instruct-v0.2',
      'top_p': 0.5
    }
  },
  'embedder': {
    'provider': 'huggingface',
    'config': {
      'model': 'sentence-transformers/all-mpnet-base-v2'
    }
  }
}
app = App.from_config(config=config)
# Dropbox API access token
if __name__ == '__main__':
  ACCESS_TOKEN = 'sl.B33Cb3G0oKbvOCUC_GSVMch_pir4Tn3n2idDegqWCtOrac0XbqAkmdIr9EZ0M754IQLjf6ey2WK9wqot7Bmz6gnRMhCJJ1fFQBuUpDZsC15nlx-32arBwL7FfrFtTA8m3iCtIEei1_GcTg9zbZ1zPV0'

  # Create a Dropbox client
  dbx = dropbox.Dropbox(ACCESS_TOKEN)

  # Dropbox folder path
  dropbox_folder_path = '/test2'

  # Local folder to save downloaded PDFs
  local_folder_path = './downloaded_pdfs'
  os.makedirs(local_folder_path, exist_ok=True)

  # List and download PDFs


  # section2 
  def list_and_download_pdfs(dbx, folder_path):
      pdf_files = []
      result = dbx.files_list_folder(folder_path)
      while result.entries:
          for entry in result.entries:
              if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith('.pdf'):

                  local_file_path = os.path.join(local_folder_path, entry.name)
                  if not os.path.exists(local_file_path):
                      pdf_files.append(entry.name)
                  with open(local_file_path, "wb") as f:
                      metadata, res = dbx.files_download(entry.path_lower)
                      f.write(res.content)
          if result.has_more:
              result = dbx.files_list_folder_continue(result.cursor)
          else:
              break
      return pdf_files

  pdf_files = list_and_download_pdfs(dbx, dropbox_folder_path)
  print(f"Downloaded PDFs: {pdf_files}")

  # Convert PDFs to text using OCR
  def pdf_to_text(pdf_path):
      pages = convert_from_path(pdf_path, 300)
      texts = [pytesseract.image_to_string(page) for page in pages]
      return "\n".join(texts)

  pdf_texts = []
  for pdf_file in pdf_files:
      local_pdf_path = os.path.join(local_folder_path, pdf_file)
      text = pdf_to_text(local_pdf_path)
      print("Added")
      pdf_texts.append((pdf_file, text))


  # section 3
  app = App.from_config(config=config)
  # Add extracted texts to EmbedChain
  for pdf_file, text in pdf_texts:
      print("something is being added \n")
      app.add(text, data_type='text')

  app.add("/gen2", data_type="dropbox")
  # Query the embedded texts
