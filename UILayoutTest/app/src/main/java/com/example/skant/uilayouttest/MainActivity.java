package com.example.skant.uilayouttest;

import android.graphics.drawable.Drawable;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{
    private ImageView imageView;
   // private Drawable image;
    private Button imageButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.layout_main);
        ActionBar actionbar = getSupportActionBar();
        if (actionbar != null){
            actionbar.hide();
        }
        imageView = (ImageView) findViewById(R.id.image_view);
       // int resID = getResources().getIdentifier("back1.png", "drawable", "com.example.skant.uilayouttest");
        //image = getResources().getDrawable(resID);
        imageButton = (Button) findViewById(R.id.title_back);
        imageButton.setOnClickListener(this);

    }

    private Boolean flag = true;
    @Override
    public void onClick(View v){
        switch (v.getId()){
            case R.id.title_back:
                //String inputText = editText.getText().toString();
                //Toast.makeText(MainActivity.this,inputText,Toast.LENGTH_SHORT).show();
                if(flag) {
                    imageView.setImageResource(R.drawable.book);
                    //imageButton.setBackground(image);
                    flag = false;
                }
                else {
                    imageView.setImageResource(R.drawable.zhaoanqi);
                    flag = true;
                }
                break;
            default:
                break;
        }
    }
}
