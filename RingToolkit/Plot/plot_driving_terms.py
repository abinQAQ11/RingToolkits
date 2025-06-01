import matplotlib
matplotlib.use('TkAgg')
from .base_plot import *
# ----------------------------------------------------------------------------------------------------------------------
def plot_driving_terms(lattice):
    data = lattice.d_terms_m
    plt.ion()
    s = np.array([item[0] for item in data])
    h_21000 = np.array([item[1]['h_21000'] for item in data])
    h_30000 = np.array([item[1]['h_30000'] for item in data])
    h_10110 = np.array([item[1]['h_10110'] for item in data])
    h_10020 = np.array([item[1]['h_10020'] for item in data])
    h_10200 = np.array([item[1]['h_10200'] for item in data])

    fig, ax1 = plt.subplots(figsize=(8,6))
    ax1.plot(s, h_21000, color= 'green', linewidth=3, label=r'$h_{21000}$')
    ax1.plot(s, h_30000, color=  'blue', linewidth=3, label=r'$h_{30000}$')
    ax1.plot(s, h_10110, color='purple', linewidth=3, label=r'$h_{10110}$')
    ax1.plot(s, h_10020, color=   'red', linewidth=3, label=r'$h_{10020}$')
    ax1.plot(s, h_10200, color=  'cyan', linewidth=3, label=r'$h_{10200}$')

    ax1.set_xlabel('s (m)', fontsize=20)
    ax1.set_ylabel(r'$Amplitude\ of\ Terms\ in\ f_3\ [\ m^{-1/2}\ ]$', fontsize=20, color='black')
    ax1.tick_params(axis='y', labelcolor='black', labelsize=18)
    ax1.tick_params(axis='x', labelcolor='black', labelsize=18)
    high = max(max(h_21000), max(h_30000), max(h_10110), max(h_10020), max(h_10200))
    height = high / 40
    ax1.set_ylim(-height, high * 1.2)
    ax1.set_xlim(-1, max(s)+1)

    magnet(ax1, height, lattice)

    ax1.legend(loc='best', fontsize=20, ncol=2)
    fig.tight_layout()
    plt.show()
    plt.ioff()