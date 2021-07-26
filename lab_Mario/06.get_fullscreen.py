# 05.get_ram.py
import retro
import numpy as np

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()

ram = env.get_ram()

full_screen = ram[0x500:0x069F+1]

print(full_screen.shape)
print(full_screen)

full_screen_count = full_screen.shape[0]
full_screen_page1 = full_screen[:full_screen_count//2].reshape((13, 16))
full_screen_page2 = full_screen[full_screen_count//2:].reshape((13, 16))

full_screen = np.concatenate((full_screen_page1, full_screen_page2), axis=1).astype(np.int)

print(full_screen)