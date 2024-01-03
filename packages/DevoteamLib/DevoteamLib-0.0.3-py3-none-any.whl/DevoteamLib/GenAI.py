import re
import os
import uuid
import json

from google.cloud import storage
from langchain.llms import VertexAI

import shutil
from pdf2image import convert_from_path


import DevoteamLib.OCRLayouting as OCRLayouting

class GenAIDocExtract:
  def __init__(self, project_id:str):
    self.storage_client = storage.Client(project = project_id)
  
  def download_blob(self, bucket_name: str, source_blob_name: str, destination_file_name:str):
    bucket     = self.storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    return destination_file_name

  def textBisonParse(self, model_name = "text-bison@002",
                    max_output_tokens: int = 2048, temperature: int = 0,
                    top_p: int = 0.8, top_k: int = 40, verbose: bool = False,
                    file_gcs_path: str = '', prompt: str = '') -> dict:
    llm = VertexAI(
          model_name        = model_name,
          max_output_tokens = max_output_tokens,
          temperature       = temperature,
          top_p             = top_p,
          top_k             = top_k,
          verbose           = verbose
      )
    
    bucket,filename         = re.findall('gs:\/\/(.*?)\/(.*)',file_gcs_path)[0]

    new_file_name           = f"{str(uuid.uuid4())}.{filename.split('.')[-1]}"
    
    self.download_blob(bucket, filename, new_file_name)

    if filename.split('.')[-1].lower() in ['jpg','jpeg','png']:
      prompt                  = f"Context: {''.join(OCRLayouting.layout_normalization(new_file_name)[1])} \n {prompt}"
      os.remove(new_file_name)
    elif filename.split('.')[-1].lower() in ['pdf']:
      images = convert_from_path(new_file_name)
      if len(images)>5:
        os.remove(new_file_name)
        return "PDF file have more than 5 pages"
      
      context    = []
      foldername = str(uuid.uuid4())
      os.mkdir(foldername)

      for index,img in enumerate(images):
        img.save(f'{foldername}/image_save.png','PNG')
        context.append(''.join(OCRLayouting.layout_normalization(f'{foldername}/image_save.png')[1]))
      
      prompt     = f"Context: {' '.join(context)} \n {prompt}"
      shutil.rmtree(foldername)

    answer                  = re.findall('(\{.*?\})',llm(prompt).replace('\n',' '))[0]
    print(answer)

    return json.loads(answer)