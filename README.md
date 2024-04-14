# Youtube playlist AI chat
Quickly summarizes the contents of youtube videos in a public playlist and answers questions based on it.
# Demo
Working of the tool
[Screencast from 14-04-24 08:31:23 AM IST.webm](https://github.com/SaumyaRR8/Youtube-playlist-chat/assets/97652981/0874ecb1-3bb8-4369-9b2c-eead3b039546)

## Running the tool
Create `.env` file in the root directory of the project, copy and paste the below config. Replace the `OPENAI_API_TOKEN` configuration value with your key `{OPENAI_API_KEY}`. Other properties are optional to change and be default.

```bash
OPENAI_API_TOKEN={OPENAI_API_KEY}
EMBEDDER_LOCATOR=text-embedding-ada-002
EMBEDDING_DIMENSION=1536
MODEL_LOCATOR=gpt-3.5-turbo
MAX_TOKENS=200
TEMPERATURE=0.0
```

2. From the project root folder, open your terminal and run `docker-compose up`.
3. Navigate to `localhost:8501` on your browser when docker installion is successful.

#### Prerequisites

1. Make sure that [Python](https://www.python.org/downloads/) 3.10 or above installed on your machine.
2. Download and Install [Pip](https://pip.pypa.io/en/stable/installation/) to manage project packages.
3. Create an [OpenAI](https://openai.com/) account and generate a new API Key: To access the OpenAI API, you will need to create an API Key. You can do this by logging into the [OpenAI website](https://openai.com/product) and navigating to the API Key management page.

Then, follow the easy steps to install and get started using the app.
