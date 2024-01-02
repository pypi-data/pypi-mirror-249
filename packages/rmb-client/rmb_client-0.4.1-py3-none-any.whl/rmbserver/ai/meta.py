from rmbcommon.models import MetaData
from rmbserver.ai.generations import ai_generate
from rmbserver.ai.prompts.agent import PROMPT_GEN_META


def gen_meta_desc_and_relations(meta_data: MetaData) -> MetaData:
    """
    生成描述和关联关系
    """
    # 使用to_string_for_llm()方法，只返回存在字段描述 curr_desc 为空的表
    inferred_meta = ai_generate("GEN_META", PROMPT_GEN_META,
                                meta_data=meta_data.to_dict_for_llm(),
                                )
    # if inferred_meta.get("MetaData"):
    #     inferred_meta = inferred_meta["MetaData"]
    return MetaData.load_from_dict(inferred_meta)

