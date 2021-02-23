import numpy as np

if __name__ == "__main__":
    session = np.array([i for i in range(10)])
    session = session[-20:]
    print(session)