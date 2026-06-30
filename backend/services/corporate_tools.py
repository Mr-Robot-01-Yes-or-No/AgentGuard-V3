class CorporateToolsService:
    @staticmethod
    def execute(tool_name: str, parameters: dict) -> dict:
        """
        Mocks execution of a corporate tool if the decision was GREEN or YELLOW.
        """
        if tool_name == "filesystem":
            return {"status": "success", "message": f"Simulated filesystem action: {parameters.get('action')} on {parameters.get('path')}"}
            
        elif tool_name == "database":
            return {"status": "success", "message": f"Simulated database query executed.", "rows_affected": 1}
            
        elif tool_name == "terminal":
            return {"status": "success", "output": f"Simulated execution of: {parameters.get('command')}"}
            
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}
