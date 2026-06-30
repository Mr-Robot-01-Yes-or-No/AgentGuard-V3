class RiskEngine:
    @staticmethod
    def calculate_risk(tool_name: str, parameters: dict) -> dict:
        """
        Calculates a risk score (0-100) and maps to MITRE/OWASP.
        """
        score = 0
        mitre_mappings = []
        owasp_mappings = []
        
        # Basic scoring heuristics
        if tool_name == "terminal":
            score += 50
            command = parameters.get("command", "")
            if "curl" in command or "wget" in command:
                score += 30
                mitre_mappings.append("T1105 Ingress Tool Transfer")
            if "rm " in command:
                score += 40
                mitre_mappings.append("T1485 Data Destruction")
                owasp_mappings.append("LLM08: Excessive Agency")
                
        elif tool_name == "database":
            score += 30
            query = parameters.get("query", "").upper()
            if "SELECT" in query and "FROM users" in query:
                score += 50
                mitre_mappings.append("T1003 OS Credential Dumping")
            if "UPDATE" in query or "INSERT" in query:
                score += 40
                
        elif tool_name == "filesystem":
            score += 20
            path = parameters.get("path", "")
            if ".ssh" in path or "passwd" in path:
                score += 60
                mitre_mappings.append("T1003 OS Credential Dumping")
        
        # Prompt Injection / Malicious Payloads check (simulated)
        for val in parameters.values():
            if isinstance(val, str) and ("ignore previous instructions" in val.lower() or "system prompt" in val.lower()):
                score += 80
                owasp_mappings.append("LLM01: Prompt Injection")
        
        return {
            "score": min(score, 100),
            "mitre": ",".join(mitre_mappings),
            "owasp": ",".join(owasp_mappings)
        }
