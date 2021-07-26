// Insert if cookie is not in array
// WARNING
export function insert_warning_cookie(cookie){
    var warnings = JSON.parse(Cookies.get('warnings'));
    var val = true;

    for(var tmp of warnings){
        if(tmp == cookie){
            val = false;
            break;
        }
    }

    if(val == true){
        warnings.push(cookie);
        Cookies.set('warnings', JSON.stringify(warnings));
    }
}

export function delete_warning_cookie(cookie){
    var warnings = JSON.parse(Cookies.get('warnings'));
    for(var tmp of warnings){
        if(tmp.includes(cookie)){
            var index = warnings.indexOf(tmp);
            warnings.splice(index,1);
            Cookies.set('warnings', JSON.stringify(warnings));
            break;
        }
    }
}

// ERROR
export function insert_error_cookie(cookie){
    var errors = JSON.parse(Cookies.get('errors'));
    var val = true;

    for(var tmp of errors){
        if(tmp == cookie){
            val = false;
            break;
        }
    }

    if(val == true){
        errors.push(cookie);
        Cookies.set('errors', JSON.stringify(errors));
    }
}

// Delete cookie if is in array, get index and then delete!
export function delete_error_cookie(cookie){
    var errors = JSON.parse(Cookies.get('errors'));
    for(var tmp of errors){
        if(tmp.includes(cookie)){
            var index = errors.indexOf(tmp);
            errors.splice(index,1);
            Cookies.set('errors', JSON.stringify(errors));
            break;
        }
    }
}

