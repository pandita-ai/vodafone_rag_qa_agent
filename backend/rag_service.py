import os
import openai
import chromadb
import json
from typing import List, Dict, Any
import asyncio

class RAGService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize ChromaDB with error handling
        try:
            # Try persistent storage first using new configuration
            self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        except Exception as e:
            print(f"Warning: Persistent ChromaDB failed ({e}), using in-memory storage")
            # Fallback to in-memory storage
            self.chroma_client = chromadb.Client()
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection("legal_documents")
        except:
            self.collection = self.chroma_client.create_collection("legal_documents")
        
        # Initialize database if empty
        if self.collection.count() == 0:
            self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the database with comprehensive legal documents"""
        legal_documents = [
            # Contract Law
            {
                "id": "contract_formation_1",
                "content": "A contract is formed when there is an offer, acceptance, and consideration. The offer must be clear and definite, and the acceptance must be unqualified and communicated to the offeror.",
                "metadata": {"type": "contract_law", "topic": "contract_formation"}
            },
            {
                "id": "contract_formation_2", 
                "content": "Consideration is something of value given in exchange for a promise. It can be money, goods, services, or a promise to do or not do something.",
                "metadata": {"type": "contract_law", "topic": "consideration"}
            },
            {
                "id": "contract_breach_1",
                "content": "A breach of contract occurs when one party fails to perform their obligations under the contract. The non-breaching party may seek damages, specific performance, or rescission.",
                "metadata": {"type": "contract_law", "topic": "breach_of_contract"}
            },
            {
                "id": "contract_remedies_1",
                "content": "Contract remedies include compensatory damages (actual losses), consequential damages (foreseeable losses), liquidated damages (pre-agreed amounts), and specific performance (court-ordered performance).",
                "metadata": {"type": "contract_law", "topic": "contract_remedies"}
            },
            {
                "id": "contract_statute_frauds_1",
                "content": "The Statute of Frauds requires certain contracts to be in writing, including contracts for the sale of real estate, contracts that cannot be performed within one year, and contracts for the sale of goods over $500.",
                "metadata": {"type": "contract_law", "topic": "statute_of_frauds"}
            },
            {
                "id": "contract_capacity_1",
                "content": "Contractual capacity refers to the legal ability to enter into a contract. Minors, mentally incompetent persons, and intoxicated persons may lack capacity and can void contracts.",
                "metadata": {"type": "contract_law", "topic": "contractual_capacity"}
            },
            
            # Tort Law
            {
                "id": "tort_negligence_1",
                "content": "Negligence requires four elements: duty of care, breach of duty, causation, and damages. The defendant must owe a duty of care to the plaintiff, breach that duty, and the breach must cause the plaintiff's damages.",
                "metadata": {"type": "tort_law", "topic": "negligence"}
            },
            {
                "id": "tort_negligence_2",
                "content": "The standard of care is what a reasonable person would do under the same circumstances. Professionals are held to a higher standard of care based on their expertise.",
                "metadata": {"type": "tort_law", "topic": "standard_of_care"}
            },
            {
                "id": "tort_intentional_1",
                "content": "Intentional torts include assault, battery, false imprisonment, intentional infliction of emotional distress, trespass to land, trespass to chattels, and conversion.",
                "metadata": {"type": "tort_law", "topic": "intentional_torts"}
            },
            {
                "id": "tort_strict_liability_1",
                "content": "Strict liability applies when a defendant is held liable for harm regardless of fault. This includes abnormally dangerous activities, defective products, and keeping wild animals.",
                "metadata": {"type": "tort_law", "topic": "strict_liability"}
            },
            {
                "id": "tort_defamation_1",
                "content": "Defamation is a false statement that harms someone's reputation. Libel is written defamation, slander is spoken defamation. Public figures must prove actual malice.",
                "metadata": {"type": "tort_law", "topic": "defamation"}
            },
            {
                "id": "tort_products_liability_1",
                "content": "Products liability holds manufacturers, distributors, and sellers liable for defective products. Claims can be based on design defects, manufacturing defects, or failure to warn.",
                "metadata": {"type": "tort_law", "topic": "products_liability"}
            },
            
            # Property Law
            {
                "id": "property_adverse_possession_1",
                "content": "Adverse possession allows someone to gain title to real property by occupying it openly, notoriously, exclusively, and continuously for the statutory period, usually 10-20 years depending on jurisdiction.",
                "metadata": {"type": "property_law", "topic": "adverse_possession"}
            },
            {
                "id": "property_tenancy_1",
                "content": "A tenancy is the right to possess and use property for a specific period. Types include tenancy for years (fixed term), periodic tenancy (renewing), tenancy at will (terminable by either party), and tenancy at sufferance (holdover).",
                "metadata": {"type": "property_law", "topic": "tenancy"}
            },
            {
                "id": "property_landlord_tenant_1",
                "content": "Landlord-tenant law governs the rights and duties of property owners and renters. Landlords must provide habitable premises, while tenants must pay rent and not damage property.",
                "metadata": {"type": "property_law", "topic": "landlord_tenant"}
            },
            {
                "id": "property_eminent_domain_1",
                "content": "Eminent domain allows the government to take private property for public use with just compensation. The Fifth Amendment requires both public use and just compensation.",
                "metadata": {"type": "property_law", "topic": "eminent_domain"}
            },
            {
                "id": "property_covenants_1",
                "content": "Covenants are promises that run with the land and bind future owners. Restrictive covenants limit land use, while affirmative covenants require certain actions.",
                "metadata": {"type": "property_law", "topic": "covenants"}
            },
            
            # Criminal Law
            {
                "id": "criminal_assault_1",
                "content": "Assault is the intentional creation of a reasonable apprehension of imminent harmful or offensive contact. Battery is the actual harmful or offensive contact. Assault can occur without battery.",
                "metadata": {"type": "criminal_law", "topic": "assault_battery"}
            },
            {
                "id": "criminal_theft_1",
                "content": "Theft involves taking someone else's property with the intent to permanently deprive them of it. Larceny is the basic theft crime, while robbery involves theft with force or intimidation.",
                "metadata": {"type": "criminal_law", "topic": "theft"}
            },
            {
                "id": "criminal_homicide_1",
                "content": "Homicide is the killing of one person by another. Murder requires malice aforethought, while manslaughter is killing without malice. Degrees of murder depend on intent and circumstances.",
                "metadata": {"type": "criminal_law", "topic": "homicide"}
            },
            {
                "id": "criminal_defenses_1",
                "content": "Criminal defenses include self-defense, defense of others, necessity, duress, insanity, intoxication, and mistake of fact. Each defense has specific requirements and limitations.",
                "metadata": {"type": "criminal_law", "topic": "criminal_defenses"}
            },
            {
                "id": "criminal_white_collar_1",
                "content": "White-collar crimes are non-violent financial crimes including fraud, embezzlement, insider trading, money laundering, and tax evasion. These crimes often involve complex schemes.",
                "metadata": {"type": "criminal_law", "topic": "white_collar_crime"}
            },
            
            # Constitutional Law
            {
                "id": "constitutional_first_amendment_1",
                "content": "The First Amendment protects freedom of speech, religion, press, assembly, and petition. However, these rights are not absolute and can be limited by compelling government interests.",
                "metadata": {"type": "constitutional_law", "topic": "first_amendment"}
            },
            {
                "id": "constitutional_fourth_amendment_1",
                "content": "The Fourth Amendment protects against unreasonable searches and seizures. Warrants are generally required, but exceptions include consent, plain view, and exigent circumstances.",
                "metadata": {"type": "constitutional_law", "topic": "fourth_amendment"}
            },
            {
                "id": "constitutional_due_process_1",
                "content": "Due process requires fair procedures before depriving someone of life, liberty, or property. Procedural due process requires notice and opportunity to be heard.",
                "metadata": {"type": "constitutional_law", "topic": "due_process"}
            },
            {
                "id": "constitutional_equal_protection_1",
                "content": "Equal protection requires that similarly situated people be treated similarly. Strict scrutiny applies to race and national origin, intermediate scrutiny to gender, and rational basis to other classifications.",
                "metadata": {"type": "constitutional_law", "topic": "equal_protection"}
            },
            
            # Employment Law
            {
                "id": "employment_at_will_1",
                "content": "Employment at will means either the employer or employee can terminate the employment relationship at any time, for any reason, or for no reason at all, unless there is a contract stating otherwise.",
                "metadata": {"type": "employment_law", "topic": "at_will_employment"}
            },
            {
                "id": "employment_discrimination_1",
                "content": "Employment discrimination is prohibited based on race, color, religion, sex, national origin, age, disability, and genetic information. The EEOC enforces these laws.",
                "metadata": {"type": "employment_law", "topic": "employment_discrimination"}
            },
            {
                "id": "employment_wage_hour_1",
                "content": "The Fair Labor Standards Act establishes minimum wage, overtime pay, recordkeeping, and child labor standards. Most employees are entitled to time-and-a-half for overtime.",
                "metadata": {"type": "employment_law", "topic": "wage_hour_law"}
            },
            {
                "id": "employment_harassment_1",
                "content": "Workplace harassment is unwelcome conduct based on protected characteristics that creates a hostile work environment. Employers must take reasonable steps to prevent and correct harassment.",
                "metadata": {"type": "employment_law", "topic": "workplace_harassment"}
            },
            {
                "id": "employment_whistleblower_1",
                "content": "Whistleblower protection laws protect employees who report illegal activities, safety violations, or other wrongdoing. Retaliation against whistleblowers is prohibited.",
                "metadata": {"type": "employment_law", "topic": "whistleblower_protection"}
            },
            
            # Family Law
            {
                "id": "family_divorce_1",
                "content": "No-fault divorce allows couples to dissolve their marriage without proving fault or wrongdoing by either party. Most states require a waiting period before the divorce can be finalized.",
                "metadata": {"type": "family_law", "topic": "divorce"}
            },
            {
                "id": "family_child_custody_1",
                "content": "Child custody decisions are based on the best interests of the child, considering factors like parental fitness, child's preferences, and stability. Joint custody is often preferred when possible.",
                "metadata": {"type": "family_law", "topic": "child_custody"}
            },
            {
                "id": "family_child_support_1",
                "content": "Child support is calculated based on both parents' income, the child's needs, and state guidelines. Support typically continues until the child reaches majority or becomes emancipated.",
                "metadata": {"type": "family_law", "topic": "child_support"}
            },
            {
                "id": "family_adoption_1",
                "content": "Adoption permanently transfers parental rights from birth parents to adoptive parents. The process involves home studies, background checks, and court approval.",
                "metadata": {"type": "family_law", "topic": "adoption"}
            },
            {
                "id": "family_domestic_violence_1",
                "content": "Domestic violence includes physical, emotional, or sexual abuse by a family or household member. Protective orders can be obtained to prevent contact and ensure safety.",
                "metadata": {"type": "family_law", "topic": "domestic_violence"}
            },
            
            # Intellectual Property
            {
                "id": "intellectual_property_copyright_1",
                "content": "Copyright protects original works of authorship fixed in a tangible medium of expression. It gives the owner exclusive rights to reproduce, distribute, perform, and display the work.",
                "metadata": {"type": "intellectual_property", "topic": "copyright"}
            },
            {
                "id": "intellectual_property_trademark_1",
                "content": "Trademarks protect words, symbols, or designs that identify the source of goods or services. Registration provides nationwide protection and presumption of validity.",
                "metadata": {"type": "intellectual_property", "topic": "trademark"}
            },
            {
                "id": "intellectual_property_patent_1",
                "content": "Patents protect new, useful, and non-obvious inventions for 20 years. Patent holders have the exclusive right to make, use, and sell their invention.",
                "metadata": {"type": "intellectual_property", "topic": "patent"}
            },
            {
                "id": "intellectual_property_trade_secret_1",
                "content": "Trade secrets are confidential business information that provides a competitive advantage. Protection requires reasonable efforts to maintain secrecy and independent economic value.",
                "metadata": {"type": "intellectual_property", "topic": "trade_secret"}
            },
            
            # Corporate Law
            {
                "id": "corporate_formation_1",
                "content": "Corporations are formed by filing articles of incorporation with the state. They provide limited liability, perpetual existence, and the ability to raise capital through stock sales.",
                "metadata": {"type": "corporate_law", "topic": "corporate_formation"}
            },
            {
                "id": "corporate_governance_1",
                "content": "Corporate governance involves the rules and practices by which corporations are directed and controlled. Boards of directors have fiduciary duties to shareholders.",
                "metadata": {"type": "corporate_law", "topic": "corporate_governance"}
            },
            {
                "id": "corporate_mergers_1",
                "content": "Mergers and acquisitions involve combining companies through various structures. Shareholder approval and regulatory clearance may be required depending on the transaction size.",
                "metadata": {"type": "corporate_law", "topic": "mergers_acquisitions"}
            },
            {
                "id": "corporate_securities_1",
                "content": "Securities laws regulate the offer and sale of stocks and bonds. Companies must register securities or qualify for exemptions before selling to the public.",
                "metadata": {"type": "corporate_law", "topic": "securities_law"}
            },
            
            # Administrative Law
            {
                "id": "administrative_agencies_1",
                "content": "Administrative agencies create and enforce regulations within their areas of expertise. They have rulemaking, enforcement, and adjudicatory powers.",
                "metadata": {"type": "administrative_law", "topic": "administrative_agencies"}
            },
            {
                "id": "administrative_rulemaking_1",
                "content": "Administrative rulemaking follows the Administrative Procedure Act, requiring notice, comment periods, and reasoned decision-making. Rules have the force of law.",
                "metadata": {"type": "administrative_law", "topic": "rulemaking"}
            },
            {
                "id": "administrative_judicial_review_1",
                "content": "Judicial review of agency actions is limited to questions of law and arbitrary or capricious decisions. Courts generally defer to agency expertise in technical matters.",
                "metadata": {"type": "administrative_law", "topic": "judicial_review"}
            },
            
            # Environmental Law
            {
                "id": "environmental_clean_air_1",
                "content": "The Clean Air Act regulates air pollution from stationary and mobile sources. It establishes air quality standards and requires permits for major sources.",
                "metadata": {"type": "environmental_law", "topic": "clean_air_act"}
            },
            {
                "id": "environmental_clean_water_1",
                "content": "The Clean Water Act regulates discharges into navigable waters. It requires permits for point source pollution and sets water quality standards.",
                "metadata": {"type": "environmental_law", "topic": "clean_water_act"}
            },
            {
                "id": "environmental_cercla_1",
                "content": "CERCLA (Superfund) provides for cleanup of hazardous waste sites. It imposes strict liability on potentially responsible parties and creates a cleanup fund.",
                "metadata": {"type": "environmental_law", "topic": "superfund"}
            },
            
            # Tax Law
            {
                "id": "tax_income_1",
                "content": "Federal income tax is imposed on individuals and corporations based on their income. Tax rates are progressive, with higher rates for higher income levels.",
                "metadata": {"type": "tax_law", "topic": "income_tax"}
            },
            {
                "id": "tax_deductions_1",
                "content": "Tax deductions reduce taxable income and include business expenses, charitable contributions, mortgage interest, and state and local taxes (with limitations).",
                "metadata": {"type": "tax_law", "topic": "tax_deductions"}
            },
            {
                "id": "tax_estate_1",
                "content": "Estate tax applies to transfers of wealth at death. The federal estate tax has an exemption amount, and transfers to spouses are generally tax-free.",
                "metadata": {"type": "tax_law", "topic": "estate_tax"}
            },
            
            # Bankruptcy Law
            {
                "id": "bankruptcy_chapter_7_1",
                "content": "Chapter 7 bankruptcy provides for liquidation of assets to pay creditors. It offers a fresh start for individuals and businesses that cannot reorganize.",
                "metadata": {"type": "bankruptcy_law", "topic": "chapter_7"}
            },
            {
                "id": "bankruptcy_chapter_11_1",
                "content": "Chapter 11 bankruptcy allows businesses to reorganize while continuing operations. It provides time to negotiate with creditors and develop a repayment plan.",
                "metadata": {"type": "bankruptcy_law", "topic": "chapter_11"}
            },
            {
                "id": "bankruptcy_automatic_stay_1",
                "content": "The automatic stay immediately stops most collection actions when bankruptcy is filed. It provides breathing room to develop a reorganization plan.",
                "metadata": {"type": "bankruptcy_law", "topic": "automatic_stay"}
            },
            
            # Immigration Law
            {
                "id": "immigration_visas_1",
                "content": "Immigration visas allow foreign nationals to enter the United States for specific purposes. Categories include family, employment, diversity, and humanitarian visas.",
                "metadata": {"type": "immigration_law", "topic": "visas"}
            },
            {
                "id": "immigration_naturalization_1",
                "content": "Naturalization is the process by which foreign nationals become U.S. citizens. Requirements include residency, good moral character, and knowledge of English and civics.",
                "metadata": {"type": "immigration_law", "topic": "naturalization"}
            },
            {
                "id": "immigration_deportation_1",
                "content": "Deportation proceedings can be initiated for various reasons including criminal convictions, visa violations, and fraud. Due process rights apply in removal proceedings.",
                "metadata": {"type": "immigration_law", "topic": "deportation"}
            },
            
            # Health Law
            {
                "id": "health_hipaa_1",
                "content": "HIPAA protects the privacy and security of health information. It requires safeguards for electronic health records and limits disclosure without patient consent.",
                "metadata": {"type": "health_law", "topic": "hipaa"}
            },
            {
                "id": "health_malpractice_1",
                "content": "Medical malpractice occurs when healthcare providers breach their duty of care, causing patient harm. It requires expert testimony and often involves complex causation issues.",
                "metadata": {"type": "health_law", "topic": "medical_malpractice"}
            },
            {
                "id": "health_informed_consent_1",
                "content": "Informed consent requires healthcare providers to disclose material risks and alternatives before treatment. Patients must have capacity to understand and make decisions.",
                "metadata": {"type": "health_law", "topic": "informed_consent"}
            }
        ]
        
        # Add documents to collection
        for doc in legal_documents:
            self.collection.add(
                documents=[doc["content"]],
                metadatas=[doc["metadata"]],
                ids=[doc["id"]]
            )
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI's API"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    async def query(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Query the RAG system with a user question"""
        
        # Generate embedding for the query using OpenAI
        query_embedding = self._get_embedding(query)
        
        # Search for similar documents
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=max_results
        )
        
        # Extract relevant documents
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []
        
        # Prepare context for LLM
        context = "\n\n".join(documents)
        
        # Generate answer using OpenAI
        prompt = f"""
        You are a legal assistant helping paralegals with legal research. 
        Based on the following legal documents, answer the user's question accurately and professionally.
        
        Legal Documents:
        {context}
        
        User Question: {query}
        
        Please provide a clear, accurate answer based on the legal documents provided. 
        If the documents don't contain enough information to answer the question, say so.
        Include relevant citations to the legal concepts mentioned.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable legal assistant specializing in helping paralegals with legal research and document analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content
            
            # Calculate confidence based on similarity scores
            confidence = 1.0 - (sum(distances) / len(distances)) if distances else 0.5
            
            # Prepare sources
            sources = []
            for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                sources.append({
                    "content": doc[:200] + "..." if len(doc) > 200 else doc,
                    "metadata": metadata,
                    "relevance_score": 1.0 - distance
                })
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": min(confidence, 1.0)
            }
            
        except Exception as e:
            return {
                "answer": f"I apologize, but I encountered an error while processing your request: {str(e)}",
                "sources": [],
                "confidence": 0.0
            }
