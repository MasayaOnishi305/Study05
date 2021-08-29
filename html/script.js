//var order_menu = order_menu.value;
var order_menu = document.getElementById('order_menu');
//var quantity　= quantity.value;
var quantity　= document.getElementById('quantity');
var confirm = document.getElementById('confirm');
var log = document.getElementById('log');
var total = document.getElementById('total');
var next = document.getElementById('next');
var storage = sessionStorage;

confirm.addEventListener('click', () => {
    //必須チェック
    if(quantity.value == ""){
        window . alert('必須項目を入力してください' );
    }
    else{
        //ログの取得
        async function run() {
            let add_value = await eel.add_order_item(order_menu.value,quantity.value)();
        }
        run();
        
    }
});

check_out.addEventListener("click", () => {
    if (payment.value == ""){
        alert("お支払い金額が入力されていません");
        return false;
    }
    eel.checkout_order(payment.value);
})

eel.expose(view_order_items)
function view_order_items(text) {
    log.value = text;
}

eel.expose(alertJs)
function alertJs(text){
    alert(text)
}

// eel.expose(view_log_js)
// function view_log_js(text){
//     var inputVal = text[0]+'\n';
//     log.value = (log.value+inputVal);
//     total.value = text[1];
//     storage.setItem('total_price',text[1]);
//     window . alert(storage.getItem('total_price'));
// }
//画面遷移処理
// function link(target) {
//     window.location.href=target;
// }
