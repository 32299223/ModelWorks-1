# 🌐 ModelWorks : `model_confidence_logic_demo`
<h2 style="font-size: 24px;"> Purpose of Branch 🌀</h2>  

<p style="font-size: 16px;">  

This is a demonstration of the logic of the JoeyLLM interface, which aims to switch between different models (JoeyLLM, Gemma3, and OpenAI) depending on user satisfaction.  The model will switch in and out of web searching, **which is not intended for the final product**.  However, since this is a demonstration, this will suffice to show progress regarding this component.

This demonstration shows model "confidence" being done by using a five-star system, which the user can control with a slider.  

This uses code from the [web_search](https://github.com/southern-cross-ai/ModelWorks/tree/web_search) branch in order to be more simplified.  This will be improved upon with future commits.

</p>  

<h2 style="font-size: 24px;"> 👾 How to Use </h2>  

<p style="font-size: 16px;">  

This is effective when running localhost and your IDE in tandem.  Otherwise, the file currently shows how the logic works switching in and out of **web searching**.  

This will be done as so:

* If the user has not touched the slider, it is assumed that they are satisfied with the results, and thus the model confidence value is set at 2.5 (half of 5).
* If the user drags the slider to a value of 3 or over, the model will stick with web searching.
  * *(* ***NOTE:*** *Web searching tends to time out, but since this is a demonstration, there is a ***cutoff by 10 seconds*** before it switches to the much-faster default mode.  This is unreasonable and also ***will not allow the user to distinguish between whether it is web searching or not***, so the message "`(this took me a while... sorry!)`" will be appended to the model's response if this occurs )*
* If the user drags the slider to a value of 2 or under, the model will switch out of web searching and back into its default settings.
* The model can switch in and out of web searching whenever the user changes the slider.

You can see what is happening by paying attention to your terminal.  For example, when the model is running on web search, the following message will be outputted:

![what is happening in the UI (might not be obvious to the average user)](https://github.com/user-attachments/assets/73b1feeb-bae4-4849-b940-77f5d3cc50b6)

![terminal message outlined in red](https://github.com/user-attachments/assets/a552572d-8200-42c0-b24c-35541d6f3496)

</p> 
