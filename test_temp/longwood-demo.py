
import os
os.environ["HF_HOME"] = "/n/lw_groups/cores/ccb/lab/models" ## path with memory to save your models
os.environ["TOKENIZERS_PARALLELISM"] = "false"


from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt
import torch 
import time 
import json
import tqdm
## configurations


model_name = "Qwen/Qwen3-235B-A22B-Instruct-2507"  #"Qwen/Qwen3-30B-A3B-Instruct-2507"  # "Qwen/Qwen3-4B-Instruct-2507"
model_id = "Qwen"
batch_size = 32  # adjust based on GPU/CPU memory
output_imagePath = 'longwood.png'

def load_model_and_tokenizer(model_name):
    # load the tokenizer and the model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print ('...tokenizer loaded')
    tokenizer.padding_side='left'
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype="auto",
        device_map="auto"
    )

    print ('...model loaded')
    return model, tokenizer

def get_ProcessedDataset(dataset_name):
    
    ## load data from Hugging Face
    data = load_dataset(dataset_name)

    ## filter the dataset by the validation dataset
    data = data['validation'].to_pandas()

    ## Filter the dataset by single questions:
    data = data[data.choice_type =='single']

    ## Filter the dataset by Subject_names : [ 'Dental', 'Pathology','Surgery', 'Medicine', 'Anaesthesia', 'Radiology']
    subject_names = [ 'Dental', 'Pathology','Surgery', 'Medicine', 'Anaesthesia', 'Radiology']
    data = data[data.subject_name.isin(subject_names)]

    # Show final data shape
    data.reset_index(inplace=True, drop=True)
    print (f'Dataset was loaded.\n Final dataset shape: {data.shape}')
        
    return data


## Helper functions to prapare data for inference
def generate_message(query):

    """
    Constructs a message for an AI assistant to answer a medical multiple-choice question.

    The function returns a list of messages formatted for use with chat-based language models
    (e.g., OpenAI's GPT API), setting the assistant's role and providing context with an example.

    The assistant is instructed to act as a medical doctor and select the correct answer from 
    the given choices (A to D) without explanation.

    Parameters:
        query (str): The medical multiple-choice question formatted with options.

    Returns:
        list: A list of dictionaries representing the chat message history. It includes:
            - A system message with detailed instructions and an example format.
            - A user message containing the input query.
    """
    instruction = '''You are a medical doctor answering real-world medical entrance exam questions.
     Based on your understanding of basic and clinical science, medical knowledge, and mechanisms underlying health, 
     disease, patient care, and modes of therapy, answer the following multiple-choice question.
     Select one correct answer from A to D. Do not provide reasons. Only the letter of the correct answer. 
     Follow the example below.'''

    example_query = '''Question: Chronic urethral obstruction due to benign prismatic hyperplasia can lead to the following change in kidney parenchyma:
    (A) Hyperplasia
    (B) Hyperophy
    (C) Atrophy
    (D) Dyplasia
    Answer: C'''


    message = [
    {"role": "system", "content": f"You are a helpful AI assistant. {instruction} \n\n Example:\n\n{example_query}"}, 
    {"role": "user", "content": f"{query}"}
    ]
    return message

## Helper function to prapare data for inference
def create_query(x):

    """
    Formats a dictionary containing a medical question and answer choices into a structured prompt.

    The function accepts a dictionary with a question and four options, and returns a string 
    formatted as a multiple-choice question, suitable for passing to a language model.

    Parameters:
        x (dict): A dictionary with the following keys:
            - 'question' (str): The question text.
            - 'opa' (str): Option A.
            - 'opb' (str): Option B.
            - 'opc' (str): Option C.
            - 'opd' (str): Option D.

    Returns:
        str: A formatted multiple-choice question string with options labeled (A) to (D).
    """

    question = x['question']
    option_A = x['opa']
    option_B = x['opb']
    option_C = x['opc']
    option_D =  x['opd']
    prompt = f'''Question: {question}
    (A) {option_A}
    (B) {option_B}
    (C) {option_C}
    (D) {option_D}
    '''
    
    return prompt

# To parse the model answer.
def extract_answer(x):
    x = x.lower()
    x = x.split(':')[-1]    
    return x.strip()

def  compute_accuracy(y_pred, y_true):
    count=0
    for y, yi in zip(y_pred, y_true):
        if y==yi:
            count +=1
    return count/len(y_true)

def batch_inference(messages, ids, model, tokenizer):
    responses = {}
    start_time = time.time()
    for i in tqdm.tqdm(range(0, len(messages), batch_size),desc="Processing data"):
        batch = messages[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        # Tokenize entire batch
        model_inputs = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(model.device)
        
        # Generate outputs for this batch
        with torch.no_grad():
            generated_ids = model.generate(
                **model_inputs, 
                do_sample=False,
                max_new_tokens=250,
            )

        # Decode 
        answers_ids = []
        for idx in range(len(generated_ids)):
            sample_ids = generated_ids[idx]
          #  print(idx, tokenizer.decode(sample_ids, skip_special_tokens=True))
            idx_answer= len(model_inputs.input_ids[idx])
            answers_ids.append(sample_ids[idx_answer:])
        generated_batch = tokenizer.batch_decode(answers_ids, skip_special_tokens=True)
        
        # store
        for id_, response in  zip(batch_ids, generated_batch):
            responses[id_] = response

        if i%10==0:
            # save checkpoint:
            output_path = "longwood-demo-LLMresponses-checkpoint.json"
            save_json(output_path = output_path, dictionary_ = responses)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Execution time: {end_time - start_time:.4f} seconds")
    # print (responses)
    return responses

def plot_results(image_path,df):
  
    # Plot bar chart
    ax = df.plot(kind='bar')  # each column is hue, each index is category
    plt.xlabel("Accuracy")
    plt.ylabel("Subjects")
    plt.title("Performance")
    plt.xticks(rotation= 'horizontal')
    plt.tight_layout()
    # Remove all spines (frames)
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.legend(title="Models", bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=2)  # Adjust legend position
    plt.savefig(image_path)

def save_json(output_path, dictionary_):
    with open(output_path, "w") as json_file:
        json.dump(dictionary_, json_file, indent=4) 


def main():
    # Step 1. load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(model_name)


    ## Step 2. load dataset
    data= get_ProcessedDataset( dataset_name = "openlifescienceai/medmcqa")[:32]

    ## Step 2. Create queries
    data['query'] = data.apply(create_query,axis=1)

    ## Step 3. Generate messages
    queries = data['query'].values
    messages = [generate_message(query) for query in queries]

    ## Step 4. Generate chat templates
    messages = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    ## Step 5. Batch inference
    responses = batch_inference(messages= messages, 
                                ids = data['id'].values, 
                                model= model, 
                                tokenizer= tokenizer)
    ### save results
    output_path = "longwood-demo-LLMresponses-1.json"
    save_json(output_path = output_path, dictionary_ = responses)
    print (f'Model outputs was saved at {output_path}')
    
    # Step 6. Parse the answers and stores
    parsed_answers= {}
    for id_ in responses:
        parsed_answers[id_] =extract_answer(responses[id_])
    data[f'pred_{model_id}'] = data['id'].map(parsed_answers)
    
    ## map prediction to 0,1,2,4
    labels2ids_dict= {'a': int(0), 'b': int(1), 'c': int(2), 'd': int(3)}
    data[f'pred_{model_id}'] = data[f'pred_{model_id}'].map(labels2ids_dict)

    # Step 7. Compute overall accuracy

    y_true = data['cop'] ### answer of the question, as per the dataset
    y_pred = data[f'pred_{model_id}'] 
    overall_accuracy = compute_accuracy(y_pred, y_true)
    print (f'Overall accuracy of {model_id}: {overall_accuracy}')


    # Step 8. Field accuracy
    subject_names = [ 'Dental', 'Pathology','Surgery', 'Medicine', 'Anaesthesia', 'Radiology'] 
    subject_accuracy = {}
    for subject in subject_names:
        X = data[data['subject_name']== subject]
        y_true = X['cop']
        y_pred = X[f'pred_{model_id}']
        subject_accuracy[subject] = compute_accuracy(y_true, y_pred)
    df_subjectAccuracies = pd.DataFrame( {model_id: subject_accuracy})
    ## show performance
    df_subjectAccuracies['Subject'] = df_subjectAccuracies.index
    print (df_subjectAccuracies)

    ## save data -- 
    data.to_csv(f'{model_id}_demoResults.csv')
    ## plot results
    plot_results(image_path = output_imagePath, df=df_subjectAccuracies )

if __name__ == "__main__":
    main()



