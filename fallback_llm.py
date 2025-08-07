import os
import logging
from typing import List, Optional, Any
from unittest.mock import Mock
from langchain_gradientai import ChatGradientAI

from models import GradientModel


logger = logging.getLogger(__name__)


class FallbackChatGradientAI:
    """
    A wrapper around ChatGradientAI that provides automatic fallback to different models
    when requests fail.
    """
    
    def __init__(
        self, 
        models: List[GradientModel], 
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the fallback LLM with a list of models to try in order.
        
        Args:
            models: List of GradientModel enums to try in order
            api_key: DigitalOcean API key (defaults to env var)
            **kwargs: Additional arguments to pass to ChatGradientAI
        """
        if not models:
            raise ValueError("At least one model must be provided")
            
        self.models = models
        self.api_key = api_key or os.getenv("DIGITALOCEAN_INFERENCE_KEY")
        self.kwargs = kwargs
        
        if not self.api_key:
            raise ValueError("API key must be provided or set in DIGITALOCEAN_INFERENCE_KEY")
    
    def _create_llm(self, model: GradientModel) -> ChatGradientAI:
        """Create a ChatGradientAI instance for the given model."""
        return ChatGradientAI(
            model=model.value,
            api_key=self.api_key,
            **self.kwargs
        )
    
    
    def invoke(self, input_data: Any) -> Any:
        """
        Invoke the LLM with automatic fallback to other models on failure.
        
        Args:
            input_data: The input to send to the LLM
            
        Returns:
            The LLM response
            
        Raises:
            Exception: If all models fail
        """
        last_exception = None
        
        for i, model in enumerate(self.models):
            logger.info(f"Attempting request with model: {model.value}")
            
            try:
                llm = self._create_llm(model)
                result = llm.invoke(input_data)
                
                if i > 0:
                    logger.info(f"Successfully fell back to model: {model.value}")
                
                return result
                
            except Exception as e:
                logger.warning(f"Model {model.value} failed: {str(e)}")
                last_exception = e
                continue
        
        # If we get here, all models failed
        raise Exception(f"All models failed. Last error: {str(last_exception)}")


class MockFallbackChatGradientAI(FallbackChatGradientAI):
    """
    Mock version of FallbackChatGradientAI for testing fallback behavior.
    Automatically fails the first model to demonstrate fallback functionality.
    """
    
    def __init__(
        self, 
        models: List[GradientModel], 
        fail_first: bool = True,
        failure_message: str = "Mocked failure for testing",
        **kwargs
    ):
        """
        Initialize mock fallback LLM.
        
        Args:
            models: List of GradientModel enums to try in order
            fail_first: Whether to fail the first model (default: True)
            failure_message: Custom failure message for mock
            **kwargs: Additional arguments to pass to parent class
        """
        super().__init__(models, **kwargs)
        self.fail_first = fail_first
        self.failure_message = failure_message
    
    def _create_llm(self, model: GradientModel) -> ChatGradientAI:
        """Create LLM instance, mocking failure for first model if enabled."""
        if self.fail_first and model == self.models[0]:
            # Return mock that always fails
            mock_instance = Mock()
            mock_instance.invoke.side_effect = Exception(self.failure_message)
            return mock_instance
        
        # All other models use real implementation
        return super()._create_llm(model)
    
