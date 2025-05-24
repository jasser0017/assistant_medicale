
from groq import Groq


class FinalGenerator:
    def __init__(self, client:Groq, model="meta-llama/llama-4-maverick-17b-128e-instruct"):
        if not client:
            raise ValueError("La clé API Groq n'est pas définie. Vérifie ton fichier .env.")
        self.client = client
        self.model = model
    def generate(self,question: str,intent: str,clarification: str | None ,rag_snippets: list[str],memory: str,user_profile: str,instruction: str | None = None ) -> str:
        

        system_prompt =(
            f"Tu es un assistant médical intelligent, empathique, multilingue, et contextuel.\n"
    "Tu échanges avec un utilisateur dans une conversation continue, et tu dois toujours tenir compte de l’historique.\n\n"

    "Voici les règles strictes que tu dois suivre :\n"
    "1. Si un prénom est mentionné, utilise-le pour personnaliser ta réponse (ex : Bonjour Jasser).\n"
    "2. Si un sujet médical a déjà été discuté (ex : diabète), reprends-le sans reposer les mêmes questions.\n"
    "3. Si une clarification a déjà été obtenue (ex : type 1), **n’en demande pas une autre** inutilement.\n"
    "4. Si l’utilisateur dit : « tous les symptômes », interprète cela comme une requête complète et donne tous les symptômes correspondants, sans relance.\n"
    "5. Si l’utilisateur dit « tu te souviens de mon nom ? » ou « de quoi on parlait ? », réfère-toi au contexte pour répondre précisément.\n"
    "6. Réponds toujours dans la langue de la requête de l’utilisateur.\n"
    f"7. Adapte ton style et ton niveau selon le profil utilisateur suivant : {user_profile}.\n"
    "8. Si la demande concerne une urgence (douleur aiguë, cancer, détresse...), reste neutre et recommande de consulter un professionnel humain."


)



        


        context_parts = [f"🧠 Intention détectée : {intent}"]
        if instruction:
            context_parts.append(f"📌 Instruction spéciale :\n{instruction}")
        if clarification:
            context_parts.append(f"❓ Clarification : {clarification}")
        if memory:
            context_parts.append(f"📂 Dossier connu :\n{memory}")
        if rag_snippets:
            context_parts.append("📚 Informations scientifiques :\n" + "\n---\n".join(rag_snippets))

        context_parts.append(f"📝 Question : {question}")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "\n\n".join(context_parts)}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()
'''
if __name__ == "__main__":
    generator=FinalGenerator()
    print(generator.generate(
    question="J’ai mal au ventre depuis hier",
    intent="diagnostic",
    clarification=None,
    rag_snippets=['Clinical and pathological characteristics and treatment of gastric cancer during pregnancy.\n\nClinical and pathological characteristics and treatment of gastric cancer during pregnancy.\n\nThis study was conducted to investigate the clinical and pathological characteristics of patients with pregnancy-associated gastric cancer.', 'Study of immunosenescence in the occurrence and immunotherapy of gastrointestinal malignancies.\n\nStudy of immunosenescence in the occurrence and immunotherapy of gastrointestinal malignancies.\n\nIn human beings heterogenous, pervasive and lethal malignancies of different parts of the gastrointestinal (GI) tract viz., tumours of the oesophagus, stomach, small intestine, colon, and rectum, represent gastrointestinal malignancies. Primary treatment modality for gastric cancer includes chemotherapy, surgical interventions, radiotherapy, monoclonal antibodies and inhibitors of angiogenesis. However, there is a need to improve upon the existing treatment modality due to associated adverse events and the development of resistance towards treatment. Additionally, age has been found to contribute to increasing the incidence of tumours due to immunosenescence-associated immunosuppression. Immunosenescence is the natural process of ageing, wherein immune cells as well as organs begin to deteriorate resulting in a dysfunctional or malfunctioning immune system. Accretion of senescent cells in immunosenescence results in the creation of a persistent inflammatory environment or inflammaging, marked with elevated expression of pro-inflammatory and immunosuppressive cytokines and chemokines. Perturbation in the T-cell pools and persistent stimulation by the antigens facilitate premature senility of the immune cells, and senile immune cells exacerbate inflammaging conditions and the inefficiency of the immune system to identify the tumour antigen. Collectively, these conditions contribute positively towards tumour generation, growth and eventually proliferation. Thus, activating the immune cells to distinguish the tumour cells from normal cells and invade them seems to be a logical strategy for the treatment of cancer. Consequently, various approaches to immunotherapy, viz., programmed death ligand-1 (PD-1) inhibitors, Cytotoxic T-lymphocyte-associated protein 4 (CTLA-4) inhibitors etc are being extensively evaluated for their efficiency in gastric cancer. In fact, PD-1 inhibitors have been sanctioned as late late-line therapy modality for gastric cancer. The present review will focus on deciphering the link between the immune system and gastric cancer, and the alterations in the immune system that incur during the development of gastrointestinal malignancies. Also, the mechanism of evasion by tumour cells and immune checkpoints involved along with different approaches of immunotherapy being evaluated in different clinical trials will be discussed.', 'Successful treatment of gastropulmonary fistula in a patient with gastric diverticulum: A case report.\n\nSuccessful treatment of gastropulmonary fistula in a patient with gastric diverticulum: A case report.\n\nGastropulmonary fistula (GPF) is defined as a communication pathway between the stomach and the lung. GPF is a rare condition, and there is no consensus regarding its treatment. GPF has been reported in only a small number of cases.', 'Gastric Cancer: Rapid Evidence Review.\n\nGastric Cancer: Rapid Evidence Review.\n\nGastric cancer is one of the deadliest and most diagnosed cancers, although the annual incidence has been steadily decreasing. Gastric cancer risk is multifactorial with a clear association with Helicobacter pylori infection. In the United States, the age-adjusted annual incidence is 4.1 per 100,000 people with a mortality rate of 1.6; the global adjusted annual incidence is roughly twice as much with a mortality rate four times higher. No randomized controlled trials have demonstrated the benefit of endoscopy or serum pepsinogen measurement in screening for gastric cancer. Patients are often asymptomatic or have general symptoms such as weight loss, abdominal pain, nausea, and anorexia, which can preclude an early diagnosis. When gastric cancer is suspected, the recommended initial test is upper gastrointestinal endoscopy with multiple tissue biopsies. A multidisciplinary treatment team should be assembled, and shared decision-making should occur with consideration of cancer staging, comorbidities, and available treatments. Treatment is guided by extent of disease, histopathology, and tumor biomarkers. Chemotherapy and radiation, in addition to various targeted therapies, may be treatment options for tumors regardless of resectability. Prognosis is directly related to the extent of disease at diagnosis; the 5-year survival rate of treated localized disease is more than 70% vs less than 10% for distant metastatic disease.', 'Gastrointestinal cytomegalovirus infection in persons with HIV: a retrospective case series study.\n\nGastrointestinal cytomegalovirus infection in persons with HIV: a retrospective case series study.\n\nGastrointestinal (GI) cytomegalovirus (CMV) infection remains an important cause of morbidity among persons with HIV (PWH), even in the late antiretroviral therapy (ART) era. However, its varied clinical presentations and outcomes are not fully understood.'],
    memory={"âge": "34 ans", "antécédents": "aucun"},
    user_profile="Patient"
))
'''