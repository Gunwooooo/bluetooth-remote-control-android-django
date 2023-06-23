package com.example.wellinkapplication.utils


object Constants {
    const val TAG = "로그"
}

object LoginedUserData {
    var token:String = ""
    var uid:String = ""
    var name:String = ""
    var protector_check:Boolean = false
    var protector_id:String = ""
}

enum class CompletionResponse {
    OK,
    FAIL
}

object API {
    const val BASE_URL = "http://192.168.1.42:8000/"
    //////////////////////////////////////////////////////////////
    const val JOIN_USER = "account/join/"
    const val LOGIN_USER = "account/login/"
    const val INFO_USER = "account/info/"
    const val DUPLICATE_CHECK_USER = "account/duplicateCheck/"
    const val PROTECTOR_INQUIRE_USER = "account/protectorInquire/"
    const val MODIFY_INFO_USER = "account/modifyInfo/"
    ///////////////////////////////////////////////////////////////
    const val LOCAL_HOSPITAL = "local/hospital/"
    const val LOCAL_PHARMACY = "local/pharmacy/"
    //////////////////////////////////////////////////////////////
    const val MODIFY_INFO_ALARM = "alarm/modifyInfo/"
    const val INFO_ALARM = "alarm/info/"
    const val MODIFY_INFO_CALENDAR = "rawcalendar/modifyInfo/"
    const val INFO_CALENDAR = "rawcalendar/info/"
}