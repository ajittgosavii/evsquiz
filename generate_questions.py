"""
Generate questions.json with 50 EVS (Environmental Studies) sample questions.
Run this script to produce questions.json in the same directory.
"""

import json
import os

questions = [
    {
        "id": 1,
        "section": "EVS",
        "question": "Black lung disease is also known as:",
        "options": {
            "A": "Pneumoconiosis",
            "B": "Silicosis",
            "C": "Asbestosis",
            "D": "Byssinosis"
        },
        "answer": "A",
        "marks": 2
    },
    {
        "id": 2,
        "section": "EVS",
        "question": "Which is the second most abundant greenhouse gas in the atmosphere?",
        "options": {
            "A": "Carbon dioxide",
            "B": "Methane",
            "C": "Nitrous oxide",
            "D": "Water vapour"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 3,
        "section": "EVS",
        "question": "The Cartagena Protocol is related to:",
        "options": {
            "A": "Climate Change",
            "B": "Wetland Conservation",
            "C": "Living Modified Organisms",
            "D": "Ozone Depletion"
        },
        "answer": "C",
        "marks": 1
    },
    {
        "id": 4,
        "section": "EVS",
        "question": "The Western Ghats Ecology Expert Panel (WGEEP) was headed by:",
        "options": {
            "A": "Sunita Narain",
            "B": "K. Kasturirangan",
            "C": "Madhav Gadgil",
            "D": "M.S. Swaminathan"
        },
        "answer": "C",
        "marks": 1
    },
    {
        "id": 5,
        "section": "EVS",
        "question": "Which of the following is NOT a greenhouse gas?",
        "options": {
            "A": "Carbon dioxide",
            "B": "Methane",
            "C": "Nitrous oxide",
            "D": "Carbon Monoxide"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 6,
        "section": "EVS",
        "question": "Which of the following statements is/are true?\n(i) Photochemical smog is formed from NOx and hydrocarbons in sunlight\n(ii) CO binds with haemoglobin and reduces oxygen-carrying capacity\n(iii) Lead is a toxic heavy metal air pollutant",
        "options": {
            "A": "Only (i)",
            "B": "Only (i) and (ii)",
            "C": "Only (ii) and (iii)",
            "D": "All of the above"
        },
        "answer": "D",
        "marks": 2
    },
    {
        "id": 7,
        "section": "EVS",
        "question": "Which state in India has the maximum number of Eco-Sensitive Zones (ESZ)?",
        "options": {
            "A": "Maharashtra",
            "B": "Kerala",
            "C": "Karnataka",
            "D": "Tamil Nadu"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 8,
        "section": "EVS",
        "question": "Which city is known as the 'Tiger Gateway of India'?",
        "options": {
            "A": "Bhopal",
            "B": "Nagpur",
            "C": "Dehradun",
            "D": "Mysore"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 9,
        "section": "EVS",
        "question": "Which fuel produces maximum CO2 emission when burnt per unit weight?",
        "options": {
            "A": "Kerosene",
            "B": "Petrol",
            "C": "Coal",
            "D": "Natural Gas"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 10,
        "section": "EVS",
        "question": "WGEEP suggested Ecologically Sensitive Area (ESA) classification for:",
        "options": {
            "A": "Eastern Ghats",
            "B": "Western Ghats",
            "C": "Himalayas",
            "D": "Vindhya Range"
        },
        "answer": "B",
        "marks": 2
    },
    {
        "id": 11,
        "section": "EVS",
        "question": "Environmental Accounting is used to:",
        "options": {
            "A": "Measure consumption of natural resources and the cost of pollution",
            "B": "Track corporate profits only",
            "C": "Calculate GDP without environmental factors",
            "D": "Audit only government expenditure"
        },
        "answer": "A",
        "marks": 2
    },
    {
        "id": 12,
        "section": "EVS",
        "question": "Which of the following always decreases in a food chain from lower to higher trophic levels?",
        "options": {
            "A": "Number of organisms",
            "B": "Energy",
            "C": "Toxin concentration",
            "D": "Water content"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 13,
        "section": "EVS",
        "question": "In e-waste from mobile phones, the most abundant metal recovered is:",
        "options": {
            "A": "Copper",
            "B": "Gold",
            "C": "Silver",
            "D": "Palladium"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 14,
        "section": "EVS",
        "question": "The end product formed when acid rain reacts with marble (CaCO3) is:",
        "options": {
            "A": "calcium chloride",
            "B": "calcium oxide",
            "C": "calcium hydroxide",
            "D": "Gypsum (calcium sulphate)"
        },
        "answer": "D",
        "marks": 2
    },
    {
        "id": 15,
        "section": "EVS",
        "question": "Which chemical element plays the most important role in ozone depletion?",
        "options": {
            "A": "Fluorine",
            "B": "Bromine",
            "C": "Chlorine",
            "D": "Iodine"
        },
        "answer": "C",
        "marks": 1
    },
    {
        "id": 16,
        "section": "EVS",
        "question": "The most dangerous greenhouse gas released from waste water treatment is:",
        "options": {
            "A": "Carbon dioxide",
            "B": "Methane",
            "C": "Nitrous oxide",
            "D": "Hydrogen sulphide"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 17,
        "section": "EVS",
        "question": "The reference gas used for calculating Global Warming Potential (GWP) is:",
        "options": {
            "A": "Carbon dioxide",
            "B": "Methane",
            "C": "Nitrous oxide",
            "D": "CFC-12"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 18,
        "section": "EVS",
        "question": "The main objective of the Taj Trapezium Zone (TTZ) is:",
        "options": {
            "A": "Protection of Taj Mahal from Pollution",
            "B": "Tourism promotion",
            "C": "Urban development",
            "D": "Industrial growth"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 19,
        "section": "EVS",
        "question": "The main source of synthetic fuel is:",
        "options": {
            "A": "Natural gas",
            "B": "Petroleum",
            "C": "Coal",
            "D": "Biomass"
        },
        "answer": "C",
        "marks": 1
    },
    {
        "id": 20,
        "section": "EVS",
        "question": "The ozone layer lies in which layer of the atmosphere?",
        "options": {
            "A": "Troposphere",
            "B": "Mesosphere",
            "C": "Thermosphere",
            "D": "Stratosphere"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 21,
        "section": "EVS",
        "question": "Which crop enriches the soil with nitrogen?",
        "options": {
            "A": "Wheat",
            "B": "Rice",
            "C": "Potato",
            "D": "Pea"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 22,
        "section": "EVS",
        "question": "Water use efficiency in agriculture refers to:",
        "options": {
            "A": "Using maximum water for irrigation",
            "B": "Pumping groundwater faster",
            "C": "Saving water from evaporation and surface runoff losses",
            "D": "Storing water in open reservoirs"
        },
        "answer": "C",
        "marks": 2
    },
    {
        "id": 23,
        "section": "EVS",
        "question": "Tipping Fee in the context of solid waste management refers to:",
        "options": {
            "A": "Tax on waste generators",
            "B": "Subsidy for recyclers",
            "C": "Charge levied on waste disposed at a landfill or waste processing facility",
            "D": "Fine for illegal dumping"
        },
        "answer": "C",
        "marks": 2
    },
    {
        "id": 24,
        "section": "EVS",
        "question": "The Montreal Protocol is related to:",
        "options": {
            "A": "Biodiversity conservation",
            "B": "Climate change mitigation",
            "C": "Protection of the Ozone layer",
            "D": "Wetland preservation"
        },
        "answer": "C",
        "marks": 1
    },
    {
        "id": 25,
        "section": "EVS",
        "question": "Who headed the expert panel appointed for the ecological study of the Western Ghats?",
        "options": {
            "A": "Dr. K. Kasturirangan",
            "B": "Dr. Madhav Gadgil",
            "C": "Dr. R.K. Pachauri",
            "D": "Dr. M.S. Swaminathan"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 26,
        "section": "EVS",
        "question": "Which of the following is NOT an air pollutant?",
        "options": {
            "A": "Sulphur dioxide",
            "B": "Carbon monoxide",
            "C": "Nitrogen dioxide",
            "D": "Nitrogen Gas (N2)"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 27,
        "section": "EVS",
        "question": "Which of the following is a biodegradable waste?",
        "options": {
            "A": "Plastic bottles",
            "B": "Aluminium cans",
            "C": "Glass jars",
            "D": "None of the above"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 28,
        "section": "EVS",
        "question": "Which type of radiation is trapped by the greenhouse effect?",
        "options": {
            "A": "UV Rays (re-radiated as infrared)",
            "B": "X-rays",
            "C": "Gamma rays",
            "D": "Radio waves"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 29,
        "section": "EVS",
        "question": "Greenhouse gases are defined as gases that:",
        "options": {
            "A": "Only come from industrial sources",
            "B": "Reduce earth's temperature",
            "C": "Are only man-made",
            "D": "Absorb and re-emit infrared radiation, trapping heat in the atmosphere"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 30,
        "section": "EVS",
        "question": "The protective ozone layer is found in which part of the atmosphere?",
        "options": {
            "A": "Troposphere",
            "B": "Mesosphere",
            "C": "Exosphere",
            "D": "Stratosphere"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 31,
        "section": "EVS",
        "question": "Which greenhouse gas is present in the atmosphere in very high quantity?",
        "options": {
            "A": "Methane",
            "B": "Nitrous oxide",
            "C": "Carbon dioxide",
            "D": "Ozone"
        },
        "answer": "C",
        "marks": 1
    },
    {
        "id": 32,
        "section": "EVS",
        "question": "The exchange of outgoing and re-emitted radiation that keeps the Earth warmer than it would otherwise be is called:",
        "options": {
            "A": "Green house effect",
            "B": "Ozone effect",
            "C": "Solar radiation effect",
            "D": "Albedo effect"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 33,
        "section": "EVS",
        "question": "Which layer protects us from harmful UV radiation from the sun?",
        "options": {
            "A": "Ozone layer",
            "B": "Ionosphere",
            "C": "Troposphere",
            "D": "Exosphere"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 34,
        "section": "EVS",
        "question": "Which chemical released from CFCs is primarily responsible for ozone destruction?",
        "options": {
            "A": "Fluorine",
            "B": "Carbon",
            "C": "Chlorine",
            "D": "Hydrogen"
        },
        "answer": "C",
        "marks": 1
    },
    {
        "id": 35,
        "section": "EVS",
        "question": "Which of the following are ozone depleting substances?",
        "options": {
            "A": "CFCs (Chlorofluorocarbons)",
            "B": "Halons",
            "C": "Carbon tetrachloride",
            "D": "All of the above"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 36,
        "section": "EVS",
        "question": "CFCs (Chlorofluorocarbons) are responsible for destroying:",
        "options": {
            "A": "Carbon dioxide molecules",
            "B": "Nitrogen molecules",
            "C": "Water vapour molecules",
            "D": "Ozone molecules"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 37,
        "section": "EVS",
        "question": "Which of the following is NOT a naturally occurring greenhouse gas?",
        "options": {
            "A": "Carbon dioxide",
            "B": "Methane",
            "C": "Nitrous oxide",
            "D": "Ethane"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 38,
        "section": "EVS",
        "question": "Burning fossil fuels causes:",
        "options": {
            "A": "Decrease in atmospheric oxygen only",
            "B": "Increased concentration of greenhouse gases in the atmosphere",
            "C": "Cooling of the earth",
            "D": "Increase in ozone layer thickness"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 39,
        "section": "EVS",
        "question": "Which of the following is NOT biodegradable?",
        "options": {
            "A": "Paper",
            "B": "Cotton cloth",
            "C": "Wood",
            "D": "Aluminium foil"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 40,
        "section": "EVS",
        "question": "Which of the following cannot be decomposed by bacteria?",
        "options": {
            "A": "Kitchen waste",
            "B": "Plastic and polythene bags",
            "C": "Dead animals",
            "D": "Crop residues"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 41,
        "section": "EVS",
        "question": "Which of the following diseases is NOT caused by noise pollution?",
        "options": {
            "A": "Diarrhoea",
            "B": "Hearing loss",
            "C": "Hypertension",
            "D": "Insomnia"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 42,
        "section": "EVS",
        "question": "When trees are cut on a large scale, the oxygen level in the atmosphere:",
        "options": {
            "A": "Increases",
            "B": "Decreases",
            "C": "Remains the same",
            "D": "First increases then decreases"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 43,
        "section": "EVS",
        "question": "The major cause of greenhouse effect is the emission of which gases?",
        "options": {
            "A": "CO2 and N2O",
            "B": "O2 and N2",
            "C": "Argon and Helium",
            "D": "Hydrogen and Oxygen"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 44,
        "section": "EVS",
        "question": "The major consumer of wood from forests is:",
        "options": {
            "A": "Furniture industry",
            "B": "Paper industry",
            "C": "Construction industry",
            "D": "Pharmaceutical industry"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 45,
        "section": "EVS",
        "question": "The Biosphere refers to:",
        "options": {
            "A": "Only the lithosphere",
            "B": "The part of the Earth where life exists, including land, water, and atmosphere",
            "C": "Only the hydrosphere",
            "D": "Only the atmosphere"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 46,
        "section": "EVS",
        "question": "Afforestation means:",
        "options": {
            "A": "Planting trees on a large scale to create a forest",
            "B": "Cutting down trees",
            "C": "Burning of forests",
            "D": "Converting forest land to agriculture"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 47,
        "section": "EVS",
        "question": "Smog is a combination of:",
        "options": {
            "A": "Smoke and Fog",
            "B": "Smoke and Dust",
            "C": "Sulphur and Fog",
            "D": "Snow and Fog"
        },
        "answer": "A",
        "marks": 1
    },
    {
        "id": 48,
        "section": "EVS",
        "question": "Deforestation generally decreases:",
        "options": {
            "A": "Soil erosion",
            "B": "Drought",
            "C": "Global warming",
            "D": "Rainfall"
        },
        "answer": "D",
        "marks": 1
    },
    {
        "id": 49,
        "section": "EVS",
        "question": "The main source of atmospheric oxygen is:",
        "options": {
            "A": "Volcanic eruptions",
            "B": "Green Plants (photosynthesis)",
            "C": "Decomposition of CO2",
            "D": "Ocean currents"
        },
        "answer": "B",
        "marks": 1
    },
    {
        "id": 50,
        "section": "EVS",
        "question": "Desertification is caused by:",
        "options": {
            "A": "Overgrazing",
            "B": "Deforestation",
            "C": "Climate change",
            "D": "All of the above"
        },
        "answer": "D",
        "marks": 1
    },
]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(questions)} questions -> {output_path}")


if __name__ == "__main__":
    main()
