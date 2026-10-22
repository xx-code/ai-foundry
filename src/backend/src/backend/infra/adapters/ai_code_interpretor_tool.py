from backend.app.adapters.ai_code_interpretor_tool import AiCodeInterpretorTool
from langchain_capsule import CapsuleJSREPLTool, CapsuleJSTool, CapsulePythonREPLTool, CapsulePythonTool
from langchain_core.tools import BaseTool

class CapsuleAiCodeInterpretor(AiCodeInterpretorTool):
    def get_python_interpretor(self) -> BaseTool | None:
        return CapsulePythonTool()

    def get_python_interpretor_repl(self) -> BaseTool | None:
        return CapsulePythonREPLTool()

    def get_js_interpretor(self) -> BaseTool | None:
        return CapsuleJSTool()

    def get_js_interpretor_repl(self) -> BaseTool | None:
        return CapsuleJSREPLTool()
