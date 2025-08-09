import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0, 
            groq_api_key=os.getenv("GROQ_API_KEY"), 
            model_name="llama3-70b-8192"
        )

    def infer_news(self, cleaned_text, ticker):
        prompt_extract = PromptTemplate.from_template(
            """
            ### Current News About {TICKER} Stock:
            {page_data}
            ### INSTRUCTIONS:
            You are given 5 current news article about {TICKER} Stock in JSON format (`title`,`link`,`content`).
            Please:
            1. Summarize the article into one short and crisp point.
            2. Assess how this news will likely affect the stock price: label the reception as 'Positive', 'Neutral' or 'Negative'.
            3. Rate the impact on a scale from 1 (lowest) to 10 (highest).
            Return the response ONLY as valid JSON with the following keys:
            {{
            "article": "<summary>",
            "reception": "<Positive, Neutral or Negative>",
            "impact": <integer between 1 and 10>
            }}
            Do NOT include any text outside the JSON object.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        # Compose chain: prompt + llm
        chain_extract = prompt_extract | self.llm

        # Pass both variables used in prompt
        response = chain_extract.invoke(input={"page_data": cleaned_text, "TICKER": ticker})

        # res might be a string, ensure correct access
        content = response.content if hasattr(response, "content") else response

        try:
            json_parser = JsonOutputParser()
            parsed = json_parser.parse(content)
        except OutputParserException as e:
            raise OutputParserException(f"Error parsing JSON output: {str(e)}")

        # Return list for consistency, even if single dict
        return parsed if isinstance(parsed, list) else [parsed]


if __name__ == "__main__":
    print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
