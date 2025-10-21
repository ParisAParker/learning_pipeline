End goal: I want to input a youtube video url into an application (Streamlit) and I want to two things outputs:
1. [X] I want a quiz with open-ended questions in pdf format
    - [X] On the backend that pdf should be saved somewhere
    - [X] The streamlit application should pull from filepath and display it so it can be downloaded from the UI

    - [] Add in option to choose how many questions are generated
        - Need to add in input on streamlit side for entering number of questions with a minimum and maximum range
        - That input should be saved as a variable and read into the function that generates the quiz
    - [] Add in option to choose between multiple choice or open-ended questions 

2. I also want a file of the questions and answers in csv format that can be loaded into Anki
- After rawopenai output is saved to json, create a loop that saves all of the questions and answers with explanation to anki flashcards