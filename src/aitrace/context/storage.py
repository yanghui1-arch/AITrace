
class AITraceStorageContext:
    """AI trace storage context stores the step and trace.
    This context can record a long calling stacks and stores them. The benefit is to easily visualize calling stacks and manage step or trace.

    For example, there is a complex track functions that solve a very complex math problem using agent.

    ```python
    final_answer = None
    complex_math_problem = "xxxxxx"
    final_answer = solve(complex_math_problem, previous_problem_answer=final_answer)

    print(final_answer)

    @track
    def solve(complex_math_problem, previous_problem_answer = None) -> str:

        sub_funcs = split_sub_func(complex_math_problem)

        if len(sub_funcs) == 1:
            return previous_problem_answer

        previous_func_solution = []
        for sub_func in sub_funcs:
            sub_func_solution = solve(
                complex_math_problem=sub_func, 
                previous_problem_answer=previous_func_solution
            )
            previous_func_solution.append(sub_func_solution)
        
        # agent solution logic
        return agent_solve(complex_math_problem, previous_func_solution)

    @track
    def split_sub_func(complex_math_problem) -> list:
        # split logic ...
        ...
    
    @track
    def agent_solve(complex_math_problem, previous_func_solution):
        # agent solve logic ...
        ...
    ```
    ID:                              1                           2                   3.1                 3.2             4     
    Now execution process is solve(complex_math_problem) -> split_sub_func -> [solve(sub_func) -> split_sub_func] -> agent_solve 
                                                                                ↑                       ↓
                                                                                 -----------------------
                                                                                        N times

    AITraceStorageContext will store the steps of solve, split_sub_func and agent_solve again and again and finally store the trace.
    ID 2 step is ID 1 step's child step. ID 3.2 is ID 3.1's child step. So the context step_stack will like as:
    STEP STACK:
        agent_solve
        split_sub_func   -----
                              |  N times
        solve(sub_func)  -----
        split_sub_func
        solve(complex_math_problem)
    """

    def __init__(self):
        pass
