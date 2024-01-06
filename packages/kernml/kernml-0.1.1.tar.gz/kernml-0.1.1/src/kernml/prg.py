# The functions that are complete and included in this file : 
# pr_1()
# pr_2()
# pr_3()
# pr_4()
# pr_5()
# pr_6()

def pr_1():
    p1 = '''
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import seaborn as sns

#Loading Data Set
iris = load_iris()

# Displays the irises bases on petal length and petal width  - the two major featues
colormap = np.array(['blue', 'orange', 'green'])
plt.scatter(iris.data[:,2], iris.data[:,3], c = colormap[iris.target])
plt.xlabel("Petal length (cm)")
plt.ylabel("Petal width (cm)")
plt.title("Actual Clusters")
plt.show()

#Data Transformation
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size = 0.3,
    random_state=42, stratify=iris.target)
    
print("Class distribution in train data set:", np.unique(y_train, return_counts=True))
print("Class distribution in test data set:", np.unique(y_test, return_counts=True))

std_scaler = StandardScaler()
X_train_scaled = std_scaler.fit_transform(X_train)

X_test_scaled = std_scaler.transform(X_test)

# MODELLING
knn_clf = KNeighborsClassifier()
knn_clf.fit(X_train, y_train)
predictions = knn_clf.predict(X_test)
prediction_probas = knn_clf.predict_proba(X_test)

# Analyzing Model Performance
test_data_with_predictions = pd.DataFrame(X_test)
test_data_with_predictions.columns = iris.feature_names
test_data_with_predictions["actual class"] = y_test
test_data_with_predictions["predicted class"] = predictions
test_data_with_predictions["Predicted Probabilities"] = [str(proba) for proba in prediction_probas]

display(test_data_with_predictions)

# Confusion Matrix
print("Accuracy score on test data set: {:.3f}".format(accuracy_score(y_test, predictions)))

conf_matrix = confusion_matrix(y_test, predictions, labels=[0, 1, 2])
sns.heatmap(
    conf_matrix, 
    annot=True, 
    xticklabels=iris.target_names, yticklabels=iris.target_names)
plt.ylabel("True Class")
plt.xlabel("Predited Class")
plt.title("Confusion Matrix of K-Nearest Neighbour Classifier Predictions")
plt.show()

# Classification Report
print(classification_report(y_test, predictions))

#Area under Receiver Operating Characteristics (ROC) Curve
auc_score = roc_auc_score(
    y_test, 
    prediction_probas, 
    multi_class="ovr",
    labels=[0, 1, 2]   # optional
)
print("Area under ROC Curve: {:.3f}".format(auc_score))
'''
    p1 = print(p1)
    return p1

def pr_2():
    p2 = '''
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import seaborn as sns

iris = load_iris()

kmeans = KMeans(n_clusters = len(iris.target_names), random_state = 42)
kmeans.fit(iris.data)

gm = GaussianMixture(n_components = len(iris.target_names), random_state = 42)
gm.fit(iris.data)
gm_predictions = gm.predict(iris.data)

colormap = np.array(['blue', 'orange', 'green'])

plt.figure(figsize=(14,7))

plt.subplot(1, 3, 1)
plt.scatter(iris.data[:,2], iris.data[:,3], c = colormap[iris.target])
plt.xlabel("Petal length (cm)")
plt.ylabel("Petal width (cm)")
plt.title("Actual Clusters")

plt.subplot(1, 3, 2)
plt.scatter(iris.data[:,2], iris.data[:,3], c = colormap[kmeans.labels_])
plt.xlabel("Petal length (cm)")
plt.ylabel("Petal width (cm)")
plt.title("K-Means Clusters")

plt.subplot(1, 3, 3)
plt.scatter(iris.data[:,2], iris.data[:,3], c = colormap[gm_predictions])
plt.xlabel("Petal length (cm)")
plt.ylabel("Petal width (cm)")
plt.title("GMM Clusters")

plt.show()
    '''
    p2 = print(p2)
    return p2

def pr_3():
    p3 = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_penalty_weights(query_x, X, tau):
    m = X.shape[0]
    
    W = np.mat(np.eye(m))

    for i in range(m):
        x = X[i]
        W[i, i] = np.exp(
            np.dot((x - query_x), (x - query_x).T) / (-2 * tau * tau)
        )
    
    return W
    
def predict(X, y, query_x, tau):
    m = X.shape[0]
    
    X_transformed = np.hstack((np.reshape(X, (-1, 1)), np.ones((m, 1))))
    
    query_x_transformed = np.mat([query_x, 1])
    
    penalty_weights = get_penalty_weights(query_x_transformed, X_transformed, tau)
    
    y_transformed = np.reshape(y, (-1, 1))
    
    theta = np.linalg.pinv(
        X_transformed.T * (penalty_weights * X_transformed)) * (X_transformed.T * (penalty_weights * y_transformed))

    prediction = np.dot(query_x_transformed, theta)
    
    return theta, prediction
    
data = pd.read_csv("./../../Data/curve.csv")

X = data.x.values
y = data.y.values

plt.scatter(X, y)

# Predictions
tau = 0.1

X_test = np.sort(np.random.randint(1, 100, size=X.shape[0]))

predictions = []

for query_instance in X_test:
    theta, prediction = predict(X, y, query_instance, tau)
    predictions.append(prediction.A[0][0])

plt.scatter(X, y, color = 'blue', alpha=1.0, label="Actual")
plt.plot(X_test, predictions, color='red', label="Predicted")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Locally Weighted Linear Regression with Tau set to {:.2f}".format(tau))
plt.legend()
plt.show()
    '''
    p3 = print(p3)
    return p3

def pr_4():
    p4 = '''
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

sales = pd.read_csv("Advertising.csv")

display(sales.head())

print(sales.shape)

print(sales.info())

#data preparation

X = sales[["TV", "Radio", "Newspaper"]]
y = sales["Sales"]

X = X.apply(lambda x: (x - X.mean()) / X.std(), axis = 1)

display(X.head())

y_scaler = MinMaxScaler()
y_transformed = y_scaler.fit_transform(y.values.reshape(-1, 1))

# Helper Functions

def sigmoid(x):
    """
    Returns sigmoid value for the input parameter
    """
    
    return 1/(1 + np.exp(-x))
    
def sigmoid_derivative(x):
    """
    Returns derivative of sigmoid function
    """
    
    return x * (1 - x)
    
# Modelling

# Initialization

input_layer_units = X.shape[1]

output_layer_units = 1

# Hyperparameters initialization

epoch = 5000

learning_rate = 0.1

hidden_layer_units = 3

hidden_layer_weights = np.random.uniform(size=(input_layer_units, hidden_layer_units))

hidden_layer_biases = np.random.uniform(size=(1, hidden_layer_units))
                                         
output_layer_weights = np.random.uniform(size=(hidden_layer_units,output_layer_units))

output_layer_biases=np.random.uniform(size=(1,output_layer_units))

# Training Model

for i in range(epoch):

    #Forward Propogation
    hidden_layer_nets = np.dot(X, hidden_layer_weights)
    hidden_layer_nets = hidden_layer_nets + hidden_layer_biases
    hidden_layer_outputs = sigmoid(hidden_layer_nets)
    
    output_layer_nets = np.dot(hidden_layer_outputs, output_layer_weights)
    output_layer_nets = output_layer_nets + output_layer_biases
    output = sigmoid(output_layer_nets)

    #Backpropagation
    output_error = y_transformed - output
    output_gradients = sigmoid_derivative(output)
    output_delta = output_error * output_gradients
    hidden_layer_error = output_delta.dot(output_layer_weights.T)

    # Calculation of hidden layer weights' contribution to error
    hidden_layer_gradients = sigmoid_derivative(hidden_layer_outputs)
    hidden_layer_delta = hidden_layer_error * hidden_layer_gradients

    # Weights updates for both output and hidden layer units
    output_layer_weights += learning_rate * hidden_layer_outputs.T.dot(output_delta)
    hidden_layer_weights += learning_rate * X.T.dot(hidden_layer_delta)
    
predictions = y_scaler.inverse_transform(output)

pd.DataFrame({"Actual Sale": y, "Predicted Sale": predictions.flatten()})
    '''
    p4 = print(p4)
    return p4

def pr_5():
    p5 = '''
import numpy as np
import matplotlib.pyplot as plt

def fitness(variables, population):
    fitness = np.sum(population * variables, axis=1)
    return fitness

def select_mating_pool(population, fitness, n_parents):
    parents = np.empty((n_parents, population.shape[1]))  # shape[1] indicates number of genes in chromosome
    for parent_idx in range(n_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_idx, :] = population[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents
    
def crossover(parents, n_offspring):
    offsprings = np.empty((n_offspring, parents.shape[1]))
    crossover_point = np.uint8(parents.shape[1]/2)
    for k in range(n_offspring):
        parent1_idx = k % parents.shape[0]
        parent2_idx = (k + 1) % parents.shape[0]
        offsprings[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offsprings[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offsprings

def mutate(offsprings, n_mutations = 1):
    mutations_counter = np.uint8(offsprings.shape[1] / n_mutations)
    for idx in range(offsprings.shape[0]):
        gene_idx = mutations_counter - 1
        for mutation_num in range(n_mutations):
            offsprings[idx, gene_idx] = offsprings[idx, gene_idx] + np.random.uniform(-1.0, 1.0, 1)
            gene_idx = gene_idx + mutations_counter
    return offsprings

variables = [4, -2, 3.5, 5, -11, -4.7]
n_coef = len(variables)
population_size = 8
population = np.random.uniform(low=-4.0, high=4.0, size=(population_size, n_coef))
print(population)

n_generations = 5
n_parents = 4
fitness_values = fitness(variables, population)
print("Fitness Values in Initial Generation:", "\\n", fitness_values, "\\n")

best_fitness_values = []
best_fitness_values.append(np.max(fitness_values))

for generation in range(n_generations):
    print("Generation: ", generation + 1)
    print("="*20, "\\n")
    parents = select_mating_pool(population, fitness_values, n_parents)
    print("Selected Parents:", "\\n", parents, "\\n")
    offsprings = crossover(parents, population.shape[0] - parents.shape[0])
    print("Crossover: Offsprings", "\\n", offsprings, "\\n")
    mutated_offsprings = mutate(offsprings)
    print("Mutated:", "\\n", mutated_offsprings, "\\n")
    population[0:parents.shape[0], :] = parents
    population[parents.shape[0]:, :] = mutated_offsprings
    fitness_values = fitness(variables, population)
    print("Fitness Values in New Generation :", "\\n", fitness_values, "\\n")
    best_fitness_values.append(np.max(fitness_values))
    
best_solution_idx = np.where(fitness_values == np.max(fitness_values))
best_solution = population[best_solution_idx, :]
print("Best Solution after Generation", n_generations, "is:", best_solution)

plt.plot(best_fitness_values)
plt.xlabel("Generation")
plt.ylabel("Fitness Value")
plt.title("Fitness of Best Solution over Generations")
plt.show()

    '''
    p5 = print(p5)
    return p5

def pr_6():
    p6 = '''
import pandas as pd
import numpy as np

def get_possible_next_states(state, F, states_count):
    possible_next_states = []
    for i in range(states_count):
        if F[state, i] == 1: 
            possible_next_states.append(i)
    return possible_next_states

def get_random_next_state(state, F, states_count):
    possible_next_states = get_possible_next_states(state, F, states_count)
    next_state = possible_next_states[np.random.randint(0, len(possible_next_states))]
    return next_state

F = np.loadtxt("./feasibility_matrix.csv", dtype="int", delimiter=',')
print(F)

R = np.loadtxt("./reward_matrix.csv", dtype="float", delimiter=',')
print(R)

Q = np.zeros(shape=[15,15], dtype=np.float32)
display(pd.DataFrame(Q, dtype=float).style.format(precision=2))

Q = np.zeros(shape=[15,15], dtype=np.float32)
display(pd.DataFrame(Q, dtype=float).style.format(precision=2))

def train(F, R, Q, gamma, lr, goal_state, states_count, episodes):
    for i in range(0, episodes):
        current_state = np.random.randint(0, states_count)
        while(True):
            next_state = get_random_next_state(current_state, F, states_count)
            possible_next_next_states = get_possible_next_states(next_state, F, states_count)
            max_Q = -9999.99
            for j in range(len(possible_next_next_states)):
                next_next_state = possible_next_next_states[j]
                q = Q[next_state, next_next_state]
                if q > max_Q:
                    max_Q = q
            Q[current_state][next_state] = ((1 - lr) * Q[current_state][next_state]) + (lr * (R[current_state][next_state] + (gamma * max_Q)))
            current_state = next_state
            if current_state == goal_state:
                break

gamma = 0.5        
lr = 0.5           
goal_state = 14
states_count = 15
episodes = 1000
np.random.seed(42)

train(F, R, Q, gamma, lr, goal_state, states_count, episodes)

display(pd.DataFrame(Q, dtype=float).style.format(precision=2))

def print_shortest_path(start_state, goal_state, Q):
    current_state = start_state
    print(str(current_state) + "->", end="")
    while current_state != goal_state:
        next_state = np.argmax(Q[current_state])
        print(str(next_state) + "->", end="")
        current_state = next_state
    print("Goal Reached.\\n")

start_state = 8
print("Best path to reach goal from state {0} to goal state {1}".format(start_state, goal_state))
print_shortest_path(start_state, goal_state, Q)

start_state = 13
print("Best path to reach goal from state {0} to goal state {1}".format(start_state, goal_state))
print_shortest_path(start_state, goal_state, Q)

start_state = 6
print("Best path to reach goal from state {0} to goal state {1}".format(start_state, goal_state))
print_shortest_path(start_state, goal_state, Q)

start_state = 1
print("Best path to reach goal from state {0} to goal state {1}".format(start_state, goal_state))
print_shortest_path(start_state, goal_state, Q)
    '''
    p6 = print(p6)
    return p6