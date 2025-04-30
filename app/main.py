import os
import gradio as gr
from langchain_ollama import OllamaLLM
from langchain.agents import Tool
from langchain_community.utilities.serpapi import SerpAPIWrapper
#from langchain.tools import SerpAPIWrapper, Tool
from langchain.agents import initialize_agent, Tool
from gradio.themes.base import Base
from gradio.themes.utils import colors, sizes, fonts
#from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain_core.exceptions import OutputParserException


########################################################
######################## UI ############################
########################################################

# Theme Definition
class Modelworks(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.violet,
        secondary_hue: colors.Color | str = colors.indigo,
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=gr.themes.Color(
                c50="#FFFFFF", c100="#FFFFFF", c200="#AB96BD",
                c300="#AB96BD", c400="#B88CE8", c500="#B88CE8",
                c600="#655BA6", c700="#211D26", c800="#211D26",
                c900="#211D26", c950="#332F40"
            ),
        )
        super().set(
            body_background_fill="white",
            body_background_fill_dark="#1B102E",
            block_border_width="3px",
            block_shadow="*shadow_drop_lg",
            button_primary_shadow="*shadow_drop_lg",
            button_large_padding="32px",
        )

# Instantiate theme
main_theme = Modelworks()

# LLM & Search Tool
llm = OllamaLLM(model="gemma3:1b")


########################################################
################### CHATBOT LOGIC ######################
########################################################

# Configure SerpAPIWrapper for web search (you need your key)
search = SerpAPIWrapper(serpapi_api_key="53afbd074061caca8efc6036cacbb255962b2e8c4c39c5ebc156276cf0ba9241")
web_search_tool = Tool(
    name="Web Search",
    func=search.run,
    description="Use this to query current web results for a user’s query."
)


# Initialize a LangChain agent that can call web search + the LLM
agent = initialize_agent(
    tools=[web_search_tool], # comment to test without search
    # tools=[dummy], # uncomment to test without search
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False,  # set True to see tool calls in console
    handle_parsing_errors=True,
    max_execution_time=10 # TODO: This is a ridiculous processing time so change this if you want to implement it into the final product
)

# Chat Function
def chat_with_model(user_message, chat_history, rating):
    # """
    # Uses a LangChain agent to decide whether to call the Web Search tool or directly invoke the LLM.
    # Appends the chosen response to the chat history.
    # """

    # # Let the agent handle tool selection and LLM invocation
    # response = agent.run(user_message)
    # chat_history = chat_history + [(user_message, response)]
    # return chat_history, ""

    if (rating < 0): # in case the user has not touched the slider
        rating = 2.5

    try:
        if (rating >= 2.5):

            print("--- I am searching because I am good at my job... (: ---")
            result = agent.run(user_message)

            if (result == "Agent stopped due to iteration limit or time limit."):
                result = llm.invoke(user_message)
                result += "\n\n (this took me a while... sorry!)\n" # TODO: You can remove this

            result += "\n\n This model used: WEB SEARCH MODE\n" # TODO: You can remove this

        else:
            print("--- I am not searching because I am bad at my job... :( ---")
            result = llm.invoke(user_message)

            result += "\n\n This model used: DEFAULT MODE\n" # TODO: You can remove this

    except OutputParserException:
        # fallback: just ask the model directly
        print("--- I have failed... )X ---")
        result = llm.invoke(user_message)

    chat_history.append((user_message, result))
    return chat_history, ""


def change_stars(rating):

    rating = int(rating)

    stars = ""

    if (rating < 0):
        rating = 2.5

    if (rating < 1 and rating >= 0):
        stars = "<div style='display: flex; margin: auto; text-align: center;'> <h2 style='display: block;margin: auto; text-align: center;'>-----</h2> </div>"
    elif (rating < 2 and rating >= 1):
        stars = "<div style='display: flex; margin: auto; text-align: center;'> <h2 style='display: block;margin: auto; text-align: center;'>★----</h2> </div>"
    elif (rating < 3 and rating >= 2):
        stars = "<div style='display: flex; margin: auto; text-align: center;'> <h2 style='display: block;margin: auto; text-align: center;'>★★---</h2> </div>"
    elif (rating < 4 and rating >= 3):
        stars = "<div style='display: flex; margin: auto; text-align: center;'> <h2 style='display: block;margin: auto; text-align: center;'>★★★--</h2> </div>"
    elif (rating < 5 and rating >= 4):
        stars = "<div style='display: flex; margin: auto; text-align: center;'> <h2 style='display: block;margin: auto; text-align: center;'>★★★★-</h2> </div>"
    elif (rating >= 5):
        stars = "<div style='display: flex; margin: auto; text-align: center;'> <h2 style='display: block;margin: auto; text-align: center;'>★★★★★</h2> </div>"

    return stars


########################################################
##################### INTERFACE ########################
########################################################

with gr.Blocks(theme=main_theme) as demo:
    

    gr.Markdown("# Modelworks Chatbot with Web Search")
    
    chatbot = gr.Chatbot(label="Conversation")
    
    with gr.Row():
        msg = gr.Textbox(placeholder="Type your message here...", label="Your message")
        send = gr.Button("Send")

    stars = gr.Markdown("<div style='display: flex; margin: auto; text-align: center;'> <h2 style='display: block;'> </h2> </div>")
    
    rate = gr.Slider(0, 5, value=-1, step=1, label="Rating System", info="## How do you rate this response?",
                    show_label = False, show_reset_button = False)

    
    # TODO: this is just for show and can be deleted
    rate.input( 
        fn=change_stars, 
        inputs=[rate], 
        outputs=[stars], 
        api_name="rating_result")


    send.click(
        fn=chat_with_model,
        inputs=[msg, chatbot, rate],
        outputs=[chatbot, msg]
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
