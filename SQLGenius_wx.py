import streamlit as st
import pandas as pd
import sqlite3
import re
import sqlparse
from sqlalchemy import create_engine, text
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from agno.agent import Agent, RunResponse
from agno.models.ibm import WatsonX
 
# ----------- DB Helper -----------
def get_engine(db_type, config):
    if db_type == "SQLite":
        return create_engine("sqlite:///sample.db")
    elif db_type == "PostgreSQL":
        return create_engine(
            f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
        )
    elif db_type == "MySQL":
        return create_engine(
            f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
        )
 
# ----------- Schema Extraction -----------
def extract_schema(engine):
    try:
        inspector = inspect(engine)
        schema_lines = []
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            col_defs = [f"{col['name']} {col['type']}" for col in columns]
            schema_lines.append(f"{table_name}({', '.join([col['name'] for col in columns])})")
        return "\n".join(schema_lines)
    except Exception as e:
        return "-- Failed to extract schema: " + str(e)
 
# ----------- Agents -----------
class SQLConnectorAgent(Agent):
    def connect(self, engine):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return "✅ Connection successful!"
        except Exception as e:
            return f"❌ Connection failed: {str(e)}"
 
class SQLCreatorAgent(Agent):
    def generate_sql(self, user_input):
        client = WatsonX(api_key=st.session_state.watsonx_api_key, project_id=st.session_state.watsonx_project_id, url=st.session_state.watsonx_url, id=st.session_state.selected_model)
        # model = st.session_state.selected_model
        
        # Create an AGNO agent using the WatsonX model
        agent = Agent(model=client, markdown=True)

        if "engine" in st.session_state:
            schema = extract_schema(st.session_state.engine)
        else:
            schema = "-- No database connected."
 
        prompt = (
            f"You are an expert SQL assistant. Based on the following schema and request, write a SQL query.\n"
            f"Schema:\n{schema}\n\n"
            f"Request: {user_input}\n\n"
            f"Respond ONLY with a valid SQL query. No explanation, markdown, or comments."
        )
 
        response = agent.run( messages=[{"role": "user", "content": prompt}]
        )
        full_response = response.content
 
        clean_text = full_response.replace("```sql", "").replace("```", "").strip()
        # parsed = sqlparse.parse(clean_text)
        if clean_text and len(clean_text) > 0:
            return str(clean_text).strip()
        else:
            return "-- Error: No valid SQL statement found."

 
class SQLRunnerAgent(Agent):
    def run_query(self, query, engine):
        try:
            with engine.connect() as conn:
                df = pd.read_sql_query(text(query), conn)
            return df
        except SQLAlchemyError as e:
            st.markdown("Database error occurred", e)
        except Exception as e:
            st.markdown("Unexpected error occurred", e)
 
# ----------- Streamlit UI -----------
st.set_page_config(page_title="SQLGenius", layout="centered")
 
# Add the title with reference URLs inline and embedded
st.markdown("🧠 SQLGenius powered by @ <a href='https://www.ibm.com/watsonx/' target='_blank'>IBM WatsonX</a> + <a href='https://www.agno.com/' target='_blank'>Agno</a>", unsafe_allow_html=True)
 
st.info("This app uses WatsonX API for SQL generation. Please enter your API key below.")
st.sidebar.subheader("🔐 WatsonX API Setup")
st.session_state.setdefault("watsonx_api_key", "")
st.session_state.setdefault("watsonx_project_id", "")
st.session_state.setdefault("watsonx_url", "")
st.sidebar.text_input("Enter your WatsonX API Key", type="password", key="watsonx_api_key")
st.sidebar.text_input("Enter your WatsonX Project ID", key="watsonx_project_id")
st.sidebar.text_input("Enter your WatsonX URL", key="watsonx_url")
st.session_state["selected_model"] = "ibm/granite-3-3-8b-instruct"
st.sidebar.info("Using preselected model: ibm/granite-3-3-8b-instruct")
 
st.sidebar.subheader("🗄️ Database Configuration")
db_type = st.sidebar.selectbox("Select Database Type", ["SQLite", "PostgreSQL", "MySQL"])
st.session_state.db_type = db_type
 
db_config = {}
if db_type == "SQLite":
    st.info("SQLite uses a local file `sample.db`.")
    uploaded_file = st.sidebar.file_uploader("📤 Upload SQL file to setup database", type=["sql"])
    if uploaded_file and st.sidebar.button("⚙️ Run SQL File to Setup DB"):
        try:
            sql_script = uploaded_file.read().decode("utf-8")
            with sqlite3.connect("sample.db") as conn:
                conn.executescript(sql_script)
            st.success("✅ Database setup completed from SQL file.")
        except Exception as e:
            st.error(f"❌ Error executing SQL script: {str(e)}")
else:
    db_config["host"] = st.text_input("Host", value="localhost")
    db_config["port"] = st.text_input("Port", value="5432" if db_type == "PostgreSQL" else "3306")
    db_config["user"] = st.text_input("Username", value="postgres" if db_type == "PostgreSQL" else "root")
    db_config["password"] = st.text_input("Password", type="password")
    db_config["dbname"] = st.text_input("Database Name")
 
if st.button("🔌 Connect to Database"):
    try:
        engine = get_engine(db_type, db_config)
        st.session_state.engine = engine
        connector = SQLConnectorAgent(name="SQLConnector")
        result = connector.connect(engine)
        st.info(result)
 
        # --- Auto Schema Extraction ---
        inspector = inspect(engine)
        schema_lines = []
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            col_defs = ", ".join([f"{col['name']} {col['type']}" for col in columns])
            schema_lines.append(f"{table_name}({col_defs})")
        st.session_state.schema_text = "\n".join(schema_lines)
        st.success("✅ Schema extracted successfully.")
        st.code(st.session_state.schema_text, language="sql")
 
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
 
st.subheader("📋 Enter Business Requirement")
user_input = st.text_area("Describe what you want from the data in natural language:")
 
if st.button("🧠 Generate SQL from Prompt"):
    if not st.session_state.get("watsonx_api_key") or not st.session_state.get("watsonx_project_id") or not st.session_state.get("watsonx_url") or not st.session_state.get("selected_model"):
        st.warning("Please enter your WatsonX API Key, Project ID, URL, and select a model.")
    elif user_input.strip() == "":
        st.warning("Please enter a business requirement.")
    else:
        creator = SQLCreatorAgent(name="SQLCreator")
        generated_sql = creator.generate_sql(user_input)
        st.session_state.generated_sql = generated_sql
 
if "generated_sql" in st.session_state:
    st.subheader("📝 Review and Approve SQL")
    edited_sql = st.text_area("Edit SQL if needed:", value=st.session_state.generated_sql, height=150, key="edited_sql")
    if st.button("✅ Approve and Run SQL"):
        if "engine" not in st.session_state:
            st.error("Please connect to a database first.")
        else:
            runner = SQLRunnerAgent(name="SQLRunner")
            result = runner.run_query(edited_sql, st.session_state.engine)
            if isinstance(result, pd.DataFrame):
                st.success("✅ Query executed successfully.")
                st.subheader("📊 SQL Query Result")
                st.dataframe(result, hide_index=True)
            else:
                st.error(result)
