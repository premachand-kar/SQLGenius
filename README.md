# SQLGenius
 
## Problem Statement:
 
Non-technical businesses face challenges in accessing and analyzing critical data due to a lack of SQL knowledge, leading to dependencies on technical teams and bot
 
## Solution:
 
SQLGenius is a Streamlit application designed to help non-technical businesses access and analyze critical data without needing SQL knowledge. The app leverages opensource technologies IBM WATSONX/Groq API for LLM hosting, as well as Agno AI agent framework for  Database Connection, SQL Query generation, as well as SQL Query execution and provides a user-friendly interface to interact with databases.

##IBM WATSONX

![image](https://github.com/user-attachments/assets/6234e2ff-85c3-4029-961c-08496ae36efc)


##GROQ

![image](https://github.com/user-attachments/assets/59b74980-b82f-40ed-afc5-ad8229738c91)



## Features
 
- **Database Connectivity**: Connect to SQLite, PostgreSQL, or MySQL databases.
- **Schema Extraction**: Automatically extract and display the database schema.
- **SQL Generation**: Generate SQL queries based on natural language input.
- **Query Execution**: Execute SQL queries and display results in a data frame.

## Installation
 
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/sqlgenius.git
    cd sqlgenius
    ```
 
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
 
3. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
 
## Usage
 
1. **API Setup for IBM WATSONX.AI**:
    - Enter your watsonx API key,project id and watsonx.ai cloud url in the provided input field.
    - Select the preselected model: `ibm/granite-3-3-8b-instruc`.
  OR
    
    **API Setup for GROQ**:
     - Enter your Groq API key in the provided input field.
     - Select the preselected model: `llama3-8b-8192`.
2. **Database Configuration**:
    - Select the database type (SQLite, PostgreSQL, MySQL).
    - For SQLite, upload a SQL file to set up the database.
    - For PostgreSQL/MySQL, enter the necessary connection details (host, port, username, password, database name).
 
3. **Connect to Database**:
    - Click the "Connect to Database" button to establish a connection.
    - If successful, the database schema will be extracted and displayed.
 
4. **Enter Business Requirement**:
    - Describe your data requirement in natural language in the provided text area.
 
5. **Generate SQL**:
    - Click the "Generate SQL from Prompt" button to generate the SQL query.
    - Review and approve the generated SQL query.
 
6. **Run SQL**:
    - Click the "Approve and Run SQL" button to execute the query.
    - The results will be displayed in a data frame.
 
## Example Queries
 
- List all employees and their departments.
- Show who is working on the Website Redesign project.
- What is the total salary in the Engineering department?
- List all projects with a budget over 40,000 and the people working on them.
- List all clients and their contact information.
- Show the total hours worked by each employee on all projects.
- List all projects along with their start and end dates.
- Show the names of employees hired after January 1st, 2020.
 
## Contributing
 
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
 
## License
 
This project is licensed under the MIT License. See the LICENSE file for details.
 
## Acknowledgements
 
- Powered by https://www.groq.com/ and https://www.agno.com/.
 
## Team Name
The Quantum Coders

## Team Members

Dheeraj Khobragade \n
Rahul Bhave
Vaidehi Dilip Choudhari
Aayush Awari
Premachand Kar
