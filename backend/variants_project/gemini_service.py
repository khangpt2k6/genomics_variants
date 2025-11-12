import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("google-generativeai not installed. Install with: pip install google-generativeai")

from variants.models import Variant, ClinicalSignificance, DrugResponse

logger = logging.getLogger(__name__)


class GeminiService:
    
    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai package is required. Install with: pip install google-generativeai")
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required. Get your free API key from https://aistudio.google.com/app/apikey")
        
        model_name = os.getenv('GEMINI_MODEL', model_name)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        
        logger.info(f"Initialized Gemini service with model: {model_name}")
        
    def generate_text(self, prompt: str, temperature: float = 0.7, max_tokens: int = 8192) -> str:
        try:
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": min(max_tokens, 8192),
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Error generating text with Gemini: {str(e)}")
            if "429" in str(e) or "quota" in str(e).lower():
                raise Exception("Rate limit exceeded. Please wait before making another request.")
            raise


class VariantInterpreter(GeminiService):
    
    def generate_variant_summary(self, variant: Variant) -> Dict[str, Any]:
        variant_data = self._prepare_variant_data(variant)
        
        prompt = f"""
You are a genetic counselor and variant interpretation expert. Analyze the following genetic variant data and provide a comprehensive, accurate summary.

Variant Information:
- Chromosome: {variant.chromosome}
- Position: {variant.position}
- Reference Allele: {variant.reference_allele}
- Alternate Allele: {variant.alternate_allele}
- Gene Symbol: {variant.gene_symbol or 'Unknown'}
- Consequence: {variant.consequence or 'Unknown'}
- Impact: {variant.impact or 'Unknown'}
- gnomAD Frequency: {variant.gnomad_af if variant.gnomad_af else 'Not available'}

Clinical Significance:
{self._format_clinical_significance(variant)}

Drug Responses:
{self._format_drug_responses(variant)}

Please provide:
1. A clear, concise summary of what this variant is
2. The functional impact in plain language
3. Clinical significance interpretation
4. Population frequency context
5. Any relevant drug response information
6. Key points for clinicians

Format your response as JSON with these keys:
- summary: Brief overview (2-3 sentences)
- functional_impact: Explanation of functional impact
- clinical_interpretation: Clinical significance explanation
- population_context: Population frequency context
- drug_implications: Drug response implications
- key_points: Array of 3-5 key points for clinicians
- confidence_level: Your confidence in the interpretation (high/medium/low)

Be accurate, evidence-based, and use accessible language while maintaining scientific accuracy.
"""
        
        try:
            response_text = self.generate_text(prompt, temperature=0.3)
            
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                result = {
                    "summary": response_text[:500],
                    "functional_impact": "See full explanation",
                    "clinical_interpretation": "See full explanation",
                    "population_context": "See full explanation",
                    "drug_implications": "See full explanation",
                    "key_points": response_text.split('\n')[:5],
                    "confidence_level": "medium",
                    "raw_response": response_text
                }
            
            return {
                "variant_id": variant.variant_id,
                "generated_at": datetime.now().isoformat(),
                "interpretation": result
            }
            
        except Exception as e:
            logger.error(f"Error generating variant summary: {str(e)}")
            return {
                "variant_id": variant.variant_id,
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }
    
    def explain_clinical_significance(self, variant: Variant) -> str:
        clinical_data = variant.clinical_significance.all()
        
        if not clinical_data.exists():
            return "No clinical significance data available for this variant."
        
        prompt = f"""
Explain the clinical significance of this variant in plain language for healthcare providers:

Variant: {variant.chromosome}:{variant.position} {variant.reference_allele}>{variant.alternate_allele}
Gene: {variant.gene_symbol or 'Unknown'}

Clinical Significance Records:
{self._format_clinical_significance(variant)}

Provide:
1. What the clinical significance means
2. How confident we can be in this classification
3. What this means for patient care
4. Any important caveats or limitations

Use clear, professional language suitable for clinicians.
"""
        
        try:
            return self.generate_text(prompt, temperature=0.2)
        except Exception as e:
            logger.error(f"Error explaining clinical significance: {str(e)}")
            return f"Unable to generate explanation: {str(e)}"
    
    def generate_patient_friendly_summary(self, variant: Variant) -> Dict[str, str]:
        prompt = f"""
You are a genetic counselor explaining a genetic variant to a patient in simple, empathetic language.

Variant Information:
- Location: Chromosome {variant.chromosome}, position {variant.position}
- Change: {variant.reference_allele} changed to {variant.alternate_allele}
- Gene: {variant.gene_symbol or 'Unknown'}
- Impact: {variant.impact or 'Unknown'}

Clinical Significance:
{self._format_clinical_significance(variant)}

Create a patient-friendly explanation that:
1. Uses simple language (avoid jargon)
2. Is empathetic and supportive
3. Explains what the variant means
4. Discusses implications (if any)
5. Provides reassurance where appropriate

Format as JSON with:
- simple_explanation: What the variant is in simple terms
- what_it_means: What this means for the patient
- next_steps: Suggested next steps
- questions_to_ask: 3-5 questions the patient might want to ask their doctor
"""
        
        try:
            response_text = self.generate_text(prompt, temperature=0.4)
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return {
                    "simple_explanation": response_text,
                    "what_it_means": "Please consult with your healthcare provider",
                    "next_steps": ["Schedule a consultation with a genetic counselor"],
                    "questions_to_ask": []
                }
        except Exception as e:
            logger.error(f"Error generating patient summary: {str(e)}")
            return {
                "error": "Unable to generate patient-friendly summary",
                "message": str(e)
            }
    
    def _prepare_variant_data(self, variant: Variant) -> Dict[str, Any]:
        return {
            "chromosome": variant.chromosome,
            "position": variant.position,
            "reference_allele": variant.reference_allele,
            "alternate_allele": variant.alternate_allele,
            "gene_symbol": variant.gene_symbol,
            "consequence": variant.consequence,
            "impact": variant.impact,
            "gnomad_af": variant.gnomad_af,
        }
    
    def _format_clinical_significance(self, variant: Variant) -> str:
        clinical_data = variant.clinical_significance.all()
        if not clinical_data.exists():
            return "No clinical significance data available."
        
        formatted = []
        for cs in clinical_data:
            formatted.append(
                f"- Significance: {cs.get_significance_display()}\n"
                f"  Review Status: {cs.get_review_status_display() if cs.review_status else 'Unknown'}\n"
                f"  ClinVar ID: {cs.clinvar_id or 'N/A'}\n"
                f"  Phenotype: {cs.phenotype or 'N/A'}"
            )
        return "\n".join(formatted)
    
    def _format_drug_responses(self, variant: Variant) -> str:
        drug_responses = variant.drug_responses.all()
        if not drug_responses.exists():
            return "No drug response data available."
        
        formatted = []
        for dr in drug_responses:
            formatted.append(
                f"- Drug: {dr.drug_name}\n"
                f"  Response Type: {dr.get_response_type_display()}\n"
                f"  Evidence Level: {dr.get_evidence_level_display()}\n"
                f"  Cancer Type: {dr.cancer_type or 'N/A'}"
            )
        return "\n".join(formatted)


class NaturalLanguageQueryProcessor(GeminiService):
    
    def process_query(self, user_query: str, available_fields: List[str]) -> Dict[str, Any]:
        prompt = f"""
You are a database query assistant for a genetic variant database.

User Query: "{user_query}"

Available Fields:
{json.dumps(available_fields, indent=2)}

Convert this natural language query into structured filter criteria.

Common filter patterns:
- "pathogenic variants" -> clinical_significance__significance__in: ['pathogenic', 'likely_pathogenic']
- "BRCA genes" -> gene_symbol__in: ['BRCA1', 'BRCA2']
- "rare variants" -> gnomad_af__lt: 0.01
- "high impact" -> impact: 'HIGH'
- "drug targets" -> drug_responses__isnull: False

Return JSON with this structure:
{{
    "filters": {{
        "field_name": {{
            "operator": "exact|contains|in|lt|gt|lte|gte",
            "value": "value or array"
        }}
    }},
    "search_terms": ["list of search terms"],
    "ordering": ["field_name", "-field_name"],
    "interpretation": "What the query means in plain language"
}}

Be precise and only include filters you're confident about.
"""
        
        try:
            response_text = self.generate_text(prompt, temperature=0.1)
            result = json.loads(response_text)
            return result
        except Exception as e:
            logger.error(f"Error processing natural language query: {str(e)}")
            return {
                "filters": {},
                "search_terms": user_query.split(),
                "interpretation": "Unable to parse query",
                "error": str(e)
            }
    
    def suggest_queries(self, partial_query: str, context: Dict[str, Any] = None) -> List[str]:
        prompt = f"""
Suggest 5 natural language query completions for a genetic variant database search.

Partial Query: "{partial_query}"

Context: {json.dumps(context or {}, indent=2)}

Suggest queries that:
1. Complete the user's thought
2. Are commonly used in variant searches
3. Are grammatically correct
4. Are specific and actionable

Return as JSON array of strings.
"""
        
        try:
            response_text = self.generate_text(prompt, temperature=0.5)
            suggestions = json.loads(response_text)
            if isinstance(suggestions, list):
                return suggestions[:5]
            return []
        except Exception as e:
            logger.error(f"Error generating query suggestions: {str(e)}")
            return []


class VariantChatAssistant(GeminiService):
    
    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        super().__init__(model_name)
        self.conversation_history = []
    
    def chat(self, message: str, variant_context: Optional[Variant] = None) -> str:
        context_prompt = ""
        if variant_context:
            context_prompt = f"""
Current Variant Context:
- Variant: {variant_context.chromosome}:{variant_context.position}
- Gene: {variant_context.gene_symbol or 'Unknown'}
- Impact: {variant_context.impact or 'Unknown'}
"""
        
        history_text = ""
        if self.conversation_history:
            history_text = "\nPrevious conversation:\n"
            for entry in self.conversation_history[-5:]:
                history_text += f"User: {entry['user']}\nAssistant: {entry['assistant']}\n"
        
        prompt = f"""
You are a helpful assistant for a genetic variant analysis platform. Answer questions about genetic variants, their clinical significance, and related topics.

{context_prompt}

{history_text}

User Question: {message}

Provide a helpful, accurate answer. If you're unsure, say so. If the question requires specific variant data that isn't in context, ask for clarification.

Answer:
"""
        
        try:
            response = self.generate_text(prompt, temperature=0.7)
            
            self.conversation_history.append({
                "user": message,
                "assistant": response
            })
            
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return response
        except Exception as e:
            logger.error(f"Error in chat assistant: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def reset_conversation(self):
        self.conversation_history = []


class AnnotationEnhancer(GeminiService):
    
    def enhance_with_literature_context(self, variant: Variant) -> Dict[str, Any]:
        prompt = f"""
You are a genomics researcher. Provide literature-based context for this variant:

Variant: {variant.chromosome}:{variant.position} {variant.reference_allele}>{variant.alternate_allele}
Gene: {variant.gene_symbol or 'Unknown'}
Consequence: {variant.consequence or 'Unknown'}

Provide:
1. Known associations with this variant/gene
2. Relevant research findings
3. Pathway involvement
4. Disease associations
5. Research gaps or areas needing more study

Format as JSON with:
- associations: Array of known associations
- research_findings: Array of key research findings
- pathways: Array of biological pathways involved
- disease_associations: Array of disease associations
- research_gaps: Array of areas needing more research
- summary: Brief summary paragraph
"""
        
        try:
            response_text = self.generate_text(prompt, temperature=0.3)
            return json.loads(response_text)
        except Exception as e:
            logger.error(f"Error enhancing annotations: {str(e)}")
            return {"error": str(e)}
    
    def generate_pathway_analysis(self, variant: Variant) -> str:
        prompt = f"""
Analyze the role of this variant in biological pathways:

Variant: {variant.chromosome}:{variant.position}
Gene: {variant.gene_symbol or 'Unknown'}
Consequence: {variant.consequence or 'Unknown'}

Explain:
1. Which biological pathways this gene/variant affects
2. How the variant impacts pathway function
3. Downstream effects
4. Therapeutic implications

Provide a clear, scientific explanation.
"""
        
        try:
            return self.generate_text(prompt, temperature=0.3)
        except Exception as e:
            logger.error(f"Error generating pathway analysis: {str(e)}")
            return f"Unable to generate pathway analysis: {str(e)}"


variant_interpreter = None
query_processor = None
chat_assistant = None
annotation_enhancer = None


def get_variant_interpreter() -> VariantInterpreter:
    global variant_interpreter
    if variant_interpreter is None:
        variant_interpreter = VariantInterpreter()
    return variant_interpreter


def get_query_processor() -> NaturalLanguageQueryProcessor:
    global query_processor
    if query_processor is None:
        query_processor = NaturalLanguageQueryProcessor()
    return query_processor


def get_chat_assistant() -> VariantChatAssistant:
    global chat_assistant
    if chat_assistant is None:
        chat_assistant = VariantChatAssistant()
    return chat_assistant


def get_annotation_enhancer() -> AnnotationEnhancer:
    global annotation_enhancer
    if annotation_enhancer is None:
        annotation_enhancer = AnnotationEnhancer()
    return annotation_enhancer
