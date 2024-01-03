## Project Level Constants 

VERSION = 1 

class Config:
  def __init__(self, hf_token="", inference_url="", system_prompt="", content_prompt="", output_prompt=""):
    self.hf_token = hf_token
    self.inference_url = inference_url
    self.system_prompt = system_prompt
    self.content_prompt = content_prompt
    self.output_prompt = output_prompt


class FineTuningSettings:
  def __init__(self, base_model, new_model_name, repo_name, dataset):
    self.base_model = base_model
    base_model_name = base_model.split("/")[-1]
    self.adapter_model = repo_name + "/" + base_model_name + "_" + new_model_name
    self.new_model = repo_name + "/" + new_model_name 
    self.dataset = dataset 