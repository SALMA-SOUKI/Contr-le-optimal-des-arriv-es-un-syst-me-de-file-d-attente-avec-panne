N1 = 10
N2 = 10
mu1 = 10
mu2 = 12
lamda = 8
alpha = 2
beta = 2.5
gamma = mu1 + mu2 + lamda + alpha + beta
delta = 0.5
phi = gamma / (gamma + delta)
c1 = 1
c2 = 5
xi = 90

States = list()
i = 0
j = 0
for i in range(N1 + 1):
    for j in range(N2 + 1):
        States.append((i, j, 0))
        States.append((i, j, 1))

Actions = [0, 1, 2]

policy = dict()
for s in States:
    policy[s] = Actions[2]


def cout(s, a):
    return s[0] * c1 + s[1] * c2


def P(s_next, s, a, working):
    if working:
        if s_next[0] == s[0] and s_next[1] == s[1] and s_next[2] == 0:
            # print("meme etat")
            return alpha
        elif s_next[0] == s[0] and s_next[1] == s[1] and s_next[2] == 1:
            # print("changement de fonctionement")
            return beta
        elif s_next[1] == s[1] and (s_next[0] == s[0] - 1 or s_next[0] == 0) and s_next[2] == s[2]:
            # print("service file1")
            return mu1
        elif s_next[0] == s[0] and (s_next[1] == s[1] - 1 or s_next[1] == 0) and s_next[2] == s[2]:
            # print("service file2")
            return mu2
        else:
            # print("rien")
            return 0
    else:
        if s_next[0] == s[0] and s_next[1] == s[1] and s_next[2] == s[2]:
            # print("meme etat")
            return alpha + mu1
        elif s_next[0] == s[0] and s_next[1] == s[1] and s_next[2] != s[2]:
            # print("changement de fonctionement")
            return beta
        elif s_next[0] == s[0] and (s_next[1] == s[1] - 1 or s_next[1] == 0) and s_next[2] == s[2]:
            # print("service file2")
            return mu2
        else:
            # print("rien")
            return 0


def policy_evaluation_improvement(policy, S, working, lamda=lamda):
    V = {s: 0 for s in S}
    x = 0
    while True:
        x = x + 1
        oldV = V.copy()
        newPolicy = {}
        for s in S:
            a = policy[s]
            # V[s]=R(s,a)+sum(P(s_next,s,a)*oldV[s_next] for s_next in S)
            sClientAjouterFile1 = (min(s[0] + 1, N1), s[1], s[2])
            sClientAjouterFile2 = (s[0], min(s[1] + 1, N2), s[2])

            if s[2] == 0:
                min1 = min(oldV[s] + xi, oldV[sClientAjouterFile2])
            elif s[1] == N2:
                min1 = min(oldV[s] + xi, oldV[sClientAjouterFile1])
            elif s[1] == N1:
                min1 = min(oldV[s] + xi, oldV[sClientAjouterFile1])
            else:
                min1 = min(V[s] + xi, V[sClientAjouterFile1], V[sClientAjouterFile2])
        

            if min1 == V[s] + xi:
                indexOfAction = 2
            elif min1 == V[sClientAjouterFile1]:
                indexOfAction = 0
            elif min1 == V[sClientAjouterFile2]:
                indexOfAction = 1
            newPolicy[s] = indexOfAction
            a = newPolicy[s]
            V[s] = cout(s, indexOfAction) + pow(delta + gamma, -1) * phi * (
                    sum(P(s_next, s, a, working) * oldV[s_next] for s_next in S) + lamda * min1)
        if all(abs(oldV[s] - V[s]) < 0.1 for s in S):
            return [V, newPolicy]


def policy_iteration(S, A, working = True, policy=policy):
    while True:
        old_policy = policy.copy()
        V = policy_evaluation_improvement(policy, S, working)[0]
        policy = policy_evaluation_improvement(policy, S, working)[1]
        print(policy_evaluation_improvement(policy, S, working)[1])
        print("\n")
        if all(old_policy[s] == policy[s] for s in S):
            break
    return policy


# optimal_policy = policy_iteration(States, Actions)
#
# from matplotlib import pyplot as plt
#
# plt.xlim(0, 11)
# plt.ylim(0, 11)
# plt.grid()
# for s in States:
#     if optimal_policy[s] == 0:
#         color = "red"
#     if optimal_policy[s] == 1:
#         color = "green"
#     if optimal_policy[s] == 2:
#         color = "blue"
#     plt.plot(s[1], s[0], marker="o", markersize=10, markeredgecolor=color, markerfacecolor=color)
#
# plt.show()

optimal_policy = policy_iteration(States, Actions, False)
from matplotlib import pyplot as plt

plt.xlim(0, 11)
plt.ylim(0, 11)
plt.grid()
for s in States:
    if optimal_policy[s] == 0:
        color = "red"
    elif optimal_policy[s] == 1:
        color = "green"
    elif optimal_policy[s] == 2:
        color = "blue"
    plt.plot(s[1], s[0], marker="o", markersize=10, markeredgecolor=color, markerfacecolor=color)

plt.show()
