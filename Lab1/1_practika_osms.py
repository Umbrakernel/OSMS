import numpy as np
import matplotlib.pyplot as plt

def PPF(x):
    N = len(x)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
    return X

f = 8
fs = 64
t = np.arange(0, 1, 1/fs)
y = 0 * t

for i in range(len(t)):
    y[i] = np.cos(2*np.pi*f*t[i]) + np.cos(8*np.pi*f*t[i])

print("Максимальная частота: 32")
print("Минимальная частота дискретизации:", fs)
print("Количество отсчетов:", len(y))
print("Объем массива, байт:", y.nbytes)


freq = np.arange(len(y)//2 + 1) * fs / len(y)
spectrum = np.abs(PPF(y)[:len(freq)]) / len(y)

print("Ширина спектра: 32 - 8 = 24 Гц")

plt.figure()
plt.plot(t, y)
plt.title("Дискретный сигнал при fs = 64 Гц")
plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.grid()

plt.figure()
plt.stem(freq, spectrum)
plt.title("Спектр сигнала при fs = 64 Гц")
plt.xlabel("Угловая частота, Гц")
plt.ylabel("Амплитуда")
plt.grid()

plt.figure()
t_ishodn = np.arange(0, 1, 1/1000)
y_ishodn = np.cos(2*np.pi*f*t_ishodn) + np.cos(8*np.pi*f*t_ishodn)
plt.plot(t_ishodn, y_ishodn, label="Исходный сигнал")
plt.plot(t, y, label="Восстановленный сигнал")
plt.title("Сравнение исходного и восстановленного сигналов при fs = 64 Гц")
plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid()

fs = 4 * 64
t = np.arange(0, 1, 1/fs)
y = 0 * t

for i in range(len(t)):
    y[i] = np.cos(2*np.pi*f*t[i]) + np.cos(8*np.pi*f*t[i])

print("\nЧастота дискретизации после увеличения в 4 раза:", fs)
print("Количество отсчетов:", len(y))
print("Объем массива, байт:", y.nbytes)

freq = np.arange(len(y)//2 + 1) * fs / len(y)
spectrum = np.abs(PPF(y)[:len(freq)]) / len(y)

print("Ширина спектра: 32 - 8 = 24 Гц")

plt.figure()
plt.plot(t, y)
plt.title("Дискретный сигнал при fs = 256 Гц")
plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.grid()

plt.figure()
plt.stem(freq, spectrum)
plt.title("Спектр сигнала при fs = 256 Гц")
plt.xlabel("Угловая частота, Гц")
plt.ylabel("Амплитуда")
plt.grid()

plt.figure()
plt.plot(t_ishodn, y_ishodn, label="Исходный сигнал")
plt.plot(t, y, label="Восстановленный сигнал")
plt.title("Сравнение исходного и восстановленного сигналов при fs = 256 Гц")
plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid()

plt.show()
