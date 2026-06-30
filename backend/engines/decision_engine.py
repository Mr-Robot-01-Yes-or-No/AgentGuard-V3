from typing import Tuple

class DecisionEngine:
    @staticmethod
    def make_decision(policy_violations: list[str], risk_data: dict) -> Tuple[str, str]:
        """
        Returns decision (GREEN, YELLOW, RED) and reason.
        GREEN: Proceed
        YELLOW: Log and Proceed
        RED: Suspend and Review
        """
        if policy_violations:
            return "RED", f"Policy Violations: {', '.join(policy_violations)}"
            
        score = risk_data["score"]
        
        if score >= 75:
            return "RED", f"High Risk Score ({score})"
        elif score >= 40:
            return "YELLOW", f"Medium Risk Score ({score})"
        else:
            return "GREEN", "Action is safe."
