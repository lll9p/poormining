# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from data.db import get_db_session, Pinkunhu2015
from sklearn.ensemble import RandomForestClassifier
from data.dbaccess import normalize


class RandomForestModel(object):
    """ 使用随机森林模型预测是否脱贫 """
    def run(self):
        """ 运行 """
        # 获取数据
        X, Y = self._fetch_data()
        clf = self.get_classifier(X, Y)
        # 测试
        X, Y = self._fetch_test_data()
        self.predict(clf, X, Y)

    def get_classifier(self, X, Y):
        """ 构建随机森林模型
        :param X: 训练数据
        :param Y: 训练数据结果
        :return: 模型
        """
        clf = RandomForestClassifier(n_estimators=10)
        clf.fit(X, Y)
        return clf

    def predict(self, clf, X, Y):
        """ 用当前的模型预测
        :param clf: 模型
        :param X: 测试数据
        :param Y: 测试数据结果
        :return: 命中率
        """
        Y2 = clf.predict(X)
        total, hit = len(Y), 0
        for idx, v in enumerate(Y2):
            if Y[idx] == v:
                hit += 1

        print 'Total: %d, Hit: %d, Precision: %.2f%%' % (total, hit, 100.0*hit/total)
        # 用 镇雄县 的模型去预测 陆良县 的结果
        # Total: 6769, Hit: 5295, Precision: 78.22%

        return hit * 1.0 / total

    def _fetch_data(self):
        """ 获取建模数据 """
        session = get_db_session()
        objs = session.query(Pinkunhu2015).filter(Pinkunhu2015.county == '镇雄县').all()
        X, Y = [], []
        for item in objs:
            col_list = []
            for col in [
                'tv', 'washing_machine', 'fridge',
                'reason', 'is_danger_house', 'is_back_poor', 'is_debt', 'standard',
                'arable_land', 'debt_total', 'living_space', 'member_count', 'person_year_total_income',
                'year_total_income', 'subsidy_total', 'wood_land', 'xin_nong_he_total', 'xin_yang_lao_total',
                'call_number', 'bank_name', 'bank_number', 'help_plan'
            ]:

                normalized_value = normalize(col, getattr(item, col))
                col_list.append(normalized_value)
            X.append(col_list)
            normalized_value = normalize('poor_status', getattr(item, 'poor_status'))
            Y.append(normalized_value)

        return X, Y

    def _fetch_test_data(self):
        """ 获取测试数据 """
        session = get_db_session()
        objs = session.query(Pinkunhu2015).filter(Pinkunhu2015.county == '彝良县').all()
        X, Y = [], []
        for item in objs:
            col_list = []
            for col in [
                'tv', 'washing_machine', 'fridge',
                'reason', 'is_danger_house', 'is_back_poor',  'is_debt', 'standard',
                'arable_land', 'debt_total', 'living_space', 'member_count', 'person_year_total_income',
                'year_total_income', 'subsidy_total', 'wood_land', 'xin_nong_he_total', 'xin_yang_lao_total',
                'call_number', 'bank_name', 'bank_number', 'help_plan'
            ]:

                normalized_value = normalize(col, getattr(item, col))
                col_list.append(normalized_value)
            X.append(col_list)
            normalized_value = normalize('poor_status', getattr(item, 'poor_status'))
            Y.append(normalized_value)

        return X, Y


if __name__ == '__main__':
    m = RandomForestModel()
    m.run()
