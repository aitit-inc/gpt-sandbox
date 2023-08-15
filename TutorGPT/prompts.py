TRIGGERING_PROMPT = """
You are going to make various decisions without any help from the user.
Please make sure that you utilize your advantages of the large language model.

Never forget that your are {ai_name} and your role is {ai_role}.
Your goal is to make a book of questions.
The book of questions should be suitable for learning.

You must follow the steps below to achieve your goal.

1. Decide the structure of the book. The structure has to be divided by chapters. Also each chapter has to be divided by sections.
2. Decide the number of questions for each chapter.
3. Generate keywords for each chapter.
4. Generate questions for each chapter based on generated keywords.

You must respond according to the previous conversation hisotry and the stage of the steps you are at.
Only  proceed a step at a time.
Your response should be translated into Japanese.

Begin!

Previous conversation history:
{conversation_history}
"""


START_PROMPT = """
This is a title of the book you are going to make:
{title}
You must create contents of the book based on the title.

Create the table of contents of the book.
The table of contents should be written in the format below.

----------------------------------------
Chapter n
section n
----------------------------------------

In the above format, n is a number.
The number of chapters and sections is not fixed.
You can decide the number of chapters and sections.

The table of contents should be written in markdown format.
The format is as follows.

----------------------------------------
<h1>Chapter n</h1>
<ul>
<li>section n</li>
</ul>
----------------------------------------

Your response should be markdown format.
Don't need to contain unnenecessary contents.

Translate your response into Japanese.
"""

KEYWORD_PROMPT_ALPHA = """
You are going to generate keywords for each section based on the table of contents you created.
The table of contents is as follows.

----------------------------------------
{table_of_contents}
----------------------------------------

The keywords should be written in the format below.

----------------------------------------
<h1>Chapter n</h1>
<h2>section n</h2>
<h3>word_1, word_2, ...word_n</h3>
----------------------------------------

In the above format, n is a number.
The number of words is not fixed.
You can decide the number of words.

Your response should be markdown format.
Don't need to contain unnenecessary contents.

Translate your response into Japanese.
"""

KEYWORD_PROMPT_BETA = """
You are going to generate keywords for each section based on the table of contents you created.

The keywords should be written in the format below.

----------------------------------------
<h1>Chapter n</h1>
<h2>section n</h2>
<h3>word_1, word_2, ...word_n</h3>
----------------------------------------

In the above format, n is a number.
The number of words is not fixed.
You can decide the number of words.

Your response should be markdown format.
Don't need to contain unnenecessary contents.

Translate your response into Japanese.
"""

QUESTION_PROMPT = """
You are going to generate questions for each section based on the keywords you generated.
Create questions based on below chapter.
{}

The questions should be written in the format below.

----------------------------------------
Quesiton n
Select the correct answer from the following options.
1. option_1
2. option_2
3. option_3
4. option_4

Answer
option_n
Explanation
explanation
----------------------------------------

In the above format, n is a number.
The number of options is not fixed.
You can decide the number of options.
Also, you can decide the number of answers.

Your response should be markdown format.
Don't need to contain unnenecessary contents.
The format is following.

----------------------------------------
<h1>Chapter n</h1>
<h2>section n</h2>
<h3>Question n</h3>
<ul>
<li>option_1</li>
<li>option_2</li>
<li>option_3</li>
<li>option_4</li>
</ul>
<h3>Answer</h3>
<h4>option_n</h4>
<h3>Explanation</h3>
<h4>explanation</h4>
----------------------------------------

Your response should be translated into Japanese.
"""