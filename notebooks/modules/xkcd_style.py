import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()  # Here the styles change...
plt.plot(np.sin(np.linspace(0, 10)), 'r', label='Red wave:)')
plt.plot(np.sin(np.linspace(0, 10)-1), 'b', label='Blue wave:)')
plt.title('Oops, will the blue one catch the red one?')
plt.legend()
plt.show()
