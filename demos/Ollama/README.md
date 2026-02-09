## 🎥 Demo Video Explanation
This demo video showcases how [Ollama](https://github.com/ollama/ollama), used through (Open WebUI)[https://github.com/open-webui/open-webui], can extract and synthesize information from a website article using multiple large language model.

*Requirements*
- [Ollama installation](https://github.com/ollama/ollama?tab=readme-ov-file). 
- [WebUI installation](https://github.com/open-webui/open-webui)

---
### Exercise 1: Information Retrieval From a Website Article

In this exercise, the [URL](https://www.npr.org/2025/10/20/nx-s1-5560956/collagen-supplements-skin-joints?utm_source=OCERMarketingCloud&utm_medium=email&utm_campaign=HMS+in+the+News+(October+20%2c+2025)&utm_content=https%3a%2f%2fwww.npr.org%2f2025%2f10%2f20%2fnx-s1-5560956%2fcollagen-supplements-skin-joints) of the article *"Can collagen supplements improve your skin? Here's what the research shows"* is added directly to the the WebUI. 

Two different LLMs (gemma3.2 and llama3.2) are prompted to:
- Read the article
- Extract three key takeaways from the article.

The resulting responses are then merged into a single, consolidated summary.

This exercise highlights how Ollama and WebUI can be used to compare model outputs, identify complementary insights, and synthesize higher-quality responses from web-based sources.


