package com.example.wellinkapplication.ui.user

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import com.example.wellinkapplication.MenuActivity
import com.example.wellinkapplication.R
import kotlinx.android.synthetic.main.activity_user_join_complete.*

class UserJoinCompleteActivity : AppCompatActivity(), View.OnClickListener {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_user_join_complete)
        userJoinComplete_btn_ok.setOnClickListener(this)
    }

    override fun onClick(v: View?) {
        when(v) {
            userJoinComplete_btn_ok -> {
                val intent = Intent(this, MenuActivity::class.java)
                startActivity(intent)
            }
        }
    }
}