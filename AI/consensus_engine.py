def build_consensus(council_results):

    summary = []

    for member, result in council_results.items():

        summary.append(f"{member}: {result}")

    combined = "\n".join(summary)

    return combined
