# Audit

Collection of functions used to audit the `ExperimentalData` results

## Files

### Specification
`<QP>_test_oracle.txt`: Quantum program's `QP` Probabilities Oracle in the form:
```
(<input>, <output>): <probability>
...
```
Where:
- `input`: quantum circuit decimal input. Example: `27`
- `output`: quantum circuit decimal output. Example: `2`
- `probability`: probability of observing the `output`, given `input`. Example: `0.24999999999999994`

### Raw results
`results.txt`: output results from mutants executions in the form:
```
The result of <mutant-file-path> with input [<input>] is: {'<output-1>': <count-1>, '<output-2>': <count-2>, ...}
...
```
Where:
- `mutant-file-path`: is the path of file. Example: `C:/Users/complex/Desktop/QuantumMutationTesting/QRam/AllMutants/1AddGate_x_inGap_1_.py`
- `input`: binary input for the quantum circuit. Example: `000000`
- `output-N`: binary output from the quantum circuit. Example: `000100`
- `count-N`: number of occurences of given `output-N`

### Accumulated results
`cleanResults.txt`: output from `resultsAnalyzer` that accumulates the (input, output) obtained from `results.txt` based on the measured qubits defined in the `resultsAnalyzer/analyzerConfig.py` (same as `resultsAnalyzer/configs/default.analyzer.toml`). It has the form:
```
<mutant-file>------------------------------------------------------------------
(<input>, <output>): <probability>
...
```
Where:
- `mutant-file`: mutant file name (`stem`). Example: `1AddGate_x_inGap_1_`
- `input`: quantum circuit decimal input. Example: `31`
- `output`: quantum circuit decimal output. Example: `3`
- `probability`: probability of observing the `output`, given `input`. Example: `0.76`

### Final results
`testResults.txt`: the program's final result after analyzing the result against the Wrong Output Oracle (unexpected output observed) and Output Probabilities Oracle (the probability of observing an output compared with the Quantum Program specification)

The result for each line can be:

#### Wrong Output observed
An output that does not belong in the specification (unexpected output) was observed.
```
File: <mutant-file> with input [<input>]FAILED DIRECTLY without checking P-Value
```

#### Output Probability rejected
The output probability observed does not match the specification probability after Chi-Squared analyses
```
FILE: <mutant-file> with input [<input>] FAILED WITH P-Value <p-value>
```

#### Output Probability not rejected
The output probability observed could not be rejected from specification probability after Chi-Squared analyses
```
FILE: <mutant-file> with input [<input>] VALID WITH P-Value <p-value>
```

Where:
- `mutant-file`: mutant file name (`stem`). Example: `1AddGate_x_inGap_1_`
- `input`: quantum circuit decimal input. Example: `31`
- `p-value`: Chi-Squared resulting p-value
