from rmbserver.ai.openai_client import openai_llm
import json
from jinja2 import Template
import time
from rmbserver.log import log


def ai_generate(prompt_name: str,
                prompt_template: str,
                template_format: str = "jinja2",  # jinja2 or string
                output_format: str = "json",  # json or str
                **input_variables
                ) -> str or dict:
    """
    根据模板生成文本或者json
    """
    _start = time.time()
    if input_variables is None:
        input_variables = {}

        # 处理Jinja2模板
    if template_format == "jinja2":
        template = Template(prompt_template)
        prompt = template.render(**input_variables)
    else:
        prompt = prompt_template.format(**input_variables)

        # 调用OpenAI API
    if output_format == "json":
        rst, in_tokens, out_tokens = openai_llm.predict(prompt, json_format=True)
        rst = json.loads(rst)
    elif output_format == "str":
        rst, in_tokens, out_tokens = openai_llm.predict(prompt)
    else:
        raise ValueError(f"output_format must be json or str, but got {output_format}")
    _end = time.time()
    log.info(f"[Perf]GeneratedAI: {prompt_name}         cost(s): {int(_end - _start)}    "
             f"in_tokens {in_tokens}     out_tokens {out_tokens} ")
    return rst
