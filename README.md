[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# oF_OSC_ReceiverSample 

### Python OSC Sender Sample
`sandbox/sender_sample.py`でX,Y,Z,Interactionの値を送信できるテストができます。
`config.py`にてportは`8008`に、ipは`127.0.0.1`に設定されてる。

```bash
HirokiNaganuma:oF_OSC_ReceiverSample hirokinaganuma$ python python_sender_sample/sender_sample.py 
[Sender] sender_ip:127.0.0.1, sender_port:8008, address:/data
type X:
44
type Y:
22
type Z:
11
type interaction:
24124
type X:
^CExit with Ctrl+C / sys.exit(0) 
```

### oF Receiver Sample
oF projectでは`src/manager/MacroManager.hpp`にて`osc_port_num = 8008`が設定されている。
上記の`sandbox/sender_sample.py`を行った時、oFでは下記のようなlogが取れる

```log
listening for osc messages on port 8008
2018-03-10 15:52:46.987432+0900 oF_OSC_ReceiverSampleDebug[42391:3043864] MessageTracer: load_domain_whitelist_search_tree:73: Search tree file's format version number (0) is not supported
2018-03-10 15:52:46.987473+0900 oF_OSC_ReceiverSampleDebug[42391:3043864] MessageTracer: Falling back to default whitelist
[notice ] [2018] heart rate :44
[notice ] [2018] heart rate :22
[notice ] [2018] heart rate :11
[notice ] [2018] heart rate :24124
```

`model/Model.hpp`の

```cpp
static int x;
static int y;
static int z;
static int interaction_value;
```

に`OSCManager::update()`にて値のupdateする

```cpp
void OSCManager::update(){

    receiver.getNextMessage(message);
    //untill all address of osc are got.

    if(message.getAddress() == "/data"){

        // OSCでデータを取得
        // OSC最終受信時刻の取得
        string osc_update_time = message.getArgAsString(0);

        // OSCの受信時刻が更新された場合、それは新しい値なので取得値のupdate
        if(osc_update_time != latest_updated_time){

            // 受信時刻更新
            latest_updated_time = osc_update_time;

            // 値の更新
            int osc_input_data_x = message.getArgAsInt(1);
            int osc_input_data_y = message.getArgAsInt(2);
            int osc_input_data_z = message.getArgAsInt(3);
            int osc_input_data_interactive = message.getArgAsInt(4);

            Model::update_values(osc_input_data_x,
                                 osc_input_data_y,
                                 osc_input_data_z,
                                 osc_input_data_interactive);

            // 値のlog出し
            ofLog() << "[" <<osc_update_time << "] heart rate :"<< osc_input_data_x;
            ofLog() << "[" <<osc_update_time << "] heart rate :"<< osc_input_data_y;
            ofLog() << "[" <<osc_update_time << "] heart rate :"<< osc_input_data_z;
            ofLog() << "[" <<osc_update_time << "] heart rate :"<< osc_input_data_interactive;

        }
    }
};
```

呼び出してしては、`ofApp.cpp`で`OSCManager::setup();`と`OSCManager::update();`を呼べばいいだけ。
`Model::interaction_value`でアクセスできる。

```cpp
//--------------------------------------------------------------
void ofApp::setup(){
    OSCManager::setup();
}

//--------------------------------------------------------------
void ofApp::update(){
    OSCManager::update();
}

//--------------------------------------------------------------
void ofApp::draw(){
    ofSetWindowTitle("Model::interaction_value: "+ofToString(Model::interaction_value));
}
```

## LISENSE

Copyright 2018 Hiroki11x(Hiroki Naganuma)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

