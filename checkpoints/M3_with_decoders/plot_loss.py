import re
import matplotlib.pyplot as plt

# Open the text file and read its contents
with open('loss_log.txt', 'r') as f:
    lines = f.readlines()

# Extract the loss values using regular expressions
epochs = []
iters = []
G_rec_losses = []
G_lp_losses = []
G_GAN_losses = []
D_real_losses = []
D_fake_losses = []
start = 0
for line in lines:
    match = re.search(r'epoch: (\d+), iters: (\d+),.*G_rec: ([\d.]+) G_lp: ([\d.]+) G_GAN: ([\d.]+) D_real: ([\d.]+) D_fake: ([\d.]+)', line)
    if match:
        epoch = int(match.group(1))
        iter = int(match.group(2))
        G_rec_loss = float(match.group(3))
        G_lp_loss = float(match.group(4))
        G_GAN_loss = float(match.group(5))
        D_real_loss = float(match.group(6))
        D_fake_loss = float(match.group(7))
        print(iter, start)
        epochs.append(epoch)
        iters.append(start)
        G_rec_losses.append(G_rec_loss)
        G_lp_losses.append(G_lp_loss)
        G_GAN_losses.append(G_GAN_loss)
        D_real_losses.append(D_real_loss)
        D_fake_losses.append(D_fake_loss)
        start += 100
# Plot the loss curves
plt.plot(iters, G_rec_losses, label='G_rec')
plt.plot(iters, G_lp_losses, label='G_lp')
plt.plot(iters, G_GAN_losses, label='G_GAN')
plt.plot(iters, D_real_losses, label='D_real')
plt.plot(iters, D_fake_losses, label='D_fake')
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.title('Training Loss for M3_FFHQ_pretrained.jpg')
plt.legend()
plt.savefig('M3_FFHQ_pretrained.jpg')