from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from thirdparty.thirdparty import gist_link
from agents.agents import lookup


if __name__ == "__main__":
    linkedin_profile_url = lookup(name="saurbh sharma")
    print("hello langchain")
    summary_template = """
    given the linkedin information {information} about the person. I want you to create
    1. Short summary
    2. two interesting fact
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    ### Get the linkedin data
    information = gist_link(
        "https://gist.githubusercontent.com/Kukreti12/413d55522d791cf9de0ae5feba22dc9c/raw/93f656ad6976f1bcaac888c054f2f35a13aafcbe/saurabh-sharma.json"
    )

    ## We can create linkedin profile url by using serp API

    print(chain.run(information=information))
