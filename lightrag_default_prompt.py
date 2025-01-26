GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["section", "category"]

PROMPTS["entity_extraction"] = """-Goal-
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [section, category]
Text:
During the monthly finance briefing, the CFO emphasized the importance of Section 194A for TDS on interest other than interest on securities. She explained that any interest on FDs from banks or post offices, as well as interest on loans, advances, and corporate deposits, all fall under the scope of Section 194A. According to her, this section specifically addresses scenarios where the payer (other than an individual/HUF not liable for tax audit) deducts TDS at 10% if the total interest amount crosses certain thresholds in a financial year.

She also clarified that if the interest arises from securities like government bonds or debentures covered under Section 193, it would not come under 194A. However, fixed deposit interest, interest on corporate deposits, and interest from loans or advances to residents would be captured by Section 194A, ensuring the government collects TDS on these income streams appropriately.

################
Output:
("entity"{tuple_delimiter}"194A"{tuple_delimiter}"section"{tuple_delimiter}"Section 194A deals with TDS on interest other than interest on securities, including FD interest, loans/advances, and corporate deposits."){record_delimiter}
("entity"{tuple_delimiter}"interest on FD"{tuple_delimiter}"category"{tuple_delimiter}"Interest on fixed deposits (FD) from banks or post offices is one major category under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"interest on loans and advances"{tuple_delimiter}"category"{tuple_delimiter}"Any interest arising from loans or advances extended to a resident also falls under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"interest on corporate deposits"{tuple_delimiter}"category"{tuple_delimiter}"Interest earned from corporate deposits is another category covered under Section 194A."){record_delimiter}
("relationship"{tuple_delimiter}"interest on FD"{tuple_delimiter}"194A"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on fixed deposit interest is governed by Section 194A."{tuple_delimiter}"FD, Banks"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"interest on loans and advances"{tuple_delimiter}"194A"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on interest from loans or advances falls under Section 194A."{tuple_delimiter}"loans, advances"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"interest on corporate deposits"{tuple_delimiter}"194A"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on corporate deposit interest is governed by Section 194A."{tuple_delimiter}"corporate, deposits"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194A, interest on fd, loans, time deposits, corporate deposits, loan interest, RD interest"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [section, category]
Text:
In a recent management meeting, the CFO reminded everyone about Section 194IA of the Income Tax Act, which applies when making payments on the transfer of immovable property. She stressed that if an individual or entity purchases a flat, commercial property, or a non-agricultural plot, and the transaction value crosses the prescribed threshold (typically INR 50 lakhs), TDS must be deducted under Section 194IA.

Additionally, some confusion arose regarding payments for lease or tenancy agreements for using plant, machinery, or equipment. However, these also fall under the purview of 194IA if structured as a transfer of rights in immovable property or related assets. The finance team clarified that one should carefully review each agreement to confirm if it triggers TDS under Section 194IA.

################
Output:
("entity"{tuple_delimiter}"194IA"{tuple_delimiter}"section"{tuple_delimiter}"Section 194IA covers TDS on payments for the transfer of immovable property, including purchases of flats, commercial property, and non-agricultural plots."){record_delimiter}
("entity"{tuple_delimiter}"payment on transfer of immovable property"{tuple_delimiter}"category"{tuple_delimiter}"Any sale or purchase transaction involving immovable property may require TDS under Section 194IA if it meets the threshold."){record_delimiter}
("entity"{tuple_delimiter}"purchase of flat, commercial property, or non-agricultural plot"{tuple_delimiter}"category"{tuple_delimiter}"These types of property acquisitions generally come under Section 194IA when the transaction value exceeds INR 50 lakhs."){record_delimiter}
("entity"{tuple_delimiter}"payments for lease or tenancy of plant, machinery, or equipment"{tuple_delimiter}"category"{tuple_delimiter}"If the arrangement effectively transfers certain property rights, it may also be covered under 194IA."){record_delimiter}
("relationship"{tuple_delimiter}"payment on transfer of immovable property"{tuple_delimiter}"194IA"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on payments for the transfer of immovable property is governed by Section 194IA."{tuple_delimiter}"immovable property, land, buildings, permanent fixtures, fences"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"purchase of flat, commercial property, or non-agricultural plot"{tuple_delimiter}"194IA"{tuple_delimiter}"falls under"{tuple_delimiter}"Purchases of immovable property such as flats, commercial property, and plots are subject to TDS under Section 194IA."{tuple_delimiter}"flats, commercial properties, non-agricultural plots"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"payments for lease or tenancy of plant, machinery, or equipment"{tuple_delimiter}"194IA"{tuple_delimiter}"falls under"{tuple_delimiter}"Lease or tenancy agreements transferring property rights may require TDS under Section 194IA."{tuple_delimiter}"lease, plant, machinery, equipment"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194IA,Property purchase, sale deed, real estate, flat purchase, threshold, immovable property, lease"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [section, category]
Text:
At the quarter-end review, the Accounts Head mentioned Section 194IB, which specifically applies to rent payments made by individuals or Hindu Undivided Families (HUF) who are not under tax audit. She reminded the team that if they are paying monthly rent exceeding INR 50,000 for a residential or commercial property, they must deduct TDS under Section 194IB. 

Moreover, this section covers payments made under lease, tenancy, or shared-space agreements for the use of land, building (including factory buildings), and even furniture or fittings. Although traditionally, monthly home rentals over INR 50,000 are the most common scenario, the team should remain vigilant about any similar arrangements that might trigger 194IB compliance.

################
Output:
("entity"{tuple_delimiter}"194IB"{tuple_delimiter}"section"{tuple_delimiter}"Section 194IB mandates TDS on rent payments by individuals/HUF (not under tax audit) when monthly rent exceeds INR 50,000."){record_delimiter}
("entity"{tuple_delimiter}"rent by individuals/HUF not under tax audit"{tuple_delimiter}"category"{tuple_delimiter}"This category captures rent payments where the payer is an individual or HUF not subject to tax audit."){record_delimiter}
("entity"{tuple_delimiter}"payment for lease/tenancy/shared space agreements"{tuple_delimiter}"category"{tuple_delimiter}"Lease or tenancy agreements for land, buildings (even factory buildings), or furniture/fittings fall under Section 194IB when rent exceeds INR 50,000."){record_delimiter}
("relationship"{tuple_delimiter}"rent by individuals/HUF not under tax audit"{tuple_delimiter}"194IB"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on rent payments by individuals or HUF (not under tax audit) is governed by Section 194IB."{tuple_delimiter}"rent, Hindu Undivided Family, HUF"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"payment for lease/tenancy/shared space agreements"{tuple_delimiter}"194IB"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for lease, tenancy, or shared-space agreements exceeding INR 50,000 are subject to TDS under Section 194IB."{tuple_delimiter}"lease, tenancy, shared-space, agreement"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194IB, monthly rent, residential property, commercial property,lease, tenancy, furniture, fittings"){completion_delimiter}
#############################""",
    """Example 4:

Entity_types: [section, category]
Text:
During the weekly finance workshop, the CFO highlighted Section 194C of the Income Tax Act. This section covers various payments made to contractors or sub-contractors, including those engaged in advertising contracts, transport or carriage of goods, catering services, as well as construction, repairs, and maintenance work. She also emphasized that manufacturing or processing activities, where the buyer supplies the raw materials, fall under 194C.

Additionally, the CFO pointed out that broadcasting and telecasting services (including production of programs for broadcasting) are also grouped under this section. The key point, she said, is recognizing any agreement that qualifies as a “contract” or “sub-contract”—be it for transport, advertising, or catering—should generally be examined for TDS applicability under Section 194C.

################
Output:
("entity"{tuple_delimiter}"194C"{tuple_delimiter}"section"{tuple_delimiter}"Section 194C mandates TDS on payments to contractors/sub-contractors for advertising, transport, catering, construction, and related services."){record_delimiter}
("entity"{tuple_delimiter}"payments to contractors/sub contractors"{tuple_delimiter}"category"{tuple_delimiter}"This covers any contractual work executed by contractors or sub-contractors, triggering TDS under 194C."){record_delimiter}
("entity"{tuple_delimiter}"advertising contracts"{tuple_delimiter}"category"{tuple_delimiter}"Agreements for advertising services (e.g., hoardings, digital ads, etc.) also fall under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"transport/carriage of goods"{tuple_delimiter}"category"{tuple_delimiter}"Payments for transportation or carriage of goods (with or without material) come under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"catering services"{tuple_delimiter}"category"{tuple_delimiter}"Engagements for providing catering (e.g., events, corporate catering) are subject to TDS under 194C."){record_delimiter}
("entity"{tuple_delimiter}"construction, repairs, maintenance"{tuple_delimiter}"category"{tuple_delimiter}"Works contract for building, repairs, or maintenance falls within the scope of Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"manufacturing/processing with buyer-supplied materials"{tuple_delimiter}"category"{tuple_delimiter}"If the buyer supplies raw materials and the contractor manufactures or processes goods, 194C applies."){record_delimiter}
("entity"{tuple_delimiter}"broadcasting and telecasting"{tuple_delimiter}"category"{tuple_delimiter}"This includes production of programs for broadcast, and TDS applies under Section 194C."){record_delimiter}
("relationship"{tuple_delimiter}"payments to contractors/sub contractors"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on any work executed by contractors or sub-contractors is governed by Section 194C."{tuple_delimiter}"contractors, sub-contractors"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"advertising contracts"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on advertising services, such as hoardings or digital ads, falls under Section 194C."{tuple_delimiter}"advertising, ads, hoardings"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"transport/carriage of goods"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on payments for transportation or carriage of goods is governed by Section 194C."{tuple_delimiter}"transport, carriage of goods"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"catering services"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"Catering services, including event or corporate catering, are subject to TDS under Section 194C."{tuple_delimiter}"catering, event-catering"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"construction, repairs, maintenance"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on construction, repair, and maintenance works falls under Section 194C."{tuple_delimiter}"construction, repairs, maintenance"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"manufacturing/processing with buyer-supplied materials"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"Manufacturing or processing with buyer-supplied raw materials is subject to TDS under Section 194C."{tuple_delimiter}"manufacturing, processing, raw materials"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"broadcasting and telecasting"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"Production of programs for broadcast or telecast falls under Section 194C."{tuple_delimiter}"broadcasting, telecasting, production of programs"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194C,contract, sub-contract, advertising, catering, carriage, transport, 194C, broadcasting, telecasting, production of programs, repair, maintenance, construction, manufacturing, processing, raw materials, hoardings, advertising, ads, event-catering, broadcast, telecast, production of programs"){completion_delimiter}
#############################""",
    """Example 5:
    
Entity_types: [section, category]
Text:
During the tax compliance workshop, the CFO outlined the TDS requirements under Section 194J, which broadly covers fees for professional or technical services and royalties. She explained that if the exact nature of a payment is known to be either purely technical (non-professional) or for the sale/exhibition/distribution of films (including call center services), then Section 194JA would be appropriate. On the other hand, if the payment is for professional services—like legal, medical, engineering, or accounting—or if it involves other forms of royalty (such as software usage rights), or non-compete fees, then Section 194JB applies.

However, the CFO also emphasized that sometimes the finance team may be unsure which sub-section applies. In that case, but still certain it falls under the umbrella of fees for professional/technical services or royalty, they should keep it categorized under Section 194J in general. This ensures the deduction of TDS is not overlooked while finer classification is resolved later.

################
Output:
("entity"{tuple_delimiter}"194J"{tuple_delimiter}"section"{tuple_delimiter}"Section 194J covers fees for professional or technical services and royalty as a broad category, used when 194JA/194JB classification is unclear."){record_delimiter}
("entity"{tuple_delimiter}"fees for professional or technical services and royalty"{tuple_delimiter}"category"{tuple_delimiter}"Any service or royalty potentially falling under 194J, 194JA, or 194JB, depending on specifics."){record_delimiter}
("entity"{tuple_delimiter}"194JA"{tuple_delimiter}"section"{tuple_delimiter}"194JA covers TDS on technical services (not professional), royalty for sale/distribution/exhibition of films, and call center services."){record_delimiter}
("entity"{tuple_delimiter}"technical services (not professional)"{tuple_delimiter}"category"{tuple_delimiter}"Services of a technical nature but not classified as professional consulting; TDS deduction under 194JA."){record_delimiter}
("entity"{tuple_delimiter}"royalty for sale/exhibition/distribution of films"{tuple_delimiter}"category"{tuple_delimiter}"Film-related royalties come under 194JA."){record_delimiter}
("entity"{tuple_delimiter}"call centre services"{tuple_delimiter}"category"{tuple_delimiter}"Payments to call centers are subject to TDS under 194JA."){record_delimiter}
("entity"{tuple_delimiter}"194JB"{tuple_delimiter}"section"{tuple_delimiter}"194JB covers TDS on professional services, other forms of royalty (e.g. software usage rights), and non-compete fees."){record_delimiter}
("entity"{tuple_delimiter}"professional services"{tuple_delimiter}"category"{tuple_delimiter}"Fees for legal, medical, engineering, architecture, interior design, accountancy, or advertising—deduct TDS under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"other royalty (software, brand usage, etc.)"{tuple_delimiter}"category"{tuple_delimiter}"Royalties not related to film distribution/exhibition, including software rights, fall under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"non-compete fees"{tuple_delimiter}"category"{tuple_delimiter}"Payments to refrain from competing in a business context are taxed under 194JB."){record_delimiter}
("relationship"{tuple_delimiter}"fees for professional or technical services and royalty"{tuple_delimiter}"194J"{tuple_delimiter}"falls under"{tuple_delimiter}"General category for professional/technical services and royalties falls under Section 194J when specific sub-section is unclear."{tuple_delimiter}"professional services, technical services, royalty"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"technical services (not professional)"{tuple_delimiter}"194JA"{tuple_delimiter}"falls under"{tuple_delimiter}"Non-professional technical services are subject to TDS under Section 194JA."{tuple_delimiter}"technical services, Non-professional services"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"royalty for sale/exhibition/distribution of films"{tuple_delimiter}"194JA"{tuple_delimiter}"falls under"{tuple_delimiter}"Film-related royalties fall under Section 194JA for TDS deduction."{tuple_delimiter}"royalty, films"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"call centre services"{tuple_delimiter}"194JA"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to call centers are governed by TDS provisions in Section 194JA."{tuple_delimiter}"call-centre"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"professional services"{tuple_delimiter}"194JB"{tuple_delimiter}"falls under"{tuple_delimiter}"Professional services like legal, medical, and engineering are taxed under Section 194JB."{tuple_delimiter}"professional services, legal, medical, engineering, architecture"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"other royalty (software, brand usage, etc.)"{tuple_delimiter}"194JB"{tuple_delimiter}"falls under"{tuple_delimiter}"Royalties for software and brand usage are covered under Section 194JB."{tuple_delimiter}"software, royalty, brand usage"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"non-compete fees"{tuple_delimiter}"194JB"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to prevent competition are subject to TDS under Section 194JB."{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194J, Section 194JA, Section 194JB, Consultancy fee, professional fee, technical services, software royalty, IP royalty, non-compete, software maintenance"){completion_delimiter}
#############################""",
    """Example 6:

Entity_types: [section, category]
Text:
In the latest quarterly review, the Finance Head explained Section 194Q, which is triggered when a buyer with an annual turnover exceeding INR 10 crores in the previous financial year purchases goods from a resident seller. This TDS requirement generally applies to large B2B transactions involving raw materials or finished goods, especially when the buyer’s total purchases from a single seller exceed the specified threshold (commonly INR 50 lakhs) during the current financial year.

She emphasized how this section helps ensure tax compliance in high-value business-to-business deals, reminding the team to deduct TDS under 194Q for each invoice that surpasses the aggregated threshold with any single seller.

################
Output:
("entity"{tuple_delimiter}"194Q"{tuple_delimiter}"section"{tuple_delimiter}"Section 194Q applies to buyers (turnover > INR 10 cr in the previous FY) who purchase goods from resident sellers, requiring TDS on large B2B transactions."){record_delimiter}
("entity"{tuple_delimiter}"purchase of goods from resident sellers by big buyers"{tuple_delimiter}"category"{tuple_delimiter}"Any high-value transactions (exceeding INR 50 lakhs) by a buyer with > INR 10 cr turnover fall under Section 194Q."){record_delimiter}
("relationship"{tuple_delimiter}"purchase of goods from resident sellers by big buyers"{tuple_delimiter}"194Q"{tuple_delimiter}"falls under"{tuple_delimiter}"High-value purchases of goods by buyers with turnover exceeding INR 10 crores are subject to TDS under Section 194Q."{tuple_delimiter}"big buyers, purchase of goods"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"goods purchase, raw material purchase, large B2B transactions, invoice, Section 194Q"){completion_delimiter}
#############################""",
    """Example 7:

Entity_types: [section, category]
Text:
In the latest tax compliance seminar, the CFO explained that Section 194H governs TDS on commission or brokerage payments, excluding those related to securities like shares, stocks, bonds, or mutual funds, and also excluding professional services. She cited examples such as sales commission, brokerage on property deals, and any stock/share commission if structured purely as a brokerage arrangement rather than a professional or technical service.

The CFO stressed that any such middleman fees, agent commissions, or distributor margins paid to a resident would require TDS deduction under Section 194H. She reminded the accounting team to distinguish these from payments that might fall under 194J (for professional/technical services) or other sections if they involve securities transactions.

################
Output:
("entity"{tuple_delimiter}"194H"{tuple_delimiter}"section"{tuple_delimiter}"Section 194H mandates TDS on commission or brokerage other than those involving securities or professional services."){record_delimiter}
("entity"{tuple_delimiter}"commission or brokerage (except securities)"{tuple_delimiter}"category"{tuple_delimiter}"General commission/brokerage payments not related to shares, stocks, bonds, or mutual funds fall under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"sales commission"{tuple_delimiter}"category"{tuple_delimiter}"Payment of a commission to sales agents or distributors is covered under 194H."){record_delimiter}
("entity"{tuple_delimiter}"brokerage on property"{tuple_delimiter}"category"{tuple_delimiter}"Real estate brokerage fees are subject to TDS under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"stock/share commission (if structured as brokerage)"{tuple_delimiter}"category"{tuple_delimiter}"If stock or share dealings involve a pure brokerage model, TDS on such commission is deducted under 194H."){record_delimiter}
("relationship"{tuple_delimiter}"commission or brokerage (except securities)"{tuple_delimiter}"194H"{tuple_delimiter}"falls under"{tuple_delimiter}"General commission or brokerage payments, excluding securities, are governed by Section 194H."{tuple_delimiter}"commission, brokerage"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"sales commission"{tuple_delimiter}"194H"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on sales commission paid to agents or distributors is covered under Section 194H."{tuple_delimiter}"sales commission, agents, distributors"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"brokerage on property"{tuple_delimiter}"194H"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on real estate brokerage fees is governed by Section 194H."{tuple_delimiter}"brokerage, property"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"stock/share commission (if structured as brokerage)"{tuple_delimiter}"194H"{tuple_delimiter}"falls under"{tuple_delimiter}"If stock/share transactions are structured purely as brokerage, they fall under Section 194H for TDS deduction."{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194H, Commission, brokerage, middleman fees, agent commission, stock brokerage, distributor margin"){completion_delimiter}
#############################""",
    """Example 8:

Entity_types: [section, category]
Text:
In the monthly audit checklist, the Finance Manager described scenarios labeled as “No TDS.” These generally involve agricultural income, interest or dividend below certain thresholds, payments to government institutions (like filing charges or penalties), or payments made to banks or insurance companies. The team was also informed that cash expenses made by oneself (such as petty cash reimbursements) often do not require TDS deduction.

Specifically, if an individual’s earnings from agriculture are wholly exempt, or if the interest or dividend earned is under the statutory threshold, there’s no need to deduct TDS. Likewise, government-related payments—like GST, challans for tax filing, or any official penalty—would not attract TDS under normal circumstances. Additionally, routine insurance premiums paid to an insurance company or fees paid to a bank for services are considered “No TDS” categories as they do not meet TDS applicability requirements.

################
Output:
("entity"{tuple_delimiter}"No TDS"{tuple_delimiter}"section"{tuple_delimiter}"This category covers payments or incomes where TDS is not applicable, including agriculture, small interest/dividends, government payments, bank/insurance payments, and reimbursements."){record_delimiter}
("entity"{tuple_delimiter}"agricultural income"{tuple_delimiter}"category"{tuple_delimiter}"Earnings from agriculture are generally exempt and fall under 'No TDS'."){record_delimiter}
("entity"{tuple_delimiter}"interest or dividend below a certain threshold"{tuple_delimiter}"category"{tuple_delimiter}"Small-scale interest or dividends under the statutory limit do not require TDS deduction."){record_delimiter}
("entity"{tuple_delimiter}"payment to government institutions"{tuple_delimiter}"category"{tuple_delimiter}"Filing charges, penalties, and other amounts paid to government bodies typically have 'No TDS'."){record_delimiter}
("entity"{tuple_delimiter}"payment to any bank or insurance company"{tuple_delimiter}"category"{tuple_delimiter}"Premiums or service fees paid to banks/insurers often do not attract TDS."){record_delimiter}
("entity"{tuple_delimiter}"cash expenses or reimbursements"{tuple_delimiter}"category"{tuple_delimiter}"Out-of-pocket or petty cash reimbursements by oneself do not require TDS deduction."){record_delimiter}
("relationship"{tuple_delimiter}"agricultural income"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Income from agriculture is exempt from TDS and categorized under 'No TDS.'"{tuple_delimiter}"agricultural income"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"interest or dividend below a certain threshold"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Small-scale interest or dividends under statutory limits are categorized as 'No TDS.'"{tuple_delimiter}"dividend income, threshold"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"payment to government institutions"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to government bodies for filing charges, penalties, or taxes are covered under 'No TDS.'"{tuple_delimiter}"government, authority"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"payment to any bank or insurance company"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Premiums or service fees paid to banks or insurers are categorized as 'No TDS.'"{tuple_delimiter}"banking, insurance premium"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"cash expenses or reimbursements"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Reimbursements or cash expenses made by oneself do not attract TDS and are categorized under 'No TDS.'"{tuple_delimiter}"cash expenses, reimbursements"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"minor interest, small dividends, agriculture, government authority, challan, gst, penalty, insurance premium, filing charges, custom duty, excise duty, bank fee, insurance premium, cash expenses, reimbursements, No TDS"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown."""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

The term 'High Level Keyword' is reffered to a term that can be directly seen in the transaction. Low level keywords open the boundaries in that domain and include terms that can be directly related to the transaction. Remember, when giving the high level and low level keywords, you should consider the provided setions and their descriptions of tds when selecting the keywords.

provided_sections: ["194C", "194JA", "194JB", "194Q", "194A", "194IA", "194IB", "194H", "No TDS"]

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "GBPA - 88356 ~ Bill Printing;POD printing & attachment	Bill Printing & Postage Charges-Bill Printing Charges"
################
Output:
{
  "high_level_keywords": ["Bill Printing", "Postage Charges", "Delivery Services"],
  "low_level_keywords": ["Payment to Contractor", "Work Contract", "Carriage of Goods"]
}
Reasoning for high_level_keywords & low_level_keywords: 'Bill Printing' categorized as part of 'manufacturing contract' or a 'work contract'. 'Postage or delivery services' can also relate to 'carriage of goods' when viewed as an extension of the primary contract.
#############################""",
#     """Example 2:

# Query: "What are the environmental consequences of deforestation on biodiversity?"
# ################
# Output:
# {
#   "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
#   "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
# }
# #############################""",
#     """Example 3:

# Query: "What is the role of education in reducing poverty?"
# ################
# Output:
# {
#   "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
#   "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
# }
# #############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate the following two points and provide a similarity score between 0 and 1 directly:
1. Whether these two questions are semantically similar
2. Whether the answer to Question 2 can be used to answer Question 1
Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""

PROMPTS["mix_rag_response"] = """---Role---

You are a professional assistant responsible for answering questions based on knowledge graph and textual information. Please respond in the same language as the user's question.

---Goal---

Generate a concise response that summarizes relevant points from the provided information. If you don't know the answer, just say so. Do not make anything up or include information where the supporting evidence is not provided.

When handling information with timestamps:
1. Each piece of information (both relationships and content) has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content/relationship and the timestamp
3. Don't automatically prefer the most recent information - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Data Sources---

1. Knowledge Graph Data:
{kg_context}

2. Vector Data:
{vector_context}

---Response Requirements---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Aim to keep content around 3 paragraphs for conciseness
- Each paragraph should be under a relevant section heading
- Each section should focus on one main point or aspect of the answer
- Use clear and descriptive section titles that reflect the content
- List up to 5 most important reference sources at the end under "References", clearly indicating whether each source is from Knowledge Graph (KG) or Vector Data (VD)
  Format: [KG/VD] Source content

Add sections and commentary to the response as appropriate for the length and format. If the provided information is insufficient to answer the question, clearly state that you don't know or cannot provide an answer in the same language as the user's question."""
