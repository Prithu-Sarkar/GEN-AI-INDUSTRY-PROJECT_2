from fastapi import FastAPI
from pydantic import BaseModel
from functions.symptom_extractor import extract_symptoms
from functions.diagnosis_symptoms import get_diagnosis
from functions.pubmed_articles import fetch_pubmed_articles_with_metadata
from functions.summerize_pubmed import summarize_text

app = FastAPI(title="ClinisightAI - Medical Diagnosis API")


class SymptomInput(BaseModel):
    description: str


@app.post("/diagnosis")
def diagnosis(data: SymptomInput):
    """
    Full medical diagnosis pipeline:
    1. Extract symptoms from free-text description.
    2. Generate LLM diagnosis.
    3. Fetch PubMed research articles.
    4. Summarise research abstracts.
    """
    symptom = extract_symptoms(data.description)
    diagnosis_result = get_diagnosis(symptom)
    pubmed_articles = fetch_pubmed_articles_with_metadata(" ".join(symptom))

    # Concatenate abstracts (cap at 3000 chars to stay within token limits)
    combined_abstracts = " ".join(
        a.get("abstract", "") for a in pubmed_articles
    )[:3000]
    summary = summarize_text(combined_abstracts)

    return {
        "symptom": symptom,
        "diagnosis": diagnosis_result,
        "pubmed_articles": pubmed_articles,
        "pubmed_summary": summary
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)