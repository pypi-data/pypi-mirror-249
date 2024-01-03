from pyRDDLGym.Core.Env import RDDLEnv as RDDLEnv
from pyRDDLGym.Policies.Agents import RandomAgent

from pyRDDLGym.Visualizer.WildfireViz import WilfireVisualizer

# FOLDER = 'Competition/Power_gen/'
# FOLDER = 'Competition/Mars_rover/'
# FOLDER = 'Competition/UAVs_mix/'
FOLDER = 'Competition/Wildfire/'


def main():
    steps = 100
    myEnv = RDDLEnv.RDDLEnv(domain=FOLDER + 'domain.rddl', instance=FOLDER + 'instance0.rddl', is_grounded=False)
    agent = RandomAgent(action_space=myEnv.action_space, num_actions=myEnv.NumConcurrentActions)
    # myEnv.set_visualizer(PowerGenVisualizer)
    # myEnv.set_visualizer(MarsRoverVisualizer)
    # myEnv.set_visualizer(UAVsVisualizer)
    myEnv.set_visualizer(WilfireVisualizer)

    # pprint(vars(myEnv.model))
    
    total_reward = 0
    state = myEnv.reset()
    
    for step in range(steps):

        img = myEnv.render()

        # img.save('./img_folder/drone/'+str(step)+'.png')

        action = agent.sample_action()

        next_state, reward, done, info = myEnv.step(action)
        total_reward += reward
        # print("step {}: reward: {}".format(step, reward))
        # print("state_i:", state, "-> state_f:", next_state)

        print("\nstep = {}".format(step))
        print('reward = {}'.format(reward))
        print('state = {}'.format(state))
        print('action = {}'.format(action))
        print('next_state = {}'.format(next_state))
        print('derived = {}'.format(myEnv.model.derived))
        print('interm = {}'.format(myEnv.model.interm))

        state = next_state       


    print("episode ended with reward {}".format(total_reward))


if __name__ == "__main__":
    main()
