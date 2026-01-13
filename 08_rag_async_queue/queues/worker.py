from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

embedding_model = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")

vector_db = QdrantVectorStore.from_existing_collection(
                                                embedding=embedding_model,
                                                url = "http://localhost:6333",
                                                collection_name = "HighBrow Leave Policy") 



def process_query(query:str):
    search_result = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([f"Page Content: {result.page_content} \n Page Number: {result.metadata['page_label']} \n File Location: {result.metadata['source']}" for result in search_result])

    SYSTEM_PROMPT = f"""
    You are a helpfull AI Assistant who answers user query based on the available context retrived from. aPDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user to open the right page number to know more.

    Context:
    {context}
    """

    # Calling the LLM and giving system prompt and user query

    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[

            {"role": "system",
            "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    print(f"🤖 {response.choices[0].message.content}")
    return response.choices[0].message.content

# user this before every run in mac / run out side this folder 
# export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES