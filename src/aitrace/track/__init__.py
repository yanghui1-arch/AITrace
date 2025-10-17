from .at_track import AITraceTracker

__all__ = [
    'track_step',
    'track_trace',
]

tracker = AITraceTracker()

track = tracker.track


if __name__ == '__main__':
    from ..models.common import LLMProvider
    from openai import OpenAI
    @track(
        func_name="llm_classisfication",
        project_name="aitrace_demo",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    def llm_classification(film_comment: str):
        prompt = "Please classify the film comment into happy, sad or others. Just tell me result. Don't output anything."
        cli = OpenAI(base_url='https://api.deepseek.com', api_key='')
        llm_counts(film_comment=film_comment)
        return cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: {film_comment}"}],
            model="deepseek-chat"
        ).choices[0].message.content
    
    @track(
        func_name="llm_classisfication",
        project_name="aitrace_demo",
        tags=['test', 'demo', 'second_demo'],
        # track_llm=LLMProvider.OPENAI,
    )
    def llm_counts(film_comment: str):
        prompt = "Count the film comment words. just output word number. Don't output anything others."
        cli = OpenAI(base_url='https://api.deepseek.com', api_key='')
        return cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: {film_comment}"}],
            model="deepseek-chat"
        ).choices[0].message.content

    llm_classification("Wow! It sucks.")

    """
    Run output:

    ```bash
    TrackerOptions(project_name='aitrace_demo', tags=['test', 'demo'], func_name='llm_classisfication', is_step=True, is_trace=False, step_type=<StepType.CUSTOMIZED: 'customized'>, model=None, step_name=None, trace_name=None)
    {'project_name': 'aitrace_demo', 'name': 'customized', 'id': UUID('0199c917-9fc9-7e8a-8fa6-670369d5df30'), 'trace_id': UUID('0199c917-9fca-790e-b2a0-d860656df9c5'), 'type': <StepType.CUSTOMIZED: 'customized'>, 'tags': ['test', 'demo'], 'input': {'film_comment': 'Wow! It sucks.'}, 'output': None, 'error_info': None, 'model': None}
    {'project_name': 'aitrace_demo', 'name': 'customized', 'id': UUID('0199c917-acce-7ba7-bebb-502234601c35'), 'trace_id': UUID('0199c917-accf-74d1-8511-3fb10828497e'), 'type': <StepType.CUSTOMIZED: 'customized'>, 'tags': ['test', 'demo'], 'input': {'input': None}, 'output': {'output': 'sad'}, 'error_info': None, 'model': None}
    ```
    
    """