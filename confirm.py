from prompt_toolkit.shortcuts import yes_no_dialog

def ConfirmPrompt(
        text:str="",
        title:str="",
        yes_text:str="Yes",
        no_text:str="No",
        style=None,
):
    answer = yes_no_dialog(text=text, title=title, yes_text=yes_text, no_text=no_text, style=style).run()
    return answer
