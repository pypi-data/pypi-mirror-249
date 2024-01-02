# Copyright (C) 2023 qBraid
#
# This file is part of the qBraid-SDK
#
# The qBraid-SDK is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid-SDK, as per Section 15 of the GPL v3.

"""
Unit tests for conversions between Cirq circuits and Qiskit circuits.

"""
import numpy as np
import pytest
from cirq import Circuit, LineQubit, ops, testing

from qbraid.interface.converter import convert_to_package
from qbraid.programs.testing import circuits_allclose
from qbraid.transpiler.exceptions import CircuitConversionError


def test_bell_state_to_qiskit():
    """Tests cirq.Circuit --> qiskit.QuantumCircuit --> cirq.Circuit
    with a Bell state circuit."""
    qreg = LineQubit.range(2)
    cirq_circuit = Circuit([ops.H.on(qreg[0]), ops.CNOT.on(qreg[0], qreg[1])])
    qiskit_circuit = convert_to_package(cirq_circuit, "qiskit")
    assert circuits_allclose(qiskit_circuit, cirq_circuit, strict_gphase=True)


@pytest.mark.parametrize("num_qubits", [1, 2, 3, 4, 5])
def test_random_circuit_to_qiskit(num_qubits):
    """Tests converting random Cirq circuits to Qiskit circuits."""
    for _ in range(10):
        cirq_circuit = testing.random_circuit(
            qubits=num_qubits,
            n_moments=np.random.randint(1, 6),
            op_density=1,
            random_state=np.random.randint(1, 10),
        )
        qiskit_circuit = convert_to_package(cirq_circuit, "qiskit")
        assert circuits_allclose(qiskit_circuit, cirq_circuit, strict_gphase=True)


def test_raise_error():
    """Tests raising error for unsupported gates."""
    with pytest.raises(CircuitConversionError):
        probs = np.random.uniform(low=0, high=0.5)
        cirq_circuit = Circuit(ops.PhaseDampingChannel(probs).on(*LineQubit.range(1)))
        convert_to_package(cirq_circuit, "qiskit")
