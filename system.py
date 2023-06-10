import collections
import random
import time
from itertools import count

DATA = collections.deque([])
RANDOM = random.randint(1, 100)


class Params:
    def __init__(self, parameters):
        for key, value in parameters.items():
            setattr(self, key, value.get())
        #self.A = int(parameters['sAgents'].get())
        s = int(self.sAgenci)
        self.sAgentList = [0] * s
        num_ones = random.randint(1, s)  # Generate a random number of ones between 1 and size

        indexes = random.sample(range(s), num_ones)  # Randomly select indexes to fill with ones

        for idx in indexes:
            self.sAgentList[idx] = 1


class Cycle:
    def __int__(self):
        self.V = []
        self.meanVs = 0.0
        self.meanVh = 0.0
        self.netOutflow = 0.0


# policy
def h_step(v, x):
    return 1.0 if v >= 1-x else 0.0


def s_bias_p(y, L):  # p
    return min(y, L)


def s_bias_r(z, L):  # r
    return min(z, L)


def provider_policy(A, p):  # Pij
    return min(A, p)


def reporter_policy(G, P, r):  # Rij
    return min(G*P, r)


def rand_expo_d(expo):
    return random.random() ** (1.0 / expo)


# --------------------
def plot(series):
    pass


def start_simulation(p, progress_fun, return_fun):
    DATA.clear()
    parameters = Params(p)
    for cycle in parameters.Cykle:
        sum_ph_to_s = 0.0
        number_hjs = 0
        sum_ps_to_h = 0.0
        number_sjh = 0
        counter_ss_coop = 0
        counter_all_coop = 0

        adj = [[0] * parameters.Agents for _ in range(parameters.Agents)]

        for i in range(parameters.Agents):
            count_c = 0
            clients = random.randint(parameters.kmin, parameters.kmax + 1)
            in_j = 0
            rn = 0
            while in_j < clients:
                rn = random.randint(0, parameters.Agents - 1)
                if rn != i and adj[i][rn] != 1:
                    adj[i][rn] = 1
                    if parameters.sAgenci[i] == 1:
                        if parameters.sAgenci[rn] != 1:
                            number_sjh += 1
                    else:
                        if parameters.sAgenci[rn] == 1:
                            number_hjs += 1
                    in_j += 1

        agents_r = {}

        for it in range(parameters.Agenci):
            clients = adj[it]
            v_prov = parameters['V0'] if cycle == 0 else DATA[cycle - 1]['V'][it]
            num_clients = clients.count(1)
            mean_policy_r = 0.0

            for j in range(parameters.Agenci):
                if adj[it][j] == 1:
                    v_repo = parameters['V0'] if cycle == 0 else DATA[cycle - 1]['V'][j]
                    l = h_step(v_repo, parameters['X'])
                    p = s_bias_p(parameters['Y'], l) if parameters.sAgenci[it] == 1 else l
                    if parameters.sAgenci[it] == 1 and parameters.sAgenci[j] == 1:
                        p = 1.0
                    policy_p = provider_policy(rand_expo_d(parameters['ExpoA']), p)
                    l = h_step(v_prov, parameters['X'])
                    r = s_bias_r(parameters['Z'], l) if parameters.sAgenci[j] == 1 else l
                    if parameters.sAgenci[it] == 1 and parameters.sAgenci[j] == 1:
                        r = 1.0
                    policy_r = reporter_policy(rand_expo_d(parameters['ExpoG']), policy_p, r)
                    mean_policy_r += policy_r * v_prov
                    if parameters.sAgenci[it] == 1 and parameters.sAgenci[j] == 1:
                        counter_ss_coop += 1
                    counter_all_coop += 1
                    if parameters.sAgenci[it] == 1:
                        if parameters.sAgenci[j] != 1:
                            sum_ps_to_h += policy_p
                    else:
                        if parameters.sAgenci[j] == 1:
                            sum_ph_to_s += policy_p

            mean_policy_r /= num_clients
            agents_r[it] = mean_policy_r

        sorted_by_r = dict(sorted(agents_r.items(), key=lambda x: x[1]))

        mean_r_higher_set = 0.0
        mean_r_lower_set = 0.0
        iter = 0

        for value in sorted_by_r.values():
            if iter < len(sorted_by_r) // 2:
                mean_r_lower_set += value
            else:
                mean_r_higher_set += value
            iter += 1

        mean_r_higher_set /= len(sorted_by_r) // 2
        mean_r_lower_set /= len(sorted_by_r) // 2

        mean_r_lower_set /= mean_r_higher_set
        mean_r_higher_set /= mean_r_higher_set

        V = [0.0] * parameters.Agenci
        iter = 0

        for key in sorted_by_r.keys():
            if iter < len(sorted_by_r) // 2:
                V[key] = mean_r_lower_set
            else:
                V[key] = mean_r_higher_set
            iter += 1

        mean_vs = 0.0
        mean_vh = 0.0

        for it in range(parameters.Agenci):
            if parameters.sAgenci[it] == 1:
                mean_vs += V[it]
            else:
                mean_vh += V[it]

        mean_vh /= parameters.Agenci - parameters['S']
        mean_vs /= parameters['S']

        net_outflow = (sum_ph_to_s / number_hjs) - (sum_ps_to_h / number_sjh)

        DATA.append(Cycle(V, mean_vs, mean_vh, net_outflow))

        time.sleep(0.01)
        progress_fun((cycle + 1) / parameters['NC'] * 100)

    series = [
        ("meanVh", [cycle['meanVh'] for cycle in DATA]),
        ("meanVs", [cycle['meanVs'] for cycle in DATA]),
        ("netOutflow", [cycle['netOutflow'] for cycle in DATA])
    ]
    plot(series)
    return_fun()


# cycle_thread = threading.Thread(target=cycle)
# cycle_thread.start()
