# serverless-llm-microservice-pattern

This is built on the much ![simpler design pattern of combining FastAPI & LangChain to create an LLM-powered microservice](https://github.com/tleers/llm-api-starterkit). 
If you're curious what the basic principle of that design pattern constitutes, I recommend you read https://blog.timleers.com/a-stupidly-minimal-llm-api-starterkit-deploy-llm-endpoints-in-a-minute-with-langchain-and-fastapi.

For a comprehensive guide, take a look at 
# Installation

## Development

[Poetry installation](https://python-poetry.org/docs/#installing-with-the-official-installer) is recommended.
To start:
```bash
poetry shell
poetry install
```

Alternatively, you can rely on trusty venv:
```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Text to music sample with replicate, Vicuna & audiocraft

Running the most shiny example would be the replicate prompt-to-sample endpoint. 
This takes a user prompt, converts it to a more rich text description with an LLM, and then send its to an audiocraft-powered endpoint.

**How?** Super easy if you have a Github account.
* Register on Replicate.com with your Github account.
* Copy your API token (left-click your username, then click API tokens)
* Paste the API token into your .secrets file
	* `REPLICATE_API_TOKEN=r8_***`
* Launch your API if you installed the poetry requirements `uvicorn app.serve_replicate_llm:app` or the Docker container if you have Docker installed with `docker-compose up`
* Surf to `localhost:8000/docs` and try it out.

**Pricing?** Replicate gives you a couple of free tries before they ask for a credit card (I presume, they never asked me). 

* The cost is less than 0.10$ per sample when combining Vicuna & Audiocraft (`prompt-to-sample`endpoint)
* Estimated unit costs for the Audiocraft endpoint were: $0.00055 / second. Four samples cost me about $0.17.
* Estimated unit costs for the Vicuna-13b endpoint were: $0.0023 / second. Four samples cost about $0.08.
	
**Latency?** 5 to 15 seconds for the LLM, about 60-90 seconds for sample generation.

* The LLM is deployed on Nvidia A100s. 
* The Audiocraft endpoint is deployed on Nvidia T4s. You could significantly improve latency by switching to A100s, and potentially optimize cost further.

