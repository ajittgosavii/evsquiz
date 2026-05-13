"""
Seed KIDO questions from ch_1_ees_mcq_set_2_w PDF (image-based, OCR not available).
Run once: python seed_kido.py
"""
import json
import os

QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "questions.json")

KIDO_QUESTIONS = [
    # ── Main Questions 1-42 ──────────────────────────────────────────────────
    {
        "question": "Environmental Studies ______",
        "options": {"A": "is an interdisciplinary academic field.", "B": "methodically studies human interaction with the environment.", "C": "includes the natural environment, built environment, and the sets of relationships between them.", "D": "all of the above."},
        "answer": "D",
    },
    {
        "question": "Environmental Studies does not involve ______",
        "options": {"A": "psychology", "B": "demography", "C": "ethics", "D": "literature"},
        "answer": "D",
    },
    {
        "question": "An organism's environment is the surrounding conditions that affect that organism.",
        "options": {"A": "True", "B": "False"},
        "answer": "A",
    },
    {
        "question": "Political decisions are made with respect to political jurisdictions; environmental problems ______",
        "options": {"A": "often transcend these jurisdictions", "B": "respect political boundaries", "C": "often have little to do with regional economic decisions", "D": "none of the above"},
        "answer": "A",
    },
    {
        "question": "Environmentalists who use an ecosystem approach to comprehend environmental issues will take into consideration which of the following?",
        "options": {"A": "Human activity", "B": "The interactions between organisms", "C": "Geography", "D": "All of the above", "E": "None of the above"},
        "answer": "E",
    },
    {
        "question": "Abiotic environment does not include ______",
        "options": {"A": "soil", "B": "water", "C": "air", "D": "plant"},
        "answer": "D",
    },
    {
        "question": "Van Mahotsav is an annual tree-planting festival in India, celebrated on ______",
        "options": {"A": "2nd June", "B": "1st July", "C": "1st December", "D": "15th September"},
        "answer": "B",
    },
    {
        "question": "Biotic environment includes ______",
        "options": {"A": "producers", "B": "consumers", "C": "decomposers", "D": "all the above"},
        "answer": "D",
    },
    {
        "question": "Outcomes of Rio Conference do not include ______",
        "options": {"A": "The UN Framework Convention on Climate Change", "B": "The Convention on Biological Diversity (CBD)", "C": "Convention for the Protection of the Ozone Layer", "D": "Commission on Sustainable Development (CSD)"},
        "answer": "C",
    },
    {
        "question": "Which of the following follow the concept of sustainable development? (i) Fishing the mature fish instead of the young fish (ii) Using wind power instead of burning coal to generate electricity (iii) The prohibition of trading endangered species",
        "options": {"A": "(i) and (ii) only", "B": "(i) and (iii) only", "C": "(ii) and (iii) only", "D": "(i), (ii) and (iii)"},
        "answer": "D",
    },
    {
        "question": "The evidence that the world is experiencing an environmental crisis is highly visible in many parts of the world.",
        "options": {"A": "True", "B": "False"},
        "answer": "A",
    },
    {
        "question": "The natural world uses resources efficiently, while humans tend to waste resources more.",
        "options": {"A": "True", "B": "False"},
        "answer": "A",
    },
    {
        "question": "The Montreal Protocol, signed in 1987 and strengthened in 1990 ______",
        "options": {"A": "attains the global optimal level of common property resource", "B": "relies on internationally tradable emission permits", "C": "minimizes free riders of public goods", "D": "reduces ozone depletion through cutting chlorofluorocarbon production"},
        "answer": "D",
    },
    {
        "question": "The main outcome of the 1992 United Nations Conference on Environment and Development (Rio de Janeiro) was ______",
        "options": {"A": "it produced a blueprint intended to guide development in sustainable directions", "B": "a global agreement on a framework for environmental legislation", "C": "a report entitled Our Common Future", "D": "it raised awareness of the need to preserve biodiversity in the Amazon River Basin"},
        "answer": "A",
    },
    {
        "question": "The notion of environmental justice refers to ______",
        "options": {"A": "grassroots activities that monitor environmental conditions and work toward equal distribution of environmental impacts and benefits", "B": "rewarding those who work hard for environmental improvement", "C": "environmental racism where waste sites and hazards are located in non-white neighborhoods", "D": "prosecution of environmental offenders by government agencies"},
        "answer": "A",
    },
    {
        "question": "Which of the following global trends is of great concern for the future of our environment?",
        "options": {"A": "degradation of fertile soils", "B": "changes in the global atmosphere", "C": "species extinction leading to biodiversity loss", "D": "population growth and increasing per-capita consumption", "E": "all of the above"},
        "answer": "E",
    },
    {
        "question": "Introduction of chemicals into atmosphere is known as ______",
        "options": {"A": "air pollution", "B": "radioactive pollution", "C": "atmospheric pollution", "D": "dense pollution"},
        "answer": "A",
    },
    {
        "question": "Second highest layer of Earth's atmosphere is ______",
        "options": {"A": "stratosphere", "B": "mesosphere", "C": "troposphere", "D": "thermosphere"},
        "answer": "A",
    },
    {
        "question": "Re-processing material to make another product ______",
        "options": {"A": "Reduce", "B": "Reuse", "C": "Recycle", "D": "Recovery"},
        "answer": "C",
    },
    {
        "question": "Most recycling focuses on four major categories of products. Which one is NOT one of them?",
        "options": {"A": "Chemicals", "B": "Paper", "C": "Plastic", "D": "Glass"},
        "answer": "A",
    },
    {
        "question": "The following is an example of reusing ______",
        "options": {"A": "Using less napkins at eateries", "B": "Using waste plastic bags as garbage bags", "C": "Bringing plastic bottles/bags at recycle facility", "D": "Using again the plastic/cloth bags for shopping"},
        "answer": "A",
    },
    {
        "question": "The following is an example of reducing ______",
        "options": {"A": "Using less water while brushing teeth", "B": "Using recycled plastic bags", "C": "Bringing newspaper at recycle facility", "D": "All of the above"},
        "answer": "A",
    },
    {
        "question": "Which of the following items cannot be recycled?",
        "options": {"A": "Food items", "B": "Plastic", "C": "Paper", "D": "Batteries"},
        "answer": "A",
    },
    {
        "question": "What is the term used to describe objects that are being washed and used again?",
        "options": {"A": "Reduce", "B": "Reuse", "C": "Recycle", "D": "Recovery"},
        "answer": "B",
    },
    {
        "question": "What does it mean if an item is \"biodegradable\"?",
        "options": {"A": "It means that it will eventually break down completely in nature", "B": "It means that it is bad for the environment", "C": "It means that it is perfect for composting", "D": "It means that it can be eaten by vultures"},
        "answer": "A",
    },
    {
        "question": "When did the Three Mile Island accident happen?",
        "options": {"A": "March 11, 1979", "B": "March 28, 1979", "C": "May 04, 2011", "D": "July 05, 1967"},
        "answer": "B",
    },
    {
        "question": "The Three Mile Island accident happened in Pennsylvania. What went wrong with the automated safety systems?",
        "options": {"A": "Operators overrode several systems which worsened the accident", "B": "Lightning strike damaged electronic systems", "C": "Designers did not account for loss of feed water to reactor", "D": "Backup cooling water supplies were insufficient"},
        "answer": "A",
    },
    {
        "question": "What was the final conclusion on the magnitude of public exposure from the Three Mile Island accident?",
        "options": {"A": "Public were not exposed to dangerous levels of radiation", "B": "Thousands were seriously exposed and hundreds died", "C": "Radiation exposure was very high but evacuation prevented deaths", "D": "Hundreds were seriously exposed and many died"},
        "answer": "A",
    },
    {
        "question": "How much response was there from the government and nuclear industry regarding the Three Mile Island accident?",
        "options": {"A": "Neither government nor industry did much", "B": "Government proposed many reforms but industry ignored them", "C": "Both government and industry made major changes in nuclear power regulation and operation", "D": "Government was distracted by Iran hostage crisis"},
        "answer": "C",
    },
    {
        "question": "The Chernobyl accident happened in 1986. How much are modern Western reactors like RBMK reactors?",
        "options": {"A": "They are very different", "B": "Western designs are similar combinations of many designs", "C": "They are very similar", "D": "Soviet design had more advanced features"},
        "answer": "A",
    },
    {
        "question": "Besides lack of containment, what feature magnified radioactive release from Chernobyl?",
        "options": {"A": "Water from broken pipes carried radioactive material away", "B": "Graphite fire and thermal plume lifted radioactive material into atmosphere", "C": "Three other reactors were damaged releasing more radiation", "D": "Workers did nothing to contain the event"},
        "answer": "B",
    },
    {
        "question": "The radioactive releases from the Chernobyl accident are expected to be the major cause of death in surrounding population for years to come.",
        "options": {"A": "True", "B": "False"},
        "answer": "B",
    },
    {
        "question": "Now the Fukushima reactors in Japan. How did the earthquake cause loss of control of reactor power?",
        "options": {"A": "Earthquake jammed control rods so reactors couldn't shut down", "B": "Reactors automatically shut down safely", "C": "Operators kept reactors running for electricity", "D": "Earthquake caused power surge like Chernobyl"},
        "answer": "B",
    },
    {
        "question": "Why didn't the Fukushima plant systems designed to keep nuclear fuel cool work?",
        "options": {"A": "Systems were poorly designed", "B": "Pipes were destroyed", "C": "Operators misunderstood situation", "D": "Earthquake and tsunami cut off all electrical power so cooling systems failed"},
        "answer": "D",
    },
    {
        "question": "Which of the following is greenhouse gas?",
        "options": {"A": "Carbon monoxide", "B": "Carbon dioxide", "C": "Acid fumes", "D": "Oxygen"},
        "answer": "B",
    },
    {
        "question": "Which of the following is greenhouse gas? (Methane group)",
        "options": {"A": "Sulphur dioxide", "B": "Methane", "C": "Nitrogen", "D": "Oxygen"},
        "answer": "B",
    },
    {
        "question": "Which among the following can cause global warming?",
        "options": {"A": "Fishing", "B": "Volcanic eruptions", "C": "Mudslides", "D": "Plantation"},
        "answer": "B",
    },
    {
        "question": "What is greenhouse effect?",
        "options": {"A": "Increased landslides", "B": "Extra volcanic eruptions", "C": "More mudslides", "D": "Sea level rise"},
        "answer": "D",
    },
    {
        "question": "What does a greenhouse gas do?",
        "options": {"A": "Causes more heat to escape Earth", "B": "Blocks sunlight from Earth", "C": "Absorbs and holds heat", "D": "Causes acid rain"},
        "answer": "C",
    },
    {
        "question": "The Taj Mahal is affected by ______",
        "options": {"A": "Soil pollution", "B": "Water pollution", "C": "Air pollution", "D": "Fog"},
        "answer": "B",
    },
    {
        "question": "How to prevent Acid Rain ______",
        "options": {"A": "By increasing emission of SO2 and NO2", "B": "By decreasing emission of SO2 and NO2", "C": "By increasing emission of HCl and phosphate", "D": "By decreasing emission of HCl and phosphate"},
        "answer": "B",
    },
    {
        "question": "The appropriate way to reduce the effect of acid rain on soil ______",
        "options": {"A": "By adding hydrochloric acid to the soil", "B": "By adding limestone to the soil", "C": "By adding nitrogen to the soil", "D": "By adding oxygen to the soil"},
        "answer": "B",
    },
    # ── Additional Objective Questions 1-50 ─────────────────────────────────
    {
        "question": "The word environment is derived from French word ______",
        "options": {"A": "Environner", "B": "Environnering", "C": "E-Environner", "D": "Envo"},
        "answer": "A",
    },
    {
        "question": "As per the French word ENVIRONNER means ______",
        "options": {"A": "atmosphere", "B": "earth and sun", "C": "encircle and surround", "D": "earth and energy"},
        "answer": "C",
    },
    {
        "question": "World Environment Day is on ______",
        "options": {"A": "June 5", "B": "June 11", "C": "July 5", "D": "July 11"},
        "answer": "A",
    },
    {
        "question": "World Water Day is on ______",
        "options": {"A": "April 22", "B": "March 23", "C": "March 24", "D": "March 22"},
        "answer": "D",
    },
    {
        "question": "Earth Day is on ______",
        "options": {"A": "January 22", "B": "February 22", "C": "March 22", "D": "April 22"},
        "answer": "D",
    },
    {
        "question": "Ecomark of our country is ______",
        "options": {"A": "Earthen pitcher", "B": "Water drop", "C": "Sun", "D": "Ashoka tree"},
        "answer": "A",
    },
    {
        "question": "Environmentally friendly products are given ISO certification called ISO ______",
        "options": {"A": "12000", "B": "13000", "C": "14000", "D": "15000"},
        "answer": "C",
    },
    {
        "question": "Nobel Peace Prize in 2004 for environmental conservation was awarded to ______",
        "options": {"A": "Ratan Tata", "B": "Wangari Maathai", "C": "S. D. Bush", "D": "Dr. Manmohan Singh"},
        "answer": "B",
    },
    {
        "question": "Earth Summit held at Rio de Janeiro in ______",
        "options": {"A": "1892", "B": "1992", "C": "2012", "D": "2011"},
        "answer": "B",
    },
    {
        "question": "World Summit on Sustainable Development held at Johannesburg in ______",
        "options": {"A": "2001", "B": "2002", "C": "2003", "D": "2004"},
        "answer": "B",
    },
    {
        "question": "He is popularly known as the Green Judge ______",
        "options": {"A": "Mr. Manmohan Singh", "B": "Kuldeep Singh", "C": "Mangal Singh", "D": "Mr. Jethmalani"},
        "answer": "B",
    },
    {
        "question": "He is known as Green Advocate ______",
        "options": {"A": "Mr. K. P. Raghav", "B": "Mr. P. Chidambaram", "C": "Mr. S. D. Rao", "D": "Mr. M. C. Mehta"},
        "answer": "D",
    },
    {
        "question": "He is known for his Chipko Movement ______",
        "options": {"A": "Atal Bihari Bajpai", "B": "Anna Hazare", "C": "Sundarlal Bahuguna", "D": "Pandit Nehru"},
        "answer": "C",
    },
    {
        "question": "He got the Magsaysay Award for water conservation effort ______",
        "options": {"A": "Rajender Singh", "B": "Ashok Singh", "C": "Nana Patekar", "D": "Anil Agrawal"},
        "answer": "A",
    },
    {
        "question": "Wild Life Week is celebrated in the period of ______",
        "options": {"A": "1-7 October", "B": "11-18 November", "C": "1-8 March", "D": "1-8 April"},
        "answer": "A",
    },
    {
        "question": "World Forest Day is on ______",
        "options": {"A": "11 March", "B": "12 March", "C": "13 March", "D": "21 March"},
        "answer": "D",
    },
    {
        "question": "Edaphic means ______",
        "options": {"A": "Related to water", "B": "Related to soil", "C": "Related to air", "D": "Related to sun"},
        "answer": "B",
    },
    {
        "question": "The environment modified by human activities is called ______",
        "options": {"A": "Natural environment", "B": "Modern environment", "C": "Anthropogenic environment", "D": "Semi-natural environment"},
        "answer": "C",
    },
    {
        "question": "The term Ecology was introduced by ______",
        "options": {"A": "Haeckel", "B": "Newton", "C": "S. S. Rao", "D": "Tansley"},
        "answer": "A",
    },
    {
        "question": "Ecological factors related to soil and substratum are called ______ factors",
        "options": {"A": "Edaphic", "B": "Somatic", "C": "Air-borne", "D": "Egis"},
        "answer": "A",
    },
    {
        "question": "The inter governmental conference on environmental education in 1977 was held in ______",
        "options": {"A": "Tbilisi (USSR)", "B": "Delhi (India)", "C": "Albita", "D": "New York (USA)"},
        "answer": "A",
    },
    {
        "question": "Abiotic components are ______",
        "options": {"A": "non-living", "B": "living", "C": "artificial", "D": "earth living"},
        "answer": "A",
    },
    {
        "question": "CFCs that contribute to depletion of ______",
        "options": {"A": "ozone layer", "B": "cartoon layer", "C": "SO2 layer", "D": "methane layer"},
        "answer": "A",
    },
    {
        "question": "The major greenhouse gases are ______",
        "options": {"A": "CO2, CH4, N2O", "B": "CO2, O2, SO2", "C": "CH4, CH2, CH5", "D": "CO2, CO2, O2"},
        "answer": "A",
    },
    {
        "question": "Greenhouse gases are regulated under UN framework convention on climate change and the ______",
        "options": {"A": "Tokyo protocol", "B": "Kyoto protocol", "C": "Mumbai protocol", "D": "Nambe protocol"},
        "answer": "B",
    },
    {
        "question": "______ are animals that have no backbone and are visible without magnification.",
        "options": {"A": "Micro", "B": "Mini", "C": "Macro invertebrates", "D": "Non-macro invertebrates"},
        "answer": "C",
    },
    {
        "question": "Montreal protocol is related to ______",
        "options": {"A": "Depletion of ozone layer", "B": "Cartoon layer", "C": "SO2 layer", "D": "Sulphur layer"},
        "answer": "A",
    },
    {
        "question": "______ are the most common cause of viral gastroenteritis in humans.",
        "options": {"A": "Noroviruses", "B": "Bitaviruses", "C": "Fungi", "D": "Yeasts"},
        "answer": "A",
    },
    {
        "question": "OECD stands for ______",
        "options": {"A": "Organisation for Economic Co-operation and Development", "B": "Organisation for Environmental Company and Development", "C": "Organisation for Environmental Company Department", "D": "Organisation for Economic Co-operation Department"},
        "answer": "A",
    },
    {
        "question": "______ on cryotic soil is soil at or below the freezing point of water (0°C / 32°F) for two or more years.",
        "options": {"A": "Permafrost", "B": "Frost", "C": "Primefrost", "D": "Thermofrost"},
        "answer": "A",
    },
    {
        "question": "Area in the interface between land and river or stream is called ______",
        "options": {"A": "spring", "B": "riparian", "C": "forest", "D": "forest land"},
        "answer": "B",
    },
    {
        "question": "Development that meets present needs without compromising future generations is called ______",
        "options": {"A": "sustainable development", "B": "stable development", "C": "future development", "D": "natural development"},
        "answer": "A",
    },
    {
        "question": "Van Mahotsav is an annual tree-planting festival in India celebrated on ______ (Additional)",
        "options": {"A": "1 March", "B": "2 March", "C": "1 July", "D": "2 July"},
        "answer": "C",
    },
    {
        "question": "The scientific method of dating based on analysis of tree rings is called ______",
        "options": {"A": "Dendrochronology", "B": "Ecosystem", "C": "Expost", "D": "Ecology"},
        "answer": "A",
    },
    {
        "question": "Place or type of site where an organism naturally occurs is called ______",
        "options": {"A": "Habitat", "B": "Collapse", "C": "Biotope", "D": "Biosphere"},
        "answer": "A",
    },
    {
        "question": "______ is the area which is interface between land and river or stream.",
        "options": {"A": "Riparian", "B": "Biosphere", "C": "Biotope", "D": "Habitat"},
        "answer": "A",
    },
    {
        "question": "The lowest atmospheric layer, the troposphere, is only ______ kilometers thick.",
        "options": {"A": "1", "B": "2", "C": "12", "D": "20"},
        "answer": "C",
    },
    {
        "question": "The stratosphere is ______ kilometers thick.",
        "options": {"A": "1", "B": "2", "C": "50", "D": "100"},
        "answer": "C",
    },
    {
        "question": "The stratosphere contains a layer of ______ which helps in the formation of rain.",
        "options": {"A": "sulphates", "B": "CO2", "C": "O2", "D": "CO2 + O2"},
        "answer": "C",
    },
    {
        "question": "Stratosphere contains layer of ______",
        "options": {"A": "O", "B": "carbon", "C": "ozone", "D": "water"},
        "answer": "C",
    },
    {
        "question": "Layer of ozone absorbs ______ known to cause cancer.",
        "options": {"A": "ultraviolet light", "B": "beta violet light", "C": "bright light", "D": "super light"},
        "answer": "A",
    },
    {
        "question": "Accumulation of carbon dioxide and other gases causes ______ in atmosphere leading to global warming.",
        "options": {"A": "light effect", "B": "greenhouse effect", "C": "yellow light effect", "D": "solar effect"},
        "answer": "B",
    },
    {
        "question": "Lithosphere provides soil for ______",
        "options": {"A": "rainwater harvesting", "B": "wildlife", "C": "agriculture", "D": "non-agriculture"},
        "answer": "C",
    },
    {
        "question": "There are ______ types of lithosphere.",
        "options": {"A": "four", "B": "six", "C": "eleven", "D": "two"},
        "answer": "D",
    },
    {
        "question": "Biosphere is also called as ______",
        "options": {"A": "zone of life on earth", "B": "zone of wildlife on earth", "C": "life in environment", "D": "life on earth and moon"},
        "answer": "A",
    },
    {
        "question": "The biosphere is believed to have evolved at least ______ billion years ago.",
        "options": {"A": "1.5", "B": "2.5", "C": "3.5", "D": "4.5"},
        "answer": "C",
    },
    {
        "question": "Four major greenhouse gases are water vapor, carbon dioxide, methane and ______",
        "options": {"A": "oxygen", "B": "sulphur", "C": "ozone", "D": "H2S"},
        "answer": "C",
    },
    {
        "question": "The global temperature has increased ______ °C in the last 100 years.",
        "options": {"A": "100", "B": "200", "C": "0.74", "D": "11.72"},
        "answer": "C",
    },
    {
        "question": "Acid rain is caused by emissions of carbon dioxide, sulphur dioxide and ______",
        "options": {"A": "nitrogen oxides", "B": "ozone", "C": "oxygen", "D": "CO2 + ozone"},
        "answer": "A",
    },
    {
        "question": "ODS stands for ______",
        "options": {"A": "Ozone depleting substances", "B": "Oxygen depleting substances", "C": "Oxygen deposit substances", "D": "Oxygen developing substances"},
        "answer": "A",
    },
]


def main():
    # Load existing questions
    if os.path.exists(QUESTIONS_PATH):
        with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    # Remove any existing KIDO questions to avoid duplicates on re-run
    existing = [q for q in existing if q.get("section") != "KIDO"]
    max_id = max((q.get("id", 0) for q in existing), default=0)

    # Build KIDO entries
    new_qs = []
    for i, q in enumerate(KIDO_QUESTIONS, start=1):
        new_qs.append({
            "id": max_id + i,
            "section": "KIDO",
            "question": q["question"],
            "options": q["options"],
            "answer": q["answer"],
            "marks": 1,
        })

    combined = existing + new_qs
    with open(QUESTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"Done. Added {len(new_qs)} KIDO questions. Total in bank: {len(combined)}")


if __name__ == "__main__":
    main()
