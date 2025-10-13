from typing import Tuple
from contextvars import ContextVar

from ..models.key_models import Trace, Step

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
        """Initialize AITraceStorageContext"""
        
        self._trace: ContextVar[Trace] = ContextVar('current_trace', default=None)
        self._steps: ContextVar[Tuple[Step, ...]] = ContextVar('steps_calling_stack', default=tuple())

    def add_step(
        self,
        new_step: Step,
    ):
        """add a new step into steps_calling_stack
        
        Args:
            new_step(Step): a new step.
        """

        old_steps:Tuple = self._steps.get()
        old_steps += (new_step, )
        self._steps.set(old_steps)
    
    def pop_step(self) -> Step:
        """pop step stack to get the top step data and remove it
        
        Returns:
            Step: top step
        """

        steps = self._steps.get()
        top_step: Step = steps[-1]
        self._steps.set(steps[:-1])
        return top_step
    
    def set_trace(self, current_trace: Trace | None):
        """set a new trace
        
        Args:
            current_trace(Trace | None): current trace. It maybe a None type for no current trace.
        """

        assert self._trace.get() is None, "Ensure _trace is empty before calling set_trace"
        self._trace.set(current_trace)
    
    def pop_trace(self) -> Trace | None:
        """pop trace
        
        Returns:
            Trace | None: current trace. None means no trace now.
        """

        trace = self._trace.get()
        self._trace.set(None)
        return trace

aitrace_storage_context = AITraceStorageContext()
