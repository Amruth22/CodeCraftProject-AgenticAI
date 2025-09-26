import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from state.state import CodeCrafterState, get_file_extension

load_dotenv()

def codegen_agent(state: CodeCrafterState) -> CodeCrafterState:
    """
    Code generation agent node that creates microservice code.
    """
    print("Running code generation agent...")
    
    # Initialize the Gemini model
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GEMINI_API_KEY_2"),
        temperature=0.1
    )
    
    service_files = {}
    
    features = state.get("features", [])
    services = state.get("services", [])
    
    for feature, service in zip(features, services):
        prompt = f"""You are a senior {state['language']} backend developer.

Generate production-ready microservice code for the following:
- Feature: {feature}
- Service Name: {service}
- Architecture: {state['architecture_config'].get('architecture', 'REST')}
- Database: {state['architecture_config'].get('database', 'PostgreSQL')}
- Messaging: {state['architecture_config'].get('messaging', 'None')}
- Cache: {state['architecture_config'].get('cache', 'None')}

Generate:
1. Controller or Route handler
2. Service class/method (business logic stub)
3. Model/Schema class

Only return JSON in this format:
{{
  "controller_filename": "...",
  "controller_code": "...",
  "service_filename": "...",
  "service_code": "...",
  "model_filename": "...",
  "model_code": "..."
}}
"""
        try:
            # Create a HumanMessage with the prompt
            message = HumanMessage(content=prompt)
            
            # Generate the response
            response = model.invoke([message])
            
            # Extract the text from the response
            raw_text = response.content.strip()
            
            # Clean the response
            raw_text = raw_text.strip("```json").strip("```").strip()
            
            # Parse JSON
            parsed = json.loads(raw_text)
            
            # Add language info for file extension determination
            parsed["language"] = state["language"]
            
            service_files[service] = parsed
            
        except Exception as e:
            error_msg = f"[CodeGen Error for {service}] {e}"
            print(error_msg)
            continue

    updated_state = {
        "service_outputs": service_files,
        "codegen_complete": True,
        "codegen_error": ""
    }
    
    print("Code generation agent completed successfully")
    return {**state, **updated_state}