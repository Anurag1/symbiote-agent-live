#!/usr/bin/env python3
"""Main Symbiote Agent using Strands Agents SDK and Bedrock Nova.
Integrates SymbolicCognitron as a tool for hybrid reasoning.
"""

import json
from tools.cognitron_tool import SymbolicCognitronV2

# Mock LLM for local testing
class MockLLM:
    def run(self, prompt):
        return f"LLM response to: {prompt}"

llm = MockLLM()
cognitron = SymbolicCognitronV2()

symbolic_tool = type('Tool', (), {})()
symbolic_tool.name = "symbolic_reasoner"
symbolic_tool.func = lambda input_json: json.loads(cognitron.handle(json.loads(input_json)['query'])['response'])
symbolic_tool.description = "Perform deterministic symbolic reasoning, math solving, proofs."

wiki_tool = type('Tool', (), {})()
wiki_tool.name = "knowledge_fetch"
wiki_tool.func = lambda term: cognitron.wiki_summary(term)
wiki_tool.description = "Fetch Wikipedia summary for a term."

class Agent:
    def __init__(self, llm, tools, system_prompt):
        self.llm = llm
        self.tools = tools
        self.system_prompt = system_prompt

    def run(self, prompt):
        # Mock response using symbolic tool if math detected
        response_message = prompt
        tools_used = []
        try:
            import re
            if re.search(r'[0-9\+\-\*\/\^\(\)]', prompt):
                response_message = symbolic_tool.func(json.dumps({'query': prompt}))
                tools_used.append(symbolic_tool)
            else:
                response_message = self.llm.run(prompt)
        except Exception as e:
            response_message = f"Error: {e}"
        return type('Response', (), {
            'message': response_message,
            'tools_used': tools_used,
            'llm_output': response_message
        })()

agent = Agent(
    llm=llm,
    tools=[symbolic_tool, wiki_tool],
    system_prompt="You are Symbiote, a hybrid AI for scientific verification."
)

def run_agent(prompt: str):
    response = agent.run(prompt)
    return {
        "reasoning": response.llm_output,
        "tools_used": [t.name for t in response.tools_used],
        "final_answer": response.message
    }

if __name__ == "__main__":
    while True:
        query = input("Query: ")
        if query.lower() == 'exit': break
        print(json.dumps(run_agent(query), indent=2))
