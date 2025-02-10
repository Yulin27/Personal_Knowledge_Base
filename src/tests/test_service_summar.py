import unittest
from unittest.mock import MagicMock
from src.services.summarization import SummarizationService
from src.models.groq_model import GroqModel


# Unit test for SummarizationService
class TestSummarizationService(unittest.TestCase):

    def test_classify_with_real_model(self):
        # Initialize the real model (use real API credentials if necessary)
        real_model = GroqModel()
        summarization_service = SummarizationService(model=real_model)

        # Define test data
        text = """编码器-解码器架构
与早期的seq2seq模型一样，原始的Transformer模型使用编码器-解码器（encoder–decoder）架构。编码器由逐层迭代处理输入的编码层组成，而解码器则由对编码器的输出执行相同操作的解码层组成。

每个编码层的功能是确定输入数据的哪些部分彼此相关。它将其编码作为输入再传递给下一个编码层。每个解码层的功能则相反，读取被编码的信息并使用集成好的上下文信息来生成输出序列。[8]为了实现这一点，每个编码层和解码层都使用了注意力机制。

对于每个输入，注意力会权衡每个其他输入的相关性，并从中提取信息以产生输出。[9]每个解码层都包含一个额外的注意力机制，它会在从编码层提取信息之前先从之前解码器的输出中提取信息。

编码层和解码层都有一个前馈神经网络用于对输出进行额外处理，并包含残差连接和层归一化步骤。[9]

缩放点积注意力
Transformer模型的基本构建单元是缩放点积注意力（scaled dot-product attention）单元。当一个句子被传递到一个Transformer模型中时，可以同时计算所有标记互相之间的注意力权重。注意力单元为上下文中的每个标记生成嵌入，其中包含有关标记本身的信息以及由注意力权重加权得到的其他相关标记的信息。

对于每个注意力单元，Transformer模型学习三个权重矩阵，分别为查询（query）权重
W
Q
{\displaystyle W_{Q}}、键（key）权重
W
K
{\displaystyle W_{K}}以及值（value）权重
W
V
{\displaystyle W_{V}}。对于每个标记
i
{\displaystyle i}，输入词嵌入
x
i
{\displaystyle x_{i}}分别与三个权重矩阵相乘以得到查询向量
q
i
=
x
i
W
Q
{\displaystyle q_{i}=x_{i}W_{Q}}、键向量
k
i
=
x
i
W
K
{\displaystyle k_{i}=x_{i}W_{K}}与值向量
v
i
=
x
i
W
V
{\displaystyle v_{i}=x_{i}W_{V}}。再使用查询向量和键向量计算注意力权重，即计算
q
i
{\displaystyle q_{i}}和
k
j
{\displaystyle k_{j}}的点积以得到从标记
i
{\displaystyle i}到标记
j
{\displaystyle j}的注意力权重
a
i
j
{\displaystyle a_{ij}}。之后再将注意力权重除以向量维度的平方根
d
k
{\displaystyle {\sqrt {d_{k}}}}以在训练期间稳定梯度，并通过softmax函数对权重进行归一化。
W
Q
{\displaystyle W_{Q}}与
W
K
{\displaystyle W_{K}}的不同意味着注意力是非对称的：如果标记
i
{\displaystyle i}很关注标记
j
{\displaystyle j}（即
q
i
⋅
k
j
{\displaystyle q_{i}\cdot k_{j}}很大）并不一定意味着标记
j
{\displaystyle j}也反过来关注标记
i
{\displaystyle i}（即
q
j
⋅
k
i
{\displaystyle q_{j}\cdot k_{i}}可能很小）。对每一个标记
i
{\displaystyle i}而言，注意力单元的输出是以
a
i
j
{\displaystyle a_{ij}}（标记
i
{\displaystyle i}到每一个标记的注意力）加权所有标记的值向量得到的加权和。

对所有标记的注意力计算可以表示为使用softmax函数的一个大型矩阵计算，由于可以对矩阵运算速度进行优化，这十分利于训练速度的提升。矩阵
Q
{\displaystyle Q}、
K
{\displaystyle K}和
V
{\displaystyle V}可分别定义为第
i
{\displaystyle i}行是向量
q
i
{\displaystyle q_{i}}、
k
i
{\displaystyle k_{i}} 和
v
i
{\displaystyle v_{i}}的矩阵。"""
        # Call the classify method
        result = summarization_service.summarize(text=text)

        # Print or assert the result
        print("Real model output:", result)

if __name__ == "__main__":
    unittest.main()



    
