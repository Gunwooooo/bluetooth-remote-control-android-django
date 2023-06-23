package com.example.wellinkapplication

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.KeyEvent
import android.view.View
import android.widget.AdapterView
import androidx.appcompat.app.AppCompatActivity
import com.afollestad.materialdialogs.MaterialDialog
import com.example.wellinkapplication.retrofit.RetrofitManager
import com.example.wellinkapplication.ui.CalendarInfo.CalendarActivity
import com.example.wellinkapplication.ui.alarmInfo.AlarmActivity
import com.example.wellinkapplication.ui.healthInfo.HealthInfoActivity
import com.example.wellinkapplication.ui.hospitalInfo.HospitalInfoActivity
import com.example.wellinkapplication.ui.user.UserInfoActivity
import com.example.wellinkapplication.ui.user.UserLoginActivity
import com.example.wellinkapplication.utils.CompletionResponse
import com.example.wellinkapplication.utils.Loading.Companion.loading
import com.example.wellinkapplication.utils.LoginedUserData
import kotlinx.android.synthetic.main.activity_menu.*


class MenuActivity : AppCompatActivity(), View.OnClickListener {
    private val TAG = "태그"

    @SuppressLint("ResourceType", "SetTextI18n")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_menu)

        //로그인 상태 확인
        RetrofitManager.instance.infoUser(completion = {
                completionResponse, s ->
            when(completionResponse) {
                CompletionResponse.FAIL -> {
                    Log.d(TAG, "onCreate: $s")
                    menu_layout_loginedLayout.visibility = View.GONE
                    menu_textView_intro.visibility = View.VISIBLE
                    menu_textView_intro_2.visibility = View.GONE
                    menu_layout_notloginedLayout.visibility = View.VISIBLE
                }
                CompletionResponse.OK -> {
                    Log.d(TAG, "onCreate: $s")
                    menu_layout_loginedLayout.visibility = View.VISIBLE
                    menu_textView_intro.visibility = View.GONE
                    menu_textView_intro_2.visibility = View.VISIBLE
                    menu_layout_notloginedLayout.visibility = View.GONE
                    menu_textView_welcome.text = "${LoginedUserData.name}님,\n환영합니다."
                }
            }
        })


        btn_hospitalInfo.setOnClickListener(this)
        btn_healthInfo.setOnClickListener(this)

        menu_btn_alarm.setOnClickListener(this)
        menu_btn_calendar.setOnClickListener(this)
        menu_btn_loginUser.setOnClickListener(this)
        menu_btn_loginProtector.setOnClickListener(this)

        //스피너 클릭 리스너 설정
        menu_spinner_userMenu.onItemSelectedListener = object: AdapterView.OnItemSelectedListener {
            override fun onItemSelected(p0: AdapterView<*>?, view: View?, position: Int, id: Long) {
                when (menu_spinner_userMenu.getItemAtPosition(position)) {
                    "내 정보" -> {
                        val intent = Intent(view?.context, UserInfoActivity::class.java)
                        startActivity(intent)
                    }
                    "로그아웃" -> {
                        LoginedUserData.token = ""
                        LoginedUserData.uid = ""
                        LoginedUserData.name = ""
                        LoginedUserData.protector_check = false
                        LoginedUserData.protector_id = ""
                        val intent = Intent(view?.context, MenuActivity::class.java)
                        startActivity(intent)
                    }
                }
            }
            override fun onNothingSelected(p0: AdapterView<*>?) {
            }
        }


    }

    override fun onClick(v: View?) {
        when(v){
            btn_hospitalInfo -> {
                val intent = Intent(this, HospitalInfoActivity::class.java)
                startActivity(intent)
            }
            btn_healthInfo -> {
                val intent = Intent(this, HealthInfoActivity::class.java)
                startActivity(intent)
            }
            menu_btn_alarm -> {
                val intent = Intent(this, AlarmActivity::class.java)
                startActivity(intent)
            }
            menu_btn_calendar -> {
                loading(this)
                val intent = Intent(this, CalendarActivity::class.java)
                startActivity(intent)
            }
            menu_btn_loginUser -> {
                val intent = Intent(this, UserLoginActivity::class.java)
                intent.putExtra("protectorCheck", 0)
                startActivity(intent)
            }
            menu_btn_loginProtector -> {
                val intent = Intent(this, UserLoginActivity::class.java)
                intent.putExtra("protectorCheck", 1)
                startActivity(intent)
            }
        }
    }

    //종료 메세지 다이어로그
    @Override
    override fun onKeyDown(keyCode:Int, event: KeyEvent): Boolean {
        return when (keyCode) {
            KeyEvent.KEYCODE_BACK -> {
                val dialog = MaterialDialog(this, MaterialDialog.DEFAULT_BEHAVIOR)
                dialog.title(null, "알림")
                dialog.message(null, "어플리케이션을 종료하시겠습니까?", null)
                dialog.positiveButton(null, "예") {
                    finishAffinity()
                }
                dialog.negativeButton(null, "아니요") {}
                dialog.show()
                false
            }
            else -> false
        }
    }
}