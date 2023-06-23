package com.example.wellinkapplication.ui.healthInfo

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.wellinkapplication.R
import kotlinx.android.synthetic.main.activity_detail_health_info.*

class DetailHealthInfoActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_detail_health_info)

        var title = intent.getStringExtra("title")
        var contents = intent.getStringExtra("contents")
        var date = intent.getStringExtra("date")
        detail_tv_title.text = title
        detail_tv_contents.text = contents
        detail_tv_date.text = date
    }
}