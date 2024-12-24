## Steps to set-up the repository

1. Clone the repository
2. Create a new environment and install the lightrag package
```
python -m venv env
source env/bin/activate
pip install git+https://github.com/HKUDS/LightRAG.git
```
3. Additionally run the following command to install the required dependencies
```
pip install -r requirements.txt
```
4. Create a `.env` file in the root directory of the project and add the following variables:
```
AZURE_OPENAI_API_VERSION = ""
AZURE_OPENAI_DEPLOYMENT = ""
AZURE_OPENAI_API_KEY = ""
AZURE_OPENAI_ENDPOINT=""
```
5. Run the `main.py` file to test the setup