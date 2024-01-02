import re
import os
import uuid
import json

from google.cloud import storage
from langchain.llms import VertexAI

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

    prompt                  = f"Context: {''.join(OCRLayouting.layout_normalization(new_file_name)[1])} \n {prompt}"

    os.remove(new_file_name)

    answer                  = re.findall('(\{.*?\})',llm(prompt).replace('\n',' '))[0]
    print(answer)

    return json.loads(answer)