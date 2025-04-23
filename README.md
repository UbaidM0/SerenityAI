# SerenityAI (HackUTA 1st Place)

# What It Does
SerenityAI is an AI-powered mental health companion that offers personalized support, including emotional check-ins, coping strategies, and tailored resources for managing stress and anxiety. It has a built-in chatbot trained to answer your personal queries and act as your personal therapist. SerenityAI’s chatbot processes the input using an LLM trained on therapeutic responses.

# How We Built It
We developed SerenityAI using a robust tech stack including React, Node and Tailwind CSS for the Frontend, which we integrated with our Python backend through the Flask framework and APIs. We also leveraged Databricks technologies such as LanceDB, as a vector store for dynamic context retrieval, and Delta Lakes, for structured conversation history maintenance and token limit optimization.

# How To Run It
First it is important to install the dependecies into a virtual environment by running:
 ```console
 pip install -r requirements.txt
```
Second it is important to have the frontend running which can be found at https://github.com/decloon/therapyai. After running the front end with instruction from the provided link, running the backend in parallel with the front end using:
```console
python3 app.py
```
If the app is running slow, removing the models ability to load the database can result in faster runtime although is not recommened as it provides worse results.

