import pandas as pd
import random
import time
import math
import numpy as np

OUTPUT_PATH = ''


class trans_generate:

    def __init__(self, total_sum=7000, user_sum=10, group_num=2, super_ratio=0.08, trans_limit=50000):
        self.total_sum = total_sum  # 总交易数
        self.user_sum = user_sum  # 总用户数
        self.super = super_ratio  # 强制交易分组的几率,越大意味着越有可能在同组交易
        # self.start_time = '2019-01-01 00:00:00'
        self.group_num = group_num  # 分组数
        self.trans_amount_limit = trans_limit
        self.per_group_num = math.floor(user_sum / group_num)  # 每组人数
        self.user_list, self.user_balance = self.user_dict_generate()  # 生成组列表，以及维护余额字典

    @staticmethod
    def account_num_generate():
        """
        生成交易账号
        :return: 账号字符串
        """
        firstnum = np.random.randint(1, 9)
        othernum = np.random.randint(0, 9, size=18)

        numstr = str(firstnum)
        for each in othernum:
            numstr = numstr + str(each)

        return numstr

    def user_dict_generate(self):
        """
        用户字典生成
        :return:
        """
        count = 0
        user_dict = dict()
        while count < self.user_sum:
            count += 1
            user_dict[trans_generate.account_num_generate()] = np.random.randint(0, 99999)  # 合成字典列表，包括余额

        return list(user_dict.keys()), user_dict  # 生成用户字典 顺带生成余额记录字典

    def trans_user_generate(self):
        while True:
            user1 = random.choice(self.user_list)
            user2 = random.choice(self.user_list)

            if user1 != user2:
                index1 = self.user_list.index(user1)
                index2 = self.user_list.index(user2)
                mod1 = math.floor(int(index1) / self.per_group_num)
                mod2 = math.floor(int(index2) / self.per_group_num)
                if mod1 == mod2:  # 如果在同组交易
                    if np.random.rand(1)[0] < self.super:  # 且满足一定比例
                        return user1, user2

                # 此处强制交易转移到下一各组别内，否则直接重新抽取
                # 由数字小的组转向大的组
                # return 的时候前一个是out 后一个in
                if (mod2 + 1) == mod1:
                    return user2, user1
                if (mod1 + 1) == mod2:
                    return user1, user2

                continue

    def trans_amount_generate(self):
        while True:
            amount = np.random.randint(1, self.trans_amount_limit)
            if amount > self.trans_amount_limit / 2:
                if np.random.rand(1)[0] < self.super:
                    return amount
            return amount

    def check_balance(self, out_account, amount):
        #余额检测
        if self.user_balance[out_account] < amount:
            return False  # 钱不够
        return True

    def trans_generate(self):
        count = 0
        trans_history = list()
        start_time = time.time()
        while count < self.total_sum:
            tmp_dict = dict()
            out_account, in_account = self.trans_user_generate()
            amount = self.trans_amount_generate()
            if self.check_balance(out_account, amount):
                continue # 跳过本次循环

            tmp_dict['in_account'] = in_account
            tmp_dict['out_account'] = out_account
            tmp_dict['amount'] = amount

            trans_history.append(tmp_dict)
            end_time = time.time()
            total_time = end_time - start_time
            count += 1
            print('{0} %, total_time : {1}'.format((count / self.total_sum), total_time))

        data = pd.DataFrame(trans_history)
        data.to_csv('test.csv')


if __name__ == '__main__':
    trans = trans_generate()
    trans.trans_generate()
