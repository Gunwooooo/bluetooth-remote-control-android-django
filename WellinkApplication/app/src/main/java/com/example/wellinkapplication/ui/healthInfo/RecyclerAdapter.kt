package com.example.wellinkapplication.ui.healthInfo

import android.content.Intent
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.RecyclerView
import com.example.wellinkapplication.R
import com.example.wellinkapplication.ui.user.UserLoginActivity
import kotlinx.android.synthetic.main.item_layout.view.*

class RecyclerAdapter(private var titles: List<String>, private var contents: List<String>, private var dates: List<String>): RecyclerView.Adapter<RecyclerAdapter.ViewHolder>(){
    inner class ViewHolder(itemView: View): RecyclerView.ViewHolder(itemView) {
        val itemTitle: TextView = itemView.findViewById(R.id.tv_title)
        val itemContents: TextView = itemView.findViewById(R.id.tv_contents)
        val itemDate: TextView = itemView.findViewById(R.id.tv_date)
        init {
            itemView.setOnClickListener{ v:View ->
                val position: Int = adapterPosition
                Log.d("태그", "${contents[position]}")
                val intent = Intent(itemView.context, DetailHealthInfoActivity::class.java)
                intent.putExtra("title", "${titles[position]}")
                intent.putExtra("contents", "${contents[position]}")
                intent.putExtra("date", "${dates[position]}")
                itemView.context.startActivity(intent)
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val v = LayoutInflater.from(parent.context).inflate(R.layout.item_layout, parent, false)
        return ViewHolder(v)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.itemTitle.text=titles[position]
        var contentsTmp: String = contents[position]
        contentsTmp = contentsTmp.replace("\n", "")
        if(contentsTmp.length > 35 ) {
            contentsTmp = contentsTmp.substring(0, 35) + "..."
        }
        holder.itemContents.text=contentsTmp
        holder.itemDate.text=dates[position]
    }

    override fun getItemCount(): Int {
        return titles.size
    }
}