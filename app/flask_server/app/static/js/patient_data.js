import {allert} from './modules/infos.js';
import {delete_warning_cookie, insert_warning_cookie} from './modules/cookies.js';

$(function(){
    delete_warning_cookie("Patient")
    insert_warning_cookie("Patient " + $("#name.data").text() + " " + $("#surname.data").text() + " was initialized!");
    allert();
});