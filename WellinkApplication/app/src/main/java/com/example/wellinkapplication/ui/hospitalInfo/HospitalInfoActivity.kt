package com.example.wellinkapplication.ui.hospitalInfo

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Color
import android.location.Location
import android.location.LocationManager
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.afollestad.materialdialogs.MaterialDialog
import com.example.wellinkapplication.R
import com.example.wellinkapplication.retrofit.RetrofitManager
import com.example.wellinkapplication.utils.CompletionResponse
import com.shashank.sony.fancytoastlib.FancyToast
import kotlinx.android.synthetic.main.activity_hospital_info.*
import net.daum.mf.map.api.*

import android.content.Intent
import android.provider.Settings


class HospitalInfoActivity : AppCompatActivity(), View.OnClickListener {
    lateinit var mapView: MapView
    lateinit var mapViewContainer: ViewGroup
    var initLng: Double = .0
    var initLat: Double = .0
    val PERMISSIONS_REQUEST_CODE = 100
    var REQUIRED_PERMISSIONS = arrayOf<String>( Manifest.permission.ACCESS_FINE_LOCATION)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hospital_info)

        initMapView()

    }

    override fun onClick(v: View?) {
        when(v){
            fab_current -> {
                FancyToast.makeText(this, "현재 위치로 이동", FancyToast.LENGTH_SHORT, FancyToast.INFO, false).show()
                mapView.setMapCenterPoint(MapPoint.mapPointWithGeoCoord(initLat, initLng), true)
                mapView.setCurrentLocationTrackingMode(MapView.CurrentLocationTrackingMode.TrackingModeOnWithoutHeading)
                mapView.setZoomLevel(4, true)
                getCurrentLocation()
            }
            fab_pharmacy -> {
                FancyToast.makeText(this, "현재위치기준 " +
                        "반경 2km 약국 검색", FancyToast.LENGTH_SHORT, FancyToast.SUCCESS, false).show()
                val mCurrentLat = mapView.mapCenterPoint.mapPointGeoCoord.latitude  //y
                val mCurrentLng = mapView.mapCenterPoint.mapPointGeoCoord.longitude //x
                clearMapView(mCurrentLat, mCurrentLng)
                //데이터 가져오기
                RetrofitManager.instance.localPharmacy(mCurrentLng, mCurrentLat, completion = {
                        completionResponse, s ->
                    when(completionResponse){
                        CompletionResponse.FAIL -> {
                        }
                        CompletionResponse.OK -> {
                            val list = s.asJsonObject["lists"].asJsonArray
                            for(i in 0 until list.size()) {
                                val jsonObject = list.get(i).asJsonObject
                                val marker = MapPOIItem()
                                marker.apply {
                                    itemName = "${jsonObject.get("pname")}"
                                    mapPoint = MapPoint.mapPointWithGeoCoord(jsonObject.get("plat").asDouble, jsonObject.get("plng").asDouble)
                                    markerType = MapPOIItem.MarkerType.CustomImage
                                    customImageResourceId = R.drawable.pharmacy_marker1
                                    selectedMarkerType = MapPOIItem.MarkerType.CustomImage
                                    customSelectedImageResourceId = R.drawable.pharmacy_marker2
                                    isCustomImageAutoscale = true
                                }
                                marker.userObject = LocalData(jsonObject.get("pcode").asString, jsonObject.get("ppost").asString, jsonObject.get("paddress").asString, jsonObject.get("pphone").asString
                                    , jsonObject.get("purl").asString, jsonObject.get("plng").asDouble, jsonObject.get("plat").asDouble)
                                mapView.addPOIItem(marker)
                            }
                        }
                    }
                })
            }
            fab_hospital -> {
                FancyToast.makeText(this, "현재위치기준 " +
                        "반경 2km 병원 검색", FancyToast.LENGTH_SHORT, FancyToast.SUCCESS, false).show()
                val mCurrentLat = mapView.mapCenterPoint.mapPointGeoCoord.latitude  //y
                val mCurrentLng = mapView.mapCenterPoint.mapPointGeoCoord.longitude //x
                clearMapView(mCurrentLat, mCurrentLng)
                //데이터 가져오기
                RetrofitManager.instance.localHospital(mCurrentLng, mCurrentLat, completion = {
                        completionResponse, s ->
                    when(completionResponse){
                        CompletionResponse.FAIL -> {
                        }
                        CompletionResponse.OK -> {
                            val list = s.asJsonObject["lists"].asJsonArray
                            for(i in 0 until list.size()) {
                                val jsonObject = list.get(i).asJsonObject
                                val marker = MapPOIItem()

                                marker.apply {
                                    itemName = "${jsonObject.get("hname")}"
                                    mapPoint = MapPoint.mapPointWithGeoCoord(jsonObject.get("hlat").asDouble, jsonObject.get("hlng").asDouble)
                                    markerType = MapPOIItem.MarkerType.CustomImage
                                    customImageResourceId = R.drawable.hospital_marker1
                                    selectedMarkerType = MapPOIItem.MarkerType.CustomImage
                                    customSelectedImageResourceId = R.drawable.hospital_marker2
                                    isCustomImageAutoscale = true
                                }
                                marker.userObject = LocalData(jsonObject.get("hcode").asString, jsonObject.get("hpost").asString, jsonObject.get("haddress").asString, jsonObject.get("hphone").asString
                                    , jsonObject.get("hurl").asString, jsonObject.get("hlng").asDouble, jsonObject.get("hlat").asDouble)
                                mapView.addPOIItem(marker)
                            }
                        }
                    }
                })
            }
        }
    }
    private fun initMapView() {
        fab_hospital.setOnClickListener(this)
        fab_pharmacy.setOnClickListener(this)
        fab_current.setOnClickListener(this)
        mapView = MapView(this)
        mapView.setCalloutBalloonAdapter(CustomBalloonAdapter(layoutInflater))  // 커스텀 말풍선 등록
        mapViewContainer = findViewById<View>(R.id.map_view) as ViewGroup
        mapViewContainer.addView(mapView)
        mapView.setZoomLevel(4, true)
        mapView.currentLocationTrackingMode = MapView.CurrentLocationTrackingMode.TrackingModeOnWithoutHeading
        getCurrentLocation()
    }
    private fun clearMapView(mCurrentLat:Double, mCurrentLng:Double) {
        mapView.currentLocationTrackingMode = MapView.CurrentLocationTrackingMode.TrackingModeOff
        //원 표시
        mapView.removeAllPOIItems()
        mapView.removeAllCircles();
        val circle = MapCircle(
            MapPoint.mapPointWithGeoCoord(mCurrentLat, mCurrentLng),  // center
            2000,  // radius
            Color.argb(70, 255, 0, 0),  // strokeColor
            Color.argb(70, 0, 255, 0) // fillColor
        )
        circle.tag = 5678
        mapView.addCircle(circle)
    }
    private fun getCurrentLocation() {
        val permissionCheck = ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
        if(permissionCheck == PackageManager.PERMISSION_GRANTED) {

            //GPS 켜져있는지 확인
            val lm = applicationContext.getSystemService(LOCATION_SERVICE) as LocationManager
            val bRet = lm.isProviderEnabled(LocationManager.GPS_PROVIDER)
            if(!bRet) {
                val dialog = MaterialDialog(this, MaterialDialog.DEFAULT_BEHAVIOR)
                dialog.title(null, "알림")
                dialog.message(null, "위치 정보 사용 옵션이 꺼져있습니다.\n정확하고 편리한 탐색을 위해 위치 정보 사용 옵션을 켜주세요.", null)
                dialog.positiveButton(null, "설정") {
                    startActivity(Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS))
                }
                dialog.negativeButton(null, "뒤로가기") {
                    mapView.setZoomLevel(4, true)
                }
                dialog.show()
            }
            
            //GPS를 통해 현재 위치 좌표 가져오기
            val providers: List<String> = lm.getProviders(true)
            var bestLocation: Location? = null
            try {
                for(i in providers) {
                    val l: Location =
                        lm.getLastKnownLocation(i) ?: continue
                    if (bestLocation == null || l.accuracy < bestLocation.getAccuracy()) {
                        // Found best last known location: %s", l);
                        bestLocation = l
                    }
                }
                initLat = bestLocation!!.latitude  //y
                initLng = bestLocation.longitude //x
            }catch(e: NullPointerException){
                Log.e("LOCATION_ERROR", e.toString())
//                ActivityCompat.finishAffinity(this)
            }


        }else{
            Toast.makeText(this, "위치 권한이 없습니다.", Toast.LENGTH_SHORT).show()
            ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, PERMISSIONS_REQUEST_CODE )
        }
    }
    class CustomBalloonAdapter(inflater: LayoutInflater): CalloutBalloonAdapter {
        val mCalloutBalloon: View = inflater.inflate(R.layout.balloon_layout, null)
        val name: TextView = mCalloutBalloon.findViewById(R.id.ball_name)
        val code: TextView = mCalloutBalloon.findViewById(R.id.ball_code)
        val post: TextView = mCalloutBalloon.findViewById(R.id.ball_post)
        val address: TextView = mCalloutBalloon.findViewById(R.id.ball_address)
        val url: TextView = mCalloutBalloon.findViewById(R.id.ball_url)
        val lng: TextView = mCalloutBalloon.findViewById(R.id.ball_lng)
        val lat: TextView = mCalloutBalloon.findViewById(R.id.ball_lat)

        override fun getCalloutBalloon(poiItem: MapPOIItem?): View {
            // 마커 클릭 시 나오는 말풍선
            val localData: LocalData = poiItem?.userObject as LocalData
            name.text = poiItem.itemName   // 해당 마커의 정보 이용 가능
            code.text = localData.code
            post.text = localData.post
            address.text = localData.address
            url.text = localData.url
            lng.text = localData.lng.toString()
            lat.text = localData.lat.toString()
            return mCalloutBalloon
        }

        override fun getPressedCalloutBalloon(poiItem: MapPOIItem?): View {
            // 말풍선 클릭 시
            return mCalloutBalloon
        }
    }
}

data class LocalData(var code:String, var post:String, var address:String, var phone:String, var url:String, var lng:Double, var lat:Double)