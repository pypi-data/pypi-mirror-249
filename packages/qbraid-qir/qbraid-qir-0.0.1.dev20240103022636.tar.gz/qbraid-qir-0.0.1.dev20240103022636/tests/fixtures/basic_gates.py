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
Module defining Cirq basic gate fixtures for use in tests.

"""

import cirq
import numpy as np
import pytest

# All of the following dictionaries map from the names of methods on Cirq Circuit objects
# to the name of the equivalent pyqir BasicQisBuilder method

_zero_qubit_operations = {"barrier": "barrier"}

_one_qubit_gates = {
    "H": "h",
    "reset": "reset",
    "T": "t",
    "X": "x",
    "Y": "y",
    "Z": "z",
}

_rotations = {"Rx": "rx", "Ry": "ry", "Rz": "rz"}

_two_qubit_gates = {"CX": "cnot", "CZ": "cz", "SWAP": "swap"}

_three_qubit_gates = {"CCX": "ccx"}

_measurements = {"measure": "mz"}


def _fixture_name(s: str) -> str:
    return f"Fixture_{s}"


def _map_gate_name(gate_name: str) -> str:
    if gate_name in _one_qubit_gates:
        return _one_qubit_gates[gate_name]
    elif gate in _measurements:
        return _measurements[gate]
    elif gate in _rotations:
        return _rotations[gate]
    elif gate in _two_qubit_gates:
        return _two_qubit_gates[gate]
    elif gate in _three_qubit_gates:
        return _three_qubit_gates[gate]

    raise ValueError(f"Unknown Cirq gate {gate_name}")


def _generate_one_qubit_fixture(gate_name: str):
    @pytest.fixture()
    def test_fixture():
        circuit = cirq.Circuit()
        q = cirq.NamedQubit("q0")
        circuit.append(getattr(cirq, gate_name)(q))
        return _map_gate_name(gate_name), circuit

    return test_fixture


# Generate simple single-qubit gate fixtures
for gate in _one_qubit_gates:
    name = _fixture_name(gate)
    locals()[name] = _generate_one_qubit_fixture(gate)


def _generate_rotation_fixture(gate_name: str):
    @pytest.fixture()
    def test_fixture():
        circuit = cirq.Circuit()
        q = cirq.NamedQubit("q0")
        circuit.append(getattr(cirq, gate_name)(rads=0.5)(q))
        return _map_gate_name(gate_name), circuit

    return test_fixture


# Generate rotation gate fixtures
for gate in _rotations.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_rotation_fixture(gate)


def _generate_two_qubit_fixture(gate_name: str):
    @pytest.fixture()
    def test_fixture():
        circuit = cirq.Circuit()
        q1 = cirq.NamedQubit("q1")
        q2 = cirq.NamedQubit("q2")
        circuit.append(getattr(cirq, gate_name)(q1, q2))
        qs = cirq.LineQubit(2)
        circuit.append(getattr(cirq, gate_name)(qs[0], qs[1]))
        return _map_gate_name(gate_name), circuit

    return test_fixture


# Create a new function to generate a fixture for n-qubit gates
def _generate_n_qubit_fixture(gate_name: str, n: int):
    @pytest.fixture()
    def test_fixture():
        circuit = cirq.Circuit()
        qubits = [cirq.NamedQubit(f"q{i}") for i in range(n)]
        circuit.append(getattr(cirq, gate_name)(*qubits))


# Generate double-qubit gate fixtures
for gate in _two_qubit_gates.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_two_qubit_fixture(gate)


def _generate_three_qubit_fixture(gate_name: str):
    @pytest.fixture()
    def test_fixture():
        circuit = cirq.Circuit()
        qs = cirq.LineQubit(3)
        circuit.append(getattr(cirq, gate_name)(qs[0], qs[1], qs[2]))
        return _map_gate_name(gate_name), circuit

    return test_fixture


# New function for more complex gate structures:
def _generate_complex_gate_fixture(gate_sequence):
    @pytest.fixture()
    def test_fixture():
        circuit = cirq.Circuit()
        qubits = [cirq.NamedQubit(f"q{i}") for i in range(len(gate_sequence))]
        for gate, qubit_indices in gate_sequence:
            gates_to_apply = [getattr(cirq, gate)(qubits[i]) for i in qubit_indices]
            circuit.append(gates_to_apply)
        return circuit

    return test_fixture


def test_qft():
    for n in range(2, 5):  # Test for different numbers of qubits
        circuit = cirq.Circuit()
        qubits = [cirq.NamedQubit(f"q{i}") for i in range(n)]
        circuit.append(cirq.qft(*qubits))
        # Add assertions or checks here


@pytest.mark.parametrize("angle", np.linspace(0, 2 * np.pi, 5))
def test_rx_gate(angle):
    qubit = cirq.NamedQubit("q0")
    circuit = cirq.Circuit(cirq.rx(angle)(qubit))
    # Add assertions or checks for the rotation


def test_bell_state():
    qubits = [cirq.NamedQubit(f"q{i}") for i in range(2)]
    circuit = cirq.Circuit()
    circuit.append([cirq.H(qubits[0]), cirq.CNOT(qubits[0], qubits[1])])
    # Check if the circuit produces the correct entangled state


single_op_tests = [_fixture_name(s) for s in _one_qubit_gates]

# Generate three-qubit gate fixtures
for gate in _three_qubit_gates.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_three_qubit_fixture(gate)


def _generate_measurement_fixture(gate_name: str):
    @pytest.fixture()
    def test_fixture():
        circuit = cirq.Circuit()
        q = cirq.NamedQubit("q")
        circuit.append(getattr(cirq, gate_name)(q))
        return _map_gate_name(gate_name), circuit

    return test_fixture


for gate in _measurements.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_measurement_fixture(gate)

single_op_tests = [_fixture_name(s) for s in _one_qubit_gates]
rotation_tests = [_fixture_name(s) for s in _rotations.keys()]
double_op_tests = [_fixture_name(s) for s in _two_qubit_gates.keys()]
triple_op_tests = [_fixture_name(s) for s in _three_qubit_gates.keys()]
measurement_tests = [_fixture_name(s) for s in _measurements.keys()]
