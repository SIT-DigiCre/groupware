/*
* 共通JSファイル
*/
function bbsStampOnClick(btn,target_id=0,kind = 'message'){
    
    stamp_name = btn.id.replace('btn_','');
    
    url = kind+'_stamp/'+String(target_id)+'/'+stamp_name;
    alert(url);
    $('#'+String(target_id)+'_stamps').load(url);
}