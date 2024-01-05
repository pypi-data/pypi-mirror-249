import subprocess
import os
import time
from yml_create_functions import make_yml, make_network_agents_yml

network_agents_parameters = {
    "default": {
        "id_message": "NaN",
        "has_tv": "false",
        "cause": -1,
        "method": "NaN",

        "type": "dumb",
        "response": "NaN",
        "stance": "agree",
        "retweet": "NaN",
        "parent_id": "NaN"

    },

    "DumbViewer": [
        {"weight": 2},
        {"weight": 2, "has_tv": "true"}
    ],
    "HerdViewer": [
        {"weight": 2, "type": "herd", "stance": "against"},
        {"weight": 2, "type": "herd", "has_tv": "true"}
    ],
    "WiseViewer": [
        {"weight": 1, "type": "wise", "stance": "against"},
        {"weight": 1, "type": "wise", "has_tv": "true", "stance": "against"}
    ],

}

parameters = {
    "default_state": "{}",
    "load_module": "schema",
    "environment_agents": "[]",
    "environment_class": "schema.NewsEnvironmentAgent",
    "environment_params": {
        "prob_neighbor_spread": 0.02,  # 006
        "prob_tv_spread": 0.006,  # 001
        "prob_neighbor_cure": 0.006,  # 001
        "prob_backsliding": 0.01,  # 003
        "prob_dead": 0.006,  # 001,
        "prob_repost": 0.8,
        "hostility_weight": 1,  # Unused yet
        "mean_time_connection": 50,
        "var_time_connection": 30
    },
    "interval": 1,
    "max_time": 100,
    "name": "MixedViewers",
    "network_params": {
        "generator": "barabasi_albert_graph",
        "n": 5000,
        "m": 20
    },
    "num_trials": 1
}


for n in range(1):
    parameters_i = parameters.copy()
    network_agents_parameters_i = network_agents_parameters.copy()
    data = make_yml(parameters_i)
    data += make_network_agents_yml(network_agents_parameters_i)
    # with open("schema/simulation_tutorial.yml", "w") as file:
    #     file.write(data)

    command = "soil"
    command2 = "schema/simulation_tutorial.yml"
    start = time.time()

    output = subprocess.check_output([command, command2])
    end = time.time()
    seconds_simulation = str(end-start)
    print("SIMULATION'S SECONDS:", seconds_simulation)
