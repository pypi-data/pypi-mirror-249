from jsonargparse import CLI
from fasttext import load_model
from pathlib import Path
from wasabi import msg
import os


def quantize(input: str, 
             output: str,
             train_file: str,
             test_file: str,
             cutoff: int = 100000, 
             retrain: bool = True, 
             qnorm: bool = False, 
             qout: bool = False,
             epoch: int = 1):
    """fasttext模型量化

    Args:
        input (str): 模型路径。
        output (str): 量化后的模型保存路径。
        train_file (str): 训练文件路径, 用于微调量化模型。
        test_file (int): 测试文件路径, 用于测试量化模型。
        cutoff (int, optional): 量化模型的ngram特征数量. Defaults to 100000.
        retrain (bool, optional): 是否继续微调训练量化后的模型embedding层. Defaults to True.
        qnorm (bool, optional): 是否量化标准化层. Defaults to True.
        qout (bool, optional): 是否量化输出层. Defaults to False.
        epoch (int, optional): 继续微调训练轮数. Defaults to 1.
    """
    
    model_path = Path(input)
    save_path = Path(output)
    if not model_path.exists():
        msg.fail(f"无法读取模型: {model_path}", exits=1)
    else:
        model = load_model(str(model_path))
        msg.good(f"成功加载模型: {model_path}.")
    with msg.loading(f"正在评估模型 {model_path} ..."):
        result = model.test(test_file)
    msg.info(f"原始模型评估结果 -> 测试数量: {result[0]} 准确率: {round(result[1], 4)} 召回率: {round(result[2], 4)}")
    model_size = round(os.path.getsize(model_path) / 1024 / 1024, 2)
    with msg.loading(f"正在量化模型: {model_path}"):
        model.quantize(input=train_file,
                       qnorm=qnorm,
                       qout=qout,
                       retrain=retrain,
                       cutoff=cutoff,
                       epoch=epoch)
    with msg.loading(f"正在评估量化模型 {output} ..."):
        quantize_result = model.test(test_file)
    msg.info(f"量化模型评估结果 -> 测试数量: {quantize_result[0]} 准确率: {round(quantize_result[1], 4)} 召回率: {round(quantize_result[2], 4)}")
    if save_path.exists():
        msg.warn(f"量化模型已存在: {save_path}. 旧模型将被覆盖.")
    model.save_model(output)
    msg.good(f"量化模型已保存: {output}.")
    quantized_model_size = round(os.path.getsize(output) / 1024 / 1024, 2)
    msg.info(f"原始模型大小: {model_size}MB. 量化后模型大小: {quantized_model_size}MB.")

def run():
    CLI(quantize, as_positional=False)