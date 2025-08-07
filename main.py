import os
import argparse
import logging
from dotenv import load_dotenv
from langchain_gradientai import ChatGradientAI

from fallback_llm import FallbackChatGradientAI, MockFallbackChatGradientAI
from models import GradientModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def basic_example():
    """Basic usage example with ChatGradientAI"""
    print("=== Basic ChatGradientAI Example ===")
    llm = ChatGradientAI(
        model="llama3.3-70b-instruct",
        api_key=os.getenv("DIGITALOCEAN_INFERENCE_KEY")
    )
    
    result = llm.invoke("What is the capital of France?")
    print(f"Result: {result}")

def real_fallback_example():
    """Example showing fallback configuration with real models"""
    print("=== Fallback Configuration Example ===")
    print("(Both models configured for fallback - first model should succeed)")
    
    models = [
        GradientModel.LLAMA3_3_70B_INSTRUCT,
        GradientModel.LLAMA3_8B_INSTRUCT,
    ]
    
    fallback_llm = FallbackChatGradientAI(models=models)
    
    try:
        result = fallback_llm.invoke("Explain quantum computing in simple terms.")
        print(f"✅ Primary model succeeded (no fallback needed): {result}")
    except Exception as e:
        logger.error(f"❌ All models failed: {e}")
        print(f"Note: This would normally trigger fallback to {models[1].value}")
    print()

def mock_fallback_example():
    """Example demonstrating fallback behavior using mock"""
    print("=== Mock: Fallback Demo ===")
    print("(First model will fail, second model will make real API call)")
    
    models = [
        GradientModel.LLAMA3_3_70B_INSTRUCT,     # Will fail (mocked)
        GradientModel.LLAMA3_8B_INSTRUCT,        # Real API call
    ]
    
    fallback_llm = MockFallbackChatGradientAI(models=models)
    
    try:
        result = fallback_llm.invoke("Explain quantum computing in simple terms.")
        print(f"✅ Fallback successful! Second model responded: {result}")
    except Exception as e:
        logger.error(f"❌ All models failed: {e}")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LangChain Gradient AI Fallback Examples')
    parser.add_argument('--basic', action='store_true', help='Run basic ChatGradientAI example')
    parser.add_argument('--mock', action='store_true', help='Run mock fallback demonstration')
    args = parser.parse_args()
    
    if args.basic:
        print("Running basic example...\n")
        basic_example()
    elif args.mock:
        print("Running mock demonstration (first provider fails, second makes real API call)...\n")
        mock_fallback_example()
    else:
        print("Running real fallback example (shows fallback configuration, no forced failures)...\n")
        real_fallback_example()