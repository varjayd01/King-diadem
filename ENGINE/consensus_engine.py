def consensus_engine(council_result):
    return {
        "final_action": council_result["decision"]["action"],
        "message": council_result["decision"]["message"],
        "confidence": council_result["score"]
    }
