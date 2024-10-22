**摘要：**膀胱癌是一种异质，复杂且广泛的疾病，如果治疗不当，其发病率，死亡率和费用很高。正如随机试验的令人信服的证据所表明的那样，膀胱癌的准确和准确的分期是治疗选择和预后预测的基础。深度卷积神经网络 (dcnn) 提取特征的非凡能力是这些类型网络提供的主要优势之一。DCNNs在许多实际的临床医学应用中都能很好地工作，因为它需要昂贵的大规模数据注释。然而，缺乏背景信息阻碍了其有效性和可解释性。临床医生通过评估肿瘤是否为肌肉浸润性来确定肿瘤的阶段，如肿瘤在膀胱壁的浸润图像所示。将这些临床知识纳入DCNN具有增强膀胱癌分期的性能并根据医学原理进行预测的能力。因此，我们引入PENet，创新的先验证据深度神经网络，用于根据临床知识对膀胱癌分期的MR图像进行分类。为此，首先，测量肿瘤渗透到膀胱壁的程度，以获得称为先验证据的类概率的先验分布参数。其次，我们根据贝叶斯定理公式化了类概率的后验分布。最后，我们根据类概率的后验分布修改损失函数，该参数在学习过程中既包括先验证据又包括预测证据。我们的调查表明，通过提供与地面事实一致的网络先验证据，可以减少PENet的预测误差和方差。使用MR图像数据集，实验表明，PENet在膀胱癌分期方面的性能优于基于图像的DCNN算法。

## 介绍

膀胱癌T分期的MIBC与T1或更低和T2或更高相关。因此，准确，准确的膀胱癌分期非常重要，因为它会影响治疗策略和预后。X射线照片，例如由磁共振成像 (MRI) 和计算机断层扫描 (CT) 产生的照片，是临床环境中用于诊断和治疗膀胱癌的主要诊断工具和治疗方式。众所周知，DCNN具有强大的特征提取能力，在临床医学成像领域前景广阔，例如基于图像的膀胱癌计算机辅助诊断 (CAD) [4]，涵盖癌症分期 [5,6]，肿瘤分割 [7-9]，癌症治疗 [10,11]，以及其他。大多数已知的基于图像的膀胱癌分期方法都依赖于直接的dcnn来根据患者膀胱的图像评估肿瘤的分期。然而，纯粹的基于图像的分类方法需要昂贵的大规模数据注释作为基础，并且忽略临床经验和先验，这可能导致不准确的肿瘤阶段预测与医学知识不一致，从而限制性能和可解释性。相反，临床医生通过检测肿瘤是否已扩散到周围肌肉来确定膀胱肿瘤的阶段，这也称为肿瘤浸润到膀胱壁。对于增强膀胱癌分期预测和使其符合医学法律，尤其有效的是将肿瘤浸润到DCNN的临床先验联系起来。为了根据临床知识实现膀胱癌的分期预测，我们引入了一种新颖的先验证据深度神经网络，称为PENet。

首先，通过测量膀胱肿瘤浸润膀胱壁的程度，我们可以使用证据理论来估计有多少证据支持我们的假设。因此类概率的先验分布参数被称为先验证据。其次，贝叶斯定理用于直接通过观察概率的似然分布和类概率的先验分布来表示类概率的后验分布。最后，我们基于类概率的后验分布重建了证据深度神经网络的目标函数，以通过整合先验证据指导来提高PENet的性能。以下段落概述了这项研究的贡献：

* 提出一种简单的策略，用于量化肿瘤渗透到膀胱壁的临床特征，以获得先前的分布参数。通过确定肿瘤和膀胱壁在彼此的内积中有多少矩阵，可以确定肿瘤和膀胱壁之间存在多少重叠，以生成先验证据作为先验分布参数。
*  构造类概率的后验分布。我们根据观察和先验分布的似然分布，根据贝叶斯定理来制定最优分布，其中分布参数分别从图像和先验中提取证据。

* 提出了一种用于对膀胱癌分期图像进行分类的PENet。我们基于类概率的后验分布，重新构造了PENet的证据深度神经网络的目标函数，以优化PENet的权重参数。正如我们所证明的那样，当融合与地面事实兼容的先前证据时，PENet的预测错误可能会减少。

## 二、相关工作

膀胱癌是泌尿系统最常见的恶性肿瘤之一 [14,15]，具有显著的发病率、死亡率和成本。根据膀胱癌的适当阶段，治疗方案和预期预后将发生变化 [16]。TNM分期系统是目前最常见的肿瘤分期系统，是临床医生对恶性肿瘤进行分类的标准方法。部分或全部膀胱切除术通常用于治疗T2或更高 (MIBC) 的肿瘤，可以通过MR成像进行诊断，并根据肿瘤是肌肉浸润还是浸润程度从T0到T4分期。Dcnn已经看到广泛的应用作为一种用于膀胱癌的计算机辅助检测的方法，因为它们能够在不同程度的图像抽象中自动提取图像的层次特征，这使得dcnn能够在不同的细节水平上分析图像 [17,18]。应用包括膀胱分割，肿瘤检测，癌症治疗和膀胱癌分期 [5]。

对于膀胱分割，Ma等人提出了一种基于U-Net的自动马分割方法，用于CT尿路造影，其中膀胱边界不需要用户输入边界框，并且由U-Net进行估计 [7]。Shkolyar等人建议CystoNet与DCNN一起改善膀胱肿瘤定位、手术切除和术中导航的肿瘤检测性能 [22]。对于癌症治疗，Rundo等人开发了一种非侵入性预测系统，该系统由ct扫描图像管道和放射电子学管道组成，以表征对免疫疗法的预期反应，从而告知医生治疗方案 [23]。

使用DCNNs自动从医学图片中检索特征，以对膀胱肿瘤进行分期，以进行膀胱癌分期。通过结合特定于膀胱分期的形态学和纹理特征与许多分类器，包括支持向量机、神经网络和随机防御系统，改进了癌症分期预测。代表累积分布函数 (CDF) 的百分位数的功能特征，代表放射学纹理特征的形态学特征，以及定义肿瘤形状的形态学特征从T2W-MRI和dw-mri作为膀胱癌分期神经网络的输入检索 。Zhang等人根据临床经验从MR图像中学习了有利于肿瘤分期的输入标准，并使用了DCNN中的规则来提高性能。使用ResNet结构，非局部注意力和图像超分辨率处理，[26] 开发了一种基于CT成像的膀胱癌分期的高性能模型。

证据理论 (Dempster-Shafer证据理论) 被视为一种广义概率，它将Dempster规则应用于推理，同时使用质量函数来评估决策不确定性 [12,13]。通过量化观点及其不确定性，证据理论已广泛应用于信息融合和不确定性推理领域。通过将证据理论与机器学习相结合，已经开发了几种用于不确定数据分析的监督和无监督学习方法，包括证据近邻 [27]，证据线性判别分析 [28]，以及有证据的神经网络 [29]。

将证据理论与医学图像分析相结合，例如医学图像分割。通过采用dempster法则来结合MR图像中每个体素附近的数据，Capelle等人提出了一种基于区域的脑肿瘤分割方法 [30]。根据Lian等人的观点，可以通过应用Dempster规则来融合不同模态分割的结果来解决每个模态中不清晰和不精确分割的问题 [31]。

Huang等人使用信念函数和Dempster规则来衡量边界区域分割的不确定性并增加性能 [32]。为了从胸部x线照片诊断肺炎，[444] 将Dempster-Shafer理论应用于五个预先训练的卷积神经网络的融合，包括VGG16，Xception，InceptionV3，ResNet50和DenseNet201，并提供良好的检测性能。证据理论除了用于医学图像的分割之外，还用于医学图像分析过程中的各种附加活动。为了提高证据理论在处理复杂数据中的有效性，一些研究人员最近将其与深度学习技术相结合，创建了构造分类不确定性的证据深度神经网络 [34] [35]。与传统的深度神经网络不同，证据深度神经网络将输出层的激活值视为从预测数据中检索到的证据，因此网络的预测扩展到具有证据参数的概率分布。因此，evidential深度神经网络提供了一种计算深度神经网络预测中不确定性程度并校正不准确程度的方法

## 三、方法

拟议的PENet的两个主要组成部分是测量膀胱癌分期的先前临床经验，以及基于贝叶斯理论的膀胱癌分期分类概率的后验概率分布。图1中显示了PENet过程的三个要素。第一个带有绿色虚线的突出显示模块描述了创建肿瘤阶段证据的过程 (当我们想要表达两种类型的高或低癌症阶段的证据或两种数据和临床经验的证据来源时，我们使用 “证据” 一词。) 使用深度卷积神经网络从标记的MR图像中获得。第二个模块 (由橙色虚线所示) 描述了从分割掩模中检索肿瘤分期的先前证据的过程。在第三个模块中，由紫色虚线所示，我们可以使用从图像中提取的证据 (视为随机变量) 作为参数来制定观察的似然分布; 类似地，基于提取的先验证据，我们制定类概率的先验分布。通过贝叶斯定理，可以用两个证据参数来源导出类概率的后验分布，这是PENet改善性能的损失函数的基础。

####肿瘤浸润临床经验评价

如第1节所述，膀胱癌的分期可分为五个阶段，从T0到T4。如果阶段高于T1，则必须进行膀胱切除术，这被认为是高阶段 [3]。肿瘤浸润到膀胱壁的程度是人类医生根据临床经验确定膀胱肿瘤分期的常用方法。因此，高肿瘤壁重叠表明高癌症分期 (T2)，而少重叠表明低分期 (&lt; T2)。由于肿瘤和膀胱壁分割面罩从临床上开始用于膀胱癌的分期，因此我们确定了重叠程度。

深度神经网络可以理解为堆叠几个非线性函数，上面有一个softmax算子来区分训练数据，这是一个多元分布的参数回归框架。目前，我们都知道传统的深度神经网络是过度自信的，因为softmax的分母压缩了输出概率，一类概率的点估计是一阶不确定性，可以通过交叉熵损失函数进行，但不能表示预测概率的方差，例如二阶不确定性。如第2.2节所述，证据深度神经网络 (EvidentialNet) [34] 提出了一种用证据参数来制定预测概率分布的原则方法，该证据参数可以直接表示预测的方差并完成可靠的分类。与EvidentialNet相反，我们认为，当将类概率视为随机变量时，不应忽略类概率的先验分布。此外，我们可以通过分布假设和贝叶斯定理直接推断类概率后验分布的表达式。通过后验分布重建的损失函数，PENet可以提供更稳定和准确的预测，以提高性能。