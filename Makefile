# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run EDA_Netflix_Data.py

# ----------------------------------
#    LOCAL CLEAN COMMANDS
# ----------------------------------

check_black:
	@black --check .

black:
	@black .

my_py:
	@mypy EDA_Netflix_Data.py
