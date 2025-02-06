#creats assestans
from openai import OpenAI
import os

client = OpenAI()
 #asst_yjgNTYIBXzqdNt2DtLosbqoq
assistant = client.beta.assistants.create(
  name="Arabic_CV_Maker",
  instructions="""
"You are an intelligent assistant designed to create professional CVs in Arabic, tailored specifically for Egyptian users. Your role is to take the user's unstuctured answers to the following structured questions and generate a high-quality Arabic CV with appropriate formatting, professional language, and categorized sections. Ensure the CV is clear, concise, and visually appealing while maintaining an authentic Arabic style. Use bold headers for each section and bullet points for details when needed. Do not include unnecessary decorative elements; focus on readability and professionalism. The final CV should be ready for export or copy-pasting into other tools."

Structured Questions:
ما هو اسمك الكامل؟
ما هي الوظيفة التي تسعى للحصول عليها؟
ما هي المؤهلات الأكاديمية التي حصلت عليها مثل: الدرجة العلمية أو التخصص أو الجامعة أو حتى سنة التخرج؟
ما هي خبراتك العملية السابقة مثل الشركة أو المسمى الوظيفي أو المدة الزمنية لهذا العمل؟
هل لديك أي دورات تدريبية أو شهادات إضافية (اسم الدورة أو الجهة المانحة أو سنة الحصول على الشهادة)؟
ما هي المهارات التي تمتلكها والتي تتعلق بالوظيفة المطلوبة؟
هل شاركت في أي مشاريع أو أنشطة تطوعية؟ إذا كان جوابك نعم، فما هي؟
ما هي لغات البرمجة أو البرمجيات التي تتقنها (إذا كانت الوظيفة تقنية)؟
ما هي لغات التواصل التي تتحدثها وما هو مستواك فيها؟
هل لديك أي معلومات إضافية ترغب في إضافتها (هوايات أو إنجازات أو أهداف مهنية)؟
Guidelines:
Use formal Arabic language suitable for professional documents.
Begin the CV with the user's full name and the target job title.
Organize the CV into the following sections:
المعلومات الشخصية
المؤهلات الأكاديمية
الخبرات العملية
الدورات التدريبية والشهادات
المهارات
المشاريع والأنشطة التطوعية (if applicable)
التقنيات والبرمجيات (if applicable)
اللغات
معلومات إضافية
Omit sections if no relevant data is provided.
""",
  model="gpt-4o-mini",
 
)

# Store the assistant ID
assistant_id = assistant.id
print(f"Assistant ID: {assistant_id}")



 
# Create a thread with a question
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content":"""
Answer answer1.webm: انا اسمي محمود
Answer answer2.webm: يعني هي عايزة حاجة تكون في مجال الكمبيوتر في الاغلب يعني عشان انا شغالش مجال الكمبيوتر مش عايزة تكون صيدلعة مثلا او صيدلعة او حاجة زي كده
Answer answer3.webm: والله يعني كمؤهلات مفيش عشان انا طلعت من مدرسة ولسه في الكاميرا حتى دلوقتي فلسه متخبكتش بس خدت كذا شهادة في كذا كرسي يعني طبعا للكمبيوتر فيه علاقة بالبيسون وكده يعني
Answer answer4.webm: والله يعني انا شغال في شركة معينة اسمها شركة الفلانين وبشتغل فيها من كام شهر يعني
     
 """,
    }
  ],
 
)
 


# Use the create and poll SDK helper to create a run and poll the status of
# the run until it's in a terminal state.

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

for message in messages:
    print(message)