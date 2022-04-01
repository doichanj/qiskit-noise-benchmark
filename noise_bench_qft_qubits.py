from qiskit import *
from qiskit.circuit.library import *
from qiskit.providers.aer import *
from qiskit.providers.aer.noise import *
import sys

noise_model = NoiseModel()

method = sys.argv[1]
dev = sys.argv[2]
shots = int(sys.argv[4])
niter = int(sys.argv[5])
error_rate = float(sys.argv[6])

if len(sys.argv) < 8:
    max_batch = 22
else:
    max_batch = int(sys.argv[7])

if len(sys.argv) < 9:
    max_qubits = 20
else:
    max_qubits = int(sys.argv[8])

if len(sys.argv) < 10:
    threads_per_gpu = 1
else:
    threads_per_gpu = int(sys.argv[9])

depth=10

if method == "statevector":
    fusion_thres=22
else:
    fusion_thres=14


if sys.argv[3] == "Kraus":
    #insert Kraus error
    error1 = amplitude_damping_error(error_rate, 1)
    noise_model.add_all_qubit_quantum_error(error1, ['u1', 'u2', 'u3','x','h','p'])
    print(">>> using Kraus noise")
else:
    #insert pauli errors
    error1 = depolarizing_error(error_rate, 1)
    error2 = depolarizing_error(error_rate, 2)
    noise_model.add_all_qubit_quantum_error(error1, ['u1', 'u2', 'u3','x','h','p'])
    noise_model.add_all_qubit_quantum_error(error2, ['cx'])
    print(">>> using Pauli noise")

sim = AerSimulator(method=method, device=dev, noise_model = noise_model)

print(" === Banchmarking QFT with {0} noise model using {1} method on {2}".format(sys.argv[3],method,dev))
print("     shots = {0}, error_rate = {1}, max_batch = {2}, thread/gpu = {3}".format(shots,error_rate,max_batch,threads_per_gpu))

for qubits in range (9, max_qubits+1):
    circuit = transpile(QFT(qubits), backend=sim,optimization_level=0)
    circuit.measure_all()

    time = 0.0
    for iter in range (0,niter):
        result = execute(circuit,sim,shots=shots,noise_model=noise_model,seed_simulator=12345,batched_shots_gpu=True,batched_shots_gpu_max_qubits=max_batch,fusion_threshold=fusion_thres,num_threads_per_group=threads_per_gpu).result()
        time = time + float(result.to_dict()['results'][0]['time_taken'])

    if result.to_dict()['metadata']['mpi_rank'] == 0:
        print("{0},{1}".format(qubits,time/float(niter)))



