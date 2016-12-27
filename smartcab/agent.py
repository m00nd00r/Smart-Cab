import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed
        
        self.num_trials = 0      # Initialized counter for epsilon decay in reset()

    
    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        self.testing = testing
        self.num_trials += 1
        
        #a = 0.01 #yields over 200 trials
        #a = 0.04 #yields 60 trials
        #a = 0.1 #yields only about 20 trials
        #a = 0.07 #yields about 50 trials
        #a = 0.06 #yields about 50 trials
        #a = 0.03 #yields about 100 trials
        #a = 0.025 #yields about 120 trials
        #a = 0.08 #yields about 40 trials
        #a = 0.02 #yields about 150 trials
        a = 0.015 #yields about 200 trials
        
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        
        if self.testing:
            self.epsilon = 0.0
            self.alpha = 0.0
        
        else:
            if self.learning:    
                #self.epsilon -= 0.0166
                self.epsilon = float(1)/math.exp(float( a * self.num_trials))
                #self.alpha = float(1)/math.exp(float( a * self.num_trials))
                #self.epsilon = float(1)/math.pow(self.num_trials,2)
                #self.epsilon = (1 + math.cos(2*math.pi + 0.04*self.num_trials))/2     #produces 68 trials
                #self.epsilon = (1 + math.cos(2*math.pi + 0.03*self.num_trials))/2     #produces 91 trials
                #self.epsilon = (1 + math.cos(2*math.pi + 0.02*self.num_trials))/2     #produces 136 trials
                
                #self.alpha -= 0.0166  #1/60
                #self.alpha = (1 + math.cos(2*math.pi + 0.04*self.num_trials))/2
                #self.alpha -= 0.0147  #1/68
                #self.alpha -= 0.011  #1/91
                self.alpha -= float(1)/200
            
        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline
        learning_inputs = {}

        ########### 
        ## TO DO ##
        ###########
        # Set 'state' as a tuple of relevant data for the agent
        
        # For this attempt at winnowing the state space for learning, I've decided that while
        # green, the smartcab can assume there is no cross-traffic, based on this code's implementation
        # for all the other agents behaving the traffic laws. Thus, if 'left' and 'right' agents have
        # a red light, smartcab won't have to worry about hitting them.
        #
        # Furthermore, when light is red, similarly, smartcab won't have to worry about the 'oncoming'
        # agent's behavior either.
        #
        # One further refinement will be that the smartcab will never have to worry about the 'left'
        # agent turning right under any conditions.
        
        if self.learning:
            
            #state = (waypoint, inputs['light'], ('oncoming',inputs['oncoming']), ('left',inputs['left']))
            
            if inputs['light'] == 'green':
                #if waypoint == 'forward' or 'right':             #forward and right are treated
                    learning_inputs['light'] = inputs['light']
                    learning_inputs['oncoming'] = inputs['oncoming'] #forward, right, or none are treated as equivalent here
 
                #else:
                #    if (inputs['oncoming'] == 'forward') or (inputs['oncoming'] == 'right'):
                #        learning_inputs['light'] = inputs['light']
                #        learning_inputs['oncoming'] = inputs['oncoming'] #forward and right are treated as equivalent
                #    else:
                #        learning_inputs['light'] = inputs['light']
                #        learning_inputs['oncoming'] = inputs['oncoming']  #left and None are treated as equivalent

            if inputs['light'] == 'red':
                learning_inputs['light'] = inputs['light']
                learning_inputs['left'] = inputs['left']
                #learning_inputs['right'] = inputs['right']
                #if waypoint == 'right':
                #    if inputs['left'] == 'right':
                #        learning_inputs['light'] = inputs['light']
                #        learning_inputs['left'] = inputs['left']
                #else:
                #    if (inputs['left'] == 'right') and (inputs['right'] == None):
                #        learning_inputs['light'] = 'red'
                #    else:
                #        learning_inputs['light'] = 'red'
                #        learning_inputs['left'] = inputs['left']
                #        learning_inputs['right'] = inputs['right']
            
            
            #if inputs['light'] == 'green' or 'red':
            #    learning_inputs['light'] = inputs['light']
            #    learning_inputs['oncoming'] = inpust=['oncoming']
            #    learning_inputs['left'] = inputs['left']
            #    #learning_inputs['right'] = None
               
            #state = str(learning_inputs)
            
            state = (waypoint, str(learning_inputs))
        else:
            state = (waypoint, str(inputs), deadline)
            
        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """
        
        self.state = state
        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state

        maxQ = max(self.Q[self.state], key=self.Q[self.state].get)
        #maxQ = max(q[state].values())

        return maxQ
    
    def rank_Q(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """
        
        self.state = state
        ########### 
        ## TO DO ##
        ###########
        # Sort the actions for a given state by Q-value from highest to lowest

        rankedQ = sorted(q[state], key=q[state].get, reverse = True)

        return rankedQ 


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """
        
        self.state = state
        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        
        if self.learning:
            self.Q.setdefault(self.state,dict((va,10.0) for va in self.valid_actions))
                

        return


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        #   Otherwise, choose an action with the highest Q-value for the current state
        
        # Choice action policy when not learning:
        # If Next Waypoint (NW) = left:
        #     If Q(state,action = left) > 0: action = left
        #     Else If Q(state, action = forward) > 0: action = forward
        #     Else: action = None
        #
        # If NW = right:
        #     If Q(state, action = right) > 0: action = right
        #     Else If Q(state, action = foreard > 0 action = forward
        #     Else: action = None
        #
        # If NW = forward and Q(state, action = forward): action = forward
        # Else: action = None 
        #     
        
        if self.learning:
            if random.random() < self.epsilon:
                action = random.choice(self.valid_actions)
            else:
                action = self.get_maxQ(self.state)
                #if self.next_waypoint == 'left':
                #    if self.get_maxQ(self.state) == 'left':
                #        action = 'left'
                #    elif self.Q[self.state]['forward'] > 0:
                #        action = 'forward'
                #    elif self.Q[self.state][None] > 0:
                #        action = None
                #    else:
                #        action = self.get_maxQ(self.state)
                #        
                #elif self.next_waypoint == 'right':
                #    if self.get_maxQ(self.state) == 'right':
                #        action = 'right'
                #    elif self.Q[self.state]['forward'] > 0:
                #        action = 'forward'
                #    elif self.Q[self.state][None] > 0:
                #        action = None
                #    else:
                #        action = self.get_maxQ(self.state)
                #        
                #elif (self.next_waypoint == 'forward') and (self.get_maxQ(self.state) == 'forward'):
                #    action = 'forward'
                #    
                #elif self.Q[self.state][None] > 0:
                #        action = None
                #else:
                #    action = self.get_maxQ(self.state)
        else:
            action = random.choice(self.valid_actions)

            
 
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards 
            when conducting learning. """
        
        self.state = state
        self.action = action
        self.reward = reward
        
        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
        
        if self.learning:
            #Q(s, a) = ((1 - alpha) * Q(s, a)) + (Reward * alpha)
            self.Q[self.state][self.action] = (1 - self.alpha)*self.Q[self.state][self.action] + (self.reward * self.alpha)
            #self.Q[self.state][self.action] = (1 - self.alpha)*self.get_maxQ(self.state) + (self.reward * self.alpha)
        
        #self.Q[str(state.items())][0]['forward']

        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent, learning = True, alpha = 1.0)
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline = True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env, display = False, update_delay = 0.005, log_metrics = True, optimized = True)
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test = 10)


if __name__ == '__main__':
    run()
