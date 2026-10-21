# v1: the prompt did not list a FUNCTION point's parameters

These runs (the one-line arms `free` and `scoped`, the multi-line arms `lines` and `lines-scoped`, on SmolLM2-135M and Qwen2.5-Coder-0.5B and 1.5B) were taken with a prompt that named a function
point's parameters only inside the tag (`params="n"`), so the three function-kind tasks (R13-R15) were answered with the call site's variable names (`nN = nN * nN`) and failed at run time. A defect of
the prompt, not of the models: the amended prompt says `Parameters: n.` and everything was re-run (`../`). Kept as the record; the numbers in the results are the amended ones.
