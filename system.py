import collections
import random
import time
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import csv
from datetime import datetime

DATA = collections.deque([])
random.seed(100)


class Params:
    def __init__(self, parameters):
        for key, value in parameters.items():
            if key in ['x', 'y', 'z', 'V_0', 'expoA', 'expoG']:
                setattr(self, key, float(value.get()))
            else:
                setattr(self, key, int(value.get()))

        s = int(self.Agenci)
        self.sAgentList = [0] * s

        indexes = random.sample(range(s), int(self.sAgenci))  # Randomly select indexes to fill with ones

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
def save_to_csv(series, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Cycle'] + [name for name, _ in series])  # Nagłówki kolumn

        n = len(series[0][1])
        x_values = list(range(1, n + 1))

        for i in range(n):
            row = [x_values[i]] + [values[i] for _, values in series]
            writer.writerow(row)


def plot_on_frame(series):
    n = len(series[0][1])
    x_values = list(range(1, n + 1))

    fig, ax = plt.subplots()
    for name, values in series:
        ax.plot(x_values, values, label=name)

    ax.set_xlabel("Cycle")
    ax.set_ylabel("Value")
    ax.legend()

    plt.show()


def start_simulation(p):
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

        formatDataKMeans = []

        for iR in range(len(Agenci_r)):
            formatDataKMeans.append([Agenci_r[iR], 1])

        kmeans = KMeans(n_clusters=2, random_state=42, n_init=50)
        kmeans.fit(formatDataKMeans)
        labels = kmeans.predict(formatDataKMeans)


        mean_r_higher_set = 0.0
        mean_r_lower_set = 0.0
        c1 = 0
        c0 = 0
        for x in range(len(labels)):
            if labels[x] == 1:
                mean_r_higher_set += Agenci_r[x]
                c1 += 1
            else:
                mean_r_lower_set += Agenci_r[x]
                c0 += 1

        mean_r_higher_set /= c1
        mean_r_lower_set /= c0

        swap = False
        if mean_r_higher_set < mean_r_lower_set:
            tmp = mean_r_lower_set
            mean_r_lower_set = mean_r_higher_set
            mean_r_higher_set = tmp
            swap = True

        print(f'meanRHigherSet: {mean_r_higher_set}, meanRLowerSet: {mean_r_lower_set}')

        mean_r_lower_set /= mean_r_higher_set
        mean_r_higher_set /= mean_r_higher_set

        V = [0.0] * parameters.Agenci
        iter = 0

        for label in labels:
            if label == 1:
                if swap:
                    V[iter] = mean_r_lower_set
                else:
                    V[iter] = mean_r_higher_set
            else:
                if swap:
                    V[iter] = mean_r_higher_set
                else:
                    V[iter] = mean_r_lower_set
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
        print(f'netOutflow: {net_outflow}, sumPHToS: {sum_ph_to_s}', end=' ')
        print(f'numberHJS: {number_hjs}, sumPSToH: {sum_ps_to_h}, numberSJH: {number_sjh}')
        print(f'meanRHigherSet: {mean_r_higher_set}, meanRLowerSet: {mean_r_lower_set}')
        print(f'meanVs: {mean_vs}, meanVh: {mean_vh}')

        print('Progres: ', round((cycle + 1) / parameters.Cykle * 100), '%',  end='\n\n')

    series = [
        ("meanVh", [cycle.meanVh for cycle in DATA]),
        ("meanVs", [cycle.meanVs for cycle in DATA]),
        ("netOutflow", [cycle.netOutflow for cycle in DATA])
    ]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_to_csv(series, f'csv_data\\{timestamp}-data.csv')
    plot_on_frame(series)
