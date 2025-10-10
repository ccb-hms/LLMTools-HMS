from llmtools.ollamamodel import Ollama as OllamaModel
import ollama


__author__ = 'Andreas Werdich'
__copyright__ = 'Core for Computational Biomedicine at Harvard Medical School'
__license__ = 'CC0-1.0'

def test_create_ollama_client():
    """ Test the create_client method """
    client = OllamaModel().create_client()
    assert client is not None
    assert isinstance(client, ollama.Client)