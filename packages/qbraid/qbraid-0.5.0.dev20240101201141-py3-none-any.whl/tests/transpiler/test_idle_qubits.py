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
Unit tests for transpiling ciruits with idle qubits

"""
import braket.circuits
import cirq
import pytest
import qiskit

from qbraid import circuit_wrapper
from qbraid.interface import convert_to_package
from qbraid.programs.testing.circuit_equality import (
    assert_allclose_up_to_global_phase,
    circuits_allclose,
)

# pylint: disable=redefined-outer-name


@pytest.fixture
def braket_circuit() -> braket.circuits.Circuit:
    """Returns Braket bell circuit with idle qubits"""
    return braket.circuits.Circuit().h(4).cnot(4, 8)


@pytest.fixture
def cirq_circuit() -> cirq.Circuit:
    """Returns Cirq bell circuit with idle qubits"""
    q4, q8 = cirq.LineQubit(4), cirq.LineQubit(8)
    circuit = cirq.Circuit(cirq.ops.H(q4), cirq.ops.CNOT(q4, q8))
    return circuit


@pytest.fixture
def qiskit_circuit() -> qiskit.QuantumCircuit:
    """Returns Qiskit bell circuit with idle qubits"""
    circuit = qiskit.QuantumCircuit(9)
    circuit.h(4)
    circuit.cx(4, 8)
    return circuit


def test_braket_to_cirq(braket_circuit):
    """Tests Braket conversions"""
    cirq_test = convert_to_package(braket_circuit, "cirq")
    assert circuits_allclose(cirq_test, braket_circuit)


def test_braket_to_qiskit(braket_circuit):
    """Tests Braket conversions"""
    qiskit_test = convert_to_package(braket_circuit, "qiskit")
    qprogram_qiskit = circuit_wrapper(qiskit_test)
    qprogram_braket = circuit_wrapper(braket_circuit)
    qprogram_braket.populate_idle_qubits()
    qiskit_u = qprogram_qiskit.unitary()
    braket_u = qprogram_braket.unitary()
    assert_allclose_up_to_global_phase(qiskit_u, braket_u, atol=1e-7)


def test_cirq_to_braket(cirq_circuit):
    """Tests Cirq conversions"""
    braket_test = convert_to_package(cirq_circuit, "braket")
    assert circuits_allclose(braket_test, cirq_circuit)


def test_cirq_to_qiskit(cirq_circuit):
    """Tests Cirq conversions"""
    qiskit_test = convert_to_package(cirq_circuit, "qiskit")
    assert circuits_allclose(qiskit_test, cirq_circuit)


def test_qiskit_to_cirq(qiskit_circuit):
    """Tests Qiskit conversions"""
    cirq_test = convert_to_package(qiskit_circuit, "cirq")
    qprogram_qiskit = circuit_wrapper(qiskit_circuit)
    qprogram_cirq = circuit_wrapper(cirq_test)
    qprogram_cirq.populate_idle_qubits()
    qiskit_u = qprogram_qiskit.unitary()
    cirq_u = qprogram_cirq.unitary()
    assert_allclose_up_to_global_phase(qiskit_u, cirq_u, atol=1e-7)


def test_qiskit_to_braket(qiskit_circuit):
    """Tests Qiskit conversions"""
    braket_test = convert_to_package(qiskit_circuit, "braket")
    qprogram_qiskit = circuit_wrapper(qiskit_circuit)
    qprogram_braket = circuit_wrapper(braket_test)
    qprogram_braket.populate_idle_qubits()
    qiskit_u = qprogram_qiskit.unitary()
    braket_u = qprogram_braket.unitary()
    assert_allclose_up_to_global_phase(qiskit_u, braket_u, atol=1e-7)
