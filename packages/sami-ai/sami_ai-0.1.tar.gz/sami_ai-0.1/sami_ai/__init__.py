import requests

def sami_ai(text):
    dev = ["Sami", "المطور", "Dev", "dev", "المبرمج", "من برمجك", "سبايدر", "SaMi", "Mr.SaMi", "قناة", "قناة", "sami"]

    if text is None or text == "":
        error_message = "You must enter text. You have not entered text"
        return {"response": error_message}
    else:
        if text not in dev:
            headers = {
                'Host': '01d73592-4d64-43f7-b664-ecd679686756-00-30a5f50srzeko.janeway.replit.dev',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/16.3.1 hw/iPhone12_5',
                'Accept-Language': 'ar',
                'Content-Type': 'application/json;charset=UTF-8'
            }
            try:
                response = requests.get(f'https://01d73592-4d64-43f7-b664-ecd679686756-00-30a5f50srzeko.janeway.replit.dev/?msg={text}', headers=headers)
                result = response.json()["response"]
                sami = f"""
{result}
                """
                return {"response": sami}
            except Exception as e:
                return {"response": f"An unexpected error occurred. Try again. It will be fixed"}
        else:
            dev_ye = """
تم برمجتي بواسطة سامي من اليمن بلغات برمجة متقدمة لتنفيذ كل طلباتكم في البرمجة أو الاختراق أو التعليم. يمكنك الانضمام لقناة المطور عبر الرابط التالي: t.me/SaMi_ye
            """
            return {"response": dev_ye}
