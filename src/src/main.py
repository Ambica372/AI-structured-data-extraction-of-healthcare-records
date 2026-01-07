import json
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 1. Define the Data Structure we want
class PatientSummary(BaseModel):
    patient_name: str = Field(description="Name of the patient")
    diagnosis: str = Field(description="The main medical condition identified")
    avg_blood_pressure: str = Field(description="Average BP reading from notes")
    medications: list = Field(description="List of medications mentioned")
    follow_up_required: bool = Field(description="True if a follow-up is mentioned")

# 2. Update the run_healthcare_extraction function
def run_structured_extraction(patient_id):
    # (Keep your existing Loader and Vectorstore code here...)
    
    parser = JsonOutputParser(pydantic_object=PatientSummary)

    template = """
    Extract the following medical details from the clinical context. 
    Return ONLY a JSON object.
    
    Context: {context}
    
    {format_instructions}
    """
    
    prompt = ChatPromptTemplate.from_template(
        template,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    
    # Run and print the clean JSON
    result = chain.invoke({"context": context_text})
    print(json.dumps(result, indent=2))
    return result