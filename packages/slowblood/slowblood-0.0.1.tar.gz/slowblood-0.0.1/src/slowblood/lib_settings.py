## Project Level Constants 

VERSION = 1 

class BasicInferenceRequest:
  def __init__(self, token="", inference_url="", system_prompt="", content_prompt="", output_prompt=""):
    self.token = token
    self.inference_url = inference_url
    self.system_prompt = system_prompt
    self.content_prompt = content_prompt
    self.output_prompt = output_prompt


class ArtifactNames:
  def __init__(self, base_model, new_model_name, repo_name, dataset):
    self.base_model = base_model
    base_model_name = base_model.split("/")[-1]
    self.adapter_model = repo_name + "/" + base_model_name + "_" + new_model_name
    self.new_model = repo_name + "/" + new_model_name 
    self.dataset = dataset 