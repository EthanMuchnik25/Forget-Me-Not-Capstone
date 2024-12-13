from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate, HumanMessagePromptTemplate
import os

def setup_local_llm(model_path: str, temperature: float = 0.7):
    """
    Set up a local LLM using LlamaCpp
    
    Args:
        model_path: Path to the downloaded model file
        temperature: Temperature parameter for text generation
        
    Returns:
        LlamaCpp: Configured LLM instance
    """
    # Set up callback manager for streaming output
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    
    try:
        # Initialize the LLM
        llm = LlamaCpp(
            model_path=model_path,
            temperature=temperature,
            callback_manager=callback_manager,
            verbose=True,
            n_ctx=2048,  # Context window
            n_gpu_layers=1  # Number of layers to offload to GPU (if available)
        )
        return llm
    except Exception as e:
        print(f"Error initializing LLM: {str(e)}")
        raise

def create_chain(llm, template: str):
    """
    Create a LangChain chain with the given LLM and prompt template
    
    Args:
        llm: The initialized LLM
        template: Prompt template string
        
    Returns:
        LLMChain: Configured chain
    """
    prompt = PromptTemplate.from_template(template)
    chain = LLMChain(prompt=prompt, llm=llm)
    return chain

def main():
    # Path to your downloaded model
    model_path = "/Users/ethanmuchnik/Downloads/Meta-Llama-3.1-8B-Instruct.f16.gguf"  # Update this path


    template ="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

    Cutting Knowledge Date: December 2023
    Today Date: 23 July 2024

    You are a helpful assistant
    
    I need you to identify the object that is being looked for and only provide that word

    <|eot_id|><|start_header_id|>user<|end_header_id|>

    Hey uhhh where is myu pencil<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    
    prompt = PromptTemplate(
    input_variables=["system_prompt", "user_prompt"],
    template=template
    )

    llm = setup_local_llm(model_path)
    
    response = llm(prompt.format(system_prompt="system_prompt", user_prompt="user_prompt"))
    
    print(response)
    return response

if __name__ == "__main__":
    main()