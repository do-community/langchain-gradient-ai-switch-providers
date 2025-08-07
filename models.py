from enum import Enum


class GradientModel(Enum):
    ALIBABA_QWEN3_32B = "alibaba-qwen3-32b"
    ANTHROPIC_CLAUDE_3_OPUS = "anthropic-claude-3-opus"
    ANTHROPIC_CLAUDE_3_5_HAIKU = "anthropic-claude-3.5-haiku"
    ANTHROPIC_CLAUDE_3_5_SONNET = "anthropic-claude-3.5-sonnet"
    ANTHROPIC_CLAUDE_3_7_SONNET = "anthropic-claude-3.7-sonnet"
    DEEPSEEK_R1_DISTILL_LLAMA_70B = "deepseek-r1-distill-llama-70b"
    LLAMA3_8B_INSTRUCT = "llama3-8b-instruct"
    LLAMA3_3_70B_INSTRUCT = "llama3.3-70b-instruct"
    MISTRAL_NEMO_INSTRUCT_2407 = "mistral-nemo-instruct-2407"
    OPENAI_GPT_4O = "openai-gpt-4o"
    OPENAI_GPT_4O_MINI = "openai-gpt-4o-mini"
    OPENAI_O3 = "openai-o3"
    OPENAI_O3_MINI = "openai-o3-mini"