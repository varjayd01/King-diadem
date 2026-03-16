from AI.persona_engine import PersonaEngine
from AI.simulation_engine import Simulation
from AI.decision_memory import save_decision
from AI.civilization_engine import add_node
from AI.freedom_signal import record_question,record_choice
from WORLD_MODEL.earth_guardian import detect_animal_context,detect_environment_harm,earth_response
from WORLD_MODEL.survival_threshold import check_choice

persona=PersonaEngine()
sim=Simulation()


def generate_options(question):

    outcomes=sim.simulate(question)

    options=[]

    for i,o in enumerate(outcomes[:3]):

        options.append({

            "option":chr(65+i),

            "strategy":o,

            "risk":round(0.3+i*0.2,2),

            "confidence":round(0.6-i*0.1,2)

        })

    return options


def process_decision(question):

    record_question()

    if detect_animal_context(question):

        return earth_response()

    harm=detect_environment_harm(question)

    if harm:

        return earth_response()

    options=generate_options(question)

    record_choice()

    save_decision(question,options)

    add_node(question,options)

    return options
