# Noise Benchmark for Qiskit Aer
This is the benchmark script to evaluate multi-shots optimization for GPU simulation on Qiskit Aer (https://github.com/Qiskit/qiskit-aer).
Please install GPU enabled version of Qiskit Aer by pip 
```
$ pip uninstall qiskit-aer
$ pip install qiskit-aer-gpu
```
or build from source code by enabling GPU support by setting `-DAER_THRUST_BACKEND=CUDA` to cmake option.

## How to run benchmark
`noise_bench_qft_qubits.py` evaluate QFT simulation with Pauli or Kraus noises for some number of qubits.
There are 10 parameters required to run the script.

```
$ python noise_bench_qft_qubits.py method device noise_model shots num_execution error_ratio max_batchable_qubits max_qubits thread_per_gpu
```
- method : method to be used for the simulation, `statevector` or `density_matrix` can be applied
- device : `CPU` or `GPU` can be applied for the simulation
- noise_model : `Pauli` or `Kraus` noise model can be applied
- shots : number of shots to be simulated for each number of qubits
- num_execution : number of run for each number of qubits, simulation time is average of all iterations
- error_ratio : error ratio of noise sampling
- max_batchable_qubits : batched multi-shots optimization will be applied to less or equal to this option, set 1 to disable multi-shots optimization or set same as `max_qubits` to enable optimization
- max_qubits : max number of qubits to be evaluated
- thread_per_gpu : This is used for Pauli noise optimization on GPU, please try some numbers that makes the best performance


Following example runs 4000 shots of statevector simulation for 9-20 qubits with 1% of Pauli noise by GPU and batche multi-shots optimization is enabled.
```
$ python noise_bench_qft_qubits.py statevector GPU Pauli 4000 10 0.01 30 20 4
```


