import whiledb_nom

state = whiledb_nom.exec(
"""
arr = malloc(100);
idx = 0;
while idx < 100 {
    *(arr + idx) = idx;
    idx = idx + 1;
}
""")

print(state)

print(whiledb_nom.eval("malloc(100)", *state))
print(whiledb_nom.eval("free(arr)", *state))
print(whiledb_nom.eval("malloc(10)", *state))

print(state)