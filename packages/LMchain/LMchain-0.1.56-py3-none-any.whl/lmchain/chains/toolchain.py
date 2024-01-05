from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from tqdm import tqdm
from lmchain.tools import tool_register


class GLMToolChain:
    def __init__(self, llm):

        self.llm = llm
        self.tool_register = tool_register
        self.tools = tool_register.get_tools()

    def __call__(self, query="", tools=None):

        if query == "":
            raise "query需要填入查询问题"
        if tools != None:
            self.tools = tools
        else:
            raise "将使用默认tools完成函数工具调用~"
        template = f"""
        你现在是一个专业的人工智能助手，你现在的需求是{query}。而你需要借助于工具在{self.tools}中找到对应的函数，用json格式返回对应的函数名和参数。

        如果找到合适的函数，就返回json格式的函数名和需要的参数，不要回答任何描述和解释。

        如果没有找到合适的函数，则返回：'未找到合适参数，请提供更详细的描述。'
        """

        flag = True
        while flag:
            try:
                res = self.llm(template)

                import json
                res_dict = json.loads(res)
                res_dict = json.loads(res_dict)
                flag = False
            except:
                template = f"""
                你现在是一个专业的人工智能助手，你现在的需求是{query}。而你需要借助于工具在{self.tools}中找到对应的函数，用json格式返回对应的函数名'function_name'和完整的有对比的参数'params'。

                如果找到合适的函数，就返回json格式的函数名和需要的参数，不要回答任何描述和解释。

                如果没有找到合适的函数，则返回：'未找到合适参数，请提供更详细的描述。'

                你刚才生成了一组结果，但是返回不符合json格式，现在请你重新按json格式生成并返回结果。
                """
        return res_dict

    def run(self, query, tools=None):
        result = self.__call__(query, tools)
        return result

    def add_tools(self, tool):
        self.tool_register.register_tool(tool)
        return True

    def dispatch_tool(self, tool_result) -> str:
        tool_name = tool_result["function_name"]
        tool_params = tool_result["params"]
        if tool_name not in self.tool_register._TOOL_HOOKS:
            return f"Tool `{tool_name}` not found. Please use a provided tool."
        tool_call = self.tool_register._TOOL_HOOKS[tool_name]

        try:
            ret = tool_call(**tool_params)
        except:
            ret = traceback.format_exc()
        return str(ret)


if __name__ == '__main__':
    from lmchain.agents import llmMultiAgent

    llm = llmMultiAgent.AgentZhipuAI()

    from lmchain.chains import toolchain

    tool_chain = toolchain.GLMToolChain(llm)

    from typing import get_origin, Annotated


    # from lmchain.tools import tool_register
    # @tool_chain.tool_register.register_tool
    def rando_numbr(
            seed: Annotated[int, 'The random seed used by the generator', True],
            range: Annotated[tuple[int, int], 'The range of the generated numbers', True],
    ) -> int:
        """
        Generates a random number x, s.t. range[0] <= x < range[1]
        """
        import random
        return random.Random(seed).randint(*range)


    print("------------------------------------------------------")

    # tool_chain.tool_register.register_tool(rando_numbr)
    tool_chain.add_tools(rando_numbr)
    tools = (tool_chain.tool_register.get_tools())

    print("------------------------------------------------------")
    query = "今天shanghai的天气是什么？"
    result = tool_chain.run(query, tools)
    print(result)

    result = (tool_chain.dispatch_tool(tool_name=result["function_name"], tool_params=result["params"]))
    print(result)



