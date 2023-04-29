// メンバー追加モーダル管理
$(function () { 
    //追加ボタンを押した際
    $('#AMB').click(function () {
        //背景を付ける
        $("body").append('<div id="modal-bg"></div>');

        //モーダルウインドウを表示
        $("#modal-bg,#modal-member").fadeIn("fast");

        //画面の背景もしくは戻るボタンを押したらモーダルを閉じる
        $('#modal-bg, #AMCB').click(function () {
            $("#modal-bg,#modal-member").fadeOut("fast", function () {
                $('#modal-bg').remove();
            });
        });
    });
});

// タスク追加モーダル管理
$(function () {
    //追加ボタンを押した際
    $('#CTB').click(function () {
        // 背景を付ける
        $("body").append('<div id="modal-bg"></div>');

        //モーダルウィンドウを表示
        $("#modal-bg,#modal-task-add").fadeIn("fast");

        //画面の背景もしくは戻るボタンを押したらモーダルを閉じる
        $('#modal-bg, #CTBC').click(function () {
            $("#modal-bg,#modal-task-add").fadeOut("fast", function () {
                $('#modal-bg').remove();
            });
        });
    });
});

// タスク詳細モーダル管理
$(function () {
    // 追加ボタンを押した際
    $('#TDI').click(function () {
        //背景を付ける
        $("body").append('<div id="modal-bg"></div>');

        //モーダルウィンドウを表示
        $("#modal-bg,#modal-task-details").fadeIn("fast");

        //画面の背景もしくは戻るボタンを押したらモーダルを閉じる
        $('#modal-bg, #CTDI').click(function () {
            $("#modal-bg,#modal-task-details").fadeOut("fast", function () {
                $('#modal-bg').remove();
            });
        });
    });
});
