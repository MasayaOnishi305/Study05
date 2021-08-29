from os import system
import eel
import desktop
from pos_system import PosSystem

app_name="html"
end_point="index.html"
size=(700,700)

ITEM_MASTER_CSV_PATH="./item-master.csv"

@ eel.expose
#index.html オーダー履歴表示処理
def add_order_item(item_code:str,item_count:int):
    '''
    オーダーに商品を追加する
    '''
    global system
    
    # Orderが存在しなければOrderインスタンスを作成
    if system.order == None:
        system.init_order()
    res = system.order.add_item_order(item_code,int(item_count))
    if not res:
        eel.alertJs(f"『{item_code}』は商品マスターに登録されていません")
    else:
        res_text = system.order.get_order_items()
        eel.view_order_items(res_text)

@eel.expose
def checkout_order(money: str):
    '''
    会計処理
    '''
    global system
    change_money = system.order.checkout(int(money))
    if change_money < 0:
        message = f"金額が {-change_money}円 不足しています。"
    else:
        message = f"{change_money}円のお返しです。\nお買い上げありがとうございました。"
        system.order.export_receipt(deposit_money=int(money), change_money=change_money)
        system.init_order()
    eel.alertJs(message)

def pos_system_start():
    '''
    POSシステムの初期化処理
    '''
    global system # グローバル変数を使用する場合の宣言
    
    # POSシステムに商品マスタを登録
    # マスタ登録
    system = PosSystem(ITEM_MASTER_CSV_PATH)
    system.add_item_master() # CSVからマスタへ登録


if __name__ == "__main__":
    pos_system_start()
    desktop.start(app_name,end_point,size)