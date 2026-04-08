# Student Course Scheduler

This course scheduler was made for UMASS Boston students to help find and build optimal, non-time conflicting class schedules that best fit their semester!

This project was made in the goal of solving a real-world problem that students face periodically. 
As a fellow student, I know building valid class schedules for our upcoming semesters can be time consuming and frustrating. 
Students might often resort to a schedule that "works" but might not be ideal or optimal

## Features: 
- In real-time it scrapes the data in open sections from the UMASS Boston course catalog
- It utilizes Depth-first search (DFS) to find all valid class combinations with backtracking
- Displays optimal schedules by scoring them based on time gaps (longer time gaps between classes = lower the score)
- Can run on command-line or a interactive web app interface (streamlit)

## How to use: 
- Run in terminal 'streamlit run app.py' to open the interactive browser
-  You can then enter the classes you want to take for the upcoming semester,
-  Select the days you prefer to take classes on,
-  (Optional) - Enter any time/class periods with their respective days that you want to avoid,
-  Click generate schedules to view results with the highest scores displayed first

## Screenshots

### Example image of the streamlit user interface:
<img width="1011" height="926" alt="streamlit user interface" src="https://github.com/user-attachments/assets/37343458-3768-46eb-92b8-f63af4ee5151" />

### Example image of the result output: 
<img width="740" height="805" alt="example results" src="https://github.com/user-attachments/assets/12abfeef-1636-4853-9fd9-ae5a5d4e315c" />


# Install streamlit
- pip install streamlit

# Install selenium:
- pip install selenium

# Run the streamlit app
- streamlit run app.py

OR:
- python -m streamlit run app.py
