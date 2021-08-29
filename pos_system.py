import pandas as pd
import sys
import datetime

RECEIPT_FOLDER="./receipt"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master
        self.set_datetime()
    
    def set_datetime(self):
        self.datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    def add_item_order(self,item_code,item_count):
        if self.get_item_data(item_code):
            self.item_order_list.append(item_code)
            self.item_count_list.append(item_count)
            return True
        else:
            return False
        
    # def view_item_list(self):
    #     self.total=0
    #     self.receipt_name="receipt_{}.log".format(self.datetime)
    #     for item_order,item_count in zip(self.item_order_list,self.item_count_list):
    #         self.write_receipt("商品コード:{}".format(item_order))
    #         item_detail =self.get_item_data(item_order)
    #         name = item_detail[0]
    #         price = item_detail[1]
    #         sub_total = int(price)*int(item_count)
    #         self.write_receipt("商品名:{}".format(name))
    #         self.write_receipt("金額:{}".format(price))
    #         self.write_receipt("単価：{0},個数：{1},小計：{2}".format(price,item_count,sub_total))
    #         self.total += sub_total
    #     self.write_receipt("合計：{}".format(self.total))

    def get_item_data(self,item_code):
        for m in self.item_master:
            if item_code==m.item_code:
                return m.item_name,m.price

    def get_order_items(self):
        '''
        オーダーの全情報をテキストをして取得する
        '''
        res =""
        total_price=0
        total_count=0
        for item_order_code,item_count in zip(self.item_order_list,self.item_count_list):
            for item in self.item_master:
                if item.item_code == item_order_code:
                    res += f"{item_order_code} {item.item_name} | ￥{item.price}円 × {item_count} 個\n"
                    total_price += item.price * item_count
                    total_count += item_count
                    break   
        res += "---------------------------------------------\n"
        res += f"合計: ￥{total_price}円 | {total_count}個\n"

        return res
        
    
    #オーダー入力
    # def input_order(self):
    #     print("いらっしゃいませ！")
    #     while True:
    #         buy_item_code = input("購入したい商品を入力してください。登録を完了する場合は、0を入力してください >>> ")
    #         if int(buy_item_code) != 0:
    #             item_count = input("個数を入力してください >>> ")
    #             self.add_item_order(buy_item_code,item_count)
    #         else:
    #             print("商品登録を終了します。")
    #             break    

    # #会計処理
    # def calc(self,money):
    #     if len(self.item_order_list)>=1:
    #         while True:
    #             self.money=int(money)
    #             self.change_money= self.money-total_price
    #             if self.change_money>=0:
    #                 self.write_receipt("お預かり金額：{}".format(self.money))
    #                 self.write_receipt("お釣り：￥{:,}".format(self.change_money))
    #                 break
    #             else:
    #                  print("￥{:,}　不足しています。再度入力してください".format(self.change_money))
            
    #         print("お買い上げありがとうございました！")
    
    # 会計処理
    def checkout(self, money):
        '''
        会計処理しお釣りの金額を返す
        '''
        change_money=int(money)-self.calc_sum_item_price()
        
        return change_money

    #合計算出
    def calc_sum_item_price(self):
        total_price=0
        for item_order_code,item_count in zip(self.item_order_list,self.item_count_list):
            for item in self.item_master:
                if item.item_code == item_order_code:
                    total_price += item.price * item_count
                    break

        return total_price

    #レシート出力処理
    def write_receipt(self,text):
        print(text)
        with open(RECEIPT_FOLDER + "\\" + self.receipt_name,mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n") 
    
    def export_receipt(self,deposit_money:int,change_money:int):
        self.total=0
        self.receipt_name="receipt_{}.log".format(self.datetime)
        for item_order,item_count in zip(self.item_order_list,self.item_count_list):
            self.write_receipt("商品コード:{}".format(item_order))
            item_detail =self.get_item_data(item_order)
            name = item_detail[0]
            price = item_detail[1]
            sub_total = int(price)*int(item_count)
            self.write_receipt("商品名:{}".format(name))
            self.write_receipt("金額:{}".format(price))
            self.write_receipt("単価：{0},個数：{1},小計：{2}".format(price,item_count,sub_total))
            self.total += sub_total

         # 合計金額、個数の表示
        self.write_receipt("-----------------------------------------------")
        self.write_receipt(f"合計金額:￥{self.total:,} ")
        self.write_receipt(f"お預かり金額:￥{deposit_money:,}")
        self.write_receipt(f"お返し:￥{change_money:,}")


def add_item_master_by_csv(csv_path):
    print("------- マスタ登録開始 ---------")
    item_master=[]
    count=0
    try:
        item_master_df=pd.read_csv(csv_path,dtype={"item_code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
        for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
            item_master.append(Item(item_code,item_name,price))
            print("{}({})".format(item_name,item_code))
            count+=1
        print("{}品の登録を完了しました。".format(count))
        print("------- マスタ登録完了 ---------")
        return item_master
    except:
        print("マスタ登録が失敗しました")
        print("------- マスタ登録完了 ---------")
        sys.exit()

class PosSystem:
    def __init__(self,csv_path:str=None):
        self.item_master = []
        self.csv_path = csv_path
        self.order = None
    
    def add_item_master(self):
        print("------- マスタ登録開始 ---------")
        count=0
        try:
            item_master_df=pd.read_csv(self.csv_path,dtype={"item_code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
            for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
                self.item_master.append(Item(item_code,item_name,price))
                print("{}({})".format(item_name,item_code))
                count+=1
            print("{}品の登録を完了しました。".format(count))
            print("------- マスタ登録完了 ---------")
            return True
        except:
            print("マスタ登録が失敗しました")
            print("------- マスタ登録完了 ---------")
            return False

    def init_order(self):
        '''
        オーダーを初期化する
        '''
        self.order = Order(self.item_master)
        


# ### メイン処理
# def main():
#     # マスタ登録
#     item_master=add_item_master_by_csv(ITEM_MASTER_CSV_PATH)
    
#     # オーダー登録
#     order=Order(item_master)
#     order.input_order()
    
#     # オーダー表示
#     order.view_item_list()

#     #会計処理
#     order.calc()

# if __name__ == "__main__":
#     main()