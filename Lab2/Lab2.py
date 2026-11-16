import numpy as np
import matplotlib.pyplot as plt
from math import log10, ceil

f = 1800
f_ghz = 1.8
bw_ul = 10e6
bw_dl = 20e6

thermal_noise_ul = -174 + 10 * log10(bw_ul)
thermal_noise_dl = -174 + 10 * log10(bw_dl)

rx_bs = 2.4 + thermal_noise_ul + 4
rx_ue = 6 + thermal_noise_dl + 2

feeder = 2 + 0.4 + 0.5
mapl_ul = 24 - feeder + 21 + 3 - 1 - 15 - rx_bs
mapl_dl = 46 - feeder + 21 + 3 - 1 - 15 - rx_ue

print("Thermal noise UL:", round(thermal_noise_ul, 2), "dBm")
print("Thermal noise DL:", round(thermal_noise_dl, 2), "dBm")
print("RxSens BS:", round(rx_bs, 2), "dBm")
print("RxSens UE:", round(rx_ue, 2), "dBm")
print("MAPL UL:", round(mapl_ul, 2), "dB")
print("MAPL DL:", round(mapl_dl, 2), "dB")

def umi(d):
    return 26 * np.log10(f_ghz) + 22.7 + 36.7 * np.log10(d)

def cost231(d):
    h_bs = 30
    h_ms = 1.5
    l_clutter = 0

    a = 3.2 * (np.log10(11.75 * h_ms))**2 - 4.97

    s = np.where(d >= 1, 44.9 - 6.55 * np.log10(h_bs), (47.88 + 13.9 * np.log10(f) - 13.9 * np.log10(h_bs)) / log10(50))

    return 46.3 + 33.9 * np.log10(f) - 13.82 * np.log10(h_bs) - a + s * np.log10(d) + l_clutter

def walfish(d):
    h_bs = 30
    h_ms = 1.5
    h_building = 20
    w = 20
    b = 50
    phi = 45
    delta_h = h_building - h_ms
    l0 = 32.44 + 20 * np.log10(f) + 20 * np.log10(d)
    lori = 2.5 + 0.075 * phi
    l2 = -16.9 - 10 * np.log10(w) + 10 * np.log10(f) + 20 * np.log10(delta_h) + lori
    l11 = -18 * np.log10(1 + h_bs - h_building)
    ka = 54
    kd = 18
    kf = -4 + 0.7 * (f / 925 - 1)
    l1 = l11 + ka + kd * np.log10(d) + kf * np.log10(f) - 9 * np.log10(b)
    return np.where(l1 + l2 > 0, l0 + l1 + l2, l0)

d_km = np.linspace(0, 10, 1000)
d_m = d_km * 1000

plt.plot(d_m, umi(d_m), label="UMiNLOS")
plt.plot(d_m, cost231(d_km), label="COST231-Hata")
plt.plot(d_m, walfish(d_km), label="Walfish-Ikegami")
plt.axhline(mapl_ul, linestyle="--", label="MAPL UL")
plt.axhline(mapl_dl, linestyle=":", label="MAPL DL")
plt.xlabel("Расстояние, м")
plt.ylabel("Потери PL, дБ")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

d = np.linspace(0.03, 10, 10000)
pl = cost231(d)
r_ul = d[np.argmin(abs(pl - mapl_ul))]
r_dl = d[np.argmin(abs(pl - mapl_dl))]
r = min(r_ul, r_dl)
area = 1.95 * r**2
bs = ceil(100 / area)

print("------------------------------------------------------")
print("Макросота COST231-Hata")
print("R UL:", round(r_ul, 3), "km")
print("R DL:", round(r_dl, 3), "km")
print("Радиус соты:", round(r, 3), "km")
print("Площадь bs:", round(area, 3), "km^2")
print("Число bs на 100 km^2:", bs)

r_ul_umi = 10 ** ((mapl_ul - 26 * log10(f_ghz) - 22.7) / 36.7)
r_dl_umi = 10 ** ((mapl_dl - 26 * log10(f_ghz) - 22.7) / 36.7)
r_umi = min(r_ul_umi, r_dl_umi)
area_umi = 1.95 * (r_umi / 1000)**2
bs_umi = ceil(4 / area_umi)

print("------------------------------------------------------")
print("Микро-/фемтосота UMiNLOS")
print("R UL:", round(r_ul_umi, 1), "m")
print("R DL:", round(r_dl_umi, 1), "m")
print("Радиус соты:", round(r_umi, 1), "m")
print("Площадь bs:", round(area_umi, 4), "km^2")
print("Число bs на 4 km^2:", bs_umi)
