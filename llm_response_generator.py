import google.generativeai as genai
import time

genai.configure(api_key='AIzaSyDBU_GtdGpaipQ7parq3p3h-tjzZQFrtiI')

# Set up the model settings
generation_config = {
  "temperature": 0.75,
  "top_p": 1,
  "top_k": 100,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  }
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Define the functions to apply to each row

# Gemini
def get_llm_response(prompt):
    try:
        response = model.generate_content(prompt)
        response = response.text
        time.sleep(0.85)
        return response
    except Exception as e:
        print("Error in the llm response: ", e)
        time.sleep(60)
        return "Error in the llm response: " + e