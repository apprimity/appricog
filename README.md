# AppriCog - an Engine to create cognitive applications 

<p>AppriCog is an innovative SDK designed to empower developers in rapidly creating production-ready Generative AI applications with ease. This framework seamlessly integrates technologies like [FastAPI](https://github.com/tiangolo/fastapi) for building APIs, [Langchain](https://github.com/langchain-ai/langchain) for cognitive backend processing, and a chatbot interface, enabling developers to build sophisticated AI-powered solutions effortlessly.<p>

## Key Features:

- **FastAPI Integration**: AppriCog engine harnesses the speed and efficiency of FastAPI, a modern Python web framework, to deliver high-performance, asynchronous APIs. With FastAPI, developers can rapidly develop, deploy, and scale AI applications with minimal effort.

- **Langchain Cognitive Backend**: Powered by Langchain, an advanced language processing framework, AppriCog enables seamless integration of natural language understanding and generation capabilities. Leveraging state-of-the-art language models, developers can build sophisticated chatbot interfaces and cognitive applications effortlessly.

- **Chatbot Interface**: AppriCog includes a user-friendly chatbot interface, allowing end-users to interact with AI-powered applications intuitively. Whether it's customer support, information retrieval, or task automation, the chatbot interface provides a seamless and engaging user experience.

- **On-Premises and Cloud Deployment**: With Docker's and FastAPI's support for both on-premises and cloud deployment, LLM powered applications built using AppriCog engine have flexibility and scalability to meet diverse deployment requirements, whether you're deploying on local servers or cloud platforms like AWS or Azure.

- **Pre-built LLM Chains**: AppriCog ships with pre-built LLM (Large Language Model) chains, including online and Wikipedia search functionalities on top of a RAG (Retriever-Augmented Generation) chain. These pre-built chains accelerate development and enable developers to get started quickly without the need for extensive configuration.

- **OAuth 2.0 Security**: AppriCog prioritizes security, incorporating OAuth 2.0-based security modules to safeguard access to AI applications. Developers can rest assured that their applications are protected against unauthorized access and data breaches.

In essence, AppriCog serves as a comprehensive toolkit for creating secured, production-ready Generative AI applications. Whether you're building customer-facing chatbots, knowledge retrieval systems, or AI-powered assistants, AppriCog empowers you to turn your AI ambitions into reality, quickly and efficiently.

## Installation

To run this SDK, you need Python 3.8 or later.

* Clone the repository to your local machine:

```
git clone https://github.com/your-username/AppriCog.git
```

* Install packages

```
pip install -r requirements.txt
```

* Run the uvicorn app

```
uvicorn main:app
```

## Usage

1. To use the SDK, set up the required environment variables for your LLM.
2. The Out of the Box (OOTB) version of this SDK will run the FastAPI application on port 7889, with the following key URLs:
    - OpenAPI Docs: [http://localhost:7889/docs](http://localhost:7889/docs)
    - Chatbot Interface: [http://localhost:7889/chatbot](http://localhost:7889/chatbot)
3. The prebuilt RAG chain is available in the `LLMKnowledgeBaseChain` class within `knowledge_base.chain.py`.
4. To add a new LLM chain, follow these steps:
   - Create a new subclass of `BaseSemanticAction` within the `src\actions\semantic` package.
   - Add Langchain-based LCEL expressions to create a Runnable as per your needs.
5. Place any new tools within the `src\actions\native` package.
6. The `KnowledgeBaseEngine` class within `src\inference_engines\knowledge_base_engine.py` triggers the OOTB RAG chain with Wikipedia and online search functionality. This is referred to as an **Inference Engine**.
7. If you need to create a new inference engine, add a new subclass accordingly into this directory and use it in the `inference_router.py` file.
8. The prebuilt RAG chain relies on the following folder structure to be available:
   - `src\knowledge_base\data`: Folder containing the Chroma Vector DB persist files
   - `src\knowledge_data`: Folder containing the documents needed for RAG
9. After pasting all the files needed for your RAG chain into the **_src\knowledge_data_** folder, use the **_loadData_** API endpoint to load it into the Chroma Vector DB and persist it into the **_src\knowledge_base\data_** folder.

## Please Note

1. This SDK is primarily created to help developers quickly create production-worthy LLM-powered applications.
2. Langchain is the main cognitive backend supported in this SDK, with plans to add support for other LLM frameworks in the future.
3. If you haven't already, check out [Langchain](https://github.com/langchain-ai/langchain). It's one of the best things that happened to the world since the Internet!
4. Please follow the guidance from Langchain repositories while setting up your developer machines for the required environment variables.
   
