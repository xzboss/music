from sklearn.model.selection import train_test_split#（导入训练集和测试集拆分函数）
from sklearn.tree import DecisionTreeClassifier #（导入决策树分类器模型）
from sklearn.datasets import load_breast_cancer#（导入乳腺癌数据读取函数）
cancer = datasets.load_breast_cancer()#（导入乳腺癌数据集）
X_train, X_test, y_train, y_test = train_test_split(
cancer.data, cancer.target, stratify=cancer.target, random_state=42)
tree = DecisionTreeClassifier(random_state=0)
clf = tree.fit(X_train,y_train)#（利用决策树拟合训练集数据）
score = clf.predict(X_test)#（利用拟合好的模型评估测试集得分）
tree = DecisionTreeClassifier(criterion='entropy',
                                     random_state=30,
                                     max_depth=4,
                                     min_samples_leaf=3
                                    )#（使用限制最大深度 4 层的预剪枝重新实例化决策树模型）
clf = tree.fit(X_train,y_train)#（利用决策树拟合训练集数据）
score = clf.predict(X_test)#（利用拟合好的模型评估测试集得分）
print(tree.feature_importances_)#（利用决策树属性显示特征重要性）