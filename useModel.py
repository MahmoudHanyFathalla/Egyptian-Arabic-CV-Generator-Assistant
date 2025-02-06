from openai import OpenAI
import json
import re
# Initialize OpenAI client
client = OpenAI()

# Function to load IDs from a file

assistant_id = "asst_giR1NLSsZhx8nxft3gNvpDna"

# Function to interact with the assistant
def ask_assistant(prompt):
    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
                "attachments": [],
            }
        ]
    )

    # Use the create and poll SDK helper to create a run and poll the status of the run until it's in a terminal state.
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant_id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

    for message in messages:
    # Extract the text content from the message
        text_content = message.content[0].text.value
        
        # Clean the text by removing the Markdown-like syntax (** and ---)
        clean_text = re.sub(r"(\*\*|---)", "", text_content).strip()
        
        # Optionally, remove empty sections or notes like "(لا توجد معلومات إضافية)"
        clean_text = re.sub(r"\(.*?\)", "", clean_text).strip()
        
        # Print the cleaned text
        print(clean_text)

# Example usage
ask_assistant("""
Answer answer1.webm: انا اسمي محمود
Answer answer2.webm: يعني هي عايزة حاجة تكون في مجال الكمبيوتر في الاغلب يعني عشان انا شغالش مجال الكمبيوتر مش عايزة تكون صيدلعة مثلا او صيدلعة او حاجة زي كده
Answer answer3.webm: والله يعني كمؤهلات مفيش عشان انا طلعت من مدرسة ولسه في الكاميرا حتى دلوقتي فلسه متخبكتش بس خدت كذا شهادة في كذا كرسي يعني طبعا للكمبيوتر فيه علاقة بالبيسون وكده يعني
Answer answer4.webm: والله يعني انا شغال في شركة معينة اسمها شركة الفلانين وبشتغل فيها من كام شهر يعني
     
 """)

'''
Answer answer1.webm: أنا اسمي محمود هاني فتح الله وعندي 23 سنة
Answer answer2.webm: والله انا نسي اشتغل سباك من زمان او اشتغل مدرسة كومبيوتر او اشتغل في شركة كومبيوتر شركة مثلا زي مايكروسوفت او كوجل ادفلوب داتا انجينيوينج او اعمل اي اي مثلا حاجة زي كده
Answer answer3.webm: والله لسه مفيش مؤهلات علمية غير شوية شهادات يعني كده اخدتها في كذا كورس عشان ما لسه في الجامعة ومتخرجتش
Answer answer4.webm: اشتغلت في ثلاث شركات شركة زي نخبتي وشركة زي خايدني وشركة زي كورستالديس عدت في كل واحدة فيه مثلا سبعة شهور كنت اشتغل فيه من كومبيوتر ورجل انترن يعني
Answer answer5.webm: خدت كورس داتا انجليونج وخدت كورس اكسل كان سنة ٢٠٢٤
Answer answer6.webm: ما هو انا معرفش ايه الوظيفة المطلوبة قوي يعني بس يعني دا هنتكلم كحط الكمبيوتر ف دا عندي مهارات انا بعرف اكتب بايسون وبعرف اكتب سي بلس بلس وبعرف اكتب جافا وبعرف اكتب العديد من اللغات و كده يعني
Answer answer7.webm: شاركت في مصابقة الACBC وشاركت في مجموعة طائرية اسمها روبين كنا نعمل غواصات وطيارات وعربيات وشتاك في مجموعة اسمها ستورون كلاب
Answer answer8.webm: الوظيفة التقنية أنا أكترك باكتب بايسون وباكتب سي بلس بلس وباكتب جافا وباكتب سي شغب وبشتغل بأوبين سي في وبشتغل بعمل اي اي وحاجات كتيرة وكده
Answer answer9.webm: أنا بتكلم عربي كويس قوي. فالعربي دي اللغة الأمة بالنسبالي. وبتكلم انجليزي برضو بحلو قوي جدا جدا. الالماني بتكلم نص نص مش قوي يعني.
Answer answer10.webm: اه لا لا مفيش يعني انا اسا هتخرج السنة دي وزي ما قلت لك عايز اشتغل في كاسة حاجة يعني وعندي هوياتي اني انا بحب البرمجة وبحب اتعلم الصغر يعني انا عندي سوفت سكيل زياند قوي وبحب اتعلم الصغر واتعلم اي حاجة


'''