class PolicyEngine:
    @staticmethod
    def evaluate(tool_name: str, parameters: dict) -> list[str]:
        """
        Evaluates a request against predefined enterprise policies.
        Returns a list of policy violations. If empty, the request passes.
        """
        violations = []
        
        # Policy: No writes or deletes on filesystem
        if tool_name == "filesystem":
            action = parameters.get("action")
            if action in ["write", "delete", "rm", "rmdir"]:
                violations.append("POLICY_VIOLATION: Unauthorized filesystem modification.")
                
        # Policy: No database drops
        if tool_name == "database":
            query = parameters.get("query", "").upper()
            if "DROP" in query or "TRUNCATE" in query or "DELETE" in query:
                violations.append("POLICY_VIOLATION: Destructive database operation.")
        
        # Policy: No shell commands as root or touching /etc
        if tool_name == "terminal":
            command = parameters.get("command", "")
            if "sudo" in command or "/etc/" in command:
                violations.append("POLICY_VIOLATION: Privileged execution or unauthorized path access.")
                
        return violations
