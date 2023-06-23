package com.example.wellinkapplication.ui.user

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.wellinkapplication.R
import com.example.wellinkapplication.retrofit.RetrofitManager
import com.example.wellinkapplication.retrofit.User
import com.example.wellinkapplication.utils.CompletionResponse
import com.example.wellinkapplication.utils.Constants.TAG
import com.shashank.sony.fancytoastlib.FancyToast
import kotlinx.android.synthetic.main.activity_menu.*
import kotlinx.android.synthetic.main.activity_user_join.*

class UserJoinActivity : AppCompatActivity(), View.OnClickListener {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_user_join)



        //로그인 된 상태일 때

        var protectorCheck:Int = intent.extras!!.getInt("protectorCheck")
        if(protectorCheck == 1) {
            userJoin_layout_inputProtector.visibility = View.GONE
        } else {
            userJoin_layout_inputProtector.visibility = View.VISIBLE
        }
        userJoin_btn_joinUser.setOnClickListener(this)
        userJoin_btn_duplicateCheck.setOnClickListener(this)
        userJoin_btn_protectorInquire.setOnClickListener(this)



    }

    override fun onClick(v: View?) {
        when(v) {
            userJoin_btn_protectorInquire -> {
                if(userJoin_editText_protector.text.toString() == "") return
                RetrofitManager.instance.protectorInquireUser(userJoin_editText_protector.text.toString(), completion =  {
                        completionResponse, s ->
                    when(completionResponse){
                        CompletionResponse.FAIL -> {
                            FancyToast.makeText(this, "등록되지 않은 보호자입니다.", FancyToast.LENGTH_SHORT, FancyToast.WARNING,true).show()
                            userJoin_editText_protector.setText("")
                        }
                        CompletionResponse.OK -> {
                            FancyToast.makeText(this, "회원 이름 : ${s}", FancyToast.LENGTH_SHORT, FancyToast.SUCCESS,true).show()
                        }
                    }

                })
            }
            userJoin_btn_duplicateCheck -> {
                RetrofitManager.instance.duplicateCheckUser(userJoin_editText_uid.text.toString(), completion = {
                        completionResponse, s ->
                    when(completionResponse) {
                        CompletionResponse.OK -> {
                            if(s == "true") {
                                FancyToast.makeText(this, "사용이 가능한 아이디입니다.", FancyToast.LENGTH_SHORT, FancyToast.SUCCESS,true).show()
                            } else{
                                FancyToast.makeText(this, "중복된 아이디입니다.", FancyToast.LENGTH_SHORT, FancyToast.WARNING,true).show()
                            }
                        }
                        CompletionResponse.FAIL -> {
                            Log.d(TAG, "아이디 중복 체크 오류 $s")
                        }
                    }
                })
            }

            userJoin_btn_joinUser -> {
                var protect_check = false
                if(intent.extras!!.getInt("protectorCheck") == 1) {
                    protect_check = true
                }
                if(checkBeforeJoin()) return
                RetrofitManager.instance.joinUser(User(userJoin_editText_uid.text.toString(), userJoin_editText_password.text.toString(),
                    userJoin_editText_name.text.toString(), protect_check, userJoin_editText_protector.text.toString()), completion = {
                        completionResponse, _ ->
                    when(completionResponse){
                        CompletionResponse.FAIL -> {
                            Log.d("태그", "회원가입 실패")
                            FancyToast.makeText(this, "회원가입 실패", FancyToast.LENGTH_LONG, FancyToast.WARNING,true).show()
                        }
                        CompletionResponse.OK -> {
                            Log.d("태그", "회원가입 성공")
                            val intent = Intent(this, UserJoinCompleteActivity::class.java)
                            startActivity(intent)
                        }
                    }
                })
            }
        }
    }

    //회원가입 체크 fun
    fun checkBeforeJoin():Boolean{
        if(userJoin_editText_uid.text.toString() == "") {
            FancyToast.makeText(this, "아이디를 입력해주세요", FancyToast.LENGTH_SHORT, FancyToast.WARNING,true) .show()
            return true
        }
        if(userJoin_editText_password.text.toString() == "" || userJoin_editText_password_check.text.toString() == "") {
            FancyToast.makeText(this, "비밀번호를 입력해주세요", FancyToast.LENGTH_SHORT, FancyToast.WARNING,true) .show()
            return true
        }
        if(userJoin_editText_password.text.toString() != userJoin_editText_password_check.text.toString()) {
            FancyToast.makeText(this, "비밀번호가 일치하지 않습니다", FancyToast.LENGTH_SHORT, FancyToast.WARNING,true) .show()
            return true
        }
        if(userJoin_editText_name.text.toString() == "") {
            FancyToast.makeText(this, "성명을 입력해주세요", FancyToast.LENGTH_SHORT, FancyToast.WARNING,true) .show()
            return true
        }
        userJoin_btn_protectorInquire.performClick()
        return false
    }
}