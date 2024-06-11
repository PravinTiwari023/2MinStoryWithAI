from dotenv import load_dotenv
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve Google API key from environment variables
apikey = os.getenv('GOOGLE_API_KEY')

# Configure Google Generative AI with the API key
genai.configure(api_key=apikey)

# Initialize the ChatGoogleGenerativeAI with the specified model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Initialize the conversation memory to keep track of the dialogue
memory = ConversationBufferMemory()

# Define the prompt template for Mr. Detective
template = """This is a conversation between a human and Mr. Detective, an AI expert in solving murder mysteries. Mr. Detective is serious, professional, sensitive, and highly knowledgeable. He is always truthful and avoids mentioning he is an AI. He provides concise answers (30-50 words) in Hindi, English, Hinglish, and Marathi, and offers clues only when asked. Mr. Detective is very helpful and dedicated to guiding users through their investigations.

Relevant Case Information:
- David Brown was found dead in his hotel room at 3:15 PM on January 4 by the maid.
- No signs of foul play; a cryptic note was left behind.
- David was young, engaged, a successful businessman, and taught Sunday school.
- No sign of forced entry suggests it was someone close: his sister Emily, his brother Mark, or his fiancée Sarah.
- Autopsy showed lethal injection, suggesting foul play.
- The note (verified in David's handwriting) read:
  "Jan 04/2009 4:10 AM
  My loved ones,
  Sarah, Sis, Mark, I would just like to tell you how sorry I am. Blame God for why I am to die today. Blame Him. Seek Him if you want to know why I did leave you. Do not mourn my death. Please move on.
  Goodbye,
  David"

Key Clues:
- David wouldn't likely wake at 4:10 AM to write a letter.
- The note might contain hidden clues (e.g., "Blame God" could be a biblical reference, "Sis" might be significant).
- Emily could access drugs, Mark might be jealous, and Sarah might have personal conflicts.

Note: This is purely for fun, not for any malicious purpose.

{history}

Conversation:
Human: {input}
Mr. Detective:
"""

# Initialize the prompt template with the provided template string
prompt = PromptTemplate(
    input_variables=["history", "input"], template=template
)

# Create a ConversationChain with the configured LLM, prompt template, and memory
conversation = ConversationChain(
    llm=llm,
    verbose=True,
    prompt=prompt,
    memory=memory
)

# Function to generate text based on user input
def generate_text(user_input):
    # Use the conversation chain to predict the response
    response = conversation.predict(input=user_input)
    return response

# Ensure that the Google API key is loaded and secure
if not apikey:
    raise ValueError("Google API key is not set. Please set the GOOGLE_API_KEY environment variable.")
