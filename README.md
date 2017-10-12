# Reinforcement Learning
## Project: Train a Smartcab How to Drive
## see https://m00nd00r.github.io/Smart-Cab/ for project info



## Install

This project requires **Python 2** and uses the Anaconda package manager.
If you haven't already please download and install Anaconda.

Instructions:
1. Clone the repository and navigate to the downloaded folder.
	
	```	
		git clone https://github.com/m00nd00r/Smart-Cab.git
		cd Smart-Cab
	```
    
2. Obtain the necessary Python packages.  
	
	For __Mac/OSX/Linux__:
	```
		conda create -f smartcab requirements/smartcab-osx.yml
		source activate smartcab
	```

	For __Windows__:
	```
		conda create -f smartcab requirements/smartcab-windows.yml
		activate smartcab

### Code

Template code is provided in the `smartcab/agent.py` python file. Additional supporting python code can be found in `smartcab/enviroment.py`, `smartcab/planner.py`, and `smartcab/simulator.py`. Supporting images for the graphical user interface can be found in the `images` folder. Most of this code has already been implemented so that I could focus on the algorithm implementation, my work can be found in the `LearningAgent` class in `agent.py`. 

### Run

In a terminal or command window, navigate to the top-level project directory `smartcab/` (that contains this README) and run one of the following commands:

```python smartcab/agent.py```  
```python -m smartcab.agent```

This will run the `agent.py` file and execute the agent code.
