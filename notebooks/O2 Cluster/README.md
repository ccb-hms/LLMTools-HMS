![image](../../images/repo-image-chatgpt.png)
[Play Demo](https://www.youtube.com/watch?v=C1Wbf5YQm_Y)

---
## 🎥 Demo Video Explanation

This demo video showcases how the [**Azure AI Platform**](https://it.hms.harvard.edu/service/azure-ai) can be used for batch inference.
A subset of the [MedMCQA](https://huggingface.co/datasets/openlifescienceai/medmcqa) dataset is used for demonstration purposes. 

The demo illustrates how to:

- Build an Azure OpenAI client

- Generate a prompt

- Submit requests and extract model responses

- Loop through a dataset to obtain responses from multiple models (GPT-4o and GPT-4.1)

The notebook used in this exercise is located at:

```LLMTools-HMS/notebooks/AzureAIPlatform/Azure-Example.ipynb```

*Requirements*
- Azure Open AI API acess. To request API access, contact **Po Yu** from HMS IT at francis_yu@hms.harvard.edu
- [Python](https://www.python.org/downloads/) 
- Python packages: [openai](https://github.com/openai/openai-python), [datasets](https://github.com/huggingface/datasets)

This exercise demonstrates how to perform scalable batch inference with Azure OpenAI models using a real-world biomedical QA dataset.
