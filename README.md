# Introduction
Maintaining efficient incident response plans becomes more difficult for corporations as cyber threats become more complex. In order to provide analysts with situational, actionable guidance, traditional methodologies sometimes rely on static playbooks that are not flexible enough to react to changing threat scenarios. 

In order to fill these gaps, we have created an AI-powered chatbot named **MiAtbot** that provides users with real-time, structured guidance that is based on industry standards, enhanced with the most recent threat data from MITRE ATT&CK ™ Framework, and customized to meet their individual needs.

# Getting Started
1. Clone this repository
2. Download the necessary libraries needed by running `pip install -r requirements.txt`
3. Replace the file path of the datasets that is commented in the `Group4_colab.ipynb`

# Getting the model up 
1. Run the `Group4_colab.ipynb` or Head to the [Google Collab](https://colab.research.google.com/drive/1KrPfP6u594aX5QFIE74w4oJ2XVpNP_ON?usp=sharing) and run all the code there
2. Get the dataset (updated_aptgroup_relationships.xlxs) and convert it into a csv format.

# Running the chatbot
1. To run the chatbot, run `python main.py` then open the link provided, http://127.0.0.1:5000
2. Proceed to ask the chatbot about the following queries available:
    - What is the `Techniques ID` or `Techniques Name`?
    - What is the `Group ID` or `Group Name`?
    - What is `Tactics`?
