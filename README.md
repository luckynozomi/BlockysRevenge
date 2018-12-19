# A solution to the Blocky's Revenge problem

## The Problem

Watch LiveOverflow's videos for a brief introduction of this problem [here](https://www.youtube.com/watch?v=PQPO5Z4lVTU&index=14&list=PLhixgUqwRTjzzBeFSHXrw9DnQtssdAwgG)
and his analysis & solution [here](https://www.youtube.com/watch?v=L8sH8VM2Bd0&list=PLhixgUqwRTjzzBeFSHXrw9DnQtssdAwgG&index=15)

To put the problem into words:

Binary array `i[0, 1, ..., 31]` is the input to a logical circuit with multiple logical gates. 
All the corresponding status of connections, the inputs and outputs of each gate, are recorded in
binary array `o[0, 1, ..., 175]`. There are 174 connections in total, and the remaining
2  do not represent any connections and are constants. 

343245 pairs of array `i` and `o` are collected by liveoverflow in `training_data`, 
and can be downloaded [here](https://www.youtube.com/redirect?v=PQPO5Z4lVTU&event=video_description&redir_token=Z7V7dxHSpVC-FMN3kX7PZ6cXpOd8MTU0NTMyMjI0NkAxNTQ1MjM1ODQ2&q=https%3A%2F%2Fraw.githubusercontent.com%2FLiveOverflow%2FPwnAdventure3%2Fmaster%2Ftools%2Fblocky%2Ftraining_data)

The goal is to find a certain input `i` such that the final output of the whole circuit is 1. 
And we already know that, to achieve this, it's sufficient for 
`o[119,96,14,123,128,140,136,148,145,158,154,167,163,160,173]` to be 0.


## Identifying logical gates

The code for retrieving the underlying logical connection is implemented in [find_gates.py](find_gates.py)

The solution is not optimal: the procedure for finding ternary gates is just based on the output of previous lines.
Because my method of finding those ternary gates is very slow, I will just illustrate my way of identifying NOT gates, 
and binary gates (AND, OR, XOR gates). If anyone has a faster algorithm to identify those connections, please let me know.

The core idea of the algorithm is:
1. first identify some outputs from the inputs
2. move those identified outputs to the set of inputs
3. repeat 1-2 until no outputs can be identified

The implementation uses the observation that at least 1 output is identical to the input.

The identified logical gates is in [gates.txt](gates.txt)


## Identifying patterns

But what does the whole logical gates do? 

To analyze this, I wrote a program [print_tree.py](print_tree.py) to print out the tree for each head in the
target output array indexes `[119,96,14,123,128,140,136,148,145,158,154,167,163,160,173]`, the tree is available at
[tree.txt](tree.txt)

Here are some of my observations:
1. All the trees begin with an `OR`, and one of its operands is from input array `i[]` (or its negation)
2. The other operand is the output (or the negation of the output) of `XOR(i[idx_1], i[idx_2], c)`. 
Two of the XOR operands are inputs (or their negations), and the remaining operand `c` is constructed in a 
recursive pattern: `c <- OR(AND(i[idx_3], i[idx_4]), AND(XOR(i[idx_3], i[idx_4]), c))`
3. The pairs of inputs `{i[idx_1], i[idx_2]}`, and every `(i[idx_3], i[idx_4])` is fixed across differen heads, and 
whether or not to negate them is fix as well. For example, if head `119` has the pair `{!i[10], i[29]}`, then across
all the heads, `!i[10]` is paired with `i[29]`.

Those are the most important observations that took me quite a long time to find out. The final computation done by
 the circuit is given and verified across all training data in [verify.py](verify.py)

By the way, [gates_spec.txt](gates_spec.txt) added some of my speculations to the logical gate to make it complete, and 
the `o[6]` is the final switch to open the gate!
The whole speculated circuit logic is printed in [tree_spec.txt](tree_spec.txt)

## Dependency

The python3 scripts are based on

* [Numpy](https://pypi.org/project/numpy/)
* [anytree](https://pypi.org/project/anytree/)