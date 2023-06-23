package com.example.wellinkapplication.ui.user

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import com.example.wellinkapplication.MenuActivity
import com.example.wellinkapplication.R
import com.example.wellinkapplication.retrofit.RetrofitManager
import com.example.wellinkapplication.utils.CompletionResponse
import com.example.wellinkapplication.utils.LoginedUserData
import com.shashank.sony.fancytoastlib.FancyToast
import kotlinx.android.synthetic.main.activity_user_info.*

class UserInfoActivity : AppCompatActivity(), View.OnClickListener{


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_user_info)

        userInfo_editText_name.setText(LoginedUserData.name)
        userInfo_editText_protector.setText(LoginedUserData.protector_id)
        userInfo_btn_protectorInquire.setOnClickListener(this)
        userInfo_btn_joinUser.setOnClickListener(this)


    }

    override fun onClick(v: View?) {
        when (v) {
            userInfo_btn_protectorInquire -> {
                if (userInfo_editText_protector.text.toString() == "") return
                RetrofitManager.instance.protectorInquireUser(
                    userInfo_editText_protector.text.toString(),
                    completion = { completionResponse, s ->
                        when (completionResponse) {
                            CompletionResponse.FAIL -> {
                                FancyToast.makeText(this, "등록되지 않은 보호자입니다.", FancyToast.LENGTH_SHORT, FancyToast.WARNING, true).show()
                                userInfo_editText_protector.setText("")
                            }
                            CompletionResponse.OK -> {
                                FancyToast.makeText(this, "회원 이름 : $s", FancyToast.LENGTH_SHORT, FancyToast.SUCCESS, true).show()
                            }
                        }
                    })
            }
            userInfo_btn_joinUser -> {
                if (checkBeforeJoin()) return
                RetrofitManager.instance.modifyInfoUser(LoginedUserData.uid, userInfo_editText_name.text.toString(), userInfo_editText_protector.text.toString(), completion = { completionResponse, s ->
                        when (completionResponse) {
                            CompletionResponse.FAIL -> {
                                FancyToast.makeText(this, "회원정보수정 실패", FancyToast.LENGTH_SHORT, FancyToast.WARNING, true).show()
                            }
                            CompletionResponse.OK -> {
                                val intent = Intent(this, MenuActivity::class.java)
                                startActivity(intent)
                            }
                        }
                    })
            }
        }
    }

    fun checkBeforeJoin():Boolean{
        if(userInfo_editText_name.text.toString() == "") {
            FancyToast.makeText(this, "성명을 입력해주세요", FancyToast.LENGTH_SHORT, FancyToast.WARNING,true) .show()
            return true
        }
        userInfo_btn_protectorInquire.performClick()
        return false
    }
}