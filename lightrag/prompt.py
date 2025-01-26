GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["section", "category", "subcategory"]

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

Entity_types: [section, category, subcategory]
Text:
During the monthly finance briefing, the CFO emphasized the importance of Section 194A for TDS on interest other than interest on securities. She explained that any interest on FDs from banks or post offices, as well as interest on loans, advances, and corporate deposits, all fall under the scope of Section 194A. According to her, this section specifically addresses scenarios where the payer (other than an individual/HUF not liable for tax audit) deducts TDS at 10% if the total interest amount crosses certain thresholds in a financial year.

She also clarified that if the interest arises from securities like government bonds or debentures covered under Section 193, it would not come under 194A. However, fixed deposit interest, interest on corporate deposits, and interest from loans or advances to residents would be captured by Section 194A, ensuring the government collects TDS on these income streams appropriately.

################
Output:
("entity"{tuple_delimiter}"194A"{tuple_delimiter}"section"{tuple_delimiter}"Section 194A deals with TDS on interest other than interest on securities, including FD interest, loans/advances, and corporate deposits."){record_delimiter}
("entity"{tuple_delimiter}"interest on FD"{tuple_delimiter}"category"{tuple_delimiter}"Interest on fixed deposits (FD) from banks or post offices is one major category under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"interest on loans and advances"{tuple_delimiter}"category"{tuple_delimiter}"Any interest arising from loans or advances extended to a resident also falls under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"interest on corporate deposits"{tuple_delimiter}"category"{tuple_delimiter}"Interest earned from corporate deposits is another category covered under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"interest on savings account"{tuple_delimiter}"subcategory"{tuple_delimiter}"Interest earned from savings accounts, often offered by banks to their savings account holders, also falls under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"interest on recurring deposits"{tuple_delimiter}"subcategory"{tuple_delimiter}"Interest from recurring deposits, where regular deposits are made into an RD account, is covered under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"interest on senior citizen fixed deposits"{tuple_delimiter}"subcategory"{tuple_delimiter}"Senior citizen fixed deposits, which offer higher interest rates to senior citizens, fall under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"interest on tax-saver fixed deposits"{tuple_delimiter}"subcategory"{tuple_delimiter}"Tax-saver fixed deposits, featuring a lock-in period that qualifies for tax savings under the Income Tax Act, are included in Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"student loans"{tuple_delimiter}"subcategory"{tuple_delimiter}"Student loans, intended for educational purposes and often featuring a grace period before repayment, are governed by Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"car loans"{tuple_delimiter}"subcategory"{tuple_delimiter}"Car loans, specifically for vehicle purchases, are categorized under loans that fall within Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"home loans"{tuple_delimiter}"subcategory"{tuple_delimiter}"Home loans, or mortgages for purchasing residential property, fall under the loans category covered by Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"personal loans"{tuple_delimiter}"subcategory"{tuple_delimiter}"Personal loans, which are general purpose loans not requiring collateral, are also covered under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"overdraft facilities"{tuple_delimiter}"subcategory"{tuple_delimiter}"Interest on overdraft facilities, which occur when amounts are overdrawn from bank accounts, falls under Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"interest on inter-company deposits"{tuple_delimiter}"subcategory"{tuple_delimiter}"Inter-company deposits, where deposits are made between different companies within the same corporate group, are included in Section 194A."){record_delimiter}
("entity"{tuple_delimiter}"commercial paper interest"{tuple_delimiter}"subcategory"{tuple_delimiter}"Interest from commercial papers, short-term unsecured promissory notes issued by corporations, falls under Section 194A."){record_delimiter}
("relationship"{tuple_delimiter}"interest on FD"{tuple_delimiter}"194A"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on fixed deposit interest is governed by Section 194A."{tuple_delimiter}"FD, Banks"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"interest on loans and advances"{tuple_delimiter}"194A"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on interest from loans or advances falls under Section 194A."{tuple_delimiter}"loans, advances"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"interest on corporate deposits"{tuple_delimiter}"194A"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on corporate deposit interest is governed by Section 194A."{tuple_delimiter}"corporate, deposits"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"interest on savings account"{tuple_delimiter}"Interest other than interest on securities"{tuple_delimiter}"falls under"{tuple_delimiter}"Interest on savings accounts is a type of interest income other than securities, governed by Section 194A."{tuple_delimiter}"savings, accounts"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"interest on recurring deposits"{tuple_delimiter}"Interest other than interest on securities"{tuple_delimiter}"falls under"{tuple_delimiter}"Interest on recurring deposits is another type of interest income other than securities, covered by Section 194A."{tuple_delimiter}"recurring, deposits"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"interest on senior citizen fixed deposits"{tuple_delimiter}"Interest on FD from banks or post offices"{tuple_delimiter}"falls under"{tuple_delimiter}"Senior citizen fixed deposits fall under the category of interest on FD from banks or post offices, as per Section 194A."{tuple_delimiter}"senior, FDs"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"interest on tax-saver fixed deposits"{tuple_delimiter}"Interest on FD from banks or post offices"{tuple_delimiter}"falls under"{tuple_delimiter}"Tax-saver fixed deposits fall under the category of interest on FD from banks or post offices according to Section 194A."{tuple_delimiter}"tax-saver, FDs"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"student loans"{tuple_delimiter}"Interest on loans/advances"{tuple_delimiter}"falls under"{tuple_delimiter}"Student loans are a type of loans/advances which is governed by Section 194A."{tuple_delimiter}"student, loans"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"car loans"{tuple_delimiter}"Interest on loans/advances"{tuple_delimiter}"falls under"{tuple_delimiter}"Car loans are included under the category of loans/advances governed by Section 194A."{tuple_delimiter}"car, loans"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"home loans"{tuple_delimiter}"Interest on loans/advances"{tuple_delimiter}"falls under"{tuple_delimiter}"Home loans are a part of the loans/advances category covered under Section 194A."{tuple_delimiter}"home, loans"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"personal loans"{tuple_delimiter}"Interest on loans/advances"{tuple_delimiter}"falls under"{tuple_delimiter}"Personal loans are also part of the loans/advances category governed by Section 194A."{tuple_delimiter}"personal, loans"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"overdraft facilities"{tuple_delimiter}"Interest on loans/advances"{tuple_delimiter}"falls under"{tuple_delimiter}"Overdraft facilities are categorized under loans/advances according to Section 194A."{tuple_delimiter}"overdraft, facilities"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"interest on inter-company deposits"{tuple_delimiter}"Interest on corporate deposits"{tuple_delimiter}"falls under"{tuple_delimiter}"Inter-company deposits fall under the category of interest on corporate deposits, as per Section 194A."{tuple_delimiter}"inter-company, deposits"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"commercial paper interest"{tuple_delimiter}"Interest on corporate deposits"{tuple_delimiter}"falls under"{tuple_delimiter}"Commercial paper interest is a type of interest on corporate deposits covered by Section 194A."{tuple_delimiter}"commercial, papers"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194A, interest on securities, interest on FD, interest on loans, interest on corporate deposits, interest on savings account, interest on recurring deposits, interest on senior citizen fixed deposits, interest on tax-saver fixed deposits, student loans, car loans, home loans, personal loans, overdraft facilities, interest on inter-company deposits, commercial paper interest"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [section, category, subcategory]
Text:
In a recent management meeting, the CFO reminded everyone about Section 194IA of the Income Tax Act, which applies when making payments on the transfer of immovable property. She stressed that if an individual or entity purchases a flat, commercial property, or a non-agricultural plot, and the transaction value crosses the prescribed threshold (typically INR 50 lakhs), TDS must be deducted under Section 194IA.

Additionally, some confusion arose regarding payments for lease or tenancy agreements for using plant, machinery, or equipment. However, these also fall under the purview of 194IA if structured as a transfer of rights in immovable property or related assets. The finance team clarified that one should carefully review each agreement to confirm if it triggers TDS under Section 194IA.

################
Output:
("entity"{tuple_delimiter}"194IA"{tuple_delimiter}"section"{tuple_delimiter}"Section 194IA covers TDS on payments for the transfer of immovable property, including purchases of flats, commercial property, and non-agricultural plots."){record_delimiter}
("entity"{tuple_delimiter}"payment on transfer of immovable property"{tuple_delimiter}"category"{tuple_delimiter}"Any sale or purchase transaction involving immovable property may require TDS under Section 194IA if it meets the threshold."){record_delimiter}
("entity"{tuple_delimiter}"purchase of flat, commercial property, or non-agricultural plot"{tuple_delimiter}"category"{tuple_delimiter}"These types of property acquisitions generally come under Section 194IA when the transaction value exceeds INR 50 lakhs."){record_delimiter}
("entity"{tuple_delimiter}"payments for lease or tenancy of plant, machinery, or equipment"{tuple_delimiter}"category"{tuple_delimiter}"If the arrangement effectively transfers certain property rights, it may also be covered under 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Residential property transactions"{tuple_delimiter}"subcategory"{tuple_delimiter}"Transactions involving the transfer of ownership of houses or apartments fall under 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Agricultural land transactions"{tuple_delimiter}"subcategory"{tuple_delimiter}"Specific transactions involving agricultural land that might be exempt from TDS under certain conditions are covered under 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Industrial property transactions"{tuple_delimiter}"subcategory"{tuple_delimiter}"Transfer of properties used for industrial purposes falls under 194IA."){record_delimiter}
("entity"{tuple_delimiter}"High-value residential flats"{tuple_delimiter}"subcategory"{tuple_delimiter}"Transactions involving luxury or high-value residential apartments are governed by 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Commercial office spaces"{tuple_delimiter}"subcategory"{tuple_delimiter}"Purchase transactions for office spaces fall under 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Retail space transactions"{tuple_delimiter}"subcategory"{tuple_delimiter}"Purchases of retail spaces like shops or showrooms are covered under 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Non-agricultural land plots"{tuple_delimiter}"subcategory"{tuple_delimiter}"The purchase of land plots not used for agriculture is included in 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Lease of heavy machinery"{tuple_delimiter}"subcategory"{tuple_delimiter}"Agreements for leasing equipment used in construction or manufacturing are categorized under 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Lease of commercial vehicles"{tuple_delimiter}"subcategory"{tuple_delimiter}"Tenancy agreements for vehicles used in commercial activities fall under 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Equipment for IT and data centers"{tuple_delimiter}"subcategory"{tuple_delimiter}"Leasing of IT infrastructure and data center equipment is governed by 194IA."){record_delimiter}
("entity"{tuple_delimiter}"Plant leases in manufacturing sectors"{tuple_delimiter}"subcategory"{tuple_delimiter}"Leases of plants used in various manufacturing processes are covered under 194IA."){record_delimiter}
("relationship"{tuple_delimiter}"payment on transfer of immovable property"{tuple_delimiter}"194IA"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on payments for the transfer of immovable property is governed by Section 194IA."{tuple_delimiter}"immovable property, land, buildings, permanent fixtures, fences"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"purchase of flat, commercial property, or non-agricultural plot"{tuple_delimiter}"194IA"{tuple_delimiter}"falls under"{tuple_delimiter}"Purchases of immovable property such as flats, commercial property, and plots are subject to TDS under Section 194IA."{tuple_delimiter}"flats, commercial properties, non-agricultural plots"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"payments for lease or tenancy of plant, machinery, or equipment"{tuple_delimiter}"194IA"{tuple_delimiter}"falls under"{tuple_delimiter}"Lease or tenancy agreements transferring property rights may require TDS under Section 194IA."{tuple_delimiter}"lease, plant, machinery, equipment"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Residential property transactions"{tuple_delimiter}"Payment on transfer of immovable property"{tuple_delimiter}"falls under"{tuple_delimiter}"Transactions involving residential properties may require TDS under Section 194IA."{tuple_delimiter}"residential, property"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Agricultural land transactions"{tuple_delimiter}"Payment on transfer of immovable property"{tuple_delimiter}"falls under"{tuple_delimiter}"Agricultural land transactions, potentially exempt, still fall under the TDS provisions of Section 194IA."{tuple_delimiter}"agricultural, land"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Industrial property transactions"{tuple_delimiter}"Payment on transfer of immovable property"{tuple_delimiter}"falls under"{tuple_delimiter}"Industrial property transfers are subject to TDS under Section 194IA."{tuple_delimiter}"industrial, property"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"High-value residential flats"{tuple_delimiter}"Purchase of flat, commercial property, or non-agricultural plot"{tuple_delimiter}"falls under"{tuple_delimiter}"High-value residential flat transactions fall under Section 194IA, requiring TDS compliance."{tuple_delimiter}"high-value, flats"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Commercial office spaces"{tuple_delimiter}"Purchase of flat, commercial property, or non-agricultural plot"{tuple_delimiter}"falls under"{tuple_delimiter}"Commercial office space purchases are regulated by TDS rules under Section 194IA."{tuple_delimiter}"office, spaces"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Retail space transactions"{tuple_delimiter}"Purchase of flat, commercial property, or non-agricultural plot"{tuple_delimiter}"falls under"{tuple_delimiter}"Retail space purchases must adhere to TDS provisions under Section 194IA."{tuple_delimiter}"retail, spaces"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Non-agricultural land plots"{tuple_delimiter}"Purchase of flat, commercial property, or non-agricultural plot"{tuple_delimiter}"falls under"{tuple_delimiter}"Non-agricultural land plot purchases are subject to TDS under Section 194IA."{tuple_delimiter}"non-agricultural, land"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Lease of heavy machinery"{tuple_delimiter}"Payments for lease or tenancy agreements for use of plant, machinery, or equipment"{tuple_delimiter}"falls under"{tuple_delimiter}"Leases of heavy machinery are covered under the TDS provisions of Section 194IA."{tuple_delimiter}"heavy, machinery"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Lease of commercial vehicles"{tuple_delimiter}"Payments for lease or tenancy agreements for use of plant, machinery, or equipment"{tuple_delimiter}"falls under"{tuple_delimiter}"Commercial vehicle leases require TDS compliance under Section 194IA."{tuple_delimiter}"commercial, vehicles"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Equipment for IT and data centers"{tuple_delimiter}"Payments for lease or tenancy agreements for use of plant, machinery, or equipment"{tuple_delimiter}"falls under"{tuple_delimiter}"Leasing IT and data center equipment falls under TDS rules of Section 194IA."{tuple_delimiter}"IT, data centers"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Plant leases in manufacturing sectors"{tuple_delimiter}"Payments for lease or tenancy agreements for use of plant, machinery, or equipment"{tuple_delimiter}"falls under"{tuple_delimiter}"Plant leases in manufacturing are governed by TDS regulations under Section 194IA."{tuple_delimiter}"manufacturing, plants"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194IA, property purchase, sale deed, real estate, flat purchase, commercial property, non-agricultural plot, lease, tenancy agreements, residential property, agricultural land, industrial property, high-value residential flats, commercial office spaces, retail spaces, non-agricultural land plots, lease of heavy machinery, lease of commercial vehicles, IT equipment lease, plant leases, machinery leases, equipment leases"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [section, category, subcategory]
Text:
At the quarter-end review, the Accounts Head mentioned Section 194IB, which specifically applies to rent payments made by individuals or Hindu Undivided Families (HUF) who are not under tax audit. She reminded the team that if they are paying monthly rent exceeding INR 50,000 for a residential or commercial property, they must deduct TDS under Section 194IB. 

Moreover, this section covers payments made under lease, tenancy, or shared-space agreements for the use of land, building (including factory buildings), and even furniture or fittings. Although traditionally, monthly home rentals over INR 50,000 are the most common scenario, the team should remain vigilant about any similar arrangements that might trigger 194IB compliance.

################
Output:
("entity"{tuple_delimiter}"194IB"{tuple_delimiter}"section"{tuple_delimiter}"Section 194IB mandates TDS on rent payments by individuals/HUF (not under tax audit) when monthly rent exceeds INR 50,000."){record_delimiter}
("entity"{tuple_delimiter}"rent by individuals/HUF not under tax audit"{tuple_delimiter}"category"{tuple_delimiter}"This category captures rent payments where the payer is an individual or HUF not subject to tax audit."){record_delimiter}
("entity"{tuple_delimiter}"payment for lease/tenancy/shared space agreements"{tuple_delimiter}"category"{tuple_delimiter}"Lease or tenancy agreements for land, buildings (even factory buildings), or furniture/fittings fall under Section 194IB when rent exceeds INR 50,000."){record_delimiter}
("entity"{tuple_delimiter}"Residential rent"{tuple_delimiter}"subcategory"{tuple_delimiter}"Rent payments for residential properties like apartments and houses are taxable under 194IB."){record_delimiter}
("entity"{tuple_delimiter}"Vacation home rent"{tuple_delimiter}"subcategory"{tuple_delimiter}"Short-term rentals of vacation properties are subject to TDS under 194IB."){record_delimiter}
("entity"{tuple_delimiter}"Subletting rent"{tuple_delimiter}"subcategory"{tuple_delimiter}"Income from subletting a part or all of a rented property is covered under 194IB."){record_delimiter}
("entity"{tuple_delimiter}"Land lease agreements"{tuple_delimiter}"subcategory"{tuple_delimiter}"Leasing of agricultural, commercial, and residential land is governed by TDS provisions under 194IB."){record_delimiter}
("entity"{tuple_delimiter}"Commercial building leases"{tuple_delimiter}"subcategory"{tuple_delimiter}"Leases for commercial spaces like offices, warehouses, or factory buildings are taxable under 194IB."){record_delimiter}
("entity"{tuple_delimiter}"Residential building leases"{tuple_delimiter}"subcategory"{tuple_delimiter}"Leases for residential buildings or units are subject to TDS requirements under 194IB."){record_delimiter}
("entity"{tuple_delimiter}"Shared-space agreements"{tuple_delimiter}"subcategory"{tuple_delimiter}"Shared facilities or co-working spaces fall under the TDS regulations of 194IB."){record_delimiter}
("entity"{tuple_delimiter}"Lease of furniture and fittings"{tuple_delimiter}"subcategory"{tuple_delimiter}"Permanent fixtures leased separately, such as in furnished apartments or offices, are included under 194IB."){record_delimiter}
("relationship"{tuple_delimiter}"rent by individuals/HUF not under tax audit"{tuple_delimiter}"194IB"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on rent payments by individuals or HUF (not under tax audit) is governed by Section 194IB."{tuple_delimiter}"rent, Hindu Undivided Family, HUF"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"payment for lease/tenancy/shared space agreements"{tuple_delimiter}"194IB"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for lease, tenancy, or shared-space agreements exceeding INR 50,000 are subject to TDS under Section 194IB."{tuple_delimiter}"lease, tenancy, shared-space, agreement"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Residential rent"{tuple_delimiter}"Rent by individuals/Hindu Undivided Family"{tuple_delimiter}"falls under"{tuple_delimiter}"Rent payments for residential properties like apartments and houses are taxable under 194IB."{tuple_delimiter}"Residential rent, Individual rent, Hindu-Undivided-Family"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Vacation home rent"{tuple_delimiter}"Rent by individuals/Hindu Undivided Family"{tuple_delimiter}"falls under"{tuple_delimiter}"Short-term rentals of vacation properties are subject to TDS under 194IB."{tuple_delimiter}"Vacation home, Individual rent, Hindu-Undivided-Family"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Subletting rent"{tuple_delimiter}"Rent by individuals/Hindu Undivided Family"{tuple_delimiter}"falls under"{tuple_delimiter}"Income from subletting a part or all of a rented property is covered under 194IB."{tuple_delimiter}"Subletting, Individual rent, Hindu-Undivided-Family"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Land lease agreements"{tuple_delimiter}"Payment for lease/tenancy/shared-space agreements for use of land, building, or furniture/fittings"{tuple_delimiter}"falls under"{tuple_delimiter}"Leasing of agricultural, commercial, and residential land is governed by TDS provisions under 194IB."{tuple_delimiter}"Land lease, Lease agreements"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Commercial building leases"{tuple_delimiter}"Payment for lease/tenancy/shared-space agreements for use of land, building, or furniture/fittings"{tuple_delimiter}"falls under"{tuple_delimiter}"Leases for commercial spaces like offices, warehouses, or factory buildings are taxable under 194IB."{tuple_delimiter}"Commercial lease, Lease agreements"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Residential building leases"{tuple_delimiter}"Payment for lease/tenancy/shared-space agreements for use of land, building, or furniture/fittings"{tuple_delimiter}"falls under"{tuple_delimiter}"Leases for residential buildings or units are subject to TDS requirements under 194IB."{tuple_delimiter}"Residential lease, Lease agreements"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Shared-space agreements"{tuple_delimiter}"Payment for lease/tenancy/shared-space agreements for use of land, building, or furniture/fittings"{tuple_delimiter}"falls under"{tuple_delimiter}"Shared facilities or co-working spaces fall under the TDS regulations of 194IB."{tuple_delimiter}"Shared-space, Lease agreements"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Lease of furniture and fittings"{tuple_delimiter}"Payment for lease/tenancy/shared-space agreements for use of land, building, or furniture/fittings"{tuple_delimiter}"falls under"{tuple_delimiter}"Permanent fixtures leased separately, such as in furnished apartments or offices, are included under 194IB."{tuple_delimiter}"Furniture lease, Lease agreements"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194IB, monthly rent, residential property, commercial property, vacation homes, subletting, land leases, commercial building leases, residential building leases, shared-space agreements, furniture and fittings leases, lease agreements, tenancy agreements"){completion_delimiter}
#############################""",
    """Example 4:

Entity_types: [section, category, subcategory]
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
("entity"{tuple_delimiter}"Building construction and repair"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for services related to construction, renovation, and repair of buildings are taxable under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Electrical and plumbing installations"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments to contractors for electrical setups and plumbing works are covered under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Print media advertising"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for advertisements published in newspapers, magazines, or other print media are taxable under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Digital advertising"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for advertising services on digital platforms, including social media and search engines, are covered under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Freight transport"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for the transportation of goods by road, rail, air, or sea are taxable under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Courier services"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments specifically for courier and delivery services are governed by Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Event catering"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for catering services provided at events like weddings, conferences, or parties are taxable under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Corporate catering"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for services provided for corporate offices, meetings, or daily office meals are covered under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Food processing"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments to contractors who handle the processing of food products are taxable under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Textile manufacturing"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for the manufacturing and processing of textiles are governed by Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Program production"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments to contractors for the production of television or radio programs are taxable under Section 194C."){record_delimiter}
("entity"{tuple_delimiter}"Live broadcasting services"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for the live broadcasting of events or shows are covered under Section 194C."){record_delimiter}
("relationship"{tuple_delimiter}"payments to contractors/sub contractors"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on any work executed by contractors or sub-contractors is governed by Section 194C."{tuple_delimiter}"contractors, sub-contractors"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"advertising contracts"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on advertising services, such as hoardings or digital ads, falls under Section 194C."{tuple_delimiter}"advertising, ads, hoardings"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"transport/carriage of goods"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on payments for transportation or carriage of goods is governed by Section 194C."{tuple_delimiter}"transport, carriage of goods"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"catering services"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"Catering services, including event or corporate catering, are subject to TDS under Section 194C."{tuple_delimiter}"catering, event-catering"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"construction, repairs, maintenance"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on construction, repair, and maintenance works falls under Section 194C."{tuple_delimiter}"construction, repairs, maintenance"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"manufacturing/processing with buyer-supplied materials"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"Manufacturing or processing with buyer-supplied raw materials is subject to TDS under Section 194C."{tuple_delimiter}"manufacturing, processing, raw materials"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"broadcasting and telecasting"{tuple_delimiter}"194C"{tuple_delimiter}"falls under"{tuple_delimiter}"Production of programs for broadcast or telecast falls under Section 194C."{tuple_delimiter}"broadcasting, telecasting, production of programs"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Building construction and repair"{tuple_delimiter}"Payments to contractors/subcontractors"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for services related to construction, renovation or repair of buildings are taxable under Section 194C."{tuple_delimiter}"Construction, building repair, contractors"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Electrical and plumbing installations"{tuple_delimiter}"Payments to contractors/subcontractors"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to contractors for electrical setups and plumbing works are taxable under Section 194C."{tuple_delimiter}"Electrical, plumbing, contractors"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Print media advertising"{tuple_delimiter}"Advertising contracts"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for advertisements published in newspapers, magazines, or other print media are taxable under Section 194C."{tuple_delimiter}"Print media, advertising"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Digital advertising"{tuple_delimiter}"Advertising contracts"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for advertising services on digital platforms, including social media and search engines, are covered under Section 194C."{tuple_delimiter}"Digital, advertising"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Freight transport"{tuple_delimiter}"Transport/carriage of goods"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for the transportation of goods by road, rail, air, or sea are taxable under Section 194C."{tuple_delimiter}"Freight, transport, carriage"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Courier services"{tuple_delimiter}"Transport/carriage of goods"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments specifically for courier and delivery services are governed by Section 194C."{tuple_delimiter}"Courier, delivery services"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Event catering"{tuple_delimiter}"Catering services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for catering services provided at events like weddings, conferences, or parties are taxable under Section 194C."{tuple_delimiter}"Event, catering, services"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Corporate catering"{tuple_delimiter}"Catering services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for services provided for corporate offices, meetings, or daily office meals are covered under Section 194C."{tuple_delimiter}"Corporate, catering, services"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Food processing"{tuple_delimiter}"Manufacturing/processing"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to contractors who handle the processing of food products are taxable under Section 194C."{tuple_delimiter}"Food, processing, contractors"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Textile manufacturing"{tuple_delimiter}"Manufacturing/processing"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for the manufacturing and processing of textiles are governed by Section 194C."{tuple_delimiter}"Textile, manufacturing, contractors"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Program production"{tuple_delimiter}"Broadcasting and telecasting (including production of programs for broadcasting)"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to contractors for the production of television or radio programs are taxable under Section 194C."{tuple_delimiter}"Program production, broadcasting"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Live broadcasting services"{tuple_delimiter}"Broadcasting and telecasting (including production of programs for broadcasting)"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for the live broadcasting of events or shows are covered under Section 194C."{tuple_delimiter}"Live broadcasting, events, shows"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194C, contract, sub-contract, advertising, catering, carriage, transport, 194C, broadcasting, telecasting, production of programs, repair, maintenance, construction, manufacturing, processing, raw materials, hoardings, ads, event catering, corporate catering, print media advertising, digital advertising, freight transport, courier services, building repair, electrical installations, plumbing setups, food processing, textile manufacturing, live broadcasting, program production"){completion_delimiter}
#############################""",
    """Example 5:
    
Entity_types: [section, category, subcategory]
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
("entity"{tuple_delimiter}"IT support services"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments made for maintenance and troubleshooting for hardware or software systems are taxed under 194JA."){record_delimiter}
("entity"{tuple_delimiter}"Industrial technical services"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments made for advisory or maintenance services for manufacturing equipment or production lines fall under 194JA."){record_delimiter}
("entity"{tuple_delimiter}"Maintenance contracts for machinery"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for ongoing technical upkeep of industrial machinery are included under 194JA."){record_delimiter}
("entity"{tuple_delimiter}"Theatrical release royalties"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments made for film screening rights in cinemas are taxable under 194JA."){record_delimiter}
("entity"{tuple_delimiter}"Digital distribution royalties"{tuple_delimiter}"subcategory"{tuple_delimiter}"Earnings from streaming or online platform distribution are subject to 194JA."){record_delimiter}
("entity"{tuple_delimiter}"Television broadcast royalties"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees for broadcasting films on TV networks fall under 194JA."){record_delimiter}
("entity"{tuple_delimiter}"Inbound customer support services"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for handling customer inquiries and complaints via call centers are included in 194JA."){record_delimiter}
("entity"{tuple_delimiter}"Outbound sales campaigns"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for telemarketing or promotional calling campaigns are taxable under 194JA."){record_delimiter}
("entity"{tuple_delimiter}"Technical helpline services"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments made for troubleshooting support provided via phone are governed by 194JA."){record_delimiter}
("entity"{tuple_delimiter}"Legal services"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees for legal consultation, contract drafting, or representation in legal proceedings are taxed under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Engineering consulting"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for specialized advice or designs for infrastructure projects fall under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Architectural planning"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees for developing detailed plans and designs for buildings or renovations are included under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Medical consulting"{tuple_delimiter}"subcategory"{tuple_delimiter}"Expert medical opinions or diagnostic services are taxable under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Advertising consultancy"{tuple_delimiter}"subcategory"{tuple_delimiter}"Strategic planning and creative direction fees for marketing campaigns fall under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Business non-compete agreements"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments made to individuals or entities to refrain from competing in a specific market are taxable under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Employee non-compete clauses"{tuple_delimiter}"subcategory"{tuple_delimiter}"Compensation to employees who agree not to join competitors for a certain period is taxed under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Software licensing fees"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for the right to use proprietary software are included under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Brand licensing royalties"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees paid to use a trademarked brand name fall under 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Intellectual property usage fees"{tuple_delimiter}"subcategory"{tuple_delimiter}"Compensation for using patented technologies or proprietary methodologies is governed by 194JB."){record_delimiter}
("entity"{tuple_delimiter}"Management consultancy fees"{tuple_delimiter}"subcategory"{tuple_delimiter}"Charges for expert advice on business operations or strategies are taxable under 194J."){record_delimiter}
("entity"{tuple_delimiter}"Accounting and auditing services"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees for financial record-keeping, compliance, and audits fall under 194J."){record_delimiter}
("entity"{tuple_delimiter}"Scientific research consulting"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments to experts providing research insights or laboratory services are included under 194J."){record_delimiter}
("entity"{tuple_delimiter}"Tax advisory services"{tuple_delimiter}"subcategory"{tuple_delimiter}"Guidance on tax planning, filing, and compliance is taxed under 194J."){record_delimiter}
("entity"{tuple_delimiter}"Music publishing royalties"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments made for the use of musical compositions are governed by 194J."){record_delimiter}
("entity"{tuple_delimiter}"Patent licensing royalties"{tuple_delimiter}"subcategory"{tuple_delimiter}"Income derived from granting permission to use patented inventions is taxable under 194J."){record_delimiter}
("entity"{tuple_delimiter}"Literary or artistic royalties"{tuple_delimiter}"subcategory"{tuple_delimiter}"Earnings from books, artwork, or creative content usage fall under 194J."){record_delimiter}
("relationship"{tuple_delimiter}"fees for professional or technical services and royalty"{tuple_delimiter}"194J"{tuple_delimiter}"falls under"{tuple_delimiter}"General category for professional/technical services and royalties falls under Section 194J when specific sub-section is unclear."{tuple_delimiter}"professional services, technical services, royalty"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"technical services (not professional)"{tuple_delimiter}"194JA"{tuple_delimiter}"falls under"{tuple_delimiter}"Non-professional technical services are subject to TDS under Section 194JA."{tuple_delimiter}"technical services, Non-professional services"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"royalty for sale/exhibition/distribution of films"{tuple_delimiter}"194JA"{tuple_delimiter}"falls under"{tuple_delimiter}"Film-related royalties fall under Section 194JA for TDS deduction."{tuple_delimiter}"royalty, films"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"call centre services"{tuple_delimiter}"194JA"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to call centers are governed by TDS provisions in Section 194JA."{tuple_delimiter}"call-centre"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"professional services"{tuple_delimiter}"194JB"{tuple_delimiter}"falls under"{tuple_delimiter}"Professional services like legal, medical, and engineering are taxed under Section 194JB."{tuple_delimiter}"professional services, legal, medical, engineering, architecture"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"other royalty (software, brand usage, etc.)"{tuple_delimiter}"194JB"{tuple_delimiter}"falls under"{tuple_delimiter}"Royalties for software and brand usage are covered under Section 194JB."{tuple_delimiter}"software, royalty, brand usage"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"non-compete fees"{tuple_delimiter}"194JB"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to prevent competition are subject to TDS under Section 194JB."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"IT support services"{tuple_delimiter}"Technical Services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for maintenance and troubleshooting for hardware or software systems are subject to TDS under Section 194JA."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Industrial technical services"{tuple_delimiter}"Technical Services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for advisory or maintenance services for manufacturing equipment or production lines are taxable under Section 194JA."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Maintenance contracts for machinery"{tuple_delimiter}"Technical Services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for ongoing technical upkeep of industrial machinery are covered under Section 194JA."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Theatrical release royalties"{tuple_delimiter}"Royalty (in connection with sale, distribution or exhibition of films)"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments made for film screening rights in cinemas are taxable under Section 194JA."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Digital distribution royalties"{tuple_delimiter}"Royalty (in connection with sale, distribution or exhibition of films)"{tuple_delimiter}"falls under"{tuple_delimiter}"Earnings from streaming or online platform distribution are subject to Section 194JA."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Television broadcast royalties"{tuple_delimiter}"Royalty (in connection with sale, distribution or exhibition of films)"{tuple_delimiter}"falls under"{tuple_delimiter}"Fees for broadcasting films on TV networks are taxable under Section 194JA."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Inbound customer support services"{tuple_delimiter}"Call centre services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for handling customer inquiries and complaints via call centers are covered under Section 194JA."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Outbound sales campaigns"{tuple_delimiter}"Call centre services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for telemarketing or promotional calling campaigns are taxable under Section 194JA."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Technical helpline services"{tuple_delimiter}"Call centre services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments made for troubleshooting support provided via phone are governed by Section 194JA."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Legal services"{tuple_delimiter}"Professional services"{tuple_delimiter}"falls under"{tuple_delimiter}"Fees for legal consultation, contract drafting, or representation in legal proceedings are taxed under Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Engineering consulting"{tuple_delimiter}"Professional services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for specialized advice or designs for infrastructure projects fall under Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Architectural planning"{tuple_delimiter}"Professional services"{tuple_delimiter}"falls under"{tuple_delimiter}"Fees for developing detailed plans and designs for buildings or renovations are included under Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Medical consulting"{tuple_delimiter}"Professional services"{tuple_delimiter}"falls under"{tuple_delimiter}"Expert medical opinions or diagnostic services are taxable under Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Advertising consultancy"{tuple_delimiter}"Professional services"{tuple_delimiter}"falls under"{tuple_delimiter}"Strategic planning and creative direction fees for marketing campaigns fall under Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Business non-compete agreements"{tuple_delimiter}"Non compete fees"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments made to individuals or entities to refrain from competing in a specific market are taxable under Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Employee non-compete clauses"{tuple_delimiter}"Non compete fees"{tuple_delimiter}"falls under"{tuple_delimiter}"Compensation to employees who agree not to join competitors for a certain period is taxed under Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Software licensing fees"{tuple_delimiter}"Other Royalty"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for the right to use proprietary software are included under Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Brand licensing royalties"{tuple_delimiter}"Other Royalty"{tuple_delimiter}"falls under"{tuple_delimiter}"Fees paid to use a trademarked brand name fall under Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Intellectual property usage fees"{tuple_delimiter}"Other Royalty"{tuple_delimiter}"falls under"{tuple_delimiter}"Compensation for using patented technologies or proprietary methodologies is governed by Section 194JB."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Management consultancy fees"{tuple_delimiter}"Fees for professional services"{tuple_delimiter}"falls under"{tuple_delimiter}"Charges for expert advice on business operations or strategies are taxable under Section 194J."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Accounting and auditing services"{tuple_delimiter}"Fees for professional services"{tuple_delimiter}"falls under"{tuple_delimiter}"Fees for financial record-keeping, compliance, and audits fall under Section 194J."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Scientific research consulting"{tuple_delimiter}"Fees for professional services"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to experts providing research insights or laboratory services are included under Section 194J."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Tax advisory services"{tuple_delimiter}"Fees for professional services"{tuple_delimiter}"falls under"{tuple_delimiter}"Guidance on tax planning, filing, and compliance is taxed under Section 194J."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Music publishing royalties"{tuple_delimiter}"Royalties"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments made for the use of musical compositions are governed by Section 194J."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Patent licensing royalties"{tuple_delimiter}"Royalties"{tuple_delimiter}"falls under"{tuple_delimiter}"Income derived from granting permission to use patented inventions is taxable under Section 194J."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Literary or artistic royalties"{tuple_delimiter}"Royalties"{tuple_delimiter}"falls under"{tuple_delimiter}"Earnings from books, artwork, or creative content usage fall under Section 194J."{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194J, Section 194JA, Section 194JB, consultancy fee, professional fee, legal services, medical consulting, engineering consulting, architectural planning, advertising consultancy, non-compete, software royalty, IP royalty, maintenance contracts, technical services, IT support services, industrial technical services, digital distribution royalties, theatrical release royalties, television broadcast royalties, inbound customer support, outbound sales campaigns, technical helpline services, software licensing fees, brand licensing royalties, intellectual property usage fees, management consultancy, tax advisory, scientific research consulting, accounting and auditing, music publishing royalties, patent licensing royalties, literary royalties"){completion_delimiter}
#############################""",
    """Example 6:

Entity_types: [section, category, subcategory]
Text:
In the latest quarterly review, the Finance Head explained Section 194Q, which is triggered when a buyer with an annual turnover exceeding INR 10 crores in the previous financial year purchases goods from a resident seller. This TDS requirement generally applies to large B2B transactions involving raw materials or finished goods, especially when the buyer’s total purchases from a single seller exceed the specified threshold (commonly INR 50 lakhs) during the current financial year.

She emphasized how this section helps ensure tax compliance in high-value business-to-business deals, reminding the team to deduct TDS under 194Q for each invoice that surpasses the aggregated threshold with any single seller.

################
Output:
("entity"{tuple_delimiter}"194Q"{tuple_delimiter}"section"{tuple_delimiter}"Section 194Q applies to buyers (turnover > INR 10 cr in the previous FY) who purchase goods from resident sellers, requiring TDS on large B2B transactions."){record_delimiter}
("entity"{tuple_delimiter}"purchase of goods from resident sellers by big buyers"{tuple_delimiter}"category"{tuple_delimiter}"Any high-value transactions (exceeding INR 50 lakhs) by a buyer with > INR 10 cr turnover fall under Section 194Q."){record_delimiter}
("entity"{tuple_delimiter}"Bulk commodity purchases"{tuple_delimiter}"subcategory"{tuple_delimiter}"Transactions involving the bulk procurement of raw materials or commodities (e.g., steel, coal, and cement) are taxable under Section 194Q."){record_delimiter}
("entity"{tuple_delimiter}"Seasonal agricultural product purchases"{tuple_delimiter}"subcategory"{tuple_delimiter}"Large-scale procurement of crops such as grains, pulses, or cotton from resident farmers or cooperatives is taxable under Section 194Q."){record_delimiter}
("entity"{tuple_delimiter}"Wholesale supplier purchases"{tuple_delimiter}"subcategory"{tuple_delimiter}"Regular acquisitions of inventory from large resident wholesalers are covered under Section 194Q."){record_delimiter}
("entity"{tuple_delimiter}"Industrial raw materials"{tuple_delimiter}"subcategory"{tuple_delimiter}"Purchases of industrial inputs like chemicals, metals, or plastics that are essential for manufacturing processes are taxable under Section 194Q."){record_delimiter}
("entity"{tuple_delimiter}"Manufactured goods"{tuple_delimiter}"subcategory"{tuple_delimiter}"Large-volume transactions of finished products, such as machinery, tools, or consumer goods, from resident suppliers are included under Section 194Q."){record_delimiter}
("entity"{tuple_delimiter}"Custom-built goods"{tuple_delimiter}"subcategory"{tuple_delimiter}"Purchases of items tailored to specific buyer requirements, such as custom equipment or specially produced components, fall under Section 194Q."){record_delimiter}
("entity"{tuple_delimiter}"Recurring supply contracts"{tuple_delimiter}"subcategory"{tuple_delimiter}"Ongoing agreements where goods are supplied on a regular basis (monthly or quarterly) are subject to Section 194Q."){record_delimiter}
("relationship"{tuple_delimiter}"purchase of goods from resident sellers by big buyers"{tuple_delimiter}"194Q"{tuple_delimiter}"falls under"{tuple_delimiter}"High-value purchases of goods by buyers with turnover exceeding INR 10 crores are subject to TDS under Section 194Q."{tuple_delimiter}"big buyers, purchase of goods"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Bulk commodity purchases"("relationship"{tuple_delimiter}"Bulk commodity purchases"{tuple_delimiter}"Purchase of goods from resident sellers by big buyers"{tuple_delimiter}"falls under"{tuple_delimiter}"Transactions involving the bulk procurement of raw materials or commodities are subject to TDS under Section 194Q."{tuple_delimiter}"bulk procurement, commodity"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Seasonal agricultural product purchases"{tuple_delimiter}"Purchase of goods from resident sellers by big buyers"{tuple_delimiter}"falls under"{tuple_delimiter}"Large-scale procurement of crops such as grains, pulses, or cotton from resident farmers or cooperatives falls under Section 194Q."{tuple_delimiter}"agricultural products, seasonal crops"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Wholesale supplier purchases"{tuple_delimiter}"Purchase of goods from resident sellers by big buyers"{tuple_delimiter}"falls under"{tuple_delimiter}"Regular acquisitions of inventory from large resident wholesalers are taxable under Section 194Q."{tuple_delimiter}"wholesale, suppliers"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Industrial raw materials"{tuple_delimiter}"Purchase/supply of goods"{tuple_delimiter}"falls under"{tuple_delimiter}"Purchases of industrial inputs like chemicals, metals, or plastics that are essential for manufacturing processes are subject to TDS under Section 194Q."{tuple_delimiter}"industrial raw materials, manufacturing"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Manufactured goods"{tuple_delimiter}"Purchase/supply of goods"{tuple_delimiter}"falls under"{tuple_delimiter}"Large-volume transactions of finished products, such as machinery, tools, or consumer goods, are covered under Section 194Q."{tuple_delimiter}"manufactured goods, finished products"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Custom-built goods"{tuple_delimiter}"Purchase/supply of goods"{tuple_delimiter}"falls under"{tuple_delimiter}"Purchases of items tailored to specific buyer requirements, such as custom equipment or specially produced components, fall under Section 194Q."{tuple_delimiter}"custom-built goods, tailor-made"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Recurring supply contracts"{tuple_delimiter}"Purchase/supply of goods"{tuple_delimiter}"falls under"{tuple_delimiter}"Ongoing agreements where goods are supplied on a regular basis are subject to TDS under Section 194Q."{tuple_delimiter}"recurring supply, regular contracts"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194Q, goods purchase, raw material purchase, large B2B transactions, invoice, bulk commodity purchases, seasonal agricultural product purchases, wholesale supplier purchases, industrial raw materials, manufactured goods, custom-built goods, recurring supply contracts, agricultural products, chemicals, metals, plastics, machinery, tools, consumer goods, custom equipment, components, regular contracts"){completion_delimiter}
#############################""",
    """Example 7:

Entity_types: [section, category, subcategory]
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
("entity"{tuple_delimiter}"insurance commission"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments made to agents for selling insurance policies are taxable under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"travel agent commissions"{tuple_delimiter}"subcategory"{tuple_delimiter}"Commissions earned by travel agents for booking flights, hotels, and holiday packages are taxable under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"telecom service commissions"{tuple_delimiter}"subcategory"{tuple_delimiter}"Commissions paid for customer acquisitions or service promotions in the telecom industry are subject to TDS under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"retail sales commissions"{tuple_delimiter}"subcategory"{tuple_delimiter}"Commissions paid to salespersons in retail settings based on the volume of goods sold are taxable under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"automobile sales commissions"{tuple_delimiter}"subcategory"{tuple_delimiter}"Specific commissions earned on the sale of vehicles are subject to TDS under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"online marketplace sales commissions"{tuple_delimiter}"subcategory"{tuple_delimiter}"Commissions earned by sellers for facilitating sales through online platforms are taxable under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"residential property brokerage"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees earned from facilitating the sale or rental of residential properties are subject to TDS under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"commercial property brokerage"{tuple_delimiter}"subcategory"{tuple_delimiter}"Commissions from the sale or leasing of commercial real estate are taxable under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"land brokerage"{tuple_delimiter}"subcategory"{tuple_delimiter}"Brokerage fees for the sale of land plots are subject to TDS under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"equity transaction brokerage"{tuple_delimiter}"subcategory"{tuple_delimiter}"Commissions on transactions involving the purchase or sale of equities are taxable under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"debt securities brokerage"{tuple_delimiter}"subcategory"{tuple_delimiter}"Brokerage on transactions involving bonds or other debt instruments is subject to TDS under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"affiliate marketing fees"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for online referral of customers via affiliate links are taxable under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"business referral fees"{tuple_delimiter}"subcategory"{tuple_delimiter}"Commissions paid for referring new clients or business to a company are subject to TDS under Section 194H."){record_delimiter}
("entity"{tuple_delimiter}"service referral fees"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees for directing customers to specific services like utilities, educational programs, or health services are taxable under Section 194H."){record_delimiter}
("relationship"{tuple_delimiter}"commission or brokerage (except securities)"{tuple_delimiter}"194H"{tuple_delimiter}"falls under"{tuple_delimiter}"General commission or brokerage payments, excluding securities, are governed by Section 194H."{tuple_delimiter}"commission, brokerage"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"sales commission"{tuple_delimiter}"194H"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on sales commission paid to agents or distributors is covered under Section 194H."{tuple_delimiter}"sales commission, agents, distributors"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"brokerage on property"{tuple_delimiter}"194H"{tuple_delimiter}"falls under"{tuple_delimiter}"TDS on real estate brokerage fees is governed by Section 194H."{tuple_delimiter}"brokerage, property"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"stock/share commission (if structured as brokerage)"{tuple_delimiter}"194H"{tuple_delimiter}"falls under"{tuple_delimiter}"If stock/share transactions are structured purely as brokerage, they fall under Section 194H for TDS deduction."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Insurance commission"{tuple_delimiter}"Commission or brokerage (except securities or professional services)"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments made to agents for selling insurance policies are taxable under Section 194H."{tuple_delimiter}"insurance commission"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Travel agent commissions"{tuple_delimiter}"Commission or brokerage (except securities or professional services)"{tuple_delimiter}"falls under"{tuple_delimiter}"Commissions earned by travel agents for booking flights, hotels, and holiday packages are taxable under Section 194H."{tuple_delimiter}"travel agent"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Telecom service commissions"{tuple_delimiter}"Commission or brokerage (except securities or professional services)"{tuple_delimiter}"falls under"{tuple_delimiter}"Commissions paid for customer acquisitions or service promotions in the telecom industry are subject to TDS under Section 194H."{tuple_delimiter}"telecom services"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Retail sales commissions"{tuple_delimiter}"Sales commission"{tuple_delimiter}"falls under"{tuple_delimiter}"Commissions paid to salespersons in retail settings based on the volume of goods sold are taxable under Section 194H."{tuple_delimiter}"retail sales"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Automobile sales commissions"{tuple_delimiter}"Sales commission"{tuple_delimiter}"falls under"{tuple_delimiter}"Specific commissions earned on the sale of vehicles are subject to TDS under Section 194H."{tuple_delimiter}"automobile sales"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Online marketplace sales commissions"{tuple_delimiter}"Sales commission"{tuple_delimiter}"falls under"{tuple_delimiter}"Commissions earned by sellers for facilitating sales through online platforms are taxable under Section 194H."{tuple_delimiter}"online marketplace"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Residential property brokerage"{tuple_delimiter}"Brokerage on property"{tuple_delimiter}"falls under"{tuple_delimiter}"Fees earned from facilitating the sale or rental of residential properties are subject to TDS under Section 194H."{tuple_delimiter}"residential property"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Commercial property brokerage"{tuple_delimiter}"Brokerage on property"{tuple_delimiter}"falls under"{tuple_delimiter}"Commissions from the sale or leasing of commercial real estate are taxable under Section 194H."{tuple_delimiter}"commercial property"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Land brokerage"{tuple_delimiter}"Brokerage on property"{tuple_delimiter}"falls under"{tuple_delimiter}"Brokerage fees for the sale of land plots are subject to TDS under Section 194H."{tuple_delimiter}"land brokerage"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Equity transaction brokerage"{tuple_delimiter}"Stock/share commission (if structured as brokerage)"{tuple_delimiter}"falls under"{tuple_delimiter}"Commissions on transactions involving the purchase or sale of equities are taxable under Section 194H."{tuple_delimiter}"equity transactions"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Debt securities brokerage"{tuple_delimiter}"Stock/share commission (if structured as brokerage)"{tuple_delimiter}"falls under"{tuple_delimiter}"Brokerage on transactions involving bonds or other debt instruments is subject to TDS under Section 194H."{tuple_delimiter}"debt securities"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Affiliate marketing fees"{tuple_delimiter}"Referral fees"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for online referral of customers via affiliate links are taxable under Section 194H."{tuple_delimiter}"affiliate marketing"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Business referral fees"{tuple_delimiter}"Referral fees"{tuple_delimiter}"falls under"{tuple_delimiter}"Commissions paid for referring new clients or business to a company are subject to TDS under Section 194H."{tuple_delimiter}"business referrals"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Service referral fees"{tuple_delimiter}"Referral fees"{tuple_delimiter}"falls under"{tuple_delimiter}"Fees for directing customers to specific services like utilities, educational programs, or health services are taxable under Section 194H."{tuple_delimiter}"service referrals"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"Section 194H, commission, brokerage, middleman fees, agent commission, stock brokerage, distributor margin, insurance commission, travel agent commissions, telecom service commissions, retail sales commissions, automobile sales commissions, online marketplace sales commissions, residential property brokerage, commercial property brokerage, land brokerage, equity transaction brokerage, debt securities brokerage, affiliate marketing fees, business referral fees, service referral fees"){completion_delimiter}
#############################""",
    """Example 8:

Entity_types: [section, category, subcategory]
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
("entity"{tuple_delimiter}"GST Payments"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments related to Goods and Services Tax (GST), including IGST, CGST, and SGST, are not taxable under any section and hence fall under No TDS section."){record_delimiter}
("entity"{tuple_delimiter}"Customs and Excise Duties"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments related to customs duty and excise duty on goods are exempt from TDS."){record_delimiter}
("entity"{tuple_delimiter}"Education Cess"{tuple_delimiter}"subcategory"{tuple_delimiter}"Specific cess payments dedicated to funding educational programs are not subject to TDS."){record_delimiter}
("entity"{tuple_delimiter}"Penalty Payments"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments made as penalties in various regulatory or legal contexts are exempt from TDS."){record_delimiter}
("entity"{tuple_delimiter}"Filing and Registration Fees"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees paid for the filing of documents and registration processes required by law are not subject to TDS."){record_delimiter}
("entity"{tuple_delimiter}"Account Maintenance Fees"{tuple_delimiter}"subcategory"{tuple_delimiter}"Regular charges levied by banks for account maintenance are exempt from TDS."){record_delimiter}
("entity"{tuple_delimiter}"Transaction Charges"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees associated with specific banking transactions are not subject to TDS."){record_delimiter}
("entity"{tuple_delimiter}"Card Service Fees"{tuple_delimiter}"subcategory"{tuple_delimiter}"Charges related to services provided for VISA, Mastercard, and other payment networks do not incur TDS."){record_delimiter}
("entity"{tuple_delimiter}"Solvency Certificate Issuance"{tuple_delimiter}"subcategory"{tuple_delimiter}"Fees for the issuance of solvency certificates by banks are not subject to TDS."){record_delimiter}
("entity"{tuple_delimiter}"Life Insurance Premiums"{tuple_delimiter}"subcategory"{tuple_delimiter}"Regular premiums paid for life insurance policies are not subject to TDS."){record_delimiter}
("entity"{tuple_delimiter}"Health Insurance Premiums"{tuple_delimiter}"subcategory"{tuple_delimiter}"Premiums for medical or health insurance coverage are exempt from TDS."){record_delimiter}
("entity"{tuple_delimiter}"Vehicle Insurance Premiums"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments for insuring vehicles against damage or theft are not subject to TDS."){record_delimiter}
("entity"{tuple_delimiter}"Petty Cash Expenses"{tuple_delimiter}"subcategory"{tuple_delimiter}"Small, incidental expenses covered through petty cash are exempt from TDS."){record_delimiter}
("entity"{tuple_delimiter}"Imprest Expenses"{tuple_delimiter}"subcategory"{tuple_delimiter}"Funds maintained on a revolving fund basis for minor expenditures are not subject to TDS."){record_delimiter}
("entity"{tuple_delimiter}"Employee Reimbursements"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments made to employees for expenses incurred on behalf of the company are not taxable under TDS."){record_delimiter}
("entity"{tuple_delimiter}"Crop Sales"{tuple_delimiter}"subcategory"{tuple_delimiter}"Income derived from the sale of crops that are grown is exempt from TDS."){record_delimiter}
("entity"{tuple_delimiter}"Farm Rental Income"{tuple_delimiter}"subcategory"{tuple_delimiter}"Income from renting out agricultural land or equipment is not subject to TDS."){record_delimiter}
("entity"{tuple_delimiter}"Agricultural Subsidies"{tuple_delimiter}"subcategory"{tuple_delimiter}"Payments received as subsidies which are not taxable under TDS."){record_delimiter}
("entity"{tuple_delimiter}"Bank Interest"{tuple_delimiter}"subcategory"{tuple_delimiter}"Interest earned from bank deposits that falls below the taxable threshold is not subject to TDS."){record_delimiter}
("entity"{tuple_delimiter}"Dividend Payments"{tuple_delimiter}"subcategory"{tuple_delimiter}"Dividend income received from investments that is below the threshold for taxation is exempt from TDS."){record_delimiter}
("relationship"{tuple_delimiter}"agricultural income"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Income from agriculture is exempt from TDS and categorized under 'No TDS.'"{tuple_delimiter}"agricultural income"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"interest or dividend below a certain threshold"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Small-scale interest or dividends under statutory limits are categorized as 'No TDS.'"{tuple_delimiter}"dividend income, threshold"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"payment to government institutions"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments to government bodies for filing charges, penalties, or taxes are covered under 'No TDS.'"{tuple_delimiter}"government, authority"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"payment to any bank or insurance company"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Premiums or service fees paid to banks or insurers are categorized as 'No TDS.'"{tuple_delimiter}"banking, insurance premium"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"cash expenses or reimbursements"{tuple_delimiter}"No TDS"{tuple_delimiter}"falls under"{tuple_delimiter}"Reimbursements or cash expenses made by oneself do not attract TDS and are categorized under 'No TDS.'"{tuple_delimiter}"cash expenses, reimbursements"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"GST Payments"{tuple_delimiter}"Government Authorities for all kinds of taxes, penalty, appeals, cess, duties etc."{tuple_delimiter}"falls under"{tuple_delimiter}"Payments related to GST, including IGST, CGST, and SGST, do not attract TDS and are categorized under 'No TDS.'"{tuple_delimiter}"GST, SGST, CGST"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Customs and Excise Duties"{tuple_delimiter}"Government Authorities for all kinds of taxes, penalty, appeals, cess, duties etc."{tuple_delimiter}"falls under"{tuple_delimiter}"Payments related to customs duty and excise duty on goods are exempt from TDS and fall under 'No TDS.'"{tuple_delimiter}"customs, excise"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Education Cess"{tuple_delimiter}"Government Authorities for all kinds of taxes, penalty, appeals, cess, duties etc."{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for Education Cess are not subject to TDS and are included under 'No TDS.'"{tuple_delimiter}"education cess"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Penalty Payments"{tuple_delimiter}"Government Authorities for all kinds of taxes, penalty, appeals, cess, duties etc."{tuple_delimiter}"falls under"{tuple_delimiter}"Penalty payments to government institutions are exempt from TDS and categorized under 'No TDS.'"{tuple_delimiter}"penalty payments"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Filing and Registration Fees"{tuple_delimiter}"Government Authorities for all kinds of taxes, penalty, appeals, cess, duties etc."{tuple_delimiter}"falls under"{tuple_delimiter}"Filing and registration fees paid to government authorities do not attract TDS and are included under 'No TDS.'"{tuple_delimiter}"filing fees, registration fees"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Account Maintenance Fees"{tuple_delimiter}"Bank charges"{tuple_delimiter}"falls under"{tuple_delimiter}"Account maintenance fees charged by banks are exempt from TDS and categorized under 'No TDS.'"{tuple_delimiter}"account maintenance"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Transaction Charges"{tuple_delimiter}"Bank charges"{tuple_delimiter}"falls under"{tuple_delimiter}"Transaction fees charged by banks are not subject to TDS and fall under 'No TDS.'"{tuple_delimiter}"transaction charges"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Card Service Fees"{tuple_delimiter}"Bank charges"{tuple_delimiter}"falls under"{tuple_delimiter}"Fees related to card services from banks do not attract TDS and are included under 'No TDS.'"{tuple_delimiter}"card services"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Solvency Certificate Issuance"{tuple_delimiter}"Bank charges"{tuple_delimiter}"falls under"{tuple_delimiter}"Solvency certificate issuance fees by banks are exempt from TDS and categorized under 'No TDS.'"{tuple_delimiter}"solvency certificate"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Life Insurance Premiums"{tuple_delimiter}"Insurance premium"{tuple_delimiter}"falls under"{tuple_delimiter}"Regular premiums for life insurance policies are not subject to TDS and are included under 'No TDS.'"{tuple_delimiter}"life insurance"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Health Insurance Premiums"{tuple_delimiter}"Insurance premium"{tuple_delimiter}"falls under"{tuple_delimiter}"Premiums for health insurance are exempt from TDS and fall under 'No TDS.'"{tuple_delimiter}"health insurance"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Vehicle Insurance Premiums"{tuple_delimiter}"Insurance premium"{tuple_delimiter}"falls under"{tuple_delimiter}"Payments for vehicle insurance premiums do not attract TDS and are categorized under 'No TDS.'"{tuple_delimiter}"vehicle insurance"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Petty Cash Expenses"{tuple_delimiter}"Out of pocket expenses"{tuple_delimiter}"falls under"{tuple_delimiter}"Petty cash expenses are not subject to TDS and are included under 'No TDS.'"{tuple_delimiter}"petty cash"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Imprest Expenses"{tuple_delimiter}"Out of pocket expenses"{tuple_delimiter}"falls under"{tuple_delimiter}"Imprest fund expenses are exempt from TDS and categorized under 'No TDS.'"{tuple_delimiter}"imprest funds"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Employee Reimbursements"{tuple_delimiter}"Out of pocket expenses"{tuple_delimiter}"falls under"{tuple_delimiter}"Employee reimbursements for company-incurred expenses are not subject to TDS and fall under 'No TDS.'"{tuple_delimiter}"employee reimbursements"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Crop Sales"{tuple_delimiter}"Agricultural income"{tuple_delimiter}"falls under"{tuple_delimiter}"Income from the sale of crops, as agricultural income, is exempt from TDS and included under 'No TDS.'"{tuple_delimiter}"crop sales"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Farm Rental Income"{tuple_delimiter}"Agricultural income"{tuple_delimiter}"falls under"{tuple_delimiter}"Rental income from agricultural land or equipment does not attract TDS and is categorized under 'No TDS.'"{tuple_delimiter}"farm rental"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Agricultural Subsidies"{tuple_delimiter}"Agricultural income"{tuple_delimiter}"falls under"{tuple_delimiter}"Subsidies received for agricultural activities are not subject to TDS and fall under 'No TDS.'"{tuple_delimiter}"agricultural subsidies"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Bank Interest"{tuple_delimiter}"Interest/dividend below a certain threshold"{tuple_delimiter}"falls under"{tuple_delimiter}"Interest earned from bank deposits below the taxable threshold is exempt from TDS and included under 'No TDS.'"{tuple_delimiter}"bank interest"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Dividend Payments"{tuple_delimiter}"Interest/dividend below a certain threshold"{tuple_delimiter}"falls under"{tuple_delimiter}"Dividend income below the threshold for taxation does not attract TDS and is categorized under 'No TDS.'"{tuple_delimiter}"dividend payments"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"No TDS, minor interest, small dividends, agriculture, government authority, challan, gst, penalty, insurance premium, filing charges, custom duty, excise duty, bank fee, account maintenance fees, transaction charges, card service fees, solvency certificate issuance, life insurance premiums, health insurance premiums, vehicle insurance premiums, petty cash expenses, imprest expenses, employee reimbursements, crop sales, farm rental income, agricultural subsidies, bank interest, dividend payments"){completion_delimiter}
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
