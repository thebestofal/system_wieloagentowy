import collections
import random
import time
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA = collections.deque([])
RANDOM = random.randint(1, 100)


class Params:
    def __init__(self, parameters):
        for key, value in parameters.items():
            if key in ['x', 'y', 'z', 'V_0']:
                setattr(self, key, float(value.get()))
            else:
                setattr(self, key, int(value.get()))

        # self.A = int(parameters['sAgenci'].get())
        s = int(self.Agenci)
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

    def __init__(self, V, meanVs, meanVh, netOutflow):
        self.V = V
        self.meanVs = meanVs
        self.meanVh = meanVh
        self.netOutflow = netOutflow


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
def plot_on_frame(series, frame, canvas):
    n = len(series[0][1])
    x_values = list(range(1, n + 1))

    fig, ax = plt.subplots()
    for name, values in series:
        ax.plot(x_values, values, label=name)

    ax.set_xlabel("Cycle")
    ax.set_ylabel("Value")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def start_simulation(p, frame, canvas):
    DATA.clear()
    parameters = Params(p)
    for cycle in range(parameters.Cykle):
        sum_ph_to_s = 0.0
        number_hjs = 0
        sum_ps_to_h = 0.0
        number_sjh = 0
        counter_ss_coop = 0
        counter_all_coop = 0

        adj = [[0] * parameters.Agenci for _ in range(parameters.Agenci)]

        for i in range(parameters.Agenci):
            clients = random.randint(parameters.kmin, parameters.kmax + 1)
            in_j = 0
            while in_j < clients:
                rn = random.randint(0, parameters.Agenci - 1)
                if rn != i and adj[i][rn] != 1:
                    adj[i][rn] = 1
                    if parameters.sAgentList[i] == 1:
                        if parameters.sAgentList[rn] != 1:
                            number_sjh += 1
                    else:
                        if parameters.sAgentList[rn] == 1:
                            number_hjs += 1
                    in_j += 1

        Agenci_r = {}

        for it in range(parameters.Agenci):
            clients = adj[it]
            v_prov = parameters.V_0 if cycle == 0 else DATA[cycle - 1].V[it]
            num_clients = clients.count(1)
            mean_policy_r = 0.0

            for j in range(parameters.Agenci):
                if adj[it][j] == 1:
                    v_repo = parameters.V_0 if cycle == 0 else DATA[cycle - 1].V[j]
                    l = h_step(v_repo, parameters.x)
                    p = s_bias_p(parameters.y, l) if parameters.sAgentList[it] == 1 else l
                    if parameters.sAgentList[it] == 1 and parameters.sAgentList[j] == 1:
                        p = 1.0
                    policy_p = provider_policy(rand_expo_d(parameters.expoA), p)
                    l = h_step(v_prov, parameters.x)
                    r = s_bias_r(parameters.z, l) if parameters.sAgentList[j] == 1 else l
                    if parameters.sAgentList[it] == 1 and parameters.sAgentList[j] == 1:
                        r = 1.0
                    policy_r = reporter_policy(rand_expo_d(parameters.expoG), policy_p, r)
                    mean_policy_r += policy_r * v_prov
                    if parameters.sAgentList[it] == 1 and parameters.sAgentList[j] == 1:
                        counter_ss_coop += 1
                    counter_all_coop += 1
                    if parameters.sAgentList[it] == 1:
                        if parameters.sAgentList[j] != 1:
                            sum_ps_to_h += policy_p
                    else:
                        if parameters.sAgentList[j] == 1:
                            sum_ph_to_s += policy_p

            mean_policy_r /= num_clients
            Agenci_r[it] = mean_policy_r

        sorted_by_r = {k: v for k, v in sorted(Agenci_r.items(), key=lambda x: x[1])}
        # sorted_by_r = dict(sorted(Agenci_r.items(), key=lambda x: x[1]))

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
            if parameters.sAgentList[it] == 1:
                mean_vs += V[it]
            else:
                mean_vh += V[it]

        mean_vh /= parameters.Agenci - parameters.sAgenci
        mean_vs /= parameters.sAgenci

        net_outflow = (sum_ph_to_s / number_hjs) - (sum_ps_to_h / number_sjh)

        DATA.append(Cycle(V, mean_vs, mean_vh, net_outflow))

        time.sleep(0.01)
        print('Progres: ', (cycle + 1) / parameters.Cykle * 100)

    series = [
        ("meanVh", [cycle.meanVh for cycle in DATA]),
        ("meanVs", [cycle.meanVs for cycle in DATA]),
        ("netOutflow", [cycle.netOutflow for cycle in DATA])
    ]
    plot_on_frame(series, frame, canvas)


# cycle_thread = threading.Thread(target=cycle)
# cycle_thread.start()
