import numpy as np
from scipy.signal import hilbert
from sklearn.preprocessing import StandardScaler

print("Loading section...")
section = np.load('../outputs/section.npy')
print('Section shape:', section.shape)

# Compute analytic signal
print("Computing attributes...")
analytic = hilbert(section, axis=1)

# Extract 8 attributes
envelope      = np.abs(analytic)
inst_phase    = np.angle(analytic)
cosine_phase  = np.cos(inst_phase)
phase_unwrap  = np.unwrap(inst_phase, axis=1)
inst_freq     = np.diff(phase_unwrap, axis=1) / (2 * np.pi)
inst_freq     = np.concatenate([inst_freq, inst_freq[:, -1:]], axis=1)

squared = section ** 2
kernel  = np.ones(5) / 5
rms     = np.sqrt(np.apply_along_axis(
              lambda x: np.convolve(x, kernel, mode='same'), 1, squared))

refl_strength = np.abs(analytic)
sweetness     = envelope / (np.abs(inst_freq) + 1e-6)

# Stack into feature matrix
attrs = np.stack([
    envelope.ravel(),
    inst_phase.ravel(),
    cosine_phase.ravel(),
    inst_freq.ravel(),
    rms.ravel(),
    refl_strength.ravel(),
    sweetness.ravel(),
    section.ravel()
], axis=1)

print('Feature matrix shape:', attrs.shape)

# Normalize
scaler = StandardScaler()
X = scaler.fit_transform(attrs)

np.save('../outputs/feature_matrix.npy', X)
print('feature_matrix.npy saved! ✅')