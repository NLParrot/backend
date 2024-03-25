# ALEX Chatbot (A.K.A Albatross school Life EXperience)
- [Design Document](DESIGNDOC.md)
- A Chatbot Assistant for Sogang University Freshmen
- A task oriented dialogue system, aimed to respond to common questions by freshmen
    - Chosen because RAG based chatbots can suffer from hallucinations, with high API costs
    - Aims for making a sustainable chatbot that can be run with low computational power.
    - Aims for easily extending user intent, and easy branching of actions corresponding to each intent
- This repository is for the AI backend of the web application


https://github.com/NLParrot/backend/assets/87269362/93b99a25-3db1-4cf1-a284-c95f7a3846f2



## Running the project
### Install dependencies
- First, install all the requirements in requirements.txt (In a preferred environment)
- Python version >= 3.11
```bash
pip install -r requirements.txt
```
### Run weaviate 
- In vector_data directory, use docker to run weaviate
```bash
docker compose up
```
- You can use the notebook file insert_data_weaviate to insert the data into weaviate db
### Run the server
- You can use gunicorn or flask dev server to run the application
```bash
gunicorn -w 4 -b 0.0.0.0:5000 chatapp.wsgi:app
flask -A chatapp.wsgi run
```

## Structure of the project
- Provides one API endpoint /api/chat/message
- Formulates a response based on the dialogue state, and user input
- Below is a Example Dialogue Pipeline (Included two of final intents)
![Image of Project Structure](img/structure.png)

1. Classifies user intent (Intent1, Intent2 classes)
    - Goes through two levels of models to enhance classification accuracy
2. Gets dialogue state by extracting entities in the sentence with a NER model. (NERState class)
3. Goes through a predefined pipeline based on user intent, current state, and DB query results
    - Uses handlers defined in response.py
    - Handlers are defined in actions/
    - Each handler .py file represents a major intent
    - Methods defined in handler .py represent a branch based on current state and DB query results.
4. Formulates a response, using templates from responses/
    - Uses .toml file type
    - defines utter, which are responses the chat system can give back 
        - There could be multiple sentences in utter, which makes interaction with the chatbot not repetetive, and more human-like
    - defines sets of variables that are used in utter, which are dynamically inserted in.
    - (Limitation: doesn't have good templating, so loop-related stuff has to be hardcoded in the handler .py)

## AI Models
### Models Used
- Fine-tuned KoElectra to achieve the following tasks: https://github.com/monologg/KoELECTRA
- User Intent Classification 
- Token Classification (Named Entity Recognition)

### Data used for Fine-tuning
- All data was written manually while working on the project

## DB Structure
### Weaviate Vector DB
- Embedding models used is: https://huggingface.co/jhgan/ko-sroberta-multitask
    - Selected by trying out different models
- Has a collection for CourseName, ProfessorName, Course, CourseEvaluation, Location
- CourseName, ProfessorName, Course is used for querying course names and professor names.
- CourseEvaluation is used to query a certain keyword within the course evaluation.
- Location is used for querying location names, and getting the coordinates.

### SQLite
- The DDL is defined in data/schema/
- If raw data has changed, you can run insert_into_sqlite_db.py to put the data into sqlite .db file

### NetworkX
- Not a proper DB, but a graph representing roads inside/around the university
- Data from OpenStreetMap
    - Fixed some data from openstreetmap


## Intents to be Added
- Greetings
- Looking for what chatbot can do
- Information / Recommendation of restaurants near the school
- School club information

## Known bugs
- DB from openstreetmap doesn't align well with kakao map api
- When searching for a path, doesn't use all the entrances of a building

