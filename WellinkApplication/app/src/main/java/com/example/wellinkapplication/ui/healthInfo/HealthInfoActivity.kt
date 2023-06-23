package com.example.wellinkapplication.ui.healthInfo

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.wellinkapplication.R
import kotlinx.android.synthetic.main.activity_health_info.*
import org.json.JSONArray
import org.json.JSONObject

class HealthInfoActivity : AppCompatActivity() {

    private var titlesList = mutableListOf<String>()
    private var contentsList = mutableListOf<String>()
    private var datesList = mutableListOf<String>()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)


        setContentView(R.layout.activity_health_info)

        postToList()

        rv_recyclerView.layoutManager = LinearLayoutManager(this)
        rv_recyclerView.adapter = RecyclerAdapter(titlesList, contentsList, datesList)

    }

    private fun addToList(title:String, contents:String, date: String) {
        titlesList.add(title)
        contentsList.add(contents)
        datesList.add(date)
    }

    private fun postToList() {
        val jsonString = assets.open("data.json").reader().readText()
        val jsonArray = JSONArray(jsonString)

        for(i in 0 until jsonArray.length()) {
            val jsonObject = jsonArray.getJSONObject(i)
            val title = jsonObject.getString("title")
            val contents = jsonObject.getString("contents")
            val date = jsonObject.getString("date")
            addToList(title, contents, date)
        }
    }

}