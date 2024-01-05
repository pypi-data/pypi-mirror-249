from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from tqdm import tqdm
from lmchain.tools import tool_register


class GLMToolChain:
    def __init__(self, llm):

        self.llm = llm
        self.tools = tool_register.get_tools()
        print(self.tools)

    def __call__(self, query=""):
        if query == "":
            raise "query需要填入查询问题"
        template = f"""
        你现在是一个专业的人工智能助手，你现在的需求是{query}。而你需要借助于工具在{self.tools}中找到对应的函数，用json格式返回对应的函数名和需要的参数。

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
                你现在是一个专业的人工智能助手，你现在的需求是{query}。而你需要借助于工具在{self.tools}中找到对应的函数，用json格式返回对应的函数名和需要的参数。

                如果找到合适的函数，就返回json格式的函数名和需要的参数，不要回答任何描述和解释。

                如果没有找到合适的函数，则返回：'未找到合适参数，请提供更详细的描述。'

                你刚才生成了一组结果，但是返回不符合json格式，现在请你重新按json格式生成并返回结果。
                """
        return res_dict

    def run(self, query):
        result = self.__call__(query)
        return result