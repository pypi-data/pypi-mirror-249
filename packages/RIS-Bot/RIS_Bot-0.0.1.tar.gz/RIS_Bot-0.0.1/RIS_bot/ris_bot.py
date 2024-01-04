import os
from datetime import datetime as dt

import transformers
import torch

class RIS_Bot():

    def __init__(self):
        self.max_length = 883
        self.history = ""
        self.set_device()
        self.load_tokenizer()
        self.load_model()

    def set_device(self):
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')

    def load_tokenizer(self):
        self.tokenizer = transformers.AutoTokenizer.from_pretrained("gpt2")
        self.tokenizer.add_special_tokens({ "pad_token": "<pad>",
                                            "bos_token": "<start>",
                                            "eos_token": "<end>"})
        self.tokenizer.add_tokens(["<bot>:"])

    def load_model(self):
        self.config = transformers.GPT2Config.from_pretrained("gpt2")
        self.config.max_length = self.max_length
        self.model = transformers.GPT2LMHeadModel.from_pretrained("gpt2", config=self.config)
        self.model.resize_token_embeddings(len(self.tokenizer))
        self.model.eval()
        self.model = self.model.to(self.device)
        self.model.load_state_dict(torch.load("./weights/model_weights_V3_6.pth", map_location=self.device))

    def inference(self, prompt:str, clear_output=True):
        user_input = prompt
        prompt = f"<start>{prompt}<bot>:"
        prompt = self.tokenizer(prompt, return_tensors="pt", padding=True)
        X = prompt["input_ids"].to(self.device)
        a = prompt["attention_mask"].to(self.device)
        output = self.model.generate(X, attention_mask=a, pad_token_id=self.tokenizer.eos_token_id)
        output = self.tokenizer.decode(output[0])

        # clean output:
        if clear_output:
            if type(output) == list and len(output) == 1:
                output = output[0]
            elif type(output) == list:
                print("Warning bigger list as Output!")

            if "<bot>:" in output:
                output = "".join(output.split("<bot>:")[1:])

            if "<end>" in output:
                print("huhu")
                output = "".join(output.split("<end>")[:1])

            if "<pad>" in output:
                print("hehe")
                output = output.replace("<pad>", "")

        if type(output) == list and len(output) == 1:
            output = output[0]

        self.history += f"\n\nuser: {user_input}\n\nbot: {output}"
        return output

    def set_topic(self, topic):
        self.topic = topic

    def save_history(self, name=None):
        if self.history != "":
            if type(name) != str:
                name = f"RIS_experience_{dt.now().strftime('%Y-%m-%d %H')}_{self.topic}"
            counter = 2
            while name in os.listdir("./histories"):
                name = f"RIS_experience_{dt.now().strftime('%Y-%m-%d %H')}_{self.topic}_{counter}"
            
            with open(f"./histories/{name}", "w") as f:
                f.write(self.history)

    def get_history(self, name=None):
        return self.history

    def reload(self):
        self.history = ""
        self.set_device()
        self.load_tokenizer()
        self.load_model()





