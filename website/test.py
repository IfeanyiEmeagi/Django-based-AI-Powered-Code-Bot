#from transformers import pipeline


#classifier = pipeline("sentiment-analysis")
#result = classifier("I am going to learn how to integrate llm in my personal project")
#print(result)

from transformers import AutoTokenizer, T5ForConditionalGeneration
device = "cpu"
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5p-220m")
model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5p-220m").to(device)


# Save the model and tokenizer to a local file
saved_directory = "website/saved_model"
model.save_pretrained(saved_directory)
tokenizer.save_pretrained(saved_directory)