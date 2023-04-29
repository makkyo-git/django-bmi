function one2two (num) {
   // 桁数が1桁だったら、先頭に0を加えて2桁に調整する
   var ret;
   if( num < 10 ) { ret = "0" + num; }
   else { ret = num; }
   return ret;
}

function showClock () {
   const nowTime = new Date();
   const nowYear = one2two( nowTime.getFullYear() );
   const nowMonth = one2two( nowTime.getMonth() + 1 );
   const nowDate = one2two( nowTime.getDate() );
   const dayOfweek  = nowTime.getDay();
   const dayname = ['日','月','火','水','木','金','土'];
   const nowDay = dayname[dayOfweek];
   const nowHour = one2two( nowTime.getHours() );
   const nowMin  = one2two( nowTime.getMinutes() );
   const nowSec  = one2two( nowTime.getSeconds() );
   const msg = "今は、" + nowYear + "年" + nowMonth + "月" + nowDate + "日" + '(' + nowDay + ')曜日' + nowHour + ":" + nowMin + ":" + nowSec + " です。<br>メシを食ったら、さっさと寝ましょう。</br>";
   document.getElementById("Clock").innerHTML = msg;
}
setInterval('showClock ()',1000);