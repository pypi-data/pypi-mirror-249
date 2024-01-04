<img src="logo.jpeg"></img>

<h1 style="text-align:center">🌊RIS-Bot⛱️</h1>

<h3 style="text-align:center">Rest in Story</h3>



Tags: 
- chatbot
- english
- GPT2
- anxiety/stress/....

<br><br>

### Description

A GPT2 model is to be extended to a new task via transfer learning. The GPT2 model is to be fine-tuned in such a way that it generates interactive, meditative and calming stories for the user.<br>
The aim is to create a reading experience that promotes positive thoughts.<br>
The language is English and the model is to be deployed on Discord.<br>
Interaction data from a user and a storyteller is required for the training data.<br>
Since such training data is difficult to obtain, ChatGPT is used to generate the data.<br>

This branch is the PyPI implentation for the model. It provides the model itself and functionality to inference the model.

<br><br>

### Guide

Simply usage:

```python
from ris_bot import RIS_Bot

bot = RIS_Bot()
res = bot.inference("Create me a unique interactive story to calm with the topic: Ocean.")
print(res)
```






