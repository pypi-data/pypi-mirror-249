from chatgpt_automation import ChatGPTAutomation

ChatGPTAutomation.DelayTimes.CONSTRUCTOR_DELAY = 10

chat = ChatGPTAutomation()


chat.login_with_gmail_from_zero("iamseyedalix", "@A1652438983701703366licom4470097756")

chat.send_prompt_to_chatgpt("Hello World")