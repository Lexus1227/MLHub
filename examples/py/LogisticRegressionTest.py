import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

from Models.LinearModels import LogisticRegression
from datasets import train_test_split
from Metrics.metrics import accuracy

from Optimizers.Optimizators import SAGDOptimizer
# будем бенчмаркать с sklearn

# пообучаем на данных с разным шумом и посмотрим метрики:


def log_test():

    for scale in [1, 2, 3, 4, 5]:

        optim = SAGDOptimizer(lr=1e-2, max_iter=10000, lam=0.95)
        simple = LogisticRegression()
        sklearn = linear_model.LogisticRegression()

        N = 200
        N2 = 25

        n_1 = int(N // 2 + np.random.randint(-N2, N2))
        n_2 = int(N // 2 + np.random.randint(-N2, N2))
        n_3 = int(N // 2 + np.random.randint(-N2, N2))

        x_1 = 10
        y_1 = 10

        x_2 = 0
        y_2 = -10

        x_3 = -10
        y_3 = 10

        pairs_1 = np.array([np.array(
            [x_1 + np.random.normal(scale=scale), y_1 + np.random.normal(scale=scale)])
            for i in range(0, n_1)])

        answers_1 = np.array([0] * n_1)

        pairs_2 = np.array([np.asarray(
            [x_2 + np.random.normal(scale=scale), y_2 + np.random.normal(scale=scale)])
            for i in range(0, n_2)])
        answers_2 = np.array([1] * n_2)

        pairs_3 = np.array([np.asarray(
            [x_3 + np.random.normal(scale=scale), y_3 + np.random.normal(scale=scale)])
            for i in range(0, n_3)])
        answers_3 = np.array([2] * n_3)

        x = np.vstack([pairs_1, pairs_2, pairs_3])
        y = np.hstack([answers_1, answers_2, answers_3])

        idx = np.random.permutation([i for i in range(x.shape[0])])

        x = x[idx]
        y = y[idx]

        x_pair, y_pair = train_test_split(x, y, ratio=0.75)

        x_train, x_test = x_pair
        y_train, y_test = y_pair

        simple.fit(x_train, y_train, optim)
        sklearn.fit(x_train, y_train)

        y_pred_simple = simple.predict(x_test)
        y_pred_sklearn = sklearn.predict(x_test)

        print(f"Scale = {scale}")
        print(f"ACC on SLKEARN = {accuracy(y_test, y_pred_sklearn)}")
        print(f"ACC on our LR = {accuracy(y_test, y_pred_simple)}")

        fig = plt.figure(figsize = (15, 10))

        idx_zero = y_test == 0
        idx_one = y_test == 1
        idx_two = y_test == 2

        plt.title("Three classes")

        plt.scatter(x_test[idx_zero, 0], x_test[idx_zero, 1], color="blue", s=50)

        plt.scatter(x_test[idx_one, 0], x_test[idx_one, 1], color="red", s=50)

        plt.scatter(x_test[idx_two, 0], x_test[idx_two, 1], color="yellow", s=50)

        b = simple.weights[2][0]
        w1 = simple.weights[0][0]
        w2 = simple.weights[1][0]
        x = [i for i in range(-15, 15)]
        y = [-i * w1 / w2 - b / w2 for i in x]
        plt.plot(x, y, color="blue")

        b = simple.weights[2][1]
        w1 = simple.weights[0][1]
        w2 = simple.weights[1][1]
        x = [i for i in range(-15, 15)]
        y = [-i * w1 / w2 - b / w2 for i in x]
        plt.plot(x, y, color="red")

        b = simple.weights[2][2]
        w1 = simple.weights[0][2]
        w2 = simple.weights[1][2]
        x = [i for i in range(-15, 15)]
        y = [-i * w1 / w2 - b / w2 for i in x]
        plt.plot(x, y, color="yellow")


        plt.ylim([-25, 25])

        # b = simple.weights[2]
        # w1 = simple.weights[0]
        # w2 = simple.weights[1]
        # x = [i for i in range(-15, 15)]
        # y = [-i * w1 / w2 - b / w2 for i in x]
        # plt.plot(x, y, color="black")
        # plt.ylim([-25, 25])

        plt.show()


if __name__ == "__main__":
    log_test()
