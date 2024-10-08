##Integrating General and Speciﬁc Priors into Deep Convolutional Neural Networks for Bladder Tumor Segmentation

磁共振 (MR) 图像的膀胱肿瘤分割对于膀胱癌的智能诊断至关重要。膀胱肿瘤分割是基于机器学习和图像处理方法实现的，该方法包括聚类，分类，强度阈值和区域生长的各种方法。然而，这些方法依赖于人为的放射组学特征，这限制了肿瘤分割的精度。近年来，由于特征学习的优越性，深度卷积神经网络 (DCNNs) 已被广泛用于分析膀胱的医学图像，用于肿瘤检测 和分割。

将DCNNs应用于膀胱肿瘤的分割，现有的大多数方法都直接基于带有标记图像的模型训练来构建分割模型。但是，**这些分割方法过度依赖于训练数据，而忽略了肿瘤大小和位置的普遍存在的先验信息，这些先验信息可以从数据中学习或从领域知识中获得。**肿瘤的先验对提高膀胱肿瘤的分割精度很有帮助，特别是对于标记图像不足以覆盖多样性的情况。==根据先验，我们知道膀胱肿瘤的大小在特定范围内，并且肿瘤的位置分布在膀胱壁附近。==因此，将这些先验信息集成到dcnn中以提高模型的鲁棒性，同时降低膀胱肿瘤分割的数据依赖性是很自然的。

对于医学图像分割，可以将两种先验集成到dcnn中，以提高分割性能。第一种是从数据中学习的特定先验。具体先验比像素级特征提供了更多的语义和直观信息，包括注意机制 [7] 、形状感知潜空间 [6] 、 [8] 和距离图 [9]。**特定先验可以表示图像细节的先验，但仍需要数据学习，当标记图像不足时，先验质量无法保证。**与从数据中学习的特定先验不同，**第二种先验是从领域专家那里获得的一般先验。作为领域知识，一般先验比具体先验更为抽象和概括，如大小范围 [10] 、形状特征 [11] 等。**尽管一般先验不需要数据学习，但先验过于粗糙，无法导致dcnn在细节上产生精确的分割。

如前所述，我们知道这两种先验是相辅相成的，==医学图像分割的最佳先验应该包括特定先验和一般先验。==受此启发，我们提出了一种新的膀胱肿瘤分割方法，该方法将来自数据的特定先验和来自领域知识的一般先验整合到 DCNN 中。具体来说，为了从图像数据中学习特定的先验，我们在分割网络中添加了一条注意力解码路径，使模型专注于肿瘤经常发生的区域。为了构建一般先验，我们制定并融合了肿瘤位置分布和肿瘤大小范围的领域知识。此外，我们还设计了保持特定先验与一般先验一致的策略。本文的贡献总结如下。

构建一个混合先验，包括膀胱肿瘤的特定先验和一般先验。具体的先验是从数据中学习并基于DCNN的注意力模型构建的，以指示膀胱肿瘤的高发区域。一般先验是基于肿瘤位置和肿瘤大小的领域知识构建的。与现有的涉及部分先验信息的分割方法相比，混合先验更全面地综合了数据和领域专家的经验。

提出一种将先验整合到 DCNN 中进行膀胱肿瘤分割的机制。我们扩展了基于 DCNN 的分割模型的目标函数，该模型包括分割损失和先验损失。除了减少分割误差外，先验损失还要求 DCNN 诱导的分割与特定和一般先验一致。此外，我们还设计了一种优化目标函数的策略，其中一般先验被认为是特定先验优化的约束，以保持两种先验一致。

## 相关工作

### 膀胱医学图像分割

在神经网络发展之前，膀胱壁的分割方法主要是基于水平集的方法[12]。秦等人。 [13] 提出了一种通过结合多加权磁共振 (MR) 图像的信息来分割内壁和外壁的方法。然而，基于水平集的方法难以处理医学图像分割的问题，包括伪影、低对比度和模糊的边界。此外，水平集是一个耗时的函数来获得分割结果，其性能与初始化密切相关。最近，随着卷积神经网络逐渐成为一种强大的工具，CNN被广泛用于膀胱癌分割。查等人。 [14]使用CNN自动找出膀胱区域并将其分割为水平集的初始值。多尔兹等人。 [15]通过将渐进式扩张添加到卷积网络中来提高膀胱多区域分割的性能。这些方法虽然可以取得很好的性能，但在面对少量训练样例时却无能为力。

###图像分割的先验深度学习

由于像素级标注的成本较高，先验与深度学习模型的结合成为医学图像分割的研究热点。已经证明，将prior合并到图像分割算法中对于获得更准确和合理的结果是有用的。通常，对于集成的先验，一种是基于数据的特定先验 。例如，Oktay等人通过设计注意门 (AG) 将注意机制与U-Net相结合。和Caliva等使用从地面真相掩码派生的距离图来创建惩罚项，将网络的重点引导到难以分割的边界区域。Luo等人提出了一种新颖的分割方法，该方法利用使用自动编码器从真实蒙版中学到的潜在空间来提高低质量图像的准确性。Li等利用自动编码器像先前一样学习膀胱壁的语义信息，并将其合并到分割网络中。另一个是从领域专家那里获得的一般先验。例如目标大小的范围，该范围被用作改善 [10] 中的分割性能的可微惩罚。此外，Mirikharaji和Hamarneh 提出了一种新颖的形状损失，然后在预测图中惩罚非星形形状段，以确保分割结果中的整体结构。如上所述，现有的方法将部分先验引入到深度学习模型中进行图像分割，从而限制了分割精度。因此，我们的方法将特定先验和一般先验集成到深度神经网络中，以增强由dcnn引起的医学图像分割。

### 将 PRIORS 集成到 DCNN 中以进行膀胱肿瘤分割

在本节中，我们介绍了将一般和特定先验整合到DCNN中以进行膀胱肿瘤分割的方法。所提出方法的框架如图1所示。第一行是基于通用编码器-解码器的分段网络，例如U-Net和DenseUnet。为了使用先验来增强DCNN的分割，我们首先通过在编码Z上添加注意解码路径来生成特定先验，以注意膀胱肿瘤频繁发生的区域，然后我们使用特定先验来调节基于DCNN的分割通过特定先验损失 (Lspecific)。此外，我们根据临床知识制定肿瘤大小和位置的一般先验，并使用一般先验通过一般先验损失 (Lgeneral) 约束特定先验的产生。

<img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1668311711583.png" alt="1668311711583" style="zoom:80%;" />



* 膀胱肿瘤分割的先验表现

通常用于肿瘤评估的一般先验包括大小范围和位置。根据膀胱肿瘤的临床知识，膀胱的位置相对固定，肿瘤一般生长在膀胱壁附近。因此，制定膀胱肿瘤位置在膀胱壁周围的分布是直观的。在本文中，我们采用高斯混合模型 (GMM) 来表示肿瘤位置分布的一般先验。

<img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1668329808731.png" alt="1668329808731" style="zoom:80%;" />

其中r是分割结果中膀胱肿瘤的中心坐标，π m，um，σ m分别表示混合系数，均值和协方差矩阵。

除了肿瘤位置外，膀胱肿瘤的大小范围也作为分割的另一个通用先验，可以通过计算分割结果中肿瘤区域的像素来衡量。假设大小范围在 a 和 b 之间，我们有

<img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1668348313849.png" alt="1668348313849" style="zoom:80%;" />

其中，Ω 表示空间域，P (r | Θ) 是肿瘤存在的概率分布。

结合肿瘤位置和大小的两个先验，我们提出了一个统一的一般先验，由大小范围一般先验 (SGP) 表示，它被公式化为

<img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1668348634468.png" alt="1668348634468" style="zoom:80%;" />

显然，一般先验SGP实际上是肿瘤大小超过肿瘤位置概率分布的期望。与以前的肿瘤位置相比，我们还构建了一个一般的先于描述膀胱肿瘤不可能的位置，这被称为背景一般先于 (BGP)。BGP公式化为 

<img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1668348736675.png" alt="1668348736675" style="zoom:80%;" />

一般先验过于抽象，无法直接指导 DCNN 实现精确的肿瘤分割结果。因此，我们采用一般先验来约束注意力区域特定先验的生成，并进一步使用特定先验来调节 DCNNs 来改进肿瘤分割。

为了以注意力的形式生成特定的先验，我们在现有的分割网络中添加了一条注意力解码路径，使 DCNN 能够关注肿瘤高发区域。我们将注意力形式的特定先验表示为注意力特定先验（ASP）。图1说明了注意力解码路径的结构，它依次包括一个上采样层、两个卷积层和一个激活层。

为了以注意力的形式生成特定的先验，我们在现有的分割网络中添加了一条注意力解码路径，使 DCNN 能够关注肿瘤高发区域。我们将注意力形式的特定先验表示为注意力特定先验（ASP）。图1说明了注意力解码路径的结构，它依次包括一个上采样层、两个卷积层和一个激活层。

* 将先验集成到分割网络中、

  为了将特定先验和一般先验整合到 DCNN 中进行肿瘤分割，我们扩展了分割模型的目标函数，包括分割损失和先验损失。

  <img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1668349366123.png" alt="1668349366123" style="zoom:80%;" />

<img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1668349681862.png" alt="1668349681862" style="zoom:80%;" />

至于（5），总损失由两项组成。第一项是关于像素标签的分割损失，由交叉熵表示。第二项是先验损失，用于衡量分割和先验之间的一致性。先验损失包括 Lspecific 和 Lgeneral。 Lspecific 是学习注意力特定先验的损失，也用于调节 DCNN 的分割。 Lgeneral 是在一般先验约束下学习注意力特定先验的损失。 Lgeneral 用于保证一般先验和特定先验之间的一致性。 β是平衡先验损失和分割损失的超参数，β的大值表明先验对分割的影响很大。

Lspecific 用于学习注意力特定的先验并约束基于 DCNN 的肿瘤分割。通过在图像上重叠注意力掩码，注意力机制使神经网络专注于高度关注的区域，从而促进像素分类。如果像素级标记图像不足，则学习到的注意力区域不准确。相反，对于肿瘤分割，更容易确定肿瘤很少出现的区域。基于此，我们设计了一个能量函数来表示这种约束，并提出了一种新的损失来抑制没有注意的区域中的肿瘤。所提出的损失是基于[19]中的函数实现的，它将Mumfordshah能量函数[20]转换为神经网络的导数损失函数。具体来说，对于给定的特定注意力先验 e(r) := e(r; α), r ∈ Ω ⊂ R2，建议的损失 Lspecific 定义为

<img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1668390891337.png" alt="1668390891337" style="zoom:80%;" />

其中y(r) := y(r; Θ) 是分段网络的softmax层的输出，q表示由

<img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1668390950504.png" alt="1668390950504" style="zoom:80%;" />

