def update_rules(issues: list) -> list:
    learned_rules = []

    for issue in issues:
        if "uncertainty" in issue.lower():
            learned_rules.append(
                "Always explicitly state uncertainty in conceptual answers."
            )
        if "repetition" in issue.lower():
            learned_rules.append(
                "Avoid repeating the same idea using different wording."
            )

    return learned_rules
