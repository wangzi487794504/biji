##PENet: 用于膀胱癌分期的深度神经网络的先前证据

由于理论和技术限制[1]，单个模态传感器拍摄的图像无法有效和全面地描述成像场景。红外传感器捕捉物体发出的热辐射，可以突出显着目标，但红外图像忽略纹理并且容易受到噪声的影响。相反，可见传感器捕获反射光信息。可见图像通常包含丰富的纹理和结构信息，但对环境敏感，例如光照和遮挡。互补的作用鼓励我们融合红外和可见图像以生成所需的图像，该图像突出突出目标并显示丰富的细节信息。因此，红外和可见图像融合已被广泛用作高级视觉任务的预处理模块，例如对象检测 [2]、跟踪 [3]、行人重新识别 [4] 和语义分割 [5]。

图 1 中的一个示例直观地显示了融合图像对分割任务的贡献。从可见图像中，分割网络可以分割汽车、自行车和几个人，但忽略隐藏在黑暗中的行人。尽管红外图像有助于分割网络准确分割汽车和所有行人，但它忽略了自行车。通过利用红外和可见图像的互补信息，融合图像提高了所有自行车、汽车和行人的分割精度。由于红外与可见光图像融合的实用性，引起了学术界的极大关注。

在过去的几十年中，已经提出了许多图像融合技术，包括传统方法 [8-10] 和最近的基于深度学习的方法 [1]。传统方法通常分为五类，即基于多尺度变换 (MST) 的方法 [11-14]、基于稀疏表示 (SR) 的方法 [15,16]、基于子空间的方法 [17-19] ，基于优化的方法[20]和混合方法[21]。在基于深度学习的方法中，基于自动编码器 (AE) 的框架 [6,22,23]、基于卷积神经网络 (CNN) 的框架 [24-26] 和基于生成对抗网络 (GAN) 的框架 [27-30] ] 是主要的框架。尽管最近基于深度学习的图像融合算法可以生成令人满意的融合图像，但图像融合社区仍然存在一些紧迫的挑战。一方面，现有的融合算法倾向于追求更好的视觉质量和更高的评价指标，但很少系统地考虑融合图像是否可以促进高级视觉任务。一些研究 [31-33] 表明，仅考虑视觉质量和定量指标无助于高级视觉任务。虽然一些工作引入了感知损失来在特征级别约束融合图像和源图像[6,7,24,28,34]，但感知损失并不能有效增强融合图像中的语义信息，如图 1 所示此外，其他研究人员通过分割掩码[26,35]指导图像融合过程，但掩码仅分割了一些显着目标，这对于提升语义信息是有限的。

另一方面，现有的评价方式主要是视觉比较和定量评价。视觉比较侧重于融合图像的对比度和纹理细节，定量评估依赖于一些统计指标来评估融合性能。然而，视觉比较和定量评估都没有反映融合图像对高级视觉任务的促进作用。此外，现有的网络架构在提取细粒度细节特征方面效果不佳。最后但并非最不重要的一点是，许多现有的融合算法在努力提高视觉质量和评估指标的同时忽略了对实时图像融合的需求。在这项研究中，提出了一种语义感知融合网络，称为 SeAFusion，以实现实时红外和可见光图像融合。我们方法的关键是同时在图像融合和高级视觉任务中获得卓越的性能。具体来说，我们引入了一个分割网络来预测融合图像的分割结果，用于构建语义损失。然后，利用语义损失通过反向传播来指导融合网络的训练，迫使融合图像包含更多的语义信息。此外，为了满足实时高级视觉任务的需求，我们开发了一种基于梯度残差密集块（GRDB）的轻量级网络。 GRDB可以通过主密集流实现特征重用，通过残差梯度流提升对细粒度细节的描述能力。