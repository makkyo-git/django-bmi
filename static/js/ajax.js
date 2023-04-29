// プロジェクトタスク追加Ajax
$(function () {
    $('#TaskAddAjax').click(function () {

        //必須事項チェック
        let taskName = $('input[name=taskName]').val();

        if (taskName != "") {

            var form = $('form[name=addTask]');
            $.ajax({
                url: form.prop("action"),
                method: form.prop("method"),
                data: form.serialize(),
                dataType: "JSON",
            })
 
                .done(function (data) {
                    var result = JSON.parse(data['taskdata'])

                    $('#taskAccordion').empty()

                    $.each(result, function (k, v) {
                        let taskData = v["fields"]

                        let taskHtml = '<li class="task' + taskData["priolity"] + '">' + taskData["task_name"] + '</li>'

                        $('#taskAccordion').append(taskHtml)
                    })
                })
      
        } else {
            alert('タスクを入力してください')
        }
    })
})

// タスク詳細取得Ajax
$(function () {
    $('.selectTask').click(function () {

        // タスクコードを取得
        let task_cd = this.value;

        if (task_cd != "") {

            $.ajax({
                url: "/task/ajax/getProjectTaskInfo",
                method: "POST",
                data: {task_cd : task_cd},
                dataType: "JSON",
           })
                .done(function (data) {
                    var result = JSON.parse(data['taskdata'])

                    $('#modal-task-details').empty()

                    $.each(result, function (k, v) {
                        let taskData = v["fields"]
                        let userName = ""
                        let details = ""
                        let period = ""

                        let taskHtml = ""
                        let formHtml = ""

                        if (taskData['user'] == "" || taskData['user'] == null) {
                            taskData['user'] = 0;
                        }

                        if (taskData['user_name'] != null) {
                            userName = taskData['user_name']
                        }

                        if (taskData['details'] != null) {
                            details = taskData['details'];
                        }

                        if (taskData['start_date'] != null) {
                            period += taskData['start_date']
                        }

                        if (period != "") {
                            period += " 〜 "
                        }

                        if (taskData['end_date'] != null) {
                            period += taskData['end_date']
                        }

                        taskHtml = "<h4>" + taskData['task_name'] + "</h4>"
                            +   "<table class='table'>"
                            +   "   <tr>"
                            +   "       <th>担当</th>"
                            +   "       <td>" + userName + "<span style='display:none'>" + taskData['user'] + "</span></td>"
                            +   "   </tr>"
                            +   "   <tr>"
                            +   "       <th>詳細</th>"
                            +   "       <td>" + details + "</td>"
                            +   "   </tr>"
                            +   "   <tr>"
                            +   "       <th>期間</th>"
                            +   "       <td>" + period + "</td>"
                            +   "   </tr>"
                            +   "</table>"
                        $('#modal-task-details').append(taskHtml)

                        formHtml = "<button type='button' id='CTDI' class='btn btn-primary' style='margin-right:10px;'>閉じる</button>"
                            +   "<button type='button' class='btn btn-primary' style='margin-right:10px;'>変更</button>"
                            +   "<button type='button' class='btn delete-btn'>削除</button>"
                        $('#modal-task-details').append(formHtml)
                    })

                    $('#TDI').click();
                })
            }
        })
    })
