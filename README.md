# langchain-gradient-ai-switch-providers
How to switch providers in LangChain easily with DigitalOcean Gradient AI

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for package management, so ensure it is [installed](https://docs.astral.sh/uv/getting-started/installation/).

Next, you will need a DigitalOcean Gradient™ AI Platform serverless inferencing key:

1. Log in to the [DigitalOcean Cloud console](https://cloud.digitalocean.com/login)
2. Click `Agent Platform` in the sidebar, and then click the `Serverless inference` tab 
3. Click `Create model access key` and follow the prompts to create the key
4. Rename `.env.example` to `.env` and then paste the created key as the value for `DIGITALOCEAN_INFERENCE_KEY`

Visit our Docs to see an up-to-date list of [available Foundation and Embedding models](https://docs.digitalocean.com/products/gradient-platform/details/models/).







`FallbackChatGradientAI`:
takes in a list of models.
_create_llm just makes the chatgradientai object with a given model (so we can switch models)
_invoke_with_retry - tries multiple times to call the llm (invoke it). After it makes two attempts (and they both fail), then it raises an exception (`RetryError` from `tenacity` library)
invoke - try to call each model. if the _invoke_with_retry for that model fails (meaning that model was tried multiple times, all failing), an exception is raised and the loop moved on to the next model. It repeats this until success, or until reaching the last model in which case it raises an exception with the last error message

